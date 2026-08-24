# C4-PlantUML

Covered: C4Context, C4Container, C4Component, C4Dynamic, C4Deployment

## Routing

- **Context** — one system plus external people/systems.
- **Container** — web apps, APIs, databases, queues, workers, mobile apps.
- **Component** — elements inside one container.
- **Dynamic** — ordered collaboration across C4 elements.
- **Deployment** — nodes, infrastructure, container instances, environments.

## Include

- Requires `!include` from stdlib or URL. If blocked, provide core fallback.

## Cross-routing

Fallback: core **Component** (`package`/`rectangle` boundaries), **Sequence** (dynamic), **Deployment**.
