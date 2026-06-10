#!/usr/bin/env python3
"""Load, clean, and chunk the Milestone 3 document corpus.

This script intentionally stops before embeddings/vector search. It creates:
- data/raw_documents.jsonl
- data/clean_documents.jsonl
- data/chunks.jsonl
- data/pipeline_report.txt
"""

from __future__ import annotations

import argparse
import html
import json
import random
import re
import sys
import textwrap
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

try:
    import pdfplumber
except ImportError:  # pragma: no cover - exercised only when dependency is missing
    pdfplumber = None

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - fallback exists for constrained envs
    BeautifulSoup = None


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DOCUMENTS_DIR = ROOT / "documents"
SOURCES_PATH = DATA_DIR / "sources.json"
RAW_PATH = DATA_DIR / "raw_documents.jsonl"
CLEAN_PATH = DATA_DIR / "clean_documents.jsonl"
CHUNKS_PATH = DATA_DIR / "chunks.jsonl"
REPORT_PATH = DATA_DIR / "pipeline_report.txt"

USER_AGENT = (
    "Mozilla/5.0 (compatible; ASU-CS-Unofficial-Guide/1.0; "
    "+https://example.edu/student-project)"
)

BOILERPLATE_PATTERNS = [
    r"^skip to main content$",
    r"^skip to content$",
    r"^report an accessibility problem$",
    r"^asu home$",
    r"^my asu$",
    r"^colleges and schools$",
    r"^main menu$",
    r"^menu$",
    r"^search$",
    r"^search asu$",
    r"^close$",
    r"^cancel$",
    r"^share$",
    r"^print$",
    r"^loading\.*$",
    r"^privacy statement$",
    r"^terms of use$",
    r"^copyright\b",
    r"^all rights reserved\.?$",
    r"^cookie(s)?\b",
    r"^accept all cookies$",
    r"^read more$",
    r"^view all posts$",
    r"^log in$",
    r"^sign up$",
    r"^advertis(e|ement)",
    r"^schedule a visit$",
    r"^request info$",
    r"^apply now$",
    r"^select a page$",
    r"^get tutoring now!?$",
    r"^view complete schedule$",
    r"^view profile$",
    r"^view program description$",
    r"^click to save to my favorites$",
    r"^follow us on social media\b",
    r"^meet (our|the) .*tutors$",
    r"^ctrl k$",
    r"^ctrl$",
    r"^k$",
    r"^copy page\b",
    r"^open in (chatgpt|claude)$",
    r"^ask questions about this page$",
    r"^github discord instagram linkedin$",
    r"^github$",
    r"^discord$",
    r"^instagram$",
    r"^linkedin$",
    r"^select theme$",
    r"^dark light auto$",
    r"^dark$",
    r"^light$",
    r"^auto$",
    r"^asu cs wiki$",
    r"^section titled\b",
    r"^student reviews$",
    r"^review 1$",
    r"^todo$",
    r"^fill out$",
    r"^this form$",
    r"^to add your review!?$",
]

MIN_CLEAN_TOKENS = 40
MIN_CHUNK_BODY_TOKENS = 40


@dataclass(frozen=True)
class Source:
    id: int
    title: str
    url: str
    source_type: str
    authority_level: str
    topic_tags: list[str]
    course_codes: list[str]
    use_case: str
    notes: str


