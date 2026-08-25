---
name: implement-interface
description: 设计接口时使用，约束接口的颗粒度和语义范围。
---

# 接口形态

接口包含组件接口和内部helper。

## Goal

1. 接口是行为契约的动作化：单一职责，显式输入/输出/错误/副作用/不变量；不依赖内部状态、时序或实现形状。

2. 接口的逻辑/数据流向保持严格的单向性。

3. 接口允许表达的东西有限、规则少而清晰、实现者/依赖者双方都知道什么合法、什么不合法。

## 基本语义

常规是 单向依赖的 Setter 和 Getter，也可以根据特定契约定义 Contract-Action。

## 接口命名

| 接口类型   |  接口命名形态      | 心智模型
| ---        | ---                | ---                              |
|  外露接口  | <Object>_<action>  | 对某一个<Object>执行某一<action> |
| 内部helper | <Object>_<action>_ | 同上，尾缀<_>表helper身份        |

# 参考模式

[references/patterns.md](references/patterns.md).
