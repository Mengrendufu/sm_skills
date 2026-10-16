---
name: qm-c-hsm-implementor
description: 根据已确认的 QM 状态机模型，使用目标语言的工作流约束和模板实现分层状态机。
---

# QM C HSM Implementor

将已确认的模型实现到选定运行时，保留状态层级、初始指向、守卫分支、事件归属和动作语义。

## 工作流

1. 读取 `qm-model-understand` 的模型结果和源代码，明确事件、数据上下文及 entry/exit/action。模型拓扑不代表动作执行次序已经验证。
2. 选择目标语言和运行时，读取对应工作流与模板；先核对目标项目实际 API、导入路径和命名规范。
3. 逐状态映射父子关系、初始化、事件处理和每个守卫分支。区分内部处理、自转移及向父状态委托；动作顺序以源代码和运行时语义为准。
4. 用目标项目的构建和测试检查实现，重点覆盖初始化、自转移、跨层转移、守卫两侧及未处理事件；发现无法忠实表达的语义时报告差异。

## 语言工作流与模板

| 目标 | 工作流 | 模板 |
|---|---|---|
| TypeScript / `ts_hsm` | [约束](references/ts-hsm-api.md) | [SampleMachine.ts](assets/templates/ts-hsm/SampleMachine.ts) |
| C / `sm_hsm` | [约束](references/sm-hsm-api.md) | [SampleMachine.h](assets/templates/sm-hsm/SampleMachine.h) |
| Rust / `rs_hsm_` | [约束](references/rs-hsm-api.md) | [SampleMachine.rs](assets/templates/rs-hsm/SampleMachine.rs) |

只读取匹配目标的资料。上述运行时是适配示例；其他运行时按实际 API 应用相同模型约束。模板是实现起点，完成后需读代码并在目标项目中验证。

## 文件输出

未明确指定落地路径时，所有新生成文件（包括代码、笔记、报告及配套资源）写入当前所在系统的临时目录：Unix 使用 `$TMPDIR`，为空则 `/tmp`；Windows 使用 `%TEMP%`。在其下创建本任务独立子目录（下文 `<tmp-task-dir>`），返回文件绝对路径；不以当前工作区作为默认输出目录。用户明确指定路径时遵循指定。
