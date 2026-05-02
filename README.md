# opencode_configs

OpenCode 全局配置仓库（`~/.config/opencode`）。

## 结构

| 条目 | 说明 |
|---|---|
| `AGENTS.md` | 全局工作规则：思考先行、证据驱动、外科式修改、比较输出 |
| `opencode.jsonc` | 主配置：GitHub MCP 远程（仅 `search_repositories` + `search_code`） |
| `agents/code-reviewer.md` | code-reviewer 子代理：四透镜审查（性能边界 / 模块交叉 / 数据所有权 / 错误传播） |
| `skills/` | 14 个代理技能 |

## 技能清单

| Skill | 用途 |
|---|---|
| `plantuml-master` | PlantUML 图表路由：Sequence、Activity、State、Class、Component、Deployment、C4 等 |
| `design-by-contract` | 契约校验与错误处理 |
| `diagnose` | 调试诊断流程：复现 → 最小化 → 假设 → 插桩 → 修复 → 回归 |
| `grill-me` | 方案/设计盘问 |
| `grill-with-docs` | 带文档更新的方案盘问 |
| `handoff` | 跨会话上下文迁移 |
| `obsidian-master` | Obsidian vault 操作 |
| `qm-c-hsm-implementor` | QM C HSM 实现 |
| `qm-c-model-master` | QM C HSM 语义模型 |
| `strict-coding` | 严格编码：窄接口、显式契约 |
| `tdd` | 测试驱动开发：红-绿-重构 |
| `win-wsl-path-converter` | Windows ↔ WSL 路径转换 |
| `write-a-skill` | 创建新的代理技能 |
| `zoom-out` | 代码高层次视角 |

## 排除了什么

- `node_modules/`
- `package.json` / `package-lock.json`

## 使用

```bash
git clone git@github.com:Mengrendufu/opencode_configs.git ~/.config/opencode
```

需要自行设置 `GITHUB_PAT` 环境变量以启用 GitHub MCP。

