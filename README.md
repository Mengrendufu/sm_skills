# sm_skills

个人、可迁移、工具无关的 Agent Skills 集合。按主要任务与交付分类，目录结构为 `<category>/<skill-name>/SKILL.md`。

## `design` — 设计与决策

澄清方案、划分边界、确定接口。

| Skill | 简述 |
|---|---|
| `grill-me` | 逐分支盘问并压力测试方案 |
| `zoom-out` | 以顶层包/模块视野拆解系统交互边界 |
| `uml-composing` | 与用户结对搭建 UML 架构 |
| `implement-interface` | 约束接口的颗粒度和语义范围 |

## `modeling` — 模型理解与提取

将已有模型或代码转成可分析、可复用的语义。

| Skill | 简述 |
|---|---|
| `uml-sync` | 将 StarUML .mdj 同步为 Agent 可读文本 |
| `qm-model-understand` | 从 QM 生成的 C 理解状态机模型拓扑 |

## `implementation` — 实现与契约检查

把语义落实到运行时代码，识别并检查违约。

| Skill | 简述 |
|---|---|
| `qm-c-hsm-implementor` | 将 QM C HSM 语义实现到其他运行时 |
| `design-by-contract` | 识别会结构性坍塌的契约违约，并在运行时拦住 |

## `visualization` — 图形表达

将概念、关系、流程或数据呈现为 HTML 视觉解释。

| Skill | 简述 |
|---|---|
| `show-me` | 以 HTML 呈现视觉解释，按需使用 Mermaid、PlantUML 或其他绘图工具 |

## `context` — 知识与上下文管理

操作笔记、迁移工作上下文。

| Skill | 简述 |
|---|---|
| `obsidian-master` | 通过本地 CLI 操作 Obsidian vault |
| `handoff` | 跨会话迁移关键上下文 |
