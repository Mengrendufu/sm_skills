#!/usr/bin/env python3
"""
Build a semantic verification bundle from strict IR and trace JSON.

Usage:
    build_verification_bundle.py <ir.json> <trace.json> <report.json> <summary.md>
"""

import json
import sys

from generate_verification_report import generate_report, load_json
from render_verification_summary import render
from validate_verification_report import validate


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def main() -> None:
    if len(sys.argv) != 5:
        fail("Usage: build_verification_bundle.py <ir.json> <trace.json> <report.json> <summary.md>")

    ir_path = sys.argv[1]
    trace_path = sys.argv[2]
    report_path = sys.argv[3]
    summary_path = sys.argv[4]

    ir = load_json(ir_path)
    trace = load_json(trace_path)
    report = generate_report(ir, trace, ir_path, trace_path)
    validate(report)

    with open(report_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    with open(summary_path, "w", encoding="utf-8") as handle:
        handle.write(render(report))
        handle.write("\n")

    print(f"Wrote verification bundle to {report_path} and {summary_path}")


if __name__ == "__main__":
    main()
