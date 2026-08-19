# UML Exchange

How human and agent exchange UML. Analysis workflow, visibility test, and required output stay in `SKILL.md`. PlantUML from `emit` is a communication draft only. The authoritative model remains the user's StarUML `.mdj` after they update it; the next `receive` must re-export.

Accepted inputs: StarUML `.mdj`, and PNG (file, chat attachment, or screenshot). Reject `.svg`, `.pdf`, `.jpeg`, `.mfj`, XMI, and other model dumps unless the user also gives a PNG. Do not invent a Graphviz or PlantUML renderer for `receive`.

## Route

Match in this order. A mixed request runs more than one step, in this sequence.

| Priority | User artifact / ask | Do |
|---|---|---|
| 1 | `.mdj` present, even if a PNG is also attached | `receive` — export that `.mdj`, then read the new PNGs. Ignore a sibling PNG unless the user says to use the PNG instead of exporting. |
| 2 | PNG / screenshot / chat image, no `.mdj` | `receive-image` — read that image. Do not search for a `.mdj`. |
| 3 | Also asks to redraw, modify, or 画出 after 1 or 2 | After `receive` or `receive-image`, if they also want architecture decisions, follow `SKILL.md`. Then `emit`. |
| 4 | Draw a new diagram, no StarUML file | `emit` only. Do not fill the analysis Required output. |
| 5 | Show / 看看 / explain an existing StarUML model, no file | Ask for the `.mdj` or a PNG. Do not `emit` as a substitute. |

`show` of an existing model is `receive`, not `emit`. Syntax for an `emit` diagram follows `plantuml-master`. Completeness and construction boundary stay in `SKILL.md`.

## Agent host

First identify where this agent is running: **Windows** or **WSL**. Use the current shell to decide (PowerShell/cmd → Windows; bash/zsh on WSL → WSL). Then run **only that environment's** commands for lookup, path conversion, export, and `Read`.

Do not mix environments. Do not keep a second cookbook "just in case". If you cannot tell, stop and ask.

The renderer is always Windows desktop `StarUML.exe`. The environment only decides how this agent talks to it.

## Path triad

Keep three paths for every export, and verify they name the same files.

| Name | Who uses it | Form |
|---|---|---|
| `mdj_win32` | `StarUML.exe` | Drive letter or WSL UNC, never a raw `/home/...` |
| `out_win32` | `StarUML.exe` | A **new empty** directory created for this run |
| `png_agent` | Agent image reader | Path **this** agent can `Read` |

Create `out_win32` yourself. Do not export into the `.mdj` folder or reuse a previous export directory.

After the host is known, convert with that environment's own tools: Windows keeps `C:\...` or calls `wsl.exe wslpath`; WSL uses `wslpath` / `win-wsl-path-converter`. Do not hardcode an install path or distro name.

## `receive` — `.mdj` to PNG to image

Do not open the `.mdj` as text or JSON. Understanding comes only from the exported images.

1. Identify the agent host, then record the `.mdj` and build `mdj_win32` with that host's commands.
2. Resolve Windows `StarUML.exe` with the same host's commands. Search the Windows desktop even from WSL. Do not accept a Linux `staruml` package.

   Order, stop at the first **verified** `StarUML.exe` on a Windows volume:

   1. Path already declared by env, project config, or this session.
   2. PATH lookup in this environment.
   3. Typical install locations in this environment's path form (`Program Files\StarUML\StarUML.exe` or `/mnt/c/Program Files/StarUML/StarUML.exe`). Do not recurse the whole drive.

   Record the executable in the form this host will pass to Shell. If none, stop and ask.

3. Create `out_win32`. Invoke the resolved executable in this environment's syntax. PNG only.

