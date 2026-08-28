---
name: uml-sync
description: 将用户的 StarUML 模型 [.mdj] 或架构图 PNG 同步为 Agent 可读文本。适用于建模前获取最新模型、查看现有 UML 架构、或提供模型上下文给其他 skill。
---

# UML Sync

将 StarUML 权威模型同步为 Agent 可读文本。纯机械操作，不做任何架构判断。

完整协议（输入路由、toolbox 类型表、receive/receive-image/emit、失败类别）见 [reference/uml-exchange.md](reference/uml-exchange.md)。

## 快速路径

1. 用户给了 `.mdj` → 运行导出脚本，读取输出：

```text
python "<skill-dir>/scripts/export_model_tree.py" --mdj "<mdj>" -o "<out>/model-tree.txt"
```

2. 输出两段：`# Explorer`（成员关系、模型关系、Documentation）与 `# Diagrams`（每张图挂载的元素、连线、Notes）。
3. 脚本非零退出 → 停止，报 `mdj-tree-unreadable`，不要手写 JSON 解析替代。

## 边界

- 只读：不改模型、不提结构建议——那是 `uml-composing` 的职责。
- 不导出图片；不手解 `.mdj` JSON。
- PNG/截图输入时树信息未知（`receive-image`），需要成员关系就向用户要 `.mdj`。

## 样板命令

```sh
# sm_tracer_tui 实例
python "<skill-dir>/scripts/export_model_tree.py" \
  --mdj "/mnt/c/mengrendufu/workshop/umls/staruml/sm_tracer/sm_tracer_tui/sm_tracer_tui.mdj" \
  -o /tmp/model-tree.txt
```
