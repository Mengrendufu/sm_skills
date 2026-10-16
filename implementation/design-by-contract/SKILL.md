---
name: design-by-contract
description: Detect destructive contract violations and assert at runtime. Use when working on assertion.
---

# 契约式防御性编程

## Goal

识别出会导致结构性坍塌的、违背设计契约的、非业务级策略的运行时错误，并对其进行断言，以使程序可显式观测，无运行时未定义行为。

## 基本语义

| 违约                                  | 检查        |
| ---                                   | ---         |
| 调用方没履行进入受信任操作的义务      | `REQUIRE`   |
| 成功返回时被调方保证不成立            | `ENSURE`    |
| 公开操作前后必须成立的状态规则被打破  | `INVARIANT` |
| 模型禁止的路径被走到                  | `ERROR`     |
| 局部假设在这段代码正确时必真          | `ASSERT`    |
| 检查被关掉时表达式仍必须执行          | `ALLEGE`    |

## 参考模式

[references/patterns.md](references/patterns.md).

## 文件输出

未明确指定落地路径时，所有新生成文件（包括代码、笔记、报告及配套资源）写入当前所在系统的临时目录：Unix 使用 `$TMPDIR`，为空则 `/tmp`；Windows 使用 `%TEMP%`。在其下创建本任务独立子目录（下文 `<tmp-task-dir>`），返回文件绝对路径；不以当前工作区作为默认输出目录。用户明确指定路径时遵循指定。
