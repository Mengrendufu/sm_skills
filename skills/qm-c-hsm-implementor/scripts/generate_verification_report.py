#!/usr/bin/env python3
"""
Generate a machine-readable semantic verification report scaffold from strict IR and trace JSON.

Usage:
    generate_verification_report.py <ir.json> <trace.json> <output.json>
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def require_fields(obj: Dict[str, Any], fields: List[str], context: str) -> None:
    for field in fields:
        if field not in obj:
            fail(f"Missing field {field!r} in {context}.")


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def iter_states(states: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    ordered: List[Dict[str, Any]] = []
    for state in states:
        ordered.append(state)
        ordered.extend(iter_states(state.get("children", [])))
    return ordered


def title_segment(name: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in name.replace("-", "_").split("_") if part)


def state_leaf_name(state_id: str) -> str:
    return state_id.split("/")[-1]


def infer_locations(machine_name: str, owner_state_id: str) -> List[Dict[str, str]]:
    leaf = state_leaf_name(owner_state_id)
    title = title_segment(leaf)
    return [
        {"runtime": "ts_hsm", "location": f"{machine_name}{title}State.handle"},
        {"runtime": "sm_hsm", "location": f"{machine_name}_{leaf}_"},
        {"runtime": "rs_hsm_", "location": f"{machine_name}_{leaf}_"},
    ]


def infer_choice_behavior(branch: Dict[str, Any]) -> str:
    kind = branch["kind"]
    if kind == "external":
        return branch["target_state_id"]
    if kind == "internal":
        if branch.get("action"):
            return "handled with side effect"
        return "handled"
    if kind == "super":
        return "delegated to parent"
    if kind == "unhandled":
        return "unhandled"
    return "review"


def relative_to_common_base(paths: List[str]) -> Tuple[str, List[str]]:
    common_base = os.path.commonpath(paths)
    return common_base, [os.path.relpath(path, common_base) for path in paths]


def generate_report(ir: Dict[str, Any], trace: Dict[str, Any], ir_path: str, trace_path: str) -> Dict[str, Any]:
    require_fields(ir, ["machine_name", "states", "transitions", "top_initial", "is_reliable", "diagnostics"], "IR")
    require_fields(trace, ["machine_name", "is_reliable", "diagnostics", "default_init_trace", "external_transition_traces", "handled_event_ownership"], "trace JSON")

    if ir["machine_name"] != trace["machine_name"]:
        fail("IR and trace JSON machine_name values do not match.")

    machine_name = ir["machine_name"]
    ordered_states = iter_states(ir["states"])
    state_ids = {state["id"] for state in ordered_states}
    roots = [state["id"] for state in ordered_states if state.get("parent_id") is None]
    composite_initials = []
    for state in ordered_states:
        initial = state.get("initial")
        if initial:
            composite_initials.append(
                {
                    "state_id": state["id"],
                    "target_state_id": initial["target_state_id"],
                }
            )

    transition_checks = []
    choice_checks = []

    trace_by_transition_id = {
        item["transition_id"]: item
        for item in trace["external_transition_traces"]
    }

    for transition in ir["transitions"]:
        transition_id = transition["id"]
        owner_state_id = transition["owner_state_id"]
        if transition["kind"] == "choice":
            branches = []
            for branch in transition.get("branches", []):
                branches.append(
                    {
                        "guard": branch["guard"] if branch["guard"] is not None else "else" if branch["is_else"] else "unguarded",
                        "kind": branch["kind"],
                        "behavior": infer_choice_behavior(branch),
                        "mappings": infer_locations(machine_name, owner_state_id),
                    }
                )
            choice_checks.append(
                {
                    "transition_id": transition_id,
                    "status": "BLOCKED",
                    "branches": branches,
                    "notes": [
                        "Review each generated branch and replace inferred runtime locations if they differ from the implementation.",
                    ],
                }
            )
        if transition["kind"] == "external":
            transition_checks.append(
                {
                    "transition_id": transition_id,
                    "status": "BLOCKED",
                    "source_state_id": owner_state_id,
                    "trigger": transition["trigger"],
                    "target_state_id": transition["target_state_id"],
                    "effect": transition["action"] if transition["action"] else "none",
                    "mappings": infer_locations(machine_name, owner_state_id),
                    "notes": [
                        "Trace-derived external transition; confirm locations and effect handling before marking PASS.",
                    ],
                }
            )
        elif transition["kind"] == "choice":
            trace_item = trace_by_transition_id.get(transition_id)
            if trace_item is not None:
                transition_checks.append(
                    {
                        "transition_id": transition_id,
                        "status": "BLOCKED",
                        "source_state_id": owner_state_id,
                        "trigger": transition["trigger"],
                        "target_state_id": trace_item["target_state_id"],
                        "effect": "review guarded branches",
                        "mappings": infer_locations(machine_name, owner_state_id),
                        "notes": [
                            "This choice transition has at least one external branch; verify branch-level mappings in choice_checks.",
                        ],
                    }
                )

    delegation_checks = []
    for state in ordered_states:
        delegate_target = state["parent_id"] if state["parent_id"] is not None else "TOP"
        delegation_checks.append(
            {
                "state_id": state["id"],
                "trigger": "DEFAULT",
                "status": "BLOCKED",
                "mechanisms": {
                    "ts_hsm": "superState()",
                    "sm_hsm": "_SM_SUPER()",
                    "rs_hsm_": "SM_RetState::Super",
                },
                "notes": [
                    f"Review default delegation path to {delegate_target}.",
                ],
            }
        )

    common_base, relative_paths = relative_to_common_base([ir_path, trace_path])
    rel_ir_path, rel_trace_path = relative_paths

    report = {
        "version": "1.0",
        "machine_name": machine_name,
        "inputs": {
            "ir_path": rel_ir_path,
            "trace_path": rel_trace_path,
            "is_reliable": bool(ir["is_reliable"] and trace["is_reliable"]),
            "diagnostics": ir["diagnostics"] + [d for d in trace["diagnostics"] if d not in ir["diagnostics"]],
        },
        "verdict": {
            "status": "BLOCKED",
            "reason": "Generated scaffold requires runtime location review and semantic confirmation before PASS.",
        },
        "hierarchy_check": {
            "status": "BLOCKED",
            "roots": roots,
            "parent_chains": [
                {
                    "state_id": state["id"],
                    "parent_id": state["parent_id"],
                }
                for state in ordered_states
                if state["parent_id"] is not None
            ],
            "notes": [
                "Confirm that each runtime preserves the same parent-child hierarchy.",
            ],
        },
        "init_check": {
            "status": "BLOCKED",
            "top_initial": {
                "source": "TOP",
                "target_state_id": ir["top_initial"]["target_state_id"],
            },
            "composite_initials": composite_initials,
            "trace_alignment": bool(trace["default_init_trace"]["target_state_id"] == ir["top_initial"]["target_state_id"]),
            "notes": [
                "Confirm init ordering against the trace JSON before marking PASS.",
            ],
        },
        "transition_checks": transition_checks,
        "choice_checks": choice_checks,
        "delegation_checks": delegation_checks,
        "adaptations": [],
        "blockers": [
            "Replace inferred runtime locations with reviewed implementation locations.",
            "Review every BLOCKED section and item before marking the report PASS.",
        ],
        "_meta": {
            "common_base": common_base,
            "generated_from": {
                "ir_path": ir_path,
                "trace_path": trace_path,
            },
            "known_state_ids": sorted(state_ids),
        },
    }
    return report


def main() -> None:
    if len(sys.argv) != 4:
        fail("Usage: generate_verification_report.py <ir.json> <trace.json> <output.json>")

    ir_path = sys.argv[1]
    trace_path = sys.argv[2]
    output_path = sys.argv[3]

    ir = load_json(ir_path)
    trace = load_json(trace_path)
    report = generate_report(ir, trace, ir_path, trace_path)

    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(f"Wrote verification report scaffold to {output_path}")


if __name__ == "__main__":
    main()
