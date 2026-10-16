#!/usr/bin/env python3
"""Export StarUML explorer membership and per-diagram contents from an .mdj file.

Element types follow StarUML's UML toolbox (docs.staruml.io working-with-uml-diagrams)
and the UML* classes inside StarUML.exe. The exporter is generic over `_type`:
it does not whitelist model kinds. Views are chrome unless they carry a model,
an edge, or a Note.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SKIP_CHILD_KEYS = {
    "ownedViews",
    "ownedLayers",
    "subViews",
    "containedViews",
    "editorState",
    "style",
    "operationSignatureStyle",
}

SKIP_REF_KEYS = {"_parent", "model"}

SKIP_EXTRA_KEYS = SKIP_CHILD_KEYS | SKIP_REF_KEYS | {
    "_type",
    "_id",
    "name",
    "documentation",
    "stereotype",
    "operands",
    "head",
    "tail",
    "source",
    "target",
    "end1",
    "end2",
    "client",
    "supplier",
    "reference",
    "points",
    "font",
    "fillColor",
    "lineColor",
    "fontColor",
    "parentStyle",
    "left",
    "top",
    "width",
    "height",
}

SKIP_SCALAR_VALUES = {"", "public", "none"}

RELATION_HINTS = (
    "Dependency",
    "Realization",
    "Generalization",
    "Association",
    "Usage",
    "Abstraction",
    "Import",
    "Merge",
    "Connector",
    "InformationFlow",
    "Manifestation",
    "Deployment",
    "Extend",
    "Include",
    "Transition",
    "ControlFlow",
    "ObjectFlow",
    "Message",
    "Link",
    "Anchor",
    "Trace",
    "Permission",
    "PackageImport",
    "PackageMerge",
    "ElementImport",
    "InterfaceRealization",
    "ComponentRealization",
    "ExceptionHandler",
    "ActivityInterrupt",
    "CommunicationPath",
    "TemplateBinding",
    "Extension",
    "RoleBinding",
)

CHROME_VIEW_EXACT = {"LabelView", "EdgeLabelView"}
CHROME_VIEW_SUFFIXES = (
    "CompartmentView",
    "ActivationView",
    "LinePartView",
)
TEXT_VIEWS = {"UMLTextView", "UMLTextBoxView"}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mdj", required=True, help="Path to the StarUML .mdj file")
    parser.add_argument("-o", "--out", default="", help="Write the text tree to this file")
    return parser.parse_args()


def _walk_dicts(node: Any):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _walk_dicts(value)
    elif isinstance(node, list):
        for item in node:
            yield from _walk_dicts(item)


def _index_by_id(root: dict) -> dict[str, dict]:
    indexed: dict[str, dict] = {}
    for node in _walk_dicts(root):
        node_id = node.get("_id")
        if isinstance(node_id, str):
            indexed[node_id] = node
    return indexed


def _deref(value: Any, indexed: dict[str, dict]) -> dict | None:
    if isinstance(value, dict) and "$ref" in value:
        return indexed.get(str(value["$ref"]))
    if isinstance(value, dict) and value.get("_type"):
        return value
    return None


def _label(node: dict | None) -> str:
    if not node:
        return "(unresolved)"
    name = node.get("name")
    type_name = node.get("_type") or "Element"
    if isinstance(name, str) and name.strip():
        return f"{name} [{type_name}]"
    return f"(unnamed) [{type_name}]"


def _is_view(node: dict) -> bool:
    return "View" in str(node.get("_type") or "")


ENDPOINT_PAIRS = (
    ("source", "target"),
    ("end1", "end2"),
    ("client", "supplier"),
    ("classSide", "associationSide"),
)


def _is_relation(node: dict) -> bool:
    type_name = str(node.get("_type") or "")
    if _is_view(node) or type_name.endswith("Diagram"):
        return False
    if any(type_name == hint or type_name.endswith(hint) for hint in RELATION_HINTS):
        return True
    return any(left in node and right in node for left, right in ENDPOINT_PAIRS)


def _endpoints(node: dict, indexed: dict[str, dict]) -> list[tuple[str, dict | None]]:
    found: list[tuple[str, dict | None]] = []
    seen: set[tuple[str, str]] = set()
    for key, value in node.items():
        if key in SKIP_REF_KEYS or key.startswith("_"):
            continue
        resolved = _deref(value, indexed)
        if resolved is None:
            continue
        nested = _deref(resolved.get("reference"), indexed)
        target = nested or resolved
        ident = str(target.get("_id") or id(target))
        if (key, ident) in seen:
            continue
        seen.add((key, ident))
        found.append((key, target))
    return found


def _end_bits(end: dict, indexed: dict[str, dict]) -> str:
    bits: list[str] = []
    name = end.get("name")
    if isinstance(name, str) and name.strip():
        bits.append(f"name={name.strip()}")
    extras = _field_extras(end, indexed).strip()
    if extras:
        bits.append(extras)
    labels: list[str] = []
    for item in end.get("qualifiers") or []:
        if isinstance(item, dict) and item.get("_type"):
            labels.append(_label(item))
    if labels:
        bits.append("qualifiers=" + ", ".join(labels))
    if not bits:
        return ""
    return "  " + "  ".join(bits)


def _endpoint_text(node: dict, indexed: dict[str, dict]) -> str:
    parts: list[str] = []
    for field, value in node.items():
        if field in SKIP_REF_KEYS or field.startswith("_"):
            continue
        resolved = _deref(value, indexed)
        if resolved is None:
            continue
        nested = _deref(resolved.get("reference"), indexed)
        target = nested or resolved
        extra = _end_bits(resolved, indexed) if nested else ""
        parts.append(f"{field}={_label(target)}{extra}")
    return "  ".join(parts)


def _field_extras(node: dict, indexed: dict[str, dict]) -> str:
    parts: list[str] = []
    skip = set(SKIP_EXTRA_KEYS)
    if str(node.get("_type") or "") == "Tag":
        skip.discard("reference")
    for key, value in node.items():
        if key in skip or key.startswith("_"):
            continue
        if isinstance(value, list):
            if value and all(isinstance(item, dict) and "$ref" in item and "_type" not in item for item in value):
                labels = []
                for item in value:
                    resolved = _deref(item, indexed)
                    if resolved and not _is_view(resolved):
                        labels.append(_label(resolved))
                if labels:
                    parts.append(f"{key}={', '.join(labels)}")
            continue
        if isinstance(value, dict):
            resolved = _deref(value, indexed)
            if resolved and not _is_view(resolved):
                parts.append(f"{key}={_label(resolved)}")
            continue
        if isinstance(value, bool):
            if value:
                parts.append(f"{key}=true")
            elif str(node.get("_type") or "") == "Tag" and key == "checked":
                parts.append("checked=false")
            continue
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            parts.append(f"{key}={value}")
            continue
        if isinstance(value, str) and value.strip() and value.strip() not in SKIP_SCALAR_VALUES:
            parts.append(f"{key}={value.strip()}")
    if not parts:
        return ""
    return "  " + "  ".join(parts)


def _child_nodes(node: dict) -> list[dict]:
    children: list[dict] = []
    for key, value in node.items():
        if key in SKIP_CHILD_KEYS or key.startswith("_"):
            continue
        if not isinstance(value, list):
            continue
        for item in value:
            if isinstance(item, dict) and item.get("_type") and not _is_view(item):
                children.append(item)
    return children


def _render_tree(node: dict, indexed: dict[str, dict], indent: int, lines: list[str]) -> None:
    pad = "  " * indent
    type_name = node.get("_type") or "Element"
    name = node.get("name")
    title = name.strip() if isinstance(name, str) and name.strip() else "(unnamed)"
    extra = ""
    if _is_relation(node):
        ends = _endpoint_text(node, indexed)
        if ends:
            extra = "  " + ends
    extra += _stereotype_text(node, indexed)
    extra += _field_extras(node, indexed)
    lines.append(f"{pad}[{type_name}] {title}{extra}")
    doc = node.get("documentation")
    if isinstance(doc, str) and doc.strip():
        for line in doc.strip().splitlines():
            lines.append(f"{pad}  documentation: {line}")
    for child in _child_nodes(node):
        _render_tree(child, indexed, indent + 1, lines)


def _is_note_view(node: dict) -> bool:
    type_name = str(node.get("_type") or "")
    return type_name.endswith("NoteView") and "Link" not in type_name


def _is_text_view(node: dict) -> bool:
    return str(node.get("_type") or "") in TEXT_VIEWS


def _is_note_link(node: dict) -> bool:
    return "NoteLinkView" in str(node.get("_type") or "")


def _view_text(node: dict) -> str:
    text = node.get("text")
    if isinstance(text, str) and text.strip():
        return text.strip()
    for child in node.get("subViews") or []:
        if isinstance(child, dict):
            nested = _view_text(child)
            if nested:
                return nested
    return ""


def _append_unique(bucket: list[dict], item: dict) -> None:
    item_id = item.get("_id")
    if any(existing.get("_id") == item_id for existing in bucket):
        return
    bucket.append(item)


def _note_links(root: dict, indexed: dict[str, dict]) -> dict[str, list[dict]]:
    linked: dict[str, list[dict]] = {}
    for node in _walk_dicts(root):
        if not isinstance(node, dict) or not _is_note_link(node):
            continue
        ends = [_deref(node.get("head"), indexed), _deref(node.get("tail"), indexed)]
        note = next((end for end in ends if end and _is_note_view(end)), None)
        other = next((end for end in ends if end and end is not note), None)
        if not note:
            continue
        note_id = str(note.get("_id") or "")
        linked.setdefault(note_id, [])
        model = _deref(other.get("model"), indexed) if other else None
        if model:
            _append_unique(linked[note_id], model)
    return linked


def _is_diagram(node: dict) -> bool:
    type_name = str(node.get("_type") or "")
    return type_name.endswith("Diagram") and "View" not in type_name


def _is_ignored_diagram_view(view: dict) -> bool:
    type_name = str(view.get("_type") or "")
    if type_name in CHROME_VIEW_EXACT:
        return True
    if any(type_name.endswith(suffix) for suffix in CHROME_VIEW_SUFFIXES):
        return True
    return _is_note_link(view)


def _view_y(view: dict) -> float:
    points = view.get("points")
    if isinstance(points, str):
        ys: list[float] = []
        for part in points.split(";"):
            if ":" not in part:
                continue
            try:
                ys.append(float(part.split(":", 1)[1]))
            except ValueError:
                continue
        if ys:
            return min(ys)
    top = view.get("top")
    if isinstance(top, (int, float)):
        return float(top)
    return 0.0


def _stereotype_text(node: dict, indexed: dict[str, dict]) -> str:
    stereo = node.get("stereotype")
    if isinstance(stereo, str) and stereo.strip():
        return f"  <<{stereo}>>"
    resolved = _deref(stereo, indexed)
    if resolved:
        name = resolved.get("name")
        if isinstance(name, str) and name.strip():
            return f"  <<{name}>>"
    return ""


def _edge_line(view: dict, model: dict | None, head: dict | None, tail: dict | None, indexed: dict[str, dict]) -> str:
    label = _label(model) if model else str(view.get("_type") or "Relation")
    extra = ""
    if model:
        extra += _stereotype_text(model, indexed)
        extra += _field_extras(model, indexed)
    return f"- {label}{extra}  tail={_label(tail)}  head={_label(head)}"


def _element_block(model: dict, indexed: dict[str, dict], contained: list[dict]) -> str:
    line = f"- {_label(model)}{_stereotype_text(model, indexed)}{_field_extras(model, indexed)}"
    if contained:
        line += "\n  contains: " + ", ".join(_label(item) for item in contained)
    for operand in model.get("operands") or []:
        if not isinstance(operand, dict):
            continue
        name = operand.get("name")
        title = name.strip() if isinstance(name, str) and name.strip() else "(unnamed)"
        guard = operand.get("guard")
        guard_text = f"  guard={guard}" if isinstance(guard, str) and guard.strip() else ""
        line += f"\n  operand: {title}{guard_text}"
    return line


def _is_edge_view(view: dict) -> bool:
    if _is_note_link(view):
        return False
    if "head" in view and "tail" in view:
        return True
    return str(view.get("_type") or "").endswith("EdgeView")


def _model_of_view(view: dict | None, indexed: dict[str, dict]) -> dict | None:
    if not view:
        return None
    return _deref(view.get("model"), indexed)


def _view_caption(view: dict) -> str:
    name = view.get("name")
    if isinstance(name, str) and name.strip():
        return name.strip()
    text = _view_text(view)
    if text:
        return text
    for child in view.get("subViews") or []:
        if not isinstance(child, dict):
            continue
        if "Label" not in str(child.get("_type") or ""):
            continue
        label = child.get("text")
        if isinstance(label, str) and label.strip():
            return label.strip()
    return "(unnamed)"


def _is_self_frame(view: dict, diagram: dict, indexed: dict[str, dict]) -> bool:
    type_name = str(view.get("_type") or "")
    if type_name not in {"UMLFrameView", "UMLTimingFrameView"}:
        return False
    model = _model_of_view(view, indexed)
    return model is diagram


def _contained_models(view: dict, indexed: dict[str, dict]) -> list[dict]:
    models: list[dict] = []
    for raw in view.get("containedViews") or []:
        inner = _deref(raw, indexed)
        model = _model_of_view(inner, indexed)
        if model:
            _append_unique(models, model)
    return models


def _collect_diagrams(root: dict, indexed: dict[str, dict]) -> list[str]:
    diagrams: list[dict] = []
    seen: set[str] = set()
    for node in _walk_dicts(root):
        if not isinstance(node, dict) or not _is_diagram(node):
            continue
        diagram_id = str(node.get("_id") or id(node))
        if diagram_id in seen:
            continue
        seen.add(diagram_id)
        diagrams.append(node)
    diagrams.sort(key=_label)
    rows: list[str] = []
    linked = _note_links(root, indexed)
    for diagram in diagrams:
        owner = _deref(diagram.get("_parent"), indexed)
        rows.append(f"## {_label(diagram)}  owner={_label(owner)}")
        element_rows: list[str] = []
        edge_rows: list[tuple[float, str]] = []
        note_rows: list[str] = []
        seen_models: set[str] = set()
        seen_edges: set[str] = set()
        for view in diagram.get("ownedViews") or []:
            if not isinstance(view, dict):
                continue
            if _is_note_view(view):
                note_id = str(view.get("_id") or "")
                targets = linked.get(note_id, [])
                linked_text = (
                    ", ".join(_label(item) for item in targets) if targets else "(unlinked)"
                )
                body = _view_text(view) or "(empty)"
                note_rows.append(f"- note  linked={linked_text}\n  text={body}")
                continue
            if _is_text_view(view):
                body = _view_text(view) or "(empty)"
                note_rows.append(f"- text  text={body}")
                continue
            if _is_ignored_diagram_view(view) or _is_self_frame(view, diagram, indexed):
                continue
            if _is_edge_view(view):
                edge_id = str(view.get("_id") or id(view))
                if edge_id in seen_edges:
                    continue
                seen_edges.add(edge_id)
                model = _model_of_view(view, indexed)
                head = _model_of_view(_deref(view.get("head"), indexed), indexed)
                tail = _model_of_view(_deref(view.get("tail"), indexed), indexed)
                edge_rows.append((_view_y(view), _edge_line(view, model, head, tail, indexed)))
                continue
            model = _model_of_view(view, indexed)
            if not model:
                type_name = str(view.get("_type") or "View")
                element_rows.append(f"- {_view_caption(view)} [{type_name}]")
                continue
            if str(model.get("_type") or "").endswith("Diagram") and str(
                view.get("_type") or ""
            ) in {"UMLFrameView", "UMLTimingFrameView"}:
                continue
            model_id = str(model.get("_id") or id(model))
            if model_id in seen_models:
                continue
            seen_models.add(model_id)
            contained = _contained_models(view, indexed)
            element_rows.append(_element_block(model, indexed, contained))
        element_rows.sort()
        edge_rows.sort(key=lambda item: (item[0], item[1]))
        note_rows.sort()
        if element_rows or edge_rows or note_rows:
            rows.extend(element_rows)
            rows.extend(line for _, line in edge_rows)
            rows.extend(note_rows)
        else:
            rows.append("(empty)")
        rows.append("")
    if rows and rows[-1] == "":
        rows.pop()
    return rows


def export_tree(root: dict) -> str:
    indexed = _index_by_id(root)
    lines = ["# Explorer", ""]
    _render_tree(root, indexed, 0, lines)
    lines.extend(["", "# Diagrams", ""])
    diagrams = _collect_diagrams(root, indexed)
    if diagrams:
        lines.extend(diagrams)
    else:
        lines.append("(none)")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = _parse_args()
    mdj = Path(args.mdj).expanduser()
    if not mdj.is_file():
        print(f"error: mdj not found: {mdj}", file=sys.stderr)
        return 2
    try:
        raw = mdj.read_text(encoding="utf-8")
        root = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: mdj-tree-unreadable: {exc}", file=sys.stderr)
        return 7
    if not isinstance(root, dict) or not root.get("_type"):
        print("error: mdj-tree-unreadable: root is not a StarUML element", file=sys.stderr)
        return 7

    text = export_tree(root)
    if args.out:
        out = Path(args.out).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
