"""Grounded retrieval + generation for the ASU CS unofficial guide.

Milestone 5 only: this module connects the Milestone 4 retriever to Groq.
Answers are generated from retrieved context only, with sources returned
programmatically for the interface.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from scripts.build_vector_store import (
    CHROMA_DIR,
    DEFAULT_TOP_K,
    MAX_INSPECTION_DISTANCE,
    MAX_RERANK_SCORE,
    MODEL_NAME,
    build_vector_store,
    get_collection,
    load_chunks,
    load_model,
    retrieve,
    CHUNKS_PATH,
)


GROQ_MODEL = "llama-3.3-70b-versatile"
MAX_CONTEXT_CHARS_PER_CHUNK = 3_000
INSUFFICIENT_ANSWER = (
    "I don't have enough information in the provided sources to answer that."
)

SYSTEM_PROMPT = f"""
You answer questions for an unofficial ASU Computer Science course planning
and workload guide.

Grounding rules:
- Use only the provided retrieved context.
- Do not use outside knowledge, assumptions, or general ASU knowledge.
- If the context does not contain enough information, answer exactly:
  "{INSUFFICIENT_ANSWER}"
- Cite sources using the bracket labels from the context, such as [S1].
- Official ASU sources are authoritative for requirements, prerequisites,
  catalog rules, major maps, advising information, and academic support.
- Reddit and student-maintained sources are only for student workload
  impressions, difficulty perception, preparation advice, common planning
  concerns, and unofficial survival advice.
- If official ASU sources and student-experience sources disagree, say that
  the official ASU source wins and recommend verifying final schedule changes
  with ASU advising.
""".strip()


@lru_cache(maxsize=1)
def _model() -> Any:
    return load_model(MODEL_NAME)


@lru_cache(maxsize=1)
def _collection() -> Any:
    collection = get_collection(CHROMA_DIR, reset=False)
    if collection.count() == 0:
        chunks = load_chunks(CHUNKS_PATH)
        build_vector_store(chunks, _model(), collection, batch_size=16)
    return collection


@lru_cache(maxsize=1)
def _groq_client() -> Groq:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GROQ_API_KEY. Add it to .env before asking questions.")
    return Groq(api_key=api_key)


def retrieve_context(question: str, top_k: int = DEFAULT_TOP_K) -> list[dict[str, Any]]:
    return retrieve(question, _model(), _collection(), top_k=top_k)


def has_enough_context(rows: list[dict[str, Any]]) -> bool:
    return any(
        row["distance"] <= MAX_INSPECTION_DISTANCE
        and row["rerank_score"] <= MAX_RERANK_SCORE
        for row in rows
    )


def source_label(index: int) -> str:
    return f"S{index}"


def build_context(rows: list[dict[str, Any]]) -> str:
    context_blocks: list[str] = []
    for index, row in enumerate(rows, start=1):
        metadata = row["metadata"]
        label = source_label(index)
        text = row["document"][:MAX_CONTEXT_CHARS_PER_CHUNK].strip()
        context_blocks.append(
            "\n".join(
                [
                    f"[{label}] {metadata['source_title']}",
                    f"Source type: {metadata['source_type']}",
                    f"Authority: {metadata['authority_level']}",
                    f"Chunk index: {metadata['chunk_index']}",
                    f"Distance: {row['distance']:.4f}",
                    "Context:",
                    text,
                ]
            )
        )
    return "\n\n---\n\n".join(context_blocks)


def format_sources(rows: list[dict[str, Any]]) -> list[str]:
    sources: list[str] = []
    seen: set[tuple[str, int]] = set()
    for index, row in enumerate(rows, start=1):
        metadata = row["metadata"]
        key = (str(metadata["source_title"]), int(metadata["chunk_index"]))
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            (
                f"[{source_label(index)}] {metadata['source_title']} "
                f"(chunk {metadata['chunk_index']}, distance {row['distance']:.4f})\n"
                f"{metadata['source_url']}"
            )
        )
    return sources


def generate_answer(question: str, rows: list[dict[str, Any]]) -> str:
    context = build_context(rows)
    user_prompt = f"""
Question:
{question}

Retrieved context:
{context}

Write a concise, grounded answer. Cite the source labels that support each
claim. If the retrieved context is not enough, use the required insufficient
information sentence exactly.
""".strip()

    response = _groq_client().chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
        max_tokens=700,
    )
    answer = response.choices[0].message.content or ""
    return answer.strip() or INSUFFICIENT_ANSWER


def ask(question: str, top_k: int = DEFAULT_TOP_K) -> dict[str, Any]:
    cleaned_question = question.strip()
    if not cleaned_question:
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "retrieved_chunks": [],
        }

    rows = retrieve_context(cleaned_question, top_k=top_k)
    if not rows or not has_enough_context(rows):
        return {
            "answer": INSUFFICIENT_ANSWER,
            "sources": [],
            "retrieved_chunks": rows,
        }

    answer = generate_answer(cleaned_question, rows)
    return {
        "answer": answer,
        "sources": format_sources(rows),
        "retrieved_chunks": rows,
    }
