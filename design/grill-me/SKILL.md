---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## 文件输出

未明确指定落地路径时，所有新生成文件（包括代码、笔记、报告及配套资源）写入当前所在系统的临时目录：Unix 使用 `$TMPDIR`，为空则 `/tmp`；Windows 使用 `%TEMP%`。在其下创建本任务独立子目录（下文 `<tmp-task-dir>`），返回文件绝对路径；不以当前工作区作为默认输出目录。用户明确指定路径时遵循指定。
