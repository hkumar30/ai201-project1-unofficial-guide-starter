#!/usr/bin/env python3
"""Run Milestone 5 grounded generation smoke tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from query import ask


REPORT_PATH = ROOT / "data" / "generation_report.txt"


TEST_QUERIES = [
    "Where can I get tutoring for CSE courses?",
    "How do I schedule or use SCAI advising?",
    "Should I take CSE 330, CSE 340, and CSE 355 in the same semester?",
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
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(report)
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
