# Superpowers Skill Candidates

这里保存用于筛选和追溯的 Superpowers Skill 上游原样副本。候选内容不会被
本仓库的安装器迁移；正式适配后的版本位于 `skills/`，两者相互独立。

## 来源

- 上游仓库：<https://github.com/obra/superpowers.git>
- 上游版本：`v6.1.1`
- 上游提交：`d884ae04edebef577e82ff7c4e143debd0bbec99`
- 摘取日期：`2026-07-19`
- 许可证：见同目录 `LICENSE`

## 首批候选

| Skill | 状态 | 通用性 | 耦合 | 主要依赖 | 建议 |
|---|---|---|---|---|---|
| `test-driven-development` | 已收录 | 高 | 低 | 同目录 `testing-anti-patterns.md` | 正式版见 `skills/` |
| `systematic-debugging` | 已收录 | 高 | 中 | 显式引用 TDD、完成前验证及同目录资料 | 正式版见 `skills/` |
| `brainstorming` | 已收录 | 高 | 高 | `writing-plans`、视觉伴侣脚本、固定文档路径 | 正式版见 `skills/` |
| `receiving-code-review` | 待筛选 | 高 | 低 | 无硬依赖；末尾含 GitHub 回复示例 | 优先筛选 |
| `verification-before-completion` | 待筛选 | 高 | 低 | 无硬依赖 | 优先筛选 |
| `using-git-worktrees` | 待筛选 | 高 | 中 | Git、宿主原生隔离能力 | 建议保留，需能力化措辞 |
| `writing-plans` | 待筛选 | 中高 | 高 | worktree、子 Agent 执行链、固定文档路径 | 先裁剪再收录 |
| `writing-skills` | 待筛选 | 高 | 高 | TDD、子 Agent 压力测试、Anthropic 参考资料 | 值得保留，需单独改造 |

## 暂未摘取

- `using-superpowers`：是整个套件的强制启动器，并包含具体 Agent 平台适配。
- `dispatching-parallel-agents`、`subagent-driven-development`、
  `executing-plans`、`requesting-code-review`：依赖子 Agent 编排能力和其他
  Superpowers Skill。
- `finishing-a-development-branch`：固定 merge、push、PR 和 worktree 清理菜单，
  更像具体交付政策而非稳定泛型能力。

## 筛选后的处理

选中的 Skill 不应直接移动到正式目录。应逐个执行：

1. 用不加载该 Skill 的场景记录基线行为。
2. 删除 `superpowers:`、固定目录和特定 Agent 工具依赖。
3. 保留真正改变行为的最小规则和必要资源。
4. 通过仓库校验及行为场景验证后，再移入 `skills/`。
