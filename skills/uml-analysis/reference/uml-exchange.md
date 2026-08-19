# UML Exchange

How human and agent exchange UML. Analysis workflow, visibility test, and required output stay in `SKILL.md`. PlantUML from `emit` is a communication draft only. The authoritative model remains the user's StarUML `.mdj` after they update it; the next `receive` must re-run the script.

Accepted inputs: StarUML `.mdj`, and PNG (file, chat attachment, or screenshot) when no `.mdj` is given. Reject `.svg`, `.pdf`, `.jpeg`, `.mfj`, XMI, and other model dumps unless the user also gives a `.mdj` or PNG.

Mechanical work is in `scripts/export_model_tree.py`. The agent runs it with this environment's `python` and then reads the text it produces. Do not export diagrams to PNG.

## Route

Match in this order. A mixed request runs more than one step, in this sequence.

| Priority | User artifact / ask | Do |
|---|---|---|
| 1 | `.mdj` present, even if a PNG is also attached | `receive` — run `export_model_tree.py`. Ignore a sibling PNG unless the user says to use that PNG instead of the `.mdj`. |
| 2 | PNG / screenshot / chat image, no `.mdj` | `receive-image` — diagram facts only. Tree unknown. Ask for the `.mdj` if analysis needs membership. |
| 3 | Also asks to redraw, modify, or 画出 after 1 or 2 | After `receive` or `receive-image`, if they also want architecture decisions, follow `SKILL.md`. Then `emit`. |
| 4 | Draw a new diagram, no StarUML file | `emit` only. Do not fill the analysis Required output. |
| 5 | Show / 看看 / explain an existing StarUML model, no file | Ask for the `.mdj`. |

`show` of an existing model is `receive`, not `emit`. Syntax for an `emit` diagram follows `plantuml-master`.

## Scripts

`<skill-dir>` is the folder that contains `SKILL.md`.

| Script | Purpose |
|---|---|
| `scripts/export_model_tree.py` | Two levels from the `.mdj`: `# Explorer` (membership, model relations, Documentation) and `# Diagrams` (mounted elements, drawn edges with names, Notes). Sequence messages keep top-to-bottom order and include message names. |

```text
python "<skill-dir>/scripts/export_model_tree.py" --mdj "<mdj>" -o "<out>/model-tree.txt"
```

On a non-zero exit, stop and use `mdj-tree-unreadable`.

Do not reimplement JSON walking. Do not call StarUML to export images.

## Toolbox types in `.mdj`

