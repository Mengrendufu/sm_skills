#!/usr/bin/env python3
"""
Validate qm-c-model-master JSON IR.

Usage:
    validate_ir.py <ir.json>
"""

import json
import sys
from typing import Any, Dict, List, Set


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def require_fields(obj: Dict[str, Any], fields: List[str], context: str) -> None:
    for field in fields:
        if field not in obj:
            fail(f"Missing field {field!r} in {context}.")


def collect_states(states: List[Dict[str, Any]], seen: Dict[str, Dict[str, Any]]) -> None:
    for state in states:
        require_fields(state, ["id", "name", "path", "parent", "parent_id", "entry", "exit"], "state")
        state_id = state["id"]
        if not state_id:
            fail("State id must not be empty.")
        if state_id in seen:
            fail(f"Duplicate state id {state_id!r}.")
        seen[state_id] = state
        for child in state.get("children", []):
            collect_states([child], seen)


def validate_transition(
    transition: Dict[str, Any],
    *,
    state_ids: Set[str],
    seen_transition_ids: Set[str],
) -> None:
    require_fields(
        transition,
        ["id", "owner_state", "owner_state_id", "trigger", "kind", "target", "target_state_id", "action", "guard"],
        "transition",
    )
    transition_id = transition["id"]
    if not transition_id:
        fail("Transition id must not be empty.")
    if transition_id in seen_transition_ids:
        fail(f"Duplicate transition id {transition_id!r}.")
    seen_transition_ids.add(transition_id)

    owner_state_id = transition["owner_state_id"]
    if owner_state_id not in state_ids:
        fail(f"Transition {transition_id!r} owner_state_id {owner_state_id!r} does not resolve to a known state.")

    kind = transition["kind"]
    if kind not in {"external", "internal", "super", "unhandled", "choice"}:
        fail(f"Transition {transition_id!r} has invalid kind {kind!r}.")

    if kind == "external" and transition["target_state_id"] not in state_ids:
        fail(f"External transition {transition_id!r} has unresolved target_state_id.")

    for branch in transition.get("branches", []):
        require_fields(branch, ["guard", "target", "target_state_id", "action", "kind", "is_else"], f"transition {transition_id} branch")
        branch_kind = branch["kind"]
        if branch_kind not in {"external", "internal", "super", "unhandled", "unknown"}:
            fail(f"Transition {transition_id!r} has invalid branch kind {branch_kind!r}.")
        if branch_kind == "external" and branch["target_state_id"] not in state_ids:
            fail(f"Transition {transition_id!r} has an external branch with unresolved target_state_id.")


def validate(ir: Dict[str, Any]) -> None:
    require_fields(
        ir,
        ["machine_name", "top_initial", "states", "transitions", "diagnostics", "is_reliable", "state_count", "transition_count"],
        "IR",
    )
    if not ir["machine_name"]:
        fail("machine_name must not be empty.")

    top_initial = ir["top_initial"]
    require_fields(top_initial, ["guard", "target", "target_state_id", "action", "kind", "is_else"], "top_initial")

    states_by_id: Dict[str, Dict[str, Any]] = {}
    collect_states(ir["states"], states_by_id)
    state_ids = set(states_by_id)

    if ir["state_count"] != len(state_ids):
        fail("state_count does not match the number of collected states.")

    if top_initial["target_state_id"] not in state_ids:
        fail("top_initial.target_state_id must resolve to a known state.")

    for state_id, state in states_by_id.items():
        parent_id = state["parent_id"]
        if parent_id is not None and parent_id not in state_ids:
            fail(f"State {state_id!r} has unresolved parent_id {parent_id!r}.")
        initial = state.get("initial")
        if initial is not None:
            require_fields(initial, ["target", "target_state_id", "action", "kind"], f"state {state_id} initial")
            if initial["target_state_id"] not in state_ids:
                fail(f"State {state_id!r} has unresolved initial target_state_id.")

    seen_transition_ids: Set[str] = set()
    for transition in ir["transitions"]:
        validate_transition(transition, state_ids=state_ids, seen_transition_ids=seen_transition_ids)

    if ir["transition_count"] != len(ir["transitions"]):
        fail("transition_count does not match the number of top-level transitions.")

    has_error = any(diagnostic.get("severity") == "error" for diagnostic in ir["diagnostics"])
    if ir["is_reliable"] and has_error:
        fail("is_reliable=true is inconsistent with error-level diagnostics.")
    if not ir["is_reliable"] and not has_error:
        fail("is_reliable=false is inconsistent with the absence of error-level diagnostics.")


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: validate_ir.py <ir.json>")

    ir_path = sys.argv[1]
    with open(ir_path, "r", encoding="utf-8") as handle:
        ir = json.load(handle)

    validate(ir)
    print("IR is valid.")


if __name__ == "__main__":
    main()
