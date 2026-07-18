# Personal Agent Skills

个人、可迁移、工具无关的 [Agent Skills](https://agentskills.io/specification) 集合。

`skills/` 是唯一事实源。每个 Agent 工具只负责加载复制后的 Skill，工具自身的配置、插件、缓存、Agent 定义和系统 Skill 不进入本仓库。

## 原则

- Skill 只使用开放的 `SKILL.md` 结构以及可选的 `scripts/`、`references/`、`assets/`。
- Skill 内不出现 Agent 产品名称、专属 frontmatter 或配置目录。
- Skill 内资源使用相对路径；脚本从 Skill 自身位置解析依赖。
- 外部工具提供的系统 Skill 和插件 Skill 由对应工具管理，不在这里复制。
- 迁移时只精确覆盖选中的 Skill，不删除目标目录中的其他 Skill。

## 结构

```text
.
├── skills/                   # 个人 Skill 唯一事实源
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── scripts/          # 可选
│       ├── references/       # 可选
│       └── assets/           # 可选
├── candidates/               # 待筛选的上游原样候选，不参与迁移
├── scripts/
│   ├── install-skills.sh     # 迁移全部或指定 Skill
│   └── validate-skills.sh    # 校验结构和可移植性
├── tests/portable-skills.sh
├── docs/specs/
└── docs/plans/
```

`candidates/` 只用于评估候选。安装器和正式校验器只读取 `skills/`。

## Skill 清单

| Skill | 用途 |
|---|---|
| `brainstorming` | 在实现前澄清意图、决策缺口与最小设计 |
| `design-by-contract` | 契约检查与错误处理语义 |
| `grill-me` | 逐分支盘问并压力测试方案 |
| `grill-with-docs` | 结合领域文档和 ADR 盘问方案 |
| `handoff` | 跨会话迁移关键上下文 |
| `obsidian-master` | 通过本地 CLI 操作 Obsidian vault |
| `plantuml-master` | 路由并生成可渲染的 PlantUML 图 |
| `qm-c-hsm-implementor` | 将 QM C HSM 语义实现到其他运行时 |
| `qm-c-model-master` | 从 QM 生成的 C 提取 HSM 语义模型 |
| `strict-coding` | 收紧接口、所有权、依赖和执行边界 |
| `systematic-debugging` | 先定位根因，再用单一假设和回归测试修复 |
| `test-driven-development` | 以 RED-GREEN-REFACTOR 驱动行为变更 |
| `using-git-worktrees` | 安全创建、复用并验证隔离的 Git 工作区 |
| `verification-before-completion` | 以当前证据约束完成、通过和交付声明 |
| `win-wsl-path-converter` | 将 Windows 绝对路径转换为 WSL 路径 |
| `zoom-out` | 从陌生代码局部提升到系统视角 |

## 校验

依赖 Bash 和常见 Unix 工具；迁移脚本额外依赖 `rsync`。

```bash
bash scripts/validate-skills.sh
bash tests/portable-skills.sh
```

校验覆盖 frontmatter、Skill 命名、相对资源、脚本执行权限、平台耦合词和迁移边界。

## 迁移

安装全部 Skill：

```bash
bash scripts/install-skills.sh <目标-skills-目录>
```

只安装指定 Skill：

```bash
bash scripts/install-skills.sh <目标-skills-目录> strict-coding plantuml-master
```

安装器会精确镜像每个选中的 Skill，包括删除该目标 Skill 内已经过时的文件；不会删除未选中的目标 Skill。

## 常用目标目录

| Agent 工具 | 个人 Skill 目录 | 官方说明 |
|---|---|---|
| Codex | `$HOME/.agents/skills` | [Build skills](https://developers.openai.com/codex/skills/) |
| OpenCode | `$HOME/.config/opencode/skills` | [Agent Skills](https://opencode.ai/docs/skills/) |
| Claude Code | `$HOME/.claude/skills` | [Extend Claude with skills](https://code.claude.com/docs/en/skills) |

目标工具若支持 Agent Skills 标准但使用其他目录，直接把该目录作为安装器的第一个参数。

## 不包含

- Agent 工具运行配置和权限配置。
- 自定义 Agent、Hook、MCP 或插件声明。
- Codex `.system` Skill、第三方插件 Skill 或任何工具缓存。
- `agents/openai.yaml` 等工具 UI 元数据。

本仓库只维护个人 Skill 的可移植核心。
