#!/usr/bin/env python3
"""
Validate a machine-readable semantic verification report.

Usage:
    validate_verification_report.py <report.json>
"""

import json
import sys
from typing import Any, Dict, List


REQUIRED_TOP_LEVEL = [
    "version",
    "machine_name",
    "inputs",
    "verdict",
    "hierarchy_check",
    "init_check",
    "transition_checks",
    "choice_checks",
    "delegation_checks",
    "adaptations",
    "blockers",
]

RUNTIMES = {"ts_hsm", "sm_hsm", "rs_hsm_"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def require_fields(obj: Dict[str, Any], fields: List[str], context: str) -> None:
    for field in fields:
        if field not in obj:
            fail(f"Missing field {field!r} in {context}.")


def require_status(value: str, context: str) -> None:
    if value not in {"PASS", "BLOCKED"}:
        fail(f"Invalid status {value!r} in {context}.")


def require_runtime_mappings(mappings: List[Dict[str, Any]], context: str) -> None:
    seen = set()
    for mapping in mappings:
        require_fields(mapping, ["runtime", "location"], context)
        runtime = mapping["runtime"]
        if runtime not in RUNTIMES:
            fail(f"Invalid runtime {runtime!r} in {context}.")
        seen.add(runtime)
    if seen != RUNTIMES:
        fail(f"{context} must contain mappings for ts_hsm, sm_hsm, and rs_hsm_.")


def validate(report: Dict[str, Any]) -> None:
    require_fields(report, REQUIRED_TOP_LEVEL, "top level")

    inputs = report["inputs"]
    verdict = report["verdict"]
    hierarchy = report["hierarchy_check"]
    init_check = report["init_check"]
    transition_checks = report["transition_checks"]
    choice_checks = report["choice_checks"]
    delegation_checks = report["delegation_checks"]
    blockers = report["blockers"]

    require_fields(inputs, ["ir_path", "trace_path", "is_reliable", "diagnostics"], "inputs")
    require_fields(verdict, ["status", "reason"], "verdict")
    require_fields(hierarchy, ["status", "roots", "parent_chains", "notes"], "hierarchy_check")
    require_fields(init_check, ["status", "top_initial", "composite_initials", "trace_alignment", "notes"], "init_check")
    require_status(verdict["status"], "verdict")
    require_status(hierarchy["status"], "hierarchy_check")
    require_status(init_check["status"], "init_check")

    require_fields(init_check["top_initial"], ["source", "target_state_id"], "init_check.top_initial")

    for item in hierarchy["parent_chains"]:
        require_fields(item, ["state_id", "parent_id"], "hierarchy_check.parent_chains[]")

    for item in init_check["composite_initials"]:
        require_fields(item, ["state_id", "target_state_id"], "init_check.composite_initials[]")

    for item in transition_checks:
        require_fields(
            item,
            ["transition_id", "status", "source_state_id", "trigger", "target_state_id", "effect", "mappings", "notes"],
            "transition_checks[]",
        )
        require_status(item["status"], f"transition {item['transition_id']}")
        require_runtime_mappings(item["mappings"], f"transition {item['transition_id']}")

    for item in choice_checks:
        require_fields(item, ["transition_id", "status", "branches", "notes"], "choice_checks[]")
        require_status(item["status"], f"choice {item['transition_id']}")
        for branch in item["branches"]:
            require_fields(branch, ["guard", "kind", "behavior", "mappings"], f"choice {item['transition_id']} branch")
            require_runtime_mappings(branch["mappings"], f"choice {item['transition_id']} branch")

    for item in delegation_checks:
        require_fields(item, ["state_id", "trigger", "status", "mechanisms", "notes"], "delegation_checks[]")
        require_status(item["status"], f"delegation {item['state_id']}:{item['trigger']}")
        mechanisms = item["mechanisms"]
        require_fields(mechanisms, ["ts_hsm", "sm_hsm", "rs_hsm_"], f"delegation {item['state_id']}:{item['trigger']} mechanisms")

    all_section_statuses = [hierarchy["status"], init_check["status"]]
    all_section_statuses.extend(item["status"] for item in transition_checks)
    all_section_statuses.extend(item["status"] for item in choice_checks)
    all_section_statuses.extend(item["status"] for item in delegation_checks)

    if verdict["status"] == "PASS":
        if not inputs["is_reliable"]:
            fail("PASS verdict requires inputs.is_reliable=true.")
        if inputs["diagnostics"]:
            fail("PASS verdict requires inputs.diagnostics to be empty.")
        if blockers:
            fail("PASS verdict requires blockers to be empty.")
        if any(status != "PASS" for status in all_section_statuses):
            fail("PASS verdict requires every section and item status to be PASS.")
        if not init_check["trace_alignment"]:
            fail("PASS verdict requires init_check.trace_alignment=true.")
    else:
        if not blockers and all(status == "PASS" for status in all_section_statuses):
            fail("BLOCKED verdict requires at least one blocker or non-PASS section/item.")


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: validate_verification_report.py <report.json>")

    report_path = sys.argv[1]
    with open(report_path, "r", encoding="utf-8") as handle:
        report = json.load(handle)

    validate(report)
    print("Verification report is valid.")


if __name__ == "__main__":
    main()
