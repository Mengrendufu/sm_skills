# sm_skills

个人、可迁移、工具无关的 Agent Skills 集合。

## `skills/sm`

个人维护的 skill。

| Skill | 简述 |
|---|---|
| `design-by-contract` | 识别会结构性坍塌的契约违约，并在运行时拦住 |
| `grill-me` | 逐分支盘问并压力测试方案 |
| `handoff` | 跨会话迁移关键上下文 |
| `implement-interface` | 约束调用方能依赖的接口形态，拦住泄漏 |
| `obsidian-master` | 通过本地 CLI 操作 Obsidian vault |
| `plantuml-master` | 路由并生成可渲染的 PlantUML 图 |
| `qm-c-hsm-implementor` | 将 QM C HSM 语义实现到其他运行时 |
| `qm-c-model-master` | 从 QM 生成的 C 提取 HSM 语义模型 |
| `uml-composing` | 与用户结对搭建 UML 架构（语料：四视角、模式、反模式） |
| `uml-sync` | 将 StarUML .mdj 同步为 Agent 可读文本 |
| `zoom-out` | 从陌生代码局部提升到系统视角 |

## `skills/superpowers`

从 Superpowers 引入的 skill。许可证见 [skills/superpowers/LICENSE.superpowers](skills/superpowers/LICENSE.superpowers)。

| Skill | 简述 |
|---|---|
| `brainstorming` | 在实现前澄清意图、决策缺口与最小设计 |
| `systematic-debugging` | 先定位根因，再用单一假设和回归测试修复 |
| `test-driven-development` | 以 RED-GREEN-REFACTOR 驱动行为变更 |
| `using-git-worktrees` | 安全创建、复用并验证隔离的 Git 工作区 |
| `verification-before-completion` | 以当前证据约束完成、通过和交付声明 |
