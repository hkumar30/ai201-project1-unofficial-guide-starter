#!/usr/bin/env python3
"""Run Milestone 6 grounded generation evaluation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from query import ask


REPORT_PATH = ROOT / "data" / "generation_report.txt"


TEST_QUERIES = [
    "Which sources should be treated as authoritative for ASU CS degree requirements?",
    "Which sources should answer questions about where to get tutoring for CSE courses?",
    "Which sources should answer questions about scheduling or using SCAI advising?",
    "What source types should be used to answer whether CSE 330, CSE 340, and CSE 355 are hard to take together?",
    "What sources should be used for CSE 340 course content versus student preparation advice?",
    "Which ASU dining hall has the best late-night food?",
]


def format_result(question: str) -> str:
    result = ask(question)
    lines = [
        "=" * 80,
        f"Question: {question}",
        "",
        "Answer:",
        result["answer"],
        "",
        "Sources:",
    ]
    if result["sources"]:
        for source in result["sources"]:
            lines.append(f"- {source}")
    else:
        lines.append("- No sources returned.")
    return "\n".join(lines)


def main() -> int:
    reports = []
    for question in TEST_QUERIES:
        reports.append(format_result(question))
    report = "\n".join(reports) + "\n"
    report = "\n".join(line.rstrip() for line in report.splitlines()) + "\n"
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(report)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
