# Sequence and Time

Covered: Sequence, Timing, Gantt

## Routing

- **Sequence** — actor-to-actor interaction, API calls, protocols, event chains.
- **Timing** — lifeline value/state changes over time. Prefer over sequence for signal/protocol traces.
- **Gantt** — dated schedules, roadmaps, task dependencies. Don't invent dates; ask.

## Cross-routing

Favor **Activity** when the main point is branching process ownership.
Favor **State** when the main point is valid lifecycle states.
Favor **Component / Deployment / C4** when the main point is topology.
