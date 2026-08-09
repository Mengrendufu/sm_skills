---
name: uml-analysis
description: Maps software requirements to capability-centred UML architecture decisions, ownership, cross-boundary contracts, and code construction boundaries. Use when locating required capabilities in Package, Subsystem, Component, or Interface models; deciding reuse, semantic refactoring, or minimal UML additions; or determining whether implementation may begin.
---

# UML Analysis

## Goal

Map a requirement to the existing UML architecture, close only genuine capability gaps, and establish the code construction boundary before implementation.

## Analysis input

Apply this skill to a specific project's UML architecture. Read the project-declared authoritative UML model, modeling rules, and any Agent-readable projection or export needed to inspect it. Use code, runtime traces, and existing contracts as evidence of the current implementation, not as automatic proof that the current architecture is correct. The project model supplies the concrete elements, layer semantics, and relationships; this skill supplies the analysis method and decision loop. If the model, project rules, and implementation disagree, stop and report the inconsistency instead of inventing architecture facts.

## Workflow

1. State the requirement goal, scope, expected result, explicit non-goals, and assumptions without choosing UML elements or code locations.
2. Extract required capabilities in domain language. Ask what must be received, produced, owned, stored, controlled, coordinated, provided, or obtained externally.
3. Collect fresh evidence for each capability from the authoritative model, project rules, existing contracts, code, and runtime behavior. Separate verified facts, assumptions, and implementation accidents.
4. Map every capability to the existing architecture:
   - `Package`: capability domain;
   - `Subsystem` or `Component`: capability owner, organizer, or carrier;
   - `Interface`: stable cross-boundary capability semantics;
   - `Dependency`: capability consumer;
   - `InterfaceRealization`: implementation provider.
5. Before adding a UML element, apply the UML visibility test. A capability warrants its own modeled element only when it has at least one of: independent responsibility ownership, independent resource lifetime, a stable cross-boundary contract, or an independent variation axis. Otherwise keep it as private behavior inside the existing carrier.
6. Identify crossed boundaries and make the following explicit:
   - responsibility and authoritative state owner;
   - resource creator, owner, borrower, mutator, transferor, and releaser;
   - copy, borrow, transfer, sharing, and lifetime semantics;
   - boundary data-type ownership and permitted dependency direction;
   - error/status translation responsibility;
   - synchronous, asynchronous, callback, and concurrency semantics;
   - runtime assembly or injection point.
7. Classify the complete capability set as exactly one of:
   - **Complete carrying**: existing elements and relationships express every capability clearly and consistently;
   - **Semantic refactoring required**: existing elements can carry the capabilities after correcting responsibilities, Interface semantics or ownership, relationships, injection direction, or resource allocation;
   - **Capability gap**: at least one capability cannot be carried through reasonable reuse or semantic refactoring.
8. For semantic refactoring, change existing semantics and relationships without adding elements, then repeat the complete mapping and classification.
9. For a capability gap, add only the smallest missing element or relationship that passes the UML visibility test, then repeat the complete mapping and classification:
   - missing domain -> `Package`;
   - missing composite capability organizer -> `Subsystem`;
   - missing single-responsibility carrier -> `Component`;
   - missing boundary capability semantics -> `Interface`;
   - missing consumer or provider relationship -> `Dependency` or `InterfaceRealization`.
10. Re-run the complete mapping after planned architecture changes. Permit implementation only when the final classification is **Complete carrying** and no ownership, dependency, contract, or assembly decision remains unresolved.
11. Hand the settled boundary to `strict-coding`. Implementation may refine internal algorithms and data structures, but must preserve Interface semantics, dependency direction, responsibility boundaries, cross-boundary data semantics, and resource ownership.
12. After implementation, verify that code and UML still correspond.

## Interface rules

- Treat `Interface` as the smallest stable cross-boundary capability contract.
- Name it so the core capability is clear without reading its operations.
- Use Attributes and Operations only for contract details the name cannot express.
- Exclude algorithms, private state, concrete system APIs, file layout, and other implementation details.
- Name the Interface owner, consumer, implementation provider, and runtime assembly point.
- Prefer provider ownership for a normal provided capability contract.
- Prefer consumer ownership for a required callback, sink, host-ops, or dependency-inversion contract implemented by another Component or Subsystem through runtime injection.
- Define cross-boundary data and status types in the lowest layer that can express their semantics without depending on a higher layer. Do not leak concrete platform types or consumer-owned business types through the Interface.

## Guardrails

- Start from required capabilities, never from files, functions, structs, or implementation complexity.
- Reuse existing elements when their semantics and relationships already fit.
- Prefer semantic refactoring over adding a parallel architecture concept.
- Never add UML elements merely because code is large, split across files, or difficult to implement.
- Do not equate a file, function, type, or platform branch with a UML Component without passing the UML visibility test.
- Use project-declared layer semantics to choose a Package; do not invent generic placement rules that conflict with the project architecture.
- Surface material ambiguity as an explicit decision with alternatives instead of silently selecting a boundary.
- Do not begin implementation while any capability mapping, ownership, dependency, boundary contract, or injection decision remains unresolved.

## Required output

```text
Evidence and assumptions:
- Verified: ...
- Assumed: ...
- Inconsistencies: none / ...

Required capabilities:
- ...

Architecture mapping:
- Capability: ...
  Package: ...
  Subsystem / Component: ...
  Interface: ...
  Interface owner: ...
  Consumer: ...
  Provider: ...
  Responsibility and resource ownership: ...
  Boundary data, error, and execution semantics: ...
  Runtime assembly or injection point: ...

UML visibility decision:
- Existing carrier / Private behavior / New modeled element: ...
- Basis: independent owner / lifetime / boundary / variation axis

Carrying decision:
- Complete carrying / Semantic refactoring required / Capability gap

Architecture changes:
- Reuse: ...
- Refactor: ...
- Add: ...

Code construction boundary:
- ...

Final carrying validation:
- Final classification: Complete carrying / unresolved
- Unresolved decisions: none / ...
- Implementation permitted: yes / no
```
