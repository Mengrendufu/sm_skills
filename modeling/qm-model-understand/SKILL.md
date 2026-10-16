---
name: qm-model-understand
description: 从 QM 生成的 C 状态处理函数理解模型拓扑，包括状态层级、初始指向、事件转移和守卫分支。
---

# QM Model Understand

以给定 QM C 为依据，解释状态包含关系、初始指向、事件归属、转移端点及各守卫分支。

## 使用

解析器使用 Python 3 标准库，支持 `Q_TRAN` / `Q_SUPER` 等状态处理函数形态；其他 QM 生成策略需先确认能否解析。

```sh
python3 "<skill-dir>/scripts/parse_qm_c.py" "<input.c>" --output text --strict
```

- `text` 用于直接理解拓扑；需要保存结构化结果时改用 `json`，参见 [模型 JSON](references/model-json.md)。
- 保留每个守卫分支；区分转移、内部处理、向父状态委托和未处理事件。
- 严格模式失败时报告诊断与未解析关系，核对源代码后重新提取。`is_reliable` 仅表示解析器未报告 error。
- entry、exit、action 是源码注记，供阅读和实现时对照；本 skill 不推演运行时执行次序或证明行为等价。
- 需要图解时将模型交给 `show-me`；进入实现时交给 `qm-c-hsm-implementor`，同时提供源代码中的动作与数据上下文。

`<skill-dir>` 为本文件所在目录。回归检查：`PYTHONDONTWRITEBYTECODE=1 python3 "<skill-dir>/scripts/test_parse_qm_c.py"`。

## 文件输出

未明确指定落地路径时，所有新生成文件（包括代码、笔记、报告及配套资源）写入当前所在系统的临时目录：Unix 使用 `$TMPDIR`，为空则 `/tmp`；Windows 使用 `%TEMP%`。在其下创建本任务独立子目录（下文 `<tmp-task-dir>`），返回文件绝对路径；不以当前工作区作为默认输出目录。用户明确指定路径时遵循指定。