class SimpleHTMLTextExtractor(HTMLParser):
    """Small fallback extractor when BeautifulSoup is unavailable."""

    BLOCK_TAGS = {
        "article",
        "aside",
        "blockquote",
        "br",
        "dd",
        "div",
        "dl",
        "dt",
        "figcaption",
        "footer",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "section",
        "table",
        "td",
        "th",
        "tr",
        "ul",
    }
    SKIP_TAGS = {"script", "style", "noscript", "svg", "head"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        return html.unescape(" ".join(self.parts))


def load_sources(path: Path) -> list[Source]:
    records = json.loads(path.read_text(encoding="utf-8"))
    return [Source(**record) for record in records]


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as output:
        for record in records:
            output.write(json.dumps(record, ensure_ascii=False) + "\n")


def fetch_url(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    response.raise_for_status()
    if not response.encoding or response.encoding.lower() == "iso-8859-1":
        response.encoding = response.apparent_encoding or "utf-8"
    return response.text


def html_to_text(markup: str) -> str:
    if BeautifulSoup is not None:
        soup = BeautifulSoup(markup, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()
        for tag in soup.find_all(["nav", "footer"]):
            tag.decompose()
        return soup.get_text("\n")

    parser = SimpleHTMLTextExtractor()
    parser.feed(markup)
    return parser.text()


def reddit_json_url(url: str) -> str:
    base = url.rstrip("/")
    return f"{base}.json?limit=50&raw_json=1"


def old_reddit_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed._replace(netloc="old.reddit.com").geturl()


def extract_reddit_items(payload: Any) -> list[str]:
    items: list[str] = []

    def walk(node: Any, depth: int = 0) -> None:
        if not isinstance(node, dict):
            return
        data = node.get("data", {})
        if isinstance(data, dict):
            title = data.get("title")
            selftext = data.get("selftext")
            body = data.get("body")
            author = data.get("author")
            if title:
                items.append(f"Original post title: {title}")
            if selftext and selftext not in {"[deleted]", "[removed]"}:
                items.append(f"Original post: {selftext}")
            if body and body not in {"[deleted]", "[removed]"}:
                label = "Comment" if depth else "Post/comment"
                byline = f" by {author}" if author else ""
                items.append(f"{label}{byline}: {body}")

            replies = data.get("replies")
            if isinstance(replies, dict):
                walk(replies, depth + 1)
            children = data.get("children")
            if isinstance(children, list):
                for child in children:
                    walk(child, depth + 1)

        children = node.get("children")
        if isinstance(children, list):
            for child in children:
                walk(child, depth + 1)

    if isinstance(payload, list):
        for entry in payload:
            walk(entry)
    else:
        walk(payload)

    return items


def load_reddit_text(source: Source) -> str:
    try:
        response = requests.get(
            reddit_json_url(source.url),
            headers={"User-Agent": USER_AGENT},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        items = extract_reddit_items(payload)
        if items:
            return "\n\n".join(items)
    except requests.RequestException:
        pass

    markup = fetch_url(old_reddit_url(source.url))
    if BeautifulSoup is None:
        return html_to_text(markup)

    soup = BeautifulSoup(markup, "html.parser")
    parts: list[str] = []
    title = soup.select_one("a.title")
    if title:
        parts.append(f"Original post title: {title.get_text(' ', strip=True)}")

    post_bodies = soup.select("div.thing.link div.usertext-body div.md")
    comment_bodies = soup.select("div.thing.comment div.usertext-body div.md")

    for index, body in enumerate(post_bodies, start=1):
        text = body.get_text("\n", strip=True)
        if not text:
            continue
        label = "Original post" if index == 1 else "Original post edit"
        parts.append(f"{label}: {text}")

    for body in comment_bodies:
        text = body.get_text("\n", strip=True)
        if text:
            parts.append(f"Comment: {text}")

    return "\n\n".join(parts) if parts else html_to_text(markup)


def matching_local_pdf(source: Source) -> Path | None:
    filename = Path(urlparse(source.url).path).name
    if filename:
        candidate = DOCUMENTS_DIR / filename
        if candidate.exists():
            return candidate
    return None


def load_pdf_text(path: Path) -> str:
    if pdfplumber is None:
        raise RuntimeError(
            "pdfplumber is required for PDF extraction. Install requirements.txt first."
        )

    page_texts: list[str] = []
    with pdfplumber.open(path) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                page_texts.append(f"Page {index}\n{text}")
    return "\n\n".join(page_texts)


def load_source_text(source: Source) -> tuple[str, str]:
    local_pdf = matching_local_pdf(source)
    if local_pdf is not None:
        return load_pdf_text(local_pdf), str(local_pdf.relative_to(ROOT))

    if source.source_type == "reddit_student_experience":
        return load_reddit_text(source), source.url

    markup = fetch_url(source.url)
    return html_to_text(markup), source.url


def normalize_markdown(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"[*_~]{1,3}", "", text)
    return text


def clean_text(text: str) -> str:
    text = html.unescape(text).replace("\xa0", " ")
    text = normalize_markdown(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)

    kept_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            kept_lines.append("")
            continue
        compact = re.sub(r"\s+", " ", line).strip()
        lower = compact.lower()
        if len(compact) <= 80 and any(
            re.search(pattern, lower) for pattern in BOILERPLATE_PATTERNS
        ):
            continue
        if re.fullmatch(r"[|/\-_= ]{3,}", compact):
            continue
        kept_lines.append(compact)

    cleaned = "\n".join(kept_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = re.sub(r" {2,}", " ", cleaned)
    return cleaned.strip()


def split_units(text: str) -> list[str]:
    blocks = [block.strip() for block in re.split(r"\n\s*\n+", text) if block.strip()]
    units: list[str] = []
    for block in blocks:
        words = block.split()
        if len(words) <= 220:
            units.append(block)
            continue

        sentences = re.split(r"(?<=[.!?])\s+", block)
        buffer: list[str] = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            candidate = " ".join(buffer + [sentence])
            if len(candidate.split()) > 180 and buffer:
                units.append(" ".join(buffer))
                buffer = [sentence]
            else:
                buffer.append(sentence)
        if buffer:
            units.append(" ".join(buffer))
    return units


def token_count(text: str) -> int:
    return len(text.split())


def split_long_unit(unit: str, max_tokens: int, overlap_tokens: int) -> list[str]:
    tokens = unit.split()
    if len(tokens) <= max_tokens:
        return [unit]

    chunks: list[str] = []
    start = 0
    step = max_tokens - overlap_tokens if overlap_tokens < max_tokens else max_tokens
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunks.append(" ".join(tokens[start:end]))
        if end == len(tokens):
            break
        start += step
    return chunks


def chunk_settings(source: Source) -> tuple[int, int, int]:
    if source.source_type == "reddit_student_experience":
        return 450, 550, 0
    return 800, 1000, 120


def make_chunk_header(source: Source, sequence: int) -> str:
    courses = ", ".join(source.course_codes) if source.course_codes else "None"
    return (
        f"Source {source.id}: {source.title}\n"
        f"Source type: {source.source_type}\n"
        f"Authority: {source.authority_level}\n"
        f"Courses: {courses}\n"
        f"Chunk: {sequence}\n\n"
    )


def chunk_document(source: Source, cleaned_text: str) -> list[dict[str, Any]]:
    target_tokens, max_tokens, overlap_tokens = chunk_settings(source)
    units = split_units(cleaned_text)
    chunks: list[dict[str, Any]] = []
    current_units: list[str] = []
    current_is_overlap_only = False

    def flush(keep_overlap: bool) -> None:
        nonlocal current_units, current_is_overlap_only
        if not current_units:
            return
        body = "\n\n".join(current_units).strip()
        if (
            not body
            or current_is_overlap_only
            or token_count(body) < MIN_CHUNK_BODY_TOKENS
        ):
            current_units = []
            current_is_overlap_only = False
            return
        sequence = len(chunks) + 1
        chunk_text = make_chunk_header(source, sequence) + body
        chunks.append(
            {
                "chunk_id": f"source-{source.id:02d}-chunk-{sequence:03d}",
                "source_id": source.id,
                "source_title": source.title,
                "source_url": source.url,
                "source_type": source.source_type,
                "authority_level": source.authority_level,
                "topic_tags": source.topic_tags,
                "course_codes": source.course_codes,
                "chunk_index": sequence,
                "token_count": token_count(chunk_text),
                "text": chunk_text,
            }
        )
        if keep_overlap and overlap_tokens:
            overlap_words = body.split()[-overlap_tokens:]
            current_units = [" ".join(overlap_words)] if overlap_words else []
            current_is_overlap_only = bool(current_units)
        else:
            current_units = []
            current_is_overlap_only = False

    for unit in units:
        for piece in split_long_unit(unit, max_tokens, overlap_tokens):
            candidate_units = current_units + [piece]
            candidate = "\n\n".join(candidate_units)
            if current_units and token_count(candidate) > target_tokens:
                flush(keep_overlap=True)
                candidate_units = current_units + [piece]
                candidate = "\n\n".join(candidate_units)

            current_units = candidate_units
            current_is_overlap_only = False
            if token_count(candidate) >= target_tokens:
                flush(keep_overlap=True)

    flush(keep_overlap=False)
    return chunks


def build_records(sources: list[Source], allow_partial: bool) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[str],
]:
    raw_records: list[dict[str, Any]] = []
    clean_records: list[dict[str, Any]] = []
    chunk_records: list[dict[str, Any]] = []
    errors: list[str] = []

    for source in sources:
        try:
            raw_text, loaded_from = load_source_text(source)
            cleaned_text = clean_text(raw_text)
            if not cleaned_text:
                raise RuntimeError("cleaned text is empty")
            clean_tokens = token_count(cleaned_text)
            if clean_tokens < MIN_CLEAN_TOKENS:
                raise RuntimeError(
                    f"cleaned text has only {clean_tokens} tokens; likely dynamic or blocked"
                )

            raw_records.append(
                {
                    "source_id": source.id,
                    "title": source.title,
                    "url": source.url,
                    "loaded_from": loaded_from,
                    "source_type": source.source_type,
                    "authority_level": source.authority_level,
                    "raw_text": raw_text,
                }
            )
            clean_records.append(
                {
                    "source_id": source.id,
                    "title": source.title,
                    "url": source.url,
                    "loaded_from": loaded_from,
                    "source_type": source.source_type,
                    "authority_level": source.authority_level,
                    "clean_token_count": clean_tokens,
                    "clean_text": cleaned_text,
                }
            )
            chunk_records.extend(chunk_document(source, cleaned_text))
        except Exception as exc:  # noqa: BLE001 - report per-source load failures
            message = f"Source {source.id} ({source.title}) failed: {exc}"
            errors.append(message)
            if not allow_partial:
                raise RuntimeError(message) from exc

    return raw_records, clean_records, chunk_records, errors


def preview(text: str, width: int = 96, max_chars: int = 1400) -> str:
    clipped = text[:max_chars].strip()
    return "\n".join(textwrap.wrap(clipped, width=width))


def make_report(
    clean_records: list[dict[str, Any]],
    chunks: list[dict[str, Any]],
    errors: list[str],
    sample_count: int,
    random_seed: int,
) -> str:
    by_source: dict[int, int] = {}
    for chunk in chunks:
        by_source[chunk["source_id"]] = by_source.get(chunk["source_id"], 0) + 1

    token_counts = [chunk["token_count"] for chunk in chunks]
    min_tokens = min(token_counts) if token_counts else 0
    max_tokens = max(token_counts) if token_counts else 0
    avg_tokens = sum(token_counts) / len(token_counts) if token_counts else 0

    randomizer = random.Random(random_seed)
    samples = randomizer.sample(chunks, k=min(sample_count, len(chunks)))

    lines = [
        "Milestone 3 Document Pipeline Report",
        "=" * 38,
        f"Loaded documents: {len(clean_records)}",
        f"Total chunks: {len(chunks)}",
        f"Chunk token count: min={min_tokens}, avg={avg_tokens:.1f}, max={max_tokens}",
        "",
        "Chunks by source:",
    ]
    for record in clean_records:
        source_id = record["source_id"]
        lines.append(
            f"- Source {source_id}: {record['title']} -> "
            f"{by_source.get(source_id, 0)} chunks"
        )

    if errors:
        lines.extend(["", "Load errors:"])
        lines.extend(f"- {error}" for error in errors)

    if clean_records:
        first = clean_records[0]
        lines.extend(
            [
                "",
                "Cleaned document preview:",
                f"Source {first['source_id']}: {first['title']}",
                preview(first["clean_text"]),
            ]
        )

    lines.extend(["", f"{len(samples)} random chunk previews:"])
    for index, chunk in enumerate(samples, start=1):
        lines.extend(
            [
                "",
                f"Random chunk {index}: {chunk['chunk_id']} "
                f"({chunk['token_count']} tokens)",
                preview(chunk["text"]),
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail instead of writing outputs if any source cannot be loaded cleanly.",
    )
    parser.add_argument(
        "--sample-count",
        type=int,
        default=5,
        help="Number of random chunks to print for inspection.",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="Seed used for repeatable random chunk previews.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    DATA_DIR.mkdir(exist_ok=True)

    sources = load_sources(SOURCES_PATH)
    raw_records, clean_records, chunks, errors = build_records(
        sources, allow_partial=not args.strict
    )

    if not chunks:
        raise RuntimeError("No chunks were produced; check document loading and cleaning.")

    write_jsonl(RAW_PATH, raw_records)
    write_jsonl(CLEAN_PATH, clean_records)
    write_jsonl(CHUNKS_PATH, chunks)

    report = make_report(
        clean_records=clean_records,
        chunks=chunks,
        errors=errors,
        sample_count=args.sample_count,
        random_seed=args.random_seed,
    )
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(report)
    print(f"Wrote {RAW_PATH.relative_to(ROOT)}")
    print(f"Wrote {CLEAN_PATH.relative_to(ROOT)}")
    print(f"Wrote {CHUNKS_PATH.relative_to(ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - CLI-friendly failure
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