```text
<resolved-staruml> image <mdj_win32> -f png -o <out_win32>/<%=filenamify(element.name)%>.png
```

   Quote paths that contain spaces. Single-quote `-o` so the shell does not expand `%` (`<%=filenamify...%>` is StarUML EJS, not a shell variable). If this environment would still expand `%` (cmd), invoke through PowerShell instead. File arguments stay Win32; from WSL only the exe path uses `/mnt/...`.

   Default selector is `@Diagram`. Bound the wait. If the process does not exit, class `timeout-gui`: stop and ask the user to dismiss the dialog or export PNG by hand.

4. After exit, accept the export only when all of these hold:

   - process exited (not hung);
   - exit code success;
   - `out_win32` contains at least one new PNG and nothing left over from a previous run;
   - each PNG is non-empty and readable as an image.

   Map PNGs to diagrams by filename. If names collide, zero files appear, or some diagrams are missing, stop and report. Do not invent cross-diagram relationships that are not visible. If there are too many diagrams to use at once, ask which ones to read.

5. Convert `out_win32` to `png_agent`. Read every accepted PNG as an image. Reconstruct what is visible: packages, subsystems, components, interfaces, arrows, labels. Do not invent missing shapes. Blank, cropped, tiny, or unreadable-label images are export-quality failures, not "the model is silent".
6. Extract only what the image actually shows:

   | Visible in the image | Record as |
   |---|---|
   | Package grouping | `Package` |
   | Grouping or component marked `«subsystem»` | `Subsystem` |
   | Component box / component icon | `Component` |
   | Lollipop or circle labeled as an interface | `Interface` |
   | Dashed or dependency arrow | `Dependency` |
   | Realization / provided-required connection to an interface | `InterfaceRealization` |

7. Record those visually confirmed elements as **Verified** model facts. Code and traces may corroborate or contradict; they do not silently override the image. If the image is silent on an element, leave it unknown. Do not fill gaps from file layout or implementation complexity.

## `receive-image` — PNG already provided

Read the given PNG / attachment / screenshot as an image. Then do steps 6–7 above.

Do not treat it as fresh if a `.mdj` is also present — that case is `receive`, not this branch.

## `emit` — diagram the user asked the agent to draw

1. Lock one communicative question. One diagram answers that question only.
2. Draw from Verified visual facts when `receive` or `receive-image` already ran. Do not parse `.mdj` to fill the drawing.
3. Choose the family that matches the question (structure → Component/Package; interaction → Sequence; lifecycle → State; process → Activity). Route syntax through `plantuml-master`.
4. Include only elements and relationships needed to answer the question. Private internals stay omitted unless they are the question.
5. Output PlantUML source in a `plantuml` fence, wrapped by `@startuml` / `@enduml`. Do not substitute Mermaid, ASCII-only sketches, image attachments, or a prose-only description.
6. Add 2–5 sentences on what to look at, what not to infer, and that this PlantUML does not replace the StarUML `.mdj`.
7. If the user asks a different question, emit a new diagram. Do not pile extra concerns onto the previous one.

After `emit`, construction still requires **Complete carrying** in `SKILL.md`. The human updates StarUML; the next `receive` re-exports.

## Failure classes

If export or read fails, stop. Name one class. Do not fall back to reading the `.mdj`. Do not debug Graphviz or PlantUML.

| Class | Meaning |
|---|---|
| `exe-not-found` | No verified Windows `StarUML.exe` |
| `path-conversion` | Could not build `mdj_win32`, `out_win32`, or `png_agent` |
| `timeout-gui` | Process hung; likely license, first-run, or other desktop dialog |
| `cli-or-permission` | Non-zero exit, cannot write `out_win32`, or bad arguments |
| `empty-or-unreadable-png` | No PNG, collision, blank, cropped, or labels unreadable |
| `unsupported-artifact` | Input is not `.mdj` or PNG |

## Guardrails

- A user `.mdj` is understood from its freshly exported PNG, never from reading the model file.
- Identify the agent environment first, then run only that environment's commands.
- Agent-drawn UML is PlantUML source for a web renderer. It is not the authoritative model.
- `emit` does not by itself permit implementation.
