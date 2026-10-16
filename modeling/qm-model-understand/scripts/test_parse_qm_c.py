#!/usr/bin/env python3
"""QM topology regressions, independent of runtime execution."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from parse_qm_c import QMCParser
from validate_ir import validate

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "assets/examples/smhsmtst.c"


def flatten(states):
    return [item for state in states for item in [state, *flatten(state.get("children", []))]]


class TopologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = EXAMPLE.read_text()
        cls.parser = QMCParser(cls.source)
        cls.model = cls.parser.parse()
        cls.states = {s["id"]: s for s in flatten(cls.model["states"])}

    def transition(self, owner, trigger):
        matches = [t for t in self.model["transitions"]
                   if t["owner_state_id"] == owner and t["trigger"] == trigger]
        self.assertEqual(len(matches), 1)
        return matches[0]

    def test_hierarchy_matches_source(self):
        self.assertEqual({key: s["parent_id"] for key, s in self.states.items()}, {
            "s": None, "s/s1": "s", "s/s1/s11": "s/s1", "s/s2": "s",
            "s/s2/s21": "s/s2", "s/s2/s21/s211": "s/s2/s21",
        })
        self.assertEqual(self.model["state_count"], 6)
        self.assertEqual(self.model["transition_count"], 19)
        validate(self.model)

    def test_initial_targets_match_source(self):
        self.assertEqual(self.model["top_initial"]["target_state_id"], "s/s2")
        self.assertEqual(self.states["s"]["initial"]["target_state_id"], "s/s1/s11")
        self.assertEqual(self.states["s/s2"]["initial"]["target_state_id"], "s/s2/s21/s211")

    def test_self_parent_child_and_cross_branch_edges(self):
        for owner, trigger, target in (
            ("s/s1", "A", "s/s1"), ("s/s1", "B", "s/s1/s11"),
            ("s/s1/s11", "H", "s"), ("s/s1/s11", "G", "s/s2/s21/s211"),
        ):
            with self.subTest(owner=owner, trigger=trigger):
                self.assertEqual(self.transition(owner, trigger)["target_state_id"], target)

    def test_guard_and_unhandled_else_are_separate(self):
        branches = self.transition("s/s1", "D")["branches"]
        self.assertEqual([(b["guard"], b["kind"], b["target_state_id"], b["is_else"])
                          for b in branches], [
            ("!me->foo", "external", "s", False), (None, "unhandled", None, True),
        ])
        self.assertEqual(self.transition("s/s1", "I")["kind"], "internal")

    def test_choice_preserves_both_external_destinations(self):
        marker = "status_ = Q_TRAN(&SmHsmTst_s);"
        prefix, rest = self.source.split(marker, 1)
        changed = prefix + marker + rest.replace(
            "status_ = Q_UNHANDLED();", "status_ = Q_TRAN(&SmHsmTst_s2);", 1)
        model = QMCParser(changed).parse()
        transition = next(t for t in model["transitions"]
                          if t["owner_state_id"] == "s/s1" and t["trigger"] == "D")
        self.assertEqual([b["target_state_id"] for b in transition["branches"]], ["s", "s/s2"])

    def test_text_explains_topology(self):
        text = self.parser.to_text()
        for item in ("State Hierarchy:", "Default Initial Path:", "Transitions By State:",
                     "[!me->foo] external -> s"):
            self.assertIn(item, text)

    def test_strict_cli_rejects_unresolved_target(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "unresolved.c"
            source.write_text(self.source.replace("return Q_TRAN(&SmHsmTst_s2);",
                                                  "return Q_TRAN(&SmHsmTst_missing);", 1))
            result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/parse_qm_c.py"),
                                     str(source), "--output", "json", "--strict"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(json.loads(result.stderr)["is_reliable"])

    def test_cli_limits_outputs_to_topology_formats(self):
        for mode in ("trace", "trace-json", "plantuml"):
            with self.subTest(mode=mode):
                result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/parse_qm_c.py"),
                                         str(EXAMPLE), "--output", mode], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
