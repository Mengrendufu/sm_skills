#!/usr/bin/env python3
"""
Parse QM-generated C state machine code into a language-neutral semantic model.

Usage:
    parse_qm_c.py <input.c> [--output json|plantuml|text|trace|trace-json] [--strict]

Example:
    parse_qm_c.py smhsmtst.c --output json
    parse_qm_c.py smhsmtst.c --output plantuml
    parse_qm_c.py smhsmtst.c --output text
    parse_qm_c.py smhsmtst.c --output trace --strict
    parse_qm_c.py smhsmtst.c --output trace-json --strict
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


RETURN_KIND_MAP = {
    "Q_TRAN": "external",
    "Q_HANDLED": "internal",
    "Q_SUPER": "super",
    "Q_UNHANDLED": "unhandled",
}


@dataclass
class TransitionBranch:
    guard: Optional[str] = None
    target: Optional[str] = None
    target_state_id: Optional[str] = None
    action: Optional[str] = None
    kind: str = "unknown"
    is_else: bool = False

    def to_dict(self) -> Dict:
        return {
            "guard": self.guard,
            "target": self.target,
            "target_state_id": self.target_state_id,
            "action": self.action,
            "kind": self.kind,
            "is_else": self.is_else,
        }


@dataclass
class Transition:
    owner_state: str
    owner_state_id: Optional[str]
    trigger: str
    id: Optional[str] = None
    kind: str = "unknown"
    target: Optional[str] = None
    target_state_id: Optional[str] = None
    action: Optional[str] = None
    guard: Optional[str] = None
    branches: List[TransitionBranch] = field(default_factory=list)

    def to_dict(self) -> Dict:
        result = {
            "id": self.id,
            "owner_state": self.owner_state,
            "owner_state_id": self.owner_state_id,
            "trigger": self.trigger,
            "kind": self.kind,
            "target": self.target,
            "target_state_id": self.target_state_id,
            "action": self.action,
            "guard": self.guard,
        }
        if self.branches:
            result["branches"] = [branch.to_dict() for branch in self.branches]
        return result


@dataclass
class State:
    name: str
    id: Optional[str] = None
    path: Optional[str] = None
    parent: Optional[str] = None
    parent_id: Optional[str] = None
    entry: Optional[str] = None
    exit: Optional[str] = None
    initial_target: Optional[str] = None
    initial_target_state_id: Optional[str] = None
    initial_action: Optional[str] = None
    transitions: List[Transition] = field(default_factory=list)
    children: List["State"] = field(default_factory=list)

    def to_dict(self) -> Dict:
        result = {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "parent": self.parent,
            "parent_id": self.parent_id,
            "entry": self.entry,
            "exit": self.exit,
        }
        if self.initial_target:
            result["initial"] = {
                "target": self.initial_target,
                "target_state_id": self.initial_target_state_id,
                "action": self.initial_action,
                "kind": "external",
            }
        if self.transitions:
            result["transitions"] = [transition.to_dict() for transition in self.transitions]
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        return result


@dataclass
class Diagnostic:
    severity: str
    code: str
    message: str
    state_id: Optional[str] = None
    transition_id: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "state_id": self.state_id,
            "transition_id": self.transition_id,
        }


@dataclass
class TraceStep:
    phase: str
    state_id: Optional[str] = None
    source_state_id: Optional[str] = None
    target_state_id: Optional[str] = None
    code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase": self.phase,
            "state_id": self.state_id,
            "source_state_id": self.source_state_id,
            "target_state_id": self.target_state_id,
            "code": self.code,
        }


class QMCParser:
    """Parser for QM-generated C state machine code."""

    def __init__(self, c_code: str):
        self.c_code = c_code
        self.machine_name: str = ""
        self.states: Dict[str, State] = {}
        self.state_name_to_ids: Dict[str, List[str]] = {}
        self.top_initial: Optional[TransitionBranch] = None
        self.transitions: List[Transition] = []
        self.diagnostics: List[Diagnostic] = []
        self.is_reliable: bool = False

    def parse(self) -> Dict:
        self._extract_machine_name()
        self._parse_initial_function()
        self._parse_state_functions()
        self._build_hierarchy_and_paths()
        self._resolve_targets()
        self._assign_transition_ids()
        self._validate_model()
        self.is_reliable = not any(d.severity == "error" for d in self.diagnostics)
        return self._build_output()

    def _extract_machine_name(self) -> None:
        match = re.search(r"QState\s+(\w+)_initial\s*\(", self.c_code)
        if match:
            self.machine_name = match.group(1)

    def _parse_initial_function(self) -> None:
        pattern = re.compile(rf"QState\s+{re.escape(self.machine_name)}_initial\s*\([^)]+\)\s*\{{")
        match = pattern.search(self.c_code)
        if not match:
            return

        body = self._extract_function_body(match.end() - 1)
        target = self._extract_transition_target(body)
        self.top_initial = TransitionBranch(
            guard=None,
            target=target,
            action=self._extract_action_code(body),
            kind="external" if target else "unknown",
            is_else=False,
        )

    def _parse_state_functions(self) -> None:
        pattern = re.compile(rf"QState\s+({re.escape(self.machine_name)}_\w+)\s*\([^)]+\)\s*\{{")

        for match in pattern.finditer(self.c_code):
            func_name = match.group(1)
            state_name = self._extract_state_name(func_name)
            if state_name == "initial":
                continue

            body = self._extract_function_body(match.end() - 1)
            state = self._parse_state_body(state_name, body)
            self.states[state_name] = state

    def _parse_state_body(self, state_name: str, body: str) -> State:
        state = State(name=state_name)

        super_match = re.search(r"Q_SUPER\s*\(\s*&(\w+)\)", body)
        if super_match:
            parent_name = self._extract_state_name(super_match.group(1))
            if parent_name != "QHsm_top":
                state.parent = parent_name

        entry_body = self._extract_case_block(body, "Q_ENTRY")
        if entry_body is not None:
            state.entry = self._extract_action_code(entry_body)

        exit_body = self._extract_case_block(body, "Q_EXIT")
        if exit_body is not None:
            state.exit = self._extract_action_code(exit_body)

        init_body = self._extract_case_block(body, "Q_INIT")
        if init_body is not None:
            state.initial_action = self._extract_action_code(init_body)
            state.initial_target = self._extract_transition_target(init_body)

        for signal, case_body in self._iter_case_blocks(body):
            if signal in ("Q_ENTRY", "Q_EXIT", "Q_INIT"):
                continue
            transition = self._parse_transition(state_name, signal, case_body)
            if transition is not None:
                state.transitions.append(transition)
                self.transitions.append(transition)

        return state

    def _parse_transition(self, state_name: str, signal: str, body: str) -> Optional[Transition]:
        branches = self._extract_if_chain(body)
        if branches:
            parsed_branches = [
                self._parse_transition_branch(branch_body, guard=guard, is_else=is_else)
                for guard, branch_body, is_else in branches
            ]
            first = parsed_branches[0]
            return Transition(
                owner_state=state_name,
                owner_state_id=None,
                trigger=signal,
                kind="choice",
                target=first.target,
                target_state_id=None,
                action=first.action,
                guard=first.guard,
                branches=parsed_branches,
            )

        branch = self._parse_transition_branch(body, guard=None, is_else=False)
        return Transition(
            owner_state=state_name,
            owner_state_id=None,
            trigger=signal,
            kind=branch.kind,
            target=branch.target,
            target_state_id=None,
            action=branch.action,
            guard=branch.guard,
            branches=[],
        )

    def _parse_transition_branch(
        self,
        body: str,
        guard: Optional[str],
        is_else: bool,
    ) -> TransitionBranch:
        target = self._extract_transition_target(body)
        action = self._extract_action_code(body)
        kind = self._classify_transition_body(body, target)
        return TransitionBranch(
            guard=guard,
            target=target,
            target_state_id=None,
            action=action,
            kind=kind,
            is_else=is_else,
        )

    def _classify_transition_body(self, body: str, target: Optional[str]) -> str:
        if target:
            return "external"
        if re.search(r"\bQ_HANDLED\s*\(", body):
            return "internal"
        if re.search(r"\bQ_SUPER\s*\(", body):
            return "super"
        if re.search(r"\bQ_UNHANDLED\s*\(", body):
            return "unhandled"
        return "unknown"

    def _iter_case_blocks(self, body: str) -> List[Tuple[str, str]]:
        results: List[Tuple[str, str]] = []
        pattern = re.compile(r"case\s+(\w+)_SIG\s*:\s*\{")
        pos = 0

        while True:
            match = pattern.search(body, pos)
            if not match:
                break
            signal = match.group(1)
            brace_start = body.find("{", match.end() - 1)
            block, brace_end = self._extract_braced_block(body, brace_start)
            if block is None:
                break
            results.append((signal, block[1:-1]))
            pos = brace_end + 1

        return results

    def _extract_case_block(self, body: str, signal_name: str) -> Optional[str]:
        pattern = re.compile(rf"case\s+{re.escape(signal_name)}_SIG\s*:\s*\{{")
        match = pattern.search(body)
        if not match:
            return None
        brace_start = body.find("{", match.end() - 1)
        block, _ = self._extract_braced_block(body, brace_start)
        if block is None:
            return None
        return block[1:-1]

    def _extract_if_chain(self, body: str) -> List[Tuple[Optional[str], str, bool]]:
        results: List[Tuple[Optional[str], str, bool]] = []
        match = re.search(r"\bif\s*\(", body)
        if not match:
            return results

        cursor = match.start()
        while cursor < len(body):
            if body.startswith("if", cursor):
                open_paren = body.find("(", cursor)
                close_paren = self._find_matching(body, open_paren, "(", ")")
                if close_paren == -1:
                    return []
                guard = body[open_paren + 1:close_paren].strip()
                brace_start = body.find("{", close_paren)
                if brace_start == -1:
                    return []
                block, brace_end = self._extract_braced_block(body, brace_start)
                if block is None:
                    return []
                results.append((guard, block[1:-1], False))
                cursor = self._skip_ws_and_comments(body, brace_end + 1)
                if cursor >= len(body) or not body.startswith("else", cursor):
                    break
                cursor = self._skip_ws_and_comments(body, cursor + 4)
                if body.startswith("if", cursor):
                    continue
                if cursor < len(body) and body[cursor] == "{":
                    block, brace_end = self._extract_braced_block(body, cursor)
                    if block is None:
                        return []
                    results.append((None, block[1:-1], True))
                break
            else:
                break

        return results

    def _extract_transition_target(self, body: str) -> Optional[str]:
        match = re.search(r"\bQ_TRAN\s*\(\s*&(\w+)\)", body)
        if not match:
            return None
        return self._extract_state_name(match.group(1))

    def _extract_action_code(self, body: str) -> Optional[str]:
        lines: List[str] = []
        for raw_line in body.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line in ("{", "}"):
                continue
            if line.startswith("/*${") and line.endswith("*/"):
                continue
            if line == "break;":
                continue
            if line == "else {":
                continue
            if re.match(r"^status_\s*=\s*Q_(TRAN|HANDLED|SUPER|UNHANDLED)\b", line):
                continue
            if re.match(r"^return\s+Q_(TRAN|HANDLED|SUPER|UNHANDLED)\b", line):
                continue
            if re.match(r"^if\s*\(", line):
                continue
            if line == "}":
                continue
            lines.append(line)

        if not lines:
            return None
        return "\n".join(lines).strip()

    def _extract_braced_block(self, text: str, brace_start: int) -> Tuple[Optional[str], int]:
        if brace_start == -1 or brace_start >= len(text) or text[brace_start] != "{":
            return None, -1
        brace_end = self._find_matching(text, brace_start, "{", "}")
        if brace_end == -1:
            return None, -1
        return text[brace_start:brace_end + 1], brace_end

    def _find_matching(self, text: str, start: int, open_char: str, close_char: str) -> int:
        depth = 0
        in_string = False
        in_char = False
        in_line_comment = False
        in_block_comment = False
        escaped = False

        idx = start
        while idx < len(text):
            ch = text[idx]
            nxt = text[idx + 1] if idx + 1 < len(text) else ""

            if in_line_comment:
                if ch == "\n":
                    in_line_comment = False
                idx += 1
                continue

            if in_block_comment:
                if ch == "*" and nxt == "/":
                    in_block_comment = False
                    idx += 2
                    continue
                idx += 1
                continue

            if in_string:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    in_string = False
                idx += 1
                continue

            if in_char:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == "'":
                    in_char = False
                idx += 1
                continue

            if ch == "/" and nxt == "/":
                in_line_comment = True
                idx += 2
                continue
            if ch == "/" and nxt == "*":
                in_block_comment = True
                idx += 2
                continue
            if ch == '"':
                in_string = True
                idx += 1
                continue
            if ch == "'":
                in_char = True
                idx += 1
                continue

            if ch == open_char:
                depth += 1
            elif ch == close_char:
                depth -= 1
                if depth == 0:
                    return idx

            idx += 1

        return -1

    def _skip_ws_and_comments(self, text: str, start: int) -> int:
        idx = start
        while idx < len(text):
            if text[idx].isspace():
                idx += 1
                continue
            if text.startswith("//", idx):
                newline = text.find("\n", idx)
                return len(text) if newline == -1 else newline + 1
            if text.startswith("/*", idx):
                end = text.find("*/", idx + 2)
                return len(text) if end == -1 else self._skip_ws_and_comments(text, end + 2)
            break
        return idx

    def _extract_function_body(self, start_pos: int) -> str:
        brace_start = self.c_code.find("{", start_pos)
        if brace_start == -1:
            return ""
        block, _ = self._extract_braced_block(self.c_code, brace_start)
        return block or ""

    def _extract_state_name(self, func_name: str) -> str:
        prefix = self.machine_name + "_"
        if func_name.startswith(prefix):
            return func_name[len(prefix):]
        return func_name

    def _build_hierarchy_and_paths(self) -> None:
        for state in self.states.values():
            state.children = []

        for state in self.states.values():
            if state.parent and state.parent in self.states:
                self.states[state.parent].children.append(state)

        root_states = [state for state in self.states.values() if not state.parent or state.parent not in self.states]
        for root in root_states:
            self._assign_state_identity(root, parent_path=None)

        self.state_name_to_ids = {}
        for state in self.states.values():
            self.state_name_to_ids.setdefault(state.name, []).append(state.id)

        for state in self.states.values():
            state.parent_id = self.states[state.parent].id if state.parent in self.states else None
            for transition in state.transitions:
                transition.owner_state_id = state.id

    def _assign_state_identity(self, state: State, parent_path: Optional[str]) -> None:
        state.path = state.name if parent_path is None else f"{parent_path}/{state.name}"
        state.id = state.path
        for child in state.children:
            self._assign_state_identity(child, state.path)

    def _resolve_targets(self) -> None:
        if self.top_initial and self.top_initial.target:
            self.top_initial.target_state_id = self._resolve_state_name(self.top_initial.target)

        for state in self.states.values():
            if state.initial_target:
                state.initial_target_state_id = self._resolve_state_name(state.initial_target)

            for transition in state.transitions:
                transition.target_state_id = self._resolve_state_name(transition.target)
                if transition.branches:
                    first_external = next((branch for branch in transition.branches if branch.target), None)
                    if first_external:
                        transition.target = first_external.target
                        transition.target_state_id = self._resolve_state_name(first_external.target)
                        transition.action = first_external.action
                        transition.guard = first_external.guard
                    for branch in transition.branches:
                        branch.target_state_id = self._resolve_state_name(branch.target)

    def _resolve_state_name(self, name: Optional[str]) -> Optional[str]:
        if not name:
            return None
        ids = self.state_name_to_ids.get(name, [])
        return ids[0] if len(ids) == 1 else None

    def _assign_transition_ids(self) -> None:
        counters: Dict[str, int] = {}
        for transition in self.transitions:
            owner = transition.owner_state_id or transition.owner_state or "unknown"
            counters.setdefault(owner, 0)
            transition.id = f"{owner}::{transition.trigger}#{counters[owner]}"
            counters[owner] += 1

    def _add_diagnostic(
        self,
        severity: str,
        code: str,
        message: str,
        *,
        state_id: Optional[str] = None,
        transition_id: Optional[str] = None,
    ) -> None:
        self.diagnostics.append(
            Diagnostic(
                severity=severity,
                code=code,
                message=message,
                state_id=state_id,
                transition_id=transition_id,
            )
        )

    def _validate_model(self) -> None:
        if not self.machine_name:
            self._add_diagnostic("error", "machine.missing_name", "Could not locate the QM machine name.")

        if not self.states:
            self._add_diagnostic("error", "state.none_found", "No QM state handlers were parsed from the C file.")

        if not self.top_initial:
            self._add_diagnostic("error", "top_initial.missing", "Top initial transition is missing.")
        elif not self.top_initial.target_state_id:
            target = self.top_initial.target or "<missing>"
            self._add_diagnostic(
                "error",
                "top_initial.unresolved_target",
                f"Top initial target could not be resolved: {target}.",
            )

        for state in self._states_preorder():
            if state.parent and state.parent_id is None:
                self._add_diagnostic(
                    "error",
                    "state.unresolved_parent",
                    f"Parent state could not be resolved: {state.parent}.",
                    state_id=state.id,
                )
            if state.initial_target and not state.initial_target_state_id:
                self._add_diagnostic(
                    "error",
                    "state.unresolved_initial",
                    f"Initial target could not be resolved: {state.initial_target}.",
                    state_id=state.id,
                )

        for transition in self.transitions:
            if transition.kind == "unknown":
                self._add_diagnostic(
                    "error",
                    "transition.unknown_kind",
                    "Transition kind could not be classified from the handler body.",
                    state_id=transition.owner_state_id,
                    transition_id=transition.id,
                )
            if transition.kind == "external" and not transition.target_state_id:
                target = transition.target or "<missing>"
                self._add_diagnostic(
                    "error",
                    "transition.unresolved_target",
                    f"External transition target could not be resolved: {target}.",
                    state_id=transition.owner_state_id,
                    transition_id=transition.id,
                )
            if transition.branches:
                for index, branch in enumerate(transition.branches):
                    if branch.kind == "unknown":
                        self._add_diagnostic(
                            "error",
                            "branch.unknown_kind",
                            f"Choice branch #{index} could not be classified from the handler body.",
                            state_id=transition.owner_state_id,
                            transition_id=transition.id,
                        )
                    if branch.kind == "external" and not branch.target_state_id:
                        target = branch.target or "<missing>"
                        self._add_diagnostic(
                            "error",
                            "branch.unresolved_target",
                            f"Choice branch #{index} target could not be resolved: {target}.",
                            state_id=transition.owner_state_id,
                            transition_id=transition.id,
                        )
                if not any(branch.is_else for branch in transition.branches):
                    self._add_diagnostic(
                        "warning",
                        "choice.no_else",
                        "Choice transition has no explicit else branch.",
                        state_id=transition.owner_state_id,
                        transition_id=transition.id,
                    )

    def _build_output(self) -> Dict:
        root_states = self._root_states()
        return {
            "machine_name": self.machine_name,
            "top_initial": self.top_initial.to_dict() if self.top_initial else None,
            "states": [state.to_dict() for state in root_states],
            "transitions": [transition.to_dict() for transition in self.transitions],
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
            "is_reliable": self.is_reliable,
            "state_count": len(self.states),
            "transition_count": len(self.transitions),
        }

    def to_text(self) -> str:
        output: List[str] = []
        output.append(f"Machine: {self.machine_name or '<unknown>'}")
        output.append(f"States: {len(self.states)}")
        output.append(f"Transitions: {len(self.transitions)}")
        output.append(f"Reliable: {'yes' if self.is_reliable else 'no'}")
        output.append("")

        output.append("Diagnostics:")
        diagnostic_lines = self._diagnostic_lines()
        if diagnostic_lines:
            output.extend(diagnostic_lines)
        else:
            output.append("- none")
        output.append("")

        output.append("State Hierarchy:")
        for root in self._root_states():
            output.extend(self._state_to_text_tree(root, 0))
        output.append("")

        output.append("Default Initial Path:")
        default_path = self._default_initial_path()
        if default_path:
            output.append(f"- top -> {' -> '.join(default_path)}")
        else:
            output.append("- unresolved")
        output.append("")

        output.append("Composite Initials:")
        composite_lines = self._composite_initial_lines()
        if composite_lines:
            output.extend(composite_lines)
        else:
            output.append("- none")
        output.append("")

        output.append("State Index:")
        for state in self._states_preorder():
            parent = state.parent_id or "top"
            output.append(f"- {state.id}: parent={parent}")
        output.append("")

        output.append("State Semantics:")
        semantics_lines = self._state_semantics_lines()
        if semantics_lines:
            output.extend(semantics_lines)
        else:
            output.append("- none")
        output.append("")

        output.append("Transitions By State:")
        transition_lines = self._transition_summary_lines()
        if transition_lines:
            output.extend(transition_lines)
        else:
            output.append("- none")

        return "\n".join(output)

    def to_trace(self) -> str:
        output: List[str] = []
        output.append(f"Machine: {self.machine_name or '<unknown>'}")
        output.append(f"Reliable: {'yes' if self.is_reliable else 'no'}")
        output.append("")

        output.append("Diagnostics:")
        diagnostic_lines = self._diagnostic_lines()
        if diagnostic_lines:
            output.extend(diagnostic_lines)
        else:
            output.append("- none")
        output.append("")

        output.append("Default Init Trace:")
        default_trace = self._default_init_trace_lines()
        if default_trace:
            output.extend(default_trace)
        else:
            output.append("- unresolved")
        output.append("")

        output.append("External Transition Traces:")
        external_lines = self._external_transition_trace_lines()
        if external_lines:
            output.extend(external_lines)
        else:
            output.append("- none")
        output.append("")

        output.append("Handled Event Ownership:")
        ownership_lines = self._handled_event_ownership_lines()
        if ownership_lines:
            output.extend(ownership_lines)
        else:
            output.append("- none")
        return "\n".join(output)

    def to_trace_dict(self) -> Dict[str, Any]:
        return {
            "machine_name": self.machine_name,
            "is_reliable": self.is_reliable,
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
            "default_init_trace": {
                "target_state_id": self.top_initial.target_state_id if self.top_initial else None,
                "steps": [step.to_dict() for step in self._default_init_trace_steps()],
            },
            "external_transition_traces": [
                self._external_transition_trace_dict(transition, branch)
                for transition, branch in self._iter_external_trace_pairs()
            ],
            "handled_event_ownership": [
                self._handled_event_ownership_dict(state)
                for state in self._states_preorder()
                if self._state_has_handling_summary(state)
            ],
        }

    def to_plantuml(self) -> str:
        output = ["@startuml", ""]

        if self.top_initial and self.top_initial.target:
            action = f" / {self.top_initial.action}" if self.top_initial.action else ""
            output.append(f"[*] --> {self.top_initial.target}{action}")
            output.append("")

        for state in self.states.values():
            if not state.parent:
                output.extend(self._state_to_plantuml(state, 0))

        output.append("")
        output.append("@enduml")
        return "\n".join(output)

    def _root_states(self) -> List[State]:
        return [
            state for state in self.states.values()
            if not state.parent or state.parent not in self.states
        ]

    def _states_preorder(self) -> List[State]:
        ordered: List[State] = []
        for root in self._root_states():
            ordered.extend(self._collect_states_preorder(root))
        return ordered

    def _collect_states_preorder(self, state: State) -> List[State]:
        ordered = [state]
        for child in state.children:
            ordered.extend(self._collect_states_preorder(child))
        return ordered

    def _state_to_text_tree(self, state: State, depth: int) -> List[str]:
        indent = "  " * depth
        line = f"{indent}- {state.id}"
        if state.initial_target_state_id:
            line += f" [initial -> {state.initial_target_state_id}]"
        return [line] + [
            child_line
            for child in state.children
            for child_line in self._state_to_text_tree(child, depth + 1)
        ]

    def _default_initial_path(self) -> List[str]:
        if not self.top_initial or not self.top_initial.target_state_id:
            return []

        path: List[str] = []
        current_id = self.top_initial.target_state_id
        visited = set()
        while current_id and current_id not in visited:
            visited.add(current_id)
            path.append(current_id)
            state = self._get_state_by_id(current_id)
            if state is None or not state.initial_target_state_id:
                break
            current_id = state.initial_target_state_id
        return path

    def _composite_initial_lines(self) -> List[str]:
        lines: List[str] = []
        for state in self._states_preorder():
            if state.initial_target_state_id:
                action = f" / {state.initial_action}" if state.initial_action else ""
                lines.append(f"- {state.id} -> {state.initial_target_state_id}{action}")
        return lines

    def _state_semantics_lines(self) -> List[str]:
        lines: List[str] = []
        for state in self._states_preorder():
            state_lines: List[str] = []
            if state.entry:
                state_lines.append(f"entry: {state.entry}")
            if state.exit:
                state_lines.append(f"exit: {state.exit}")
            if state.initial_target_state_id:
                action = f" / {state.initial_action}" if state.initial_action else ""
                state_lines.append(f"initial: {state.initial_target_state_id}{action}")
            if state_lines:
                lines.append(f"- {state.id}")
                lines.extend([f"  - {item}" for item in state_lines])
        return lines

    def _transition_summary_lines(self) -> List[str]:
        lines: List[str] = []
        for state in self._states_preorder():
            if not state.transitions:
                continue
            lines.append(f"- {state.id}")
            for transition in state.transitions:
                lines.extend(self._describe_transition(transition))
        return lines

    def _describe_transition(self, transition: Transition) -> List[str]:
        lines: List[str] = []
        if transition.branches:
            lines.append(f"  - {transition.trigger}: choice [{transition.id}]")
            for branch in transition.branches:
                branch_label = "[else]" if branch.is_else else (
                    f"[{branch.guard}]" if branch.guard else "[unguarded]"
                )
                target = branch.target_state_id or branch.target or "-"
                branch_line = f"    - {branch_label} {branch.kind}"
                if branch.kind == "external":
                    branch_line += f" -> {target}"
                elif branch.kind in ("super", "unhandled") and target != "-":
                    branch_line += f" -> {target}"
                if branch.action:
                    branch_line += f" / {branch.action}"
                lines.append(branch_line)
            return lines

        line = f"  - {transition.trigger}: {transition.kind} [{transition.id}]"
        target = transition.target_state_id or transition.target
        if target:
            line += f" -> {target}"
        if transition.guard:
            line += f" [{transition.guard}]"
        if transition.action:
            line += f" / {transition.action}"
        lines.append(line)
        return lines

    def _get_state_by_id(self, state_id: Optional[str]) -> Optional[State]:
        if not state_id:
            return None
        for state in self.states.values():
            if state.id == state_id:
                return state
        return None

    def _diagnostic_lines(self) -> List[str]:
        lines: List[str] = []
        for diagnostic in self.diagnostics:
            suffix_parts: List[str] = []
            if diagnostic.state_id:
                suffix_parts.append(f"state={diagnostic.state_id}")
            if diagnostic.transition_id:
                suffix_parts.append(f"transition={diagnostic.transition_id}")
            suffix = f" ({', '.join(suffix_parts)})" if suffix_parts else ""
            lines.append(f"- {diagnostic.severity.upper()} {diagnostic.code}: {diagnostic.message}{suffix}")
        return lines

    def _default_init_trace_lines(self) -> List[str]:
        return self._trace_steps_to_lines(self._default_init_trace_steps())

    def _external_transition_trace_lines(self) -> List[str]:
        lines: List[str] = []
        for transition, branch in self._iter_external_trace_pairs():
            lines.extend(self._trace_steps_to_lines(self._external_trace_steps_for_branch(transition, branch)))
        return lines

    def _external_trace_steps_for_branch(
        self,
        transition: Transition,
        branch: TransitionBranch,
    ) -> List[TraceStep]:
        if not transition.owner_state_id or not branch.target_state_id:
            return []

        steps: List[TraceStep] = [
            TraceStep(
                phase="transition",
                source_state_id=transition.owner_state_id,
                target_state_id=branch.target_state_id,
                code=self._transition_header(transition, branch),
            )
        ]

        for state_id in self._exit_chain_for_transition(transition.owner_state_id, branch.target_state_id):
            steps.append(TraceStep(phase="exit", state_id=state_id))
        if branch.action:
            steps.append(TraceStep(phase="effect", code=branch.action))
        for state_id in self._entry_chain_for_transition(transition.owner_state_id, branch.target_state_id):
            steps.append(TraceStep(phase="enter", state_id=state_id))
        steps.extend(self._nested_init_chain_after_entry_steps(branch.target_state_id))
        return steps

    def _handled_event_ownership_lines(self) -> List[str]:
        lines: List[str] = []
        for state in self._states_preorder():
            handled = [transition for transition in state.transitions if transition.kind in ("internal", "choice", "external")]
            supered = [transition for transition in state.transitions if transition.kind == "super"]
            if not handled and not supered:
                continue
            lines.append(f"- {state.id}")
            for transition in handled:
                lines.append(f"  - {transition.trigger}: owned here as {transition.kind} [{transition.id}]")
            for transition in supered:
                parent = state.parent_id or "top"
                lines.append(f"  - {transition.trigger}: delegated to {parent} [{transition.id}]")
        return lines

    def _iter_external_trace_pairs(self) -> List[Tuple[Transition, TransitionBranch]]:
        pairs: List[Tuple[Transition, TransitionBranch]] = []
        for transition in self.transitions:
            if transition.kind == "external" and transition.owner_state_id and transition.target_state_id:
                pairs.append(
                    (
                        transition,
                        TransitionBranch(
                            guard=transition.guard,
                            target=transition.target,
                            target_state_id=transition.target_state_id,
                            action=transition.action,
                            kind=transition.kind,
                            is_else=False,
                        ),
                    )
                )
            elif transition.branches:
                for branch in transition.branches:
                    if branch.kind == "external" and transition.owner_state_id and branch.target_state_id:
                        pairs.append((transition, branch))
        return pairs

    def _transition_header(self, transition: Transition, branch: TransitionBranch) -> str:
        branch_label = "[else]" if branch.is_else else (f"[{branch.guard}]" if branch.guard else "")
        header = f"{transition.id}: {transition.owner_state_id} --{transition.trigger}"
        if branch_label:
            header += f" {branch_label}"
        header += f"--> {branch.target_state_id}"
        return header

    def _state_has_handling_summary(self, state: State) -> bool:
        handled = [transition for transition in state.transitions if transition.kind in ("internal", "choice", "external")]
        delegated = [transition for transition in state.transitions if transition.kind == "super"]
        return bool(handled or delegated)

    def _handled_event_ownership_dict(self, state: State) -> Dict[str, Any]:
        handled = [transition for transition in state.transitions if transition.kind in ("internal", "choice", "external")]
        delegated = [transition for transition in state.transitions if transition.kind == "super"]
        return {
            "state_id": state.id,
            "owned": [
                {
                    "transition_id": transition.id,
                    "trigger": transition.trigger,
                    "kind": transition.kind,
                }
                for transition in handled
            ],
            "delegated": [
                {
                    "transition_id": transition.id,
                    "trigger": transition.trigger,
                    "delegates_to": state.parent_id or "top",
                }
                for transition in delegated
            ],
        }

    def _default_init_trace_steps(self) -> List[TraceStep]:
        if not self.top_initial or not self.top_initial.target_state_id:
            return []
        steps = [
            TraceStep(
                phase="top_init",
                source_state_id="TOP",
                target_state_id=self.top_initial.target_state_id,
            )
        ]
        if self.top_initial.action:
            steps.append(TraceStep(phase="effect", code=self.top_initial.action))
        current_id = self.top_initial.target_state_id
        steps.extend(TraceStep(phase="enter", state_id=state_id) for state_id in self._entry_chain_for_target(current_id))
        steps.extend(self._nested_init_chain_after_entry_steps(current_id))
        return self._dedupe_adjacent_trace_steps(steps)

    def _nested_init_chain_after_entry_steps(self, target_state_id: str) -> List[TraceStep]:
        steps: List[TraceStep] = []
        current_id = target_state_id
        visited = set()
        while current_id and current_id not in visited:
            visited.add(current_id)
            state = self._get_state_by_id(current_id)
            if state is None or not state.initial_target_state_id:
                break
            steps.append(
                TraceStep(
                    phase="init",
                    source_state_id=state.id,
                    target_state_id=state.initial_target_state_id,
                )
            )
            if state.initial_action:
                steps.append(TraceStep(phase="effect", code=state.initial_action))
            for entry_state_id in self._entry_chain_for_transition(state.id, state.initial_target_state_id):
                steps.append(TraceStep(phase="enter", state_id=entry_state_id))
            current_id = state.initial_target_state_id
        return steps

    def _trace_steps_to_lines(self, steps: List[TraceStep]) -> List[str]:
        lines: List[str] = []
        for step in steps:
            if step.phase == "top_init":
                lines.append(f"- TOP_INIT -> {step.target_state_id}")
            elif step.phase == "transition":
                lines.append(f"- {step.code}")
            elif step.phase == "exit":
                lines.append(f"  - exit: {step.state_id}")
            elif step.phase == "enter":
                prefix = "  - enter: " if lines and lines[-1].startswith("  -") else "- enter: "
                lines.append(f"{prefix}{step.state_id}")
            elif step.phase == "init":
                lines.append(f"  - init: {step.source_state_id} -> {step.target_state_id}")
            elif step.phase == "effect":
                prefix = "  - effect: " if lines and lines[-1].startswith("  -") else "- effect: "
                lines.append(f"{prefix}{step.code}")
        return lines

    def _dedupe_adjacent_trace_steps(self, steps: List[TraceStep]) -> List[TraceStep]:
        result: List[TraceStep] = []
        previous: Optional[Tuple[str, Optional[str], Optional[str], Optional[str], Optional[str]]] = None
        for step in steps:
            marker = (step.phase, step.state_id, step.source_state_id, step.target_state_id, step.code)
            if marker != previous:
                result.append(step)
            previous = marker
        return result

    def _external_transition_trace_dict(self, transition: Transition, branch: TransitionBranch) -> Dict[str, Any]:
        return {
            "transition_id": transition.id,
            "source_state_id": transition.owner_state_id,
            "trigger": transition.trigger,
            "guard": branch.guard,
            "is_else": branch.is_else,
            "target_state_id": branch.target_state_id,
            "steps": [step.to_dict() for step in self._external_trace_steps_for_branch(transition, branch)],
        }

    def _state_lineage(self, state_id: str) -> List[str]:
        lineage: List[str] = []
        current = self._get_state_by_id(state_id)
        while current is not None:
            lineage.append(current.id or current.name)
            current = self._get_state_by_id(current.parent_id)
        return lineage

    def _entry_chain_for_target(self, target_state_id: str) -> List[str]:
        lineage = list(reversed(self._state_lineage(target_state_id)))
        return lineage

    def _exit_chain_for_transition(self, source_state_id: str, target_state_id: str) -> List[str]:
        source_lineage = self._state_lineage(source_state_id)
        target_lineage = self._state_lineage(target_state_id)
        target_set = set(target_lineage)
        exits: List[str] = []
        for state_id in source_lineage:
            if state_id in target_set:
                break
            exits.append(state_id)
        return exits

    def _entry_chain_for_transition(self, source_state_id: str, target_state_id: str) -> List[str]:
        source_lineage = self._state_lineage(source_state_id)
        target_lineage = self._state_lineage(target_state_id)
        common_index: Optional[int] = None
        source_set = set(source_lineage)
        for index, state_id in enumerate(target_lineage):
            if state_id in source_set:
                common_index = index
                break
        if common_index is None:
            return list(reversed(target_lineage))
        return list(reversed(target_lineage[:common_index]))

    def _nested_init_chain_after_entry(self, target_state_id: str) -> List[str]:
        return self._trace_steps_to_lines(self._nested_init_chain_after_entry_steps(target_state_id))

    def _dedupe_adjacent(self, lines: List[str]) -> List[str]:
        result: List[str] = []
        previous: Optional[str] = None
        for line in lines:
            if line != previous:
                result.append(line)
            previous = line
        return result

    def _state_to_plantuml(self, state: State, indent: int) -> List[str]:
        lines: List[str] = []
        prefix = "  " * indent
        inner_prefix = prefix + "  "

        if state.children:
            lines.append(f"{prefix}state {state.name} {{")
        else:
            lines.append(f"{prefix}state {state.name}")

        if state.initial_target:
            action = f" / {state.initial_action}" if state.initial_action else ""
            lines.append(f"{inner_prefix}[*] --> {state.initial_target}{action}")

        if state.entry:
            lines.append(f"{inner_prefix}entry: {state.entry}")
        if state.exit:
            lines.append(f"{inner_prefix}exit: {state.exit}")

        for transition in state.transitions:
            if transition.branches:
                for branch in transition.branches:
                    if branch.target:
                        guard = " [else]" if branch.is_else else (f" [{branch.guard}]" if branch.guard else "")
                        action = f" / {branch.action}" if branch.action else ""
                        lines.append(
                            f"{inner_prefix}{state.name} --> {branch.target}: {transition.trigger}{guard}{action}"
                        )
            elif transition.target:
                guard = f" [{transition.guard}]" if transition.guard else ""
                action = f" / {transition.action}" if transition.action else ""
                lines.append(
                    f"{inner_prefix}{state.name} --> {transition.target}: {transition.trigger}{guard}{action}"
                )

        for child in state.children:
            lines.extend(self._state_to_plantuml(child, indent + 1))

        if state.children:
            lines.append(f"{prefix}}}")

        return lines


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse QM-generated C state machine code into a semantic model",
    )
    parser.add_argument("input", help="Input C file")
    parser.add_argument(
        "--output",
        "-o",
        choices=["json", "plantuml", "text", "trace", "trace-json"],
        default="json",
        help="Output format",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 2 when unresolved or unreliable semantics remain.",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as handle:
        c_code = handle.read()

    qm_parser = QMCParser(c_code)
    result = qm_parser.parse()

    if args.strict and not qm_parser.is_reliable:
        print(json.dumps(result, indent=2, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)

    if args.output == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.output == "plantuml":
        print(qm_parser.to_plantuml())
    elif args.output == "trace-json":
        print(json.dumps(qm_parser.to_trace_dict(), indent=2, ensure_ascii=False))
    elif args.output == "trace":
        print(qm_parser.to_trace())
    else:
        print(qm_parser.to_text())


if __name__ == "__main__":
    main()
