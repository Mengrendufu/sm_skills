#!/usr/bin/env python3
"""Tests for export_model_tree note and documentation sections."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from export_model_tree import export_tree


def _section(text: str, start: str, end: str | None = None) -> str:
    lines = text.splitlines()
    begin = None
    stop = len(lines)
    for i, line in enumerate(lines):
        if begin is None and (line == start or line.startswith(start + " ")):
            begin = i
            continue
        if begin is not None and end and (line == end or line.startswith(end + " ")):
            stop = i
            break
    if begin is None:
        return ""
    return "\n".join(lines[begin:stop])


def _model():
    return {
        "_type": "Project",
        "_id": "P",
        "name": "Demo",
        "ownedElements": [
            {
                "_type": "UMLModel",
                "_id": "M",
                "_parent": {"$ref": "P"},
                "name": "project",
                "documentation": "model-level docs",
                "ownedElements": [
                    {
                        "_type": "UMLPackageDiagram",
                        "_id": "D",
                        "_parent": {"$ref": "M"},
                        "name": "Arch",
                        "ownedViews": [
                            {
                                "_type": "UMLPackageView",
                                "_id": "PV",
                                "_parent": {"$ref": "D"},
                                "model": {"$ref": "Pkg"},
                            },
                            {
                                "_type": "UMLNoteView",
                                "_id": "N1",
                                "_parent": {"$ref": "D"},
                                "text": "FrontEnd talks to BackEnd",
                            },
                            {
                                "_type": "UMLNoteLinkView",
                                "_id": "L1",
                                "_parent": {"$ref": "D"},
                                "head": {"$ref": "N1"},
                                "tail": {"$ref": "PV"},
                            },
                            {
                                "_type": "UMLNoteView",
                                "_id": "N2",
                                "_parent": {"$ref": "D"},
                            },
                        ],
                    },
                    {
                        "_type": "UMLPackage",
                        "_id": "Pkg",
                        "_parent": {"$ref": "M"},
                        "name": "FrontEnd",
                        "documentation": "owns the webview",
                    },
                ],
            }
        ],
    }


def _shared_element_model():
    return {
        "_type": "Project",
        "_id": "P",
        "name": "Demo",
        "ownedElements": [
            {
                "_type": "UMLModel",
                "_id": "M",
                "_parent": {"$ref": "P"},
                "name": "project",
                "ownedElements": [
                    {
                        "_type": "UMLPackageDiagram",
                        "_id": "D1",
                        "_parent": {"$ref": "M"},
                        "name": "Arch",
                        "ownedViews": [
                            {
                                "_type": "UMLPackageView",
                                "_id": "PV1",
                                "_parent": {"$ref": "D1"},
                                "model": {"$ref": "FE"},
                                "containedViews": [{"$ref": "PV2"}],
                            },
                            {
                                "_type": "UMLPackageView",
                                "_id": "PV2",
                                "_parent": {"$ref": "D1"},
                                "model": {"$ref": "WV"},
                            },
                            {
                                "_type": "UMLPackageView",
                                "_id": "PV3",
                                "_parent": {"$ref": "D1"},
                                "model": {"$ref": "BE"},
                            },
                            {
                                "_type": "UMLDependencyView",
                                "_id": "DV1",
                                "_parent": {"$ref": "D1"},
                                "model": {"$ref": "Dep"},
                                "head": {"$ref": "PV3"},
                                "tail": {"$ref": "PV1"},
                            },
                        ],
                    },
                    {
                        "_type": "UMLPackageDiagram",
                        "_id": "D2",
                        "_parent": {"$ref": "M"},
                        "name": "Detail",
                        "ownedViews": [
                            {
                                "_type": "UMLPackageView",
                                "_id": "PV4",
                                "_parent": {"$ref": "D2"},
                                "model": {"$ref": "FE"},
                            }
                        ],
                    },
                    {
                        "_type": "UMLPackage",
                        "_id": "FE",
                        "_parent": {"$ref": "M"},
                        "name": "FrontEnd",
                        "ownedElements": [
                            {
                                "_type": "UMLPackage",
                                "_id": "WV",
                                "_parent": {"$ref": "FE"},
                                "name": "webview",
                            },
                            {
                                "_type": "UMLDependency",
                                "_id": "Dep",
                                "_parent": {"$ref": "FE"},
                                "source": {"$ref": "FE"},
                                "target": {"$ref": "BE"},
                            },
                        ],
                    },
                    {
                        "_type": "UMLPackage",
                        "_id": "BE",
                        "_parent": {"$ref": "M"},
                        "name": "BackEnd",
                    },
                ],
            }
        ],
    }


class ExportTreeAnnotationsTest(unittest.TestCase):
    def test_output_has_explorer_and_diagrams_only(self):
        text = export_tree(_model())
        headings = [line for line in text.splitlines() if line.startswith("# ")]
        self.assertEqual(headings, ["# Explorer", "# Diagrams"])

    def test_notes_and_documentation_are_listed_not_as_explorer_children(self):
        text = export_tree(_model())
        explorer, diagrams = _section(text, "# Explorer", "# Diagrams"), _section(text, "# Diagrams")
        self.assertNotIn("[UMLNoteView]", explorer)
        self.assertIn("documentation: model-level docs", explorer)
        self.assertIn("documentation: owns the webview", explorer)
        self.assertIn("note  linked=FrontEnd [UMLPackage]", diagrams)
        self.assertIn("text=FrontEnd talks to BackEnd", diagrams)
        self.assertIn("text=(empty)", diagrams)

    def test_same_element_listed_on_each_diagram_it_appears_on(self):
        text = export_tree(_shared_element_model())
        explorer, diagrams = _section(text, "# Explorer", "# Diagrams"), _section(text, "# Diagrams")
        self.assertEqual(explorer.count("[UMLPackage] FrontEnd"), 1)
        arch = diagrams.split("## Detail")[0]
        detail = diagrams.split("## Detail", 1)[1]
        self.assertIn("## Arch [UMLPackageDiagram]  owner=project [UMLModel]", arch)
        self.assertIn("FrontEnd [UMLPackage]", arch)
        self.assertIn("contains: webview [UMLPackage]", arch)
        self.assertIn("BackEnd [UMLPackage]", arch)
        self.assertIn("(unnamed) [UMLDependency]  tail=FrontEnd [UMLPackage]  head=BackEnd [UMLPackage]", arch)
        self.assertIn("FrontEnd [UMLPackage]", detail)
        self.assertNotIn("BackEnd [UMLPackage]", detail)
        self.assertNotIn("[UMLDependency]", detail)


def _sequence_model():
    return {
        "_type": "Project",
        "_id": "P",
        "name": "Demo",
        "ownedElements": [
            {
                "_type": "UMLCollaboration",
                "_id": "C",
                "_parent": {"$ref": "P"},
                "name": "ops",
                "ownedElements": [
                    {
                        "_type": "UMLInteraction",
                        "_id": "I",
                        "_parent": {"$ref": "C"},
                        "name": "Connect",
                        "ownedElements": [
                            {
                                "_type": "UMLSequenceDiagram",
                                "_id": "SD",
                                "_parent": {"$ref": "I"},
                                "name": "ConnectSerialPort",
                                "ownedViews": [
                                    {
                                        "_type": "UMLFrameView",
                                        "_id": "FV",
                                        "_parent": {"$ref": "SD"},
                                        "model": {"$ref": "SD"},
                                    },
                                    {
                                        "_type": "UMLSeqLifelineView",
                                        "_id": "LV1",
                                        "_parent": {"$ref": "SD"},
                                        "model": {"$ref": "L1"},
                                    },
                                    {
                                        "_type": "UMLSeqLifelineView",
                                        "_id": "LV2",
                                        "_parent": {"$ref": "SD"},
                                        "model": {"$ref": "L2"},
                                    },
                                    {
                                        "_type": "UMLSeqMessageView",
                                        "_id": "MV1",
                                        "_parent": {"$ref": "SD"},
                                        "model": {"$ref": "M1"},
                                        "head": {"$ref": "LV2"},
                                        "tail": {"$ref": "LV1"},
                                        "points": "10:200;90:200",
                                    },
                                    {
                                        "_type": "UMLSeqMessageView",
                                        "_id": "MV2",
                                        "_parent": {"$ref": "SD"},
                                        "model": {"$ref": "M2"},
                                        "head": {"$ref": "LV2"},
                                        "tail": {"$ref": "LV1"},
                                        "points": "10:80;90:80",
                                    },
                                    {
                                        "_type": "UMLCombinedFragmentView",
                                        "_id": "CV",
                                        "_parent": {"$ref": "SD"},
                                        "model": {"$ref": "CF"},
                                    },
                                ],
                            },
                            {
                                "_type": "UMLLifeline",
                                "_id": "L1",
                                "_parent": {"$ref": "I"},
                                "name": "UI",
                                "represent": {"$ref": "UICls"},
                            },
                            {
                                "_type": "UMLLifeline",
                                "_id": "L2",
                                "_parent": {"$ref": "I"},
                                "name": "SP_Manager",
                            },
                            {
                                "_type": "UMLMessage",
                                "_id": "M2",
                                "_parent": {"$ref": "I"},
                                "name": "SPMNGR_PORT_CONNECT",
                                "messageSort": "asynchSignal",
                                "source": {"$ref": "L1"},
                                "target": {"$ref": "L2"},
                            },
                            {
                                "_type": "UMLMessage",
                                "_id": "M1",
                                "_parent": {"$ref": "I"},
                                "name": "UI_REFRESHED_PORTS",
                                "source": {"$ref": "L1"},
                                "target": {"$ref": "L2"},
                            },
                            {
                                "_type": "UMLCombinedFragment",
                                "_id": "CF",
                                "_parent": {"$ref": "I"},
                                "name": "SerialPort_openResult",
                                "interactionOperator": "alt",
                                "operands": [
                                    {
                                        "_type": "UMLInteractionOperand",
                                        "_id": "OP1",
                                        "_parent": {"$ref": "CF"},
                                        "name": "connected",
                                        "guard": "success",
                                    },
                                    {
                                        "_type": "UMLInteractionOperand",
                                        "_id": "OP2",
                                        "_parent": {"$ref": "CF"},
                                        "name": "connectFailed",
                                        "guard": "else",
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
            {
                "_type": "UMLClass",
                "_id": "UICls",
                "_parent": {"$ref": "P"},
                "name": "SMUI",
            },
        ],
    }


class ExportTreeSequenceTest(unittest.TestCase):
    def test_sequence_edges_include_message_name_order_and_fragment(self):
        text = export_tree(_sequence_model())
        diagrams = _section(text, "# Diagrams")
        self.assertNotIn("- ConnectSerialPort [UMLSequenceDiagram]", diagrams)
        self.assertIn("UI [UMLLifeline]  represent=SMUI [UMLClass]", diagrams)
        self.assertIn("SPMNGR_PORT_CONNECT [UMLMessage]  messageSort=asynchSignal", diagrams)
        self.assertIn("UI_REFRESHED_PORTS [UMLMessage]", diagrams)
        connect_at = diagrams.find("SPMNGR_PORT_CONNECT [UMLMessage]")
        refreshed_at = diagrams.find("UI_REFRESHED_PORTS [UMLMessage]")
        self.assertLess(connect_at, refreshed_at)
        self.assertIn("SerialPort_openResult [UMLCombinedFragment]  interactionOperator=alt", diagrams)
        self.assertIn("operand: connected  guard=success", diagrams)
        self.assertIn("operand: connectFailed  guard=else", diagrams)


_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "coverage.mdj"


class ExportTreeCoverageFixtureTest(unittest.TestCase):
    def test_coverage_mdj_lists_structure_behavior_notes_and_shared_views(self):
        root = json.loads(_FIXTURE.read_text(encoding="utf-8"))
        text = export_tree(root)
        explorer, diagrams = _section(text, "# Explorer", "# Diagrams"), _section(text, "# Diagrams")

        self.assertIn("[UMLPackage] Application", explorer)
        self.assertIn("documentation: app layer", explorer)
        self.assertIn("[UMLComponent] UIThread", explorer)
        self.assertIn("<<active>>", explorer)
        self.assertIn("[UMLInterface] IUI", explorer)
        self.assertIn("documentation: ui contract", explorer)
        self.assertIn("[UMLOperation] init", explorer)
        self.assertIn("[UMLParameter] code", explorer)
        self.assertIn("type=int", explorer)
        self.assertIn("direction=return", explorer)
        self.assertIn("[UMLAttribute] kind", explorer)
        self.assertIn("type=string", explorer)
        self.assertRegex(
            explorer,
            r"\[UMLGeneralization\].*source=SerialPort \[UMLClass\].*target=Port \[UMLClass\]",
        )
        self.assertIn("[UMLAssociation] uses", explorer)
        self.assertIn("end1=SerialPort [UMLClass]", explorer)
        self.assertIn("end2=PortId [UMLDataType]", explorer)
        self.assertIn("[UMLMessage] SPMNGR_PORT_CONNECT", explorer)
        self.assertIn("[UMLState] Closed", explorer)
        self.assertIn("[UMLTransition] open", explorer)
        self.assertIn("source=Closed [UMLState]", explorer)
        self.assertIn("[UMLActor] User", explorer)
        self.assertIn("[UMLUseCase] ConnectPort", explorer)
        self.assertIn("[UMLSignal] PortEvent", explorer)
        self.assertIn("[UMLPrimitiveType] Handle", explorer)
        self.assertIn("[UMLEnumeration] PortKind", explorer)
        self.assertIn("[UMLEnumerationLiteral] Usb", explorer)
        self.assertIn("[UMLSubsystem] CoreSystem", explorer)
        self.assertIn("[UMLArtifact] firmware.bin", explorer)
        self.assertIn("[UMLPort] sp", explorer)
        self.assertIn("[UMLReception] onEvent", explorer)
        self.assertIn("[UMLTemplateParameter] T", explorer)
        self.assertIn("[UMLConstraint] MustHaveId", explorer)
        self.assertIn("constrainedElements=SerialPort [UMLClass]", explorer)
        self.assertIn("[Tag] layer", explorer)
        self.assertIn("[UMLInclude]", explorer)
        self.assertIn("[UMLExtend]", explorer)
        self.assertIn("[UMLUseCaseSubject] SerialApp", explorer)
        self.assertIn("[UMLAction] connect", explorer)
        self.assertIn("[UMLControlFlow]", explorer)
        self.assertIn("[UMLNode] Host", explorer)
        self.assertIn("[UMLDeployment]", explorer)
        self.assertIn("[UMLObject] port0", explorer)
        self.assertIn("[UMLSlot] kind", explorer)
        self.assertIn("[UMLLink] owns", explorer)
        self.assertIn("[UMLStereotype] active", explorer)
        self.assertIn("[UMLMetaClass] Component", explorer)
        self.assertIn("[UMLExtension]", explorer)
        self.assertIn("[UMLPseudostate] init", explorer)
        self.assertIn("kind=initial", explorer)
        self.assertIn("[UMLConstraint] Busy", explorer)
        self.assertIn("[UMLStateInvariant] t0", explorer)
        self.assertIn("[UMLInformationFlow]", explorer)
        self.assertIn("aggregation=shared", explorer)
        self.assertIn("name=port", explorer)

        self.assertEqual(explorer.count("[UMLComponent] UIThread"), 1)
        self.assertGreaterEqual(diagrams.count("UIThread [UMLComponent]"), 2)

        arch = _section(diagrams, "## Architecture")
        self.assertIn("## Architecture [UMLPackageDiagram]  owner=StructuralArchitecture [UMLModel]", arch)
        self.assertIn("contains: UIThread [UMLComponent]", arch)
        self.assertIn("IUI [UMLInterface]", arch)
        self.assertIn("note  linked=UIThread [UMLComponent]", arch)
        self.assertIn("text=Cmp provides IFace", arch)
        self.assertIn("tail=UIThread [UMLComponent]  head=IUI [UMLInterface]", arch)

        types = _section(diagrams, "## Types")
        self.assertIn("SerialPort [UMLClass]", types)
        self.assertIn("Port [UMLClass]", types)
        self.assertIn("PortId [UMLDataType]", types)
        self.assertIn("uses [UMLAssociation]", types)
        self.assertIn("PortEvent [UMLSignal]", types)
        self.assertIn("text  text=toolbox sweep", types)
        self.assertNotIn("Context [UMLFrame]", types)

        seq = _section(diagrams, "## ConnectSerialPort")
        self.assertIn("SPMNGR_PORT_CONNECT [UMLMessage]", seq)
        self.assertIn("UI_REFRESHED_PORTS [UMLMessage]", seq)
        self.assertLess(seq.find("SPMNGR_PORT_CONNECT"), seq.find("UI_REFRESHED_PORTS"))
        self.assertIn("SerialPort_openResult [UMLCombinedFragment]", seq)
        self.assertIn("operand: connected  guard=success", seq)
        self.assertIn("represent=UIThread [UMLComponent]", seq)

        states = _section(diagrams, "## PortLife")
        self.assertIn("Closed [UMLState]", states)
        self.assertIn("Open [UMLState]", states)
        self.assertIn("open [UMLTransition]", states)
        self.assertIn("tail=Closed [UMLState]  head=Open [UMLState]", states)

        self.assertIn("## Deploy [UMLDeploymentDiagram]", diagrams)
        self.assertIn("firmware.bin [UMLArtifact]", diagrams)
        self.assertIn("## OpenPort [UMLActivityDiagram]", diagrams)
        self.assertIn("connect [UMLAction]", diagrams)
        self.assertIn("## UseCases [UMLUseCaseDiagram]", diagrams)
        self.assertIn("SerialApp [UMLUseCaseSubject]", diagrams)
        self.assertIn("## Profile [UMLProfileDiagram]", diagrams)
        self.assertIn("active [UMLStereotype]", diagrams)
        self.assertIn("## Objects [UMLObjectDiagram]", diagrams)
        self.assertIn("## Clock [UMLTimingDiagram]", diagrams)
        self.assertIn("Busy [UMLConstraint]", diagrams)
        self.assertIn("t0 [UMLStateInvariant]", diagrams)
        self.assertIn("t=5 [UMLTimeTickView]", diagrams)
        self.assertIn("[UMLRealization]", explorer)
        self.assertIn("[UMLAssociationClassLink]", explorer)
        self.assertIn("[UMLForkNode] fork", explorer)
        self.assertIn("[UMLInputPin] in", explorer)
        self.assertIn("[UMLTemplateParameterSubstitution]", explorer)


class ExportTreeReviewFixesTest(unittest.TestCase):
    def test_stereotype_ref_tag_kinds_and_association_end_name(self):
        text = export_tree(
            {
                "_type": "Project",
                "_id": "P",
                "name": "Demo",
                "ownedElements": [
                    {
                        "_type": "UMLStereotype",
                        "_id": "St",
                        "name": "active",
                    },
                    {
                        "_type": "UMLClass",
                        "_id": "C",
                        "name": "Box",
                        "stereotype": {"$ref": "St"},
                        "tags": [
                            {
                                "_type": "Tag",
                                "_id": "T1",
                                "name": "count",
                                "kind": "number",
                                "number": 3,
                            },
                            {
                                "_type": "Tag",
                                "_id": "T2",
                                "name": "owner",
                                "kind": "reference",
                                "reference": {"$ref": "C"},
                            },
                            {
                                "_type": "Tag",
                                "_id": "T3",
                                "name": "on",
                                "kind": "boolean",
                                "checked": False,
                            },
                        ],
                    },
                    {
                        "_type": "UMLClass",
                        "_id": "D",
                        "name": "Peer",
                    },
                    {
                        "_type": "UMLAssociation",
                        "_id": "A",
                        "name": "link",
                        "end1": {
                            "_type": "UMLAssociationEnd",
                            "_id": "E1",
                            "name": "port",
                            "aggregation": "shared",
                            "reference": {"$ref": "C"},
                            "qualifiers": [
                                {
                                    "_type": "UMLAttribute",
                                    "_id": "Q",
                                    "name": "id",
                                }
                            ],
                        },
                        "end2": {
                            "_type": "UMLAssociationEnd",
                            "_id": "E2",
                            "reference": {"$ref": "D"},
                        },
                    },
                ],
            }
        )
        explorer = _section(text, "# Explorer", "# Diagrams")
        self.assertIn("[UMLClass] Box  <<active>>", explorer)
        self.assertIn("[Tag] count  kind=number  number=3", explorer)
        self.assertIn("[Tag] owner  kind=reference  reference=Box [UMLClass]", explorer)
        self.assertIn("[Tag] on  kind=boolean  checked=false", explorer)
        self.assertIn(
            "[UMLAssociation] link  end1=Box [UMLClass]  name=port  aggregation=shared  qualifiers=id [UMLAttribute]  end2=Peer [UMLClass]",
            explorer,
        )

    def test_model_less_timing_tick_and_inline_interaction_are_listed(self):
        text = export_tree(
            {
                "_type": "Project",
                "_id": "P",
                "name": "Demo",
                "ownedElements": [
                    {
                        "_type": "UMLTimingDiagram",
                        "_id": "TD",
                        "name": "Clock",
                        "ownedViews": [
                            {
                                "_type": "UMLTimingFrameView",
                                "_id": "FV",
                                "model": {"$ref": "TD"},
                            },
                            {
                                "_type": "UMLTimeTickView",
                                "_id": "TV",
                                "subViews": [
                                    {
                                        "_type": "LabelView",
                                        "text": "t=5",
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "_type": "UMLSequenceDiagram",
                        "_id": "SD",
                        "name": "Inner",
                    },
                    {
                        "_type": "UMLInteractionOverviewDiagram",
                        "_id": "IOD",
                        "name": "Overview",
                        "ownedViews": [
                            {
                                "_type": "UMLInteractionInlineView",
                                "_id": "IV",
                                "model": {"$ref": "SD"},
                            }
                        ],
                    },
                ],
            }
        )
        diagrams = _section(text, "# Diagrams")
        clock = _section(diagrams, "## Clock")
        overview = _section(diagrams, "## Overview")
        self.assertIn("t=5 [UMLTimeTickView]", clock)
        self.assertNotIn("- Clock [UMLTimingDiagram]", clock)
        self.assertIn("Inner [UMLSequenceDiagram]", overview)

    def test_template_substitution_is_not_emitted_as_relation_endpoints(self):
        text = export_tree(
            {
                "_type": "Project",
                "_id": "P",
                "name": "Demo",
                "ownedElements": [
                    {
                        "_type": "UMLTemplateParameterSubstitution",
                        "_id": "S",
                        "name": "bindT",
                        "formal": {"$ref": "TP"},
                        "actual": {"$ref": "C"},
                    },
                    {
                        "_type": "UMLTemplateParameter",
                        "_id": "TP",
                        "name": "T",
                    },
                    {
                        "_type": "UMLClass",
                        "_id": "C",
                        "name": "Int",
                    },
                ],
            }
        )
        explorer = _section(text, "# Explorer", "# Diagrams")
        self.assertIn("[UMLTemplateParameterSubstitution] bindT  formal=T [UMLTemplateParameter]  actual=Int [UMLClass]", explorer)
        self.assertNotIn("source=", explorer.split("[UMLTemplateParameterSubstitution]", 1)[-1].split("\n", 1)[0])


if __name__ == "__main__":
    unittest.main()
