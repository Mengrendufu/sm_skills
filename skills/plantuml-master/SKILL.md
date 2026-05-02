---
name: plantuml-master
description: Route PlantUML work to the correct diagram family, reference file, and rendering-safe syntax. Use when drafting, repairing, converting, or reviewing PlantUML diagrams.
---

# PlantUML Master

## Workflow

1. Read `references/syntax-routing.md` — match intent to diagram family.
2. Read only the routed reference file — skim when-to-use / when-not-to-use, skip syntax tutorials.
3. When syntax is uncertain, check `references/official-docs.md` for the exact PlantUML page.
4. Output inside `@startuml` / `@enduml`.

## References

- `references/syntax-routing.md` — routing table + intent shortcuts
- `references/sequence-and-time.md` — Sequence, Timing, Gantt
- `references/behavior-and-flow.md` — Activity, State, Use Case
- `references/structure-and-architecture.md` — Class, Object, Component, Deployment, Package
- `references/data-and-specialized.md` — ER, JSON/YAML, MindMap, WBS, ArchiMate, Salt, Ditaa, Regex
- `references/c4-plantuml.md` — C4-PlantUML
- `references/official-docs.md` — PlantUML URL index
