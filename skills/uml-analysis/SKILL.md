---
name: uml-analysis
description: Maps software requirements to capability-centred UML architecture decisions and code construction boundaries. Use when locating required capabilities in Package, Subsystem, Component, or Interface models; deciding reuse, semantic refactoring, or minimal UML additions; or determining whether implementation may begin.
---

# UML Analysis

## Goal

Map a requirement to the existing UML architecture, close only genuine capability gaps, and establish the code construction boundary before implementation.

## Analysis input

Apply this skill to a specific project's UML architecture. Read the project-declared authoritative UML model and any Agent-readable projection or export needed to inspect it. The project model supplies the concrete elements and relationships; this skill supplies the analysis method and decision loop. If model representations disagree, stop and report the inconsistency instead of inventing architecture facts.

## Workflow

1. State the requirement goal, scope, expected result, and explicit non-goals without choosing UML elements or code locations.
2. Extract required capabilities in domain language. Ask what must be received, produced, owned, stored, controlled, coordinated, provided, or obtained externally.
3. Map every capability to the existing architecture:
   - `Package`: capability domain;
   - `Subsystem` or `Component`: capability owner, organizer, or carrier;
   - `Interface`: stable cross-boundary capability semantics;
   - `Dependency`: capability consumer;
   - `InterfaceRealization`: implementation provider.
4. Identify crossed boundaries and make responsibility, state, and resource ownership explicit, including borrowing, transfer, lifetime, mutation, and release.
5. Classify the complete capability set as exactly one of:
   - **Complete carrying**: existing elements and relationships express every capability clearly and consistently;
   - **Semantic refactoring required**: existing elements can carry the capabilities after correcting responsibilities, Interface semantics or ownership, relationships, injection direction, or resource allocation;
   - **Capability gap**: at least one capability cannot be carried through reasonable reuse or semantic refactoring.
6. For semantic refactoring, change existing semantics and relationships without adding elements, then repeat the complete mapping and classification.
7. For a capability gap, add only the smallest missing element or relationship, then repeat the complete mapping and classification:
   - missing domain -> `Package`;
   - missing composite capability organizer -> `Subsystem`;
   - missing single-responsibility carrier -> `Component`;
   - missing boundary capability semantics -> `Interface`;
   - missing consumer or provider relationship -> `Dependency` or `InterfaceRealization`.
8. Permit implementation only after every capability has a domain, carrier, required Interface, consumer, provider, responsibility and resource owner, code construction boundary, and runtime assembly or injection point.
9. Hand the settled boundary to `strict-coding`. Implementation may refine internal algorithms and data structures, but must preserve Interface semantics, dependency direction, responsibility boundaries, and resource ownership.
10. After implementation, verify that code and UML still correspond.

## Interface rules

- Treat `Interface` as the smallest stable cross-boundary capability contract.
- Name it so the core capability is clear without reading its operations.
- Use Attributes and Operations only for contract details the name cannot express.
- Exclude algorithms, private state, concrete system APIs, file layout, and other implementation details.
- Name the Interface owner, consumer, and implementation provider. The consumer may own an Interface implemented by another Component or Subsystem through runtime injection.

## Guardrails

- Start from required capabilities, never from files, functions, structs, or implementation complexity.
- Reuse existing elements when their semantics and relationships already fit.
- Prefer semantic refactoring over adding a parallel architecture concept.
- Never add UML elements merely because code is large, split across files, or difficult to implement.
- Do not begin implementation while any capability mapping, ownership, dependency, or injection decision remains unresolved.

## Required output

```text
Required capabilities:
- ...

Architecture mapping:
- Capability: ...
  Package: ...
  Subsystem / Component: ...
  Interface: ...
  Consumer: ...
  Provider: ...
  Responsibility and resource ownership: ...

Carrying decision:
- Complete carrying / Semantic refactoring required / Capability gap

Architecture changes:
- Reuse: ...
- Refactor: ...
- Add: ...

Code construction boundary:
- ...
```