Source: StarUML [Working with UML Diagrams](https://docs.staruml.io/working-with-uml-diagrams) plus the UML metamodel in `StarUML.exe`. The parser does not whitelist `_type`. A new toolbox item still prints if it has `_type`, child lists, `$ref` endpoints, or scalar fields. Kind variants share one `_type` and differ by a field.

View-only toolbox items have no explorer node: Containment, Note, Text, Note Link, Frame, Time Tick.

| Toolbox (docs) | `.mdj` `_type` | Distinguishing field |
|---|---|---|
| Package / Model / Subsystem | `UMLPackage` / `UMLModel` / `UMLSubsystem` | |
| Class / Interface / Signal / DataType / PrimitiveType / Enumeration | `UMLClass` / `UMLInterface` / `UMLSignal` / `UMLDataType` / `UMLPrimitiveType` / `UMLEnumeration` | literals on Enumeration |
| Attribute / Operation / Parameter / Reception / Template Parameter | `UMLAttribute` / `UMLOperation` / `UMLParameter` / `UMLReception` / `UMLTemplateParameter` | `type`, `direction` |
| Association / Aggregation / Composition / Directed Association | `UMLAssociation` | `end*.aggregation` = `shared` / `composite`; end `name`; `qualifiers` |
| Generalization / Interface Realization / Dependency / Realization | `UMLGeneralization` / `UMLInterfaceRealization` / `UMLDependency` / `UMLRealization` | `source` / `target` |
| Association Class / Template Binding | `UMLClass` + `UMLAssociation` + `UMLAssociationClassLink` / `UMLTemplateBinding` | link `classSide` / `associationSide`; substitutions are `UMLTemplateParameterSubstitution` |
| Constraint / Tag / Frame | `UMLConstraint` / `Tag` / view-only `UMLFrameView` | `specification`; Tag `kind` plus `value` / `number` / `reference` / `checked`; Frame `model` is the diagram |
| Port / Part / Connector / Collaboration Use / Role Binding | `UMLPort` / `UMLAttribute` / `UMLConnector` / `UMLCollaborationUse` / `UMLRoleBinding` | Part is an Attribute with a Part view |
| Object / Slot / Link / Artifact-Component-Node Instance | `UMLObject` / `UMLSlot` / `UMLLink` / `UMLArtifactInstance` / `UMLComponentInstance` / `UMLNodeInstance` | Object `classifier` |
| Component / Artifact / Component Realization | `UMLComponent` / `UMLArtifact` / `UMLComponentRealization` | |
| Node / Deployment / Communication Path | `UMLNode` / `UMLDeployment` / `UMLCommunicationPath` | |
| Actor / Use Case / Use Case Subject / Include / Extend / Extension Point | `UMLActor` / `UMLUseCase` / `UMLUseCaseSubject` / `UMLInclude` / `UMLExtend` / `UMLExtensionPoint` | |
| Lifeline / Message / Combined Fragment / Operand | `UMLLifeline` / `UMLMessage` / `UMLCombinedFragment` / `UMLInteractionOperand` | `represent`; `messageSort`; `interactionOperator`; `guard` |
| Endpoint / Gate / State Invariant / Continuation / Interaction Use | `UMLEndpoint` / `UMLGate` / `UMLStateInvariant` / `UMLContinuation` / `UMLInteractionUse` | |
| Simple/Composite/Submachine/Orthogonal State | `UMLState` | submachine / regions |
| Initial/Choice/Join/Fork/Junction/History/Entry/Exit/Terminate | `UMLPseudostate` | `kind` |
| Final State / Transition / Region / Connection Point Reference | `UMLFinalState` / `UMLTransition` / `UMLRegion` / `UMLConnectionPointReference` | |
| Action / Send Signal / Accept Signal / Accept Time Event | `UMLAction` | `kind` = `opaque` / `sendSignal` / `acceptSignal` / `timeEvent` |
| Initial / Activity Final / Flow Final / Fork / Join / Merge / Decision | `UMLInitialNode` / `UMLActivityFinalNode` / `UMLFlowFinalNode` / `UMLForkNode` / `UMLJoinNode` / `UMLMergeNode` / `UMLDecisionNode` | |
| Control Flow / Object Flow / Exception Handler / Activity Interrupt | `UMLControlFlow` / `UMLObjectFlow` / `UMLExceptionHandler` / `UMLActivityInterrupt` | |
| Swimlane / Object Node / Pin / Expansion Region | `UMLActivityPartition` / `UMLObjectNode` / `UMLInputPin`/`UMLOutputPin` / `UMLExpansionRegion` | |
| Information Item / Information Flow | `UMLInformationItem` / `UMLInformationFlow` | `conveyed` |
| Profile / MetaClass / Stereotype / Extension | `UMLProfile` / `UMLMetaClass` / `UMLStereotype` / `UMLExtension` | |
| Timing State/Condition / Time Segment / Time/Duration Constraint | `UMLConstraint` + `UMLTimingStateView` / `UMLStateInvariant` + `UMLTimeSegmentView` / `UMLTimeConstraint` / `UMLDurationConstraint` | Time Tick is view-only |

`scripts/fixtures/coverage.mdj` holds one instance of each distinct persisted `_type` family from the toolbox. Kind variants share that `_type` (`UMLPseudostate.kind`, `UMLAction.kind`, `UMLAssociationEnd.aggregation`). Timing State/Condition and Time Segment reuse `UMLConstraint` / `UMLStateInvariant`; they are not separate model classes.

## `receive`

1. Run `export_model_tree.py`. Read two levels only: `# Explorer` is Model Explorer membership, owned relations, and element Documentation; `# Diagrams` is each diagram's mounted elements, drawn edges, visual `contains:`, and Notes (including Note Link targets). Sequence-diagram edges include the message name and are ordered top-to-bottom. Combined fragments list operator and operand guards. The same element may appear under more than one `##` diagram.
2. If Explorer names an element no diagram shows, keep it as explorer-only.

## `receive-image`

Read the given PNG / attachment / screenshot. Tree and relation list stay unknown. Do not invent parents from picture grouping. If analysis needs membership, ask for the `.mdj`.

## `emit`

1. Lock one communicative question. One diagram answers that question only.
2. Draw from `# Explorer` and `# Diagrams` when `receive` ran. Nest `package` / subsystem to match the explorer tree. Do not dump the whole tree into one diagram.
3. Route syntax through `plantuml-master`.
4. Output PlantUML in a `plantuml` fence, wrapped by `@startuml` / `@enduml`.
5. Add 2–5 sentences on what to look at, and that PlantUML does not replace the `.mdj`.
6. A new question gets a new diagram.

`emit` does not permit implementation. The human updates StarUML; the next `receive` re-runs the script.

## Failure classes

| Class | Typical source |
|---|---|
| `mdj-tree-unreadable` | `export_model_tree.py` exit 7 |
| `unsupported-artifact` | input is not `.mdj` or PNG |

## Guardrails

- Run `export_model_tree.py`. Do not hand-parse `.mdj`.
- Do not export diagrams to PNG.
- Explorer membership, model relations, and Documentation come from `# Explorer`.
- Which elements, edges, and Notes are drawn on which diagram come from `# Diagrams`. The same element may appear under more than one diagram.
- Agent-drawn UML is PlantUML source for a web renderer. It is not the authoritative model.
