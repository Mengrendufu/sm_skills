# Syntax Routing

Use this file first. Match intent to the narrowest diagram family, then read only that reference.

## Rules

- If the user names a PlantUML type, route to it directly.
- Prefer semantic diagrams: Sequence for interactions, Activity for process, State for lifecycle, Class for type model.
- Prefer core PlantUML. Use C4 / ArchiMate / Salt / WBS / mindmap / timing / JSON / YAML only when asked.
- Unknown renderer → avoid `!include`, avoid beta syntax.

## Family Index

| Syntax | Category | Read |
|---|---|---|
| Sequence | Interaction/Time | `sequence-and-time.md` |
| Timing | Interaction/Time | `sequence-and-time.md` |
| Gantt | Interaction/Time | `sequence-and-time.md` |
| Activity | Behavior/Flow | `behavior-and-flow.md` |
| State | Behavior/Flow | `behavior-and-flow.md` |
| Use Case | Behavior/Flow | `behavior-and-flow.md` |
| Class | Structure/Architecture | `structure-and-architecture.md` |
| Object | Structure/Architecture | `structure-and-architecture.md` |
| Component | Structure/Architecture | `structure-and-architecture.md` |
| Deployment | Structure/Architecture | `structure-and-architecture.md` |
| Package | Structure/Architecture | `structure-and-architecture.md` |
| C4-PlantUML | C4 | `c4-plantuml.md` |
| Entity / Chen ER | Data/Specialized | `data-and-specialized.md` |
| JSON / YAML | Data/Specialized | `data-and-specialized.md` |
| MindMap / WBS | Data/Specialized | `data-and-specialized.md` |
| ArchiMate | Data/Specialized | `data-and-specialized.md` |
| Salt / Wireframe | Data/Specialized | `data-and-specialized.md` |
| Ditaa / Regex | Data/Specialized | `data-and-specialized.md` |

## Intent Shortcuts

- "时序 / 调用链 / 请求响应" → Sequence
- "流程 / branch / pipeline / 审批" → Activity
- "状态机 / lifecycle / HSM" → State
- "类 / interface / 继承 / 类型关系" → Class
- "组件 / 模块 / 依赖" → Component or C4-PlantUML
- "部署 / 节点 / pod / host" → Deployment or C4-PlantUML
- "用例 / actor / 用户目标" → Use Case
- "ER / schema / 实体关系" → Entity
- "甘特 / roadmap / 计划" → Gantt
- "脑图 / WBS / 层级" → MindMap or WBS
- "UI / wireframe / 表单" → Salt

## Fallback

- External `!include` may not work → core Component, Deployment, Activity, or Sequence.
- Process modeled as components → Activity.
- Architecture mostly messages → Sequence or C4 Dynamic.
