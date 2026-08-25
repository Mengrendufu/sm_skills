#!/usr/bin/env python3
"""
Render a machine-readable semantic verification report into Markdown.

Usage:
    render_verification_summary.py <report.json> <output.md>
"""

import json
import sys
from typing import Any, Dict, List


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def bullet_lines(items: List[str]) -> List[str]:
    return [f"- {item}" for item in items]


def render(report: Dict[str, Any]) -> str:
    inputs = report["inputs"]
    verdict = report["verdict"]
    hierarchy = report["hierarchy_check"]
    init_check = report["init_check"]

    lines: List[str] = ["# Semantic Verification Summary", ""]

    lines.append("## Input Evidence")
    lines.append("")
    lines.extend(
        bullet_lines(
            [
                f"IR: `{inputs['ir_path']}`",
                f"Trace: `{inputs['trace_path']}`",
                f"`is_reliable`: `{str(inputs['is_reliable']).lower()}`",
                f"Diagnostics: `{ 'none' if not inputs['diagnostics'] else 'present' }`",
            ]
        )
    )
    lines.append("")

    lines.append("## Verdict")
    lines.append("")
    lines.extend(
        bullet_lines(
            [
                f"`{verdict['status']}`",
                f"Reason: {verdict['reason']}",
            ]
        )
    )
    lines.append("")

    lines.append("## Hierarchy Check")
    lines.append("")
    lines.append(f"- Status: `{hierarchy['status']}`")
    lines.append(f"- Roots: {', '.join(f'`{root}`' for root in hierarchy['roots']) if hierarchy['roots'] else '`none`'}")
    lines.append("- Parent chains:")
    for item in hierarchy["parent_chains"]:
        lines.append(f"- `{item['state_id']} -> {item['parent_id']}`")
    lines.append("- Notes:")
    if hierarchy["notes"]:
        lines.extend(bullet_lines(hierarchy["notes"]))
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Init Check")
    lines.append("")
    lines.append(f"- Status: `{init_check['status']}`")
    lines.append(f"- `top_initial`: `{init_check['top_initial']['source']} -> {init_check['top_initial']['target_state_id']}`")
    lines.append("- Composite initials:")
    for item in init_check["composite_initials"]:
        lines.append(f"- `{item['state_id']} -> {item['target_state_id']}`")
    lines.append(f"- Trace alignment: `{str(init_check['trace_alignment']).lower()}`")
    lines.append("- Notes:")
    if init_check["notes"]:
        lines.extend(bullet_lines(init_check["notes"]))
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Transition Check")
    lines.append("")
    for item in report["transition_checks"]:
        lines.append(f"- `{item['transition_id']}` `{item['status']}`: `{item['source_state_id']} --{item['trigger']}--> {item['target_state_id']}`")
        lines.append(f"- Effect: `{item['effect']}`")
        lines.append("- Target locations:")
        for mapping in item["mappings"]:
            lines.append(f"- `{mapping['runtime']}`: `{mapping['location']}`")
        if item["notes"]:
            lines.append("- Notes:")
            lines.extend(bullet_lines(item["notes"]))
    if not report["transition_checks"]:
        lines.append("- none")
    lines.append("")

    lines.append("## Choice Check")
    lines.append("")
    for item in report["choice_checks"]:
        lines.append(f"- `{item['transition_id']}` `{item['status']}`")
        for branch in item["branches"]:
            lines.append(f"- `[{branch['guard']}]` `{branch['kind']}` `{branch['behavior']}`")
            for mapping in branch["mappings"]:
                lines.append(f"- `{mapping['runtime']}`: `{mapping['location']}`")
        if item["notes"]:
            lines.append("- Notes:")
            lines.extend(bullet_lines(item["notes"]))
    if not report["choice_checks"]:
        lines.append("- none")
    lines.append("")

    lines.append("## Delegation Check")
    lines.append("")
    for item in report["delegation_checks"]:
        lines.append(f"- `{item['state_id']}` `{item['trigger']}` `{item['status']}`")
        lines.append(f"- `ts_hsm`: `{item['mechanisms']['ts_hsm']}`")
        lines.append(f"- `sm_hsm`: `{item['mechanisms']['sm_hsm']}`")
        lines.append(f"- `rs_hsm_`: `{item['mechanisms']['rs_hsm_']}`")
        if item["notes"]:
            lines.append("- Notes:")
            lines.extend(bullet_lines(item["notes"]))
    if not report["delegation_checks"]:
        lines.append("- none")
    lines.append("")

    lines.append("## Adaptations")
    lines.append("")
    if report["adaptations"]:
        lines.extend(bullet_lines(report["adaptations"]))
    else:
        lines.append("- `none`")
    lines.append("")

    if report["blockers"]:
        lines.append("## Blockers")
        lines.append("")
        lines.extend(bullet_lines(report["blockers"]))
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 3:
        fail("Usage: render_verification_summary.py <report.json> <output.md>")

    report_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(report_path, "r", encoding="utf-8") as handle:
        report = json.load(handle)

    rendered = render(report)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(rendered)
        handle.write("\n")

    print(f"Wrote Markdown verification summary to {output_path}")


if __name__ == "__main__":
    main()
