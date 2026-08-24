---
name: design-by-contract
description: 识别会破坏性的契约违约，并在运行时断言。
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
