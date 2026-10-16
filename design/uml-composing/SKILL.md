---
name: uml-composing
description: Use when talking or composing UML architecture.
---

先内化Reference，并根据当前架构任务的每个方面对我进行反复询问，沿着设计树的各分支逐一展开，逐项解决各项决策之间的依赖关系，直至我认为我们达成了共识并允许你映射出对应的 UML 架构草案。

## Basic Philosophy

参考文档中的元素分层、归属和红线是本集合采用的建模约定；应用前与目标项目的建模规范对齐。

1. UML结构对功能的承载映射最终体现在UML元素内部独立数据、逻辑I/O和元素之间的接口协作。

2. 逻辑扩散和数据传递的单向可追溯性。

## Reference

- [references/viewpoints.md](references/viewpoints.md) —— 四视角、归属层级树、实体/虚体识别特征
- [references/anti-patterns.md](references/anti-patterns.md) —— 红线清单

## 文件输出

未明确指定落地路径时，所有新生成文件（包括代码、笔记、报告及配套资源）写入当前所在系统的临时目录：Unix 使用 `$TMPDIR`，为空则 `/tmp`；Windows 使用 `%TEMP%`。在其下创建本任务独立子目录（下文 `<tmp-task-dir>`），返回文件绝对路径；不以当前工作区作为默认输出目录。用户明确指定路径时遵循指定。
