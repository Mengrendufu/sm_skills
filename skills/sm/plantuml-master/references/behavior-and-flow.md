# Behavior and Flow

Covered: Activity, State, Use Case

## Routing

- **Activity** — workflows, branching, loops, approvals, pipelines, swimlanes. If user says "flowchart", use activity.
- **State** — lifecycle, state machines, HSMs, allowed transitions. Use composite states only for real hierarchy.
- **Use Case** — actors and goals, not implementation flow. Keep each case as a user-visible goal.

## Cross-routing

Favor **Sequence** when the main point is actor-to-actor message order.
Favor **Class** when the main point is type/domain model.
Favor **Component / Deployment** when the main point is system topology.
