# UML 四元素语料

## 建模视角

| 元素 | 视角 | 回答的问题 |
|---|---|---|
| Package | 架构层级 | 能力归哪组？ |
| Subsystem | 聚合对象 | 谁在协调多个下级兑现一个承诺？ |
| Component | 叶子对象 | 谁能独自承诺完整语义？ |
| Interface | I/O 契约 | 外部如何使用这个能力？`

## 视角切面图

四元素按三条带理解：分层轴、承载带、跨越面。

```
┌─ Band 1 ─ Package :: 架构层级
│    应用层 / BSP 层 / PORTS 层 / 内核层 / BackEnd / FrontEnd / …
│
├─ Band 2 ─ Subsystem :: 聚合对象 ＆ Component :: 叶子对象
│    ├─ 实体
│    │    状态上下文 · 数据 Ownership · I/O 接口
│    └─ 虚体
│         Runtime 调度逻辑抽象
│
└─ Band 3 ─ Interface :: I/O 契约
     Operations（规格声明）/ Method（具体实现）
```

Scope 链：`Package >> Subsystem > Component >> Interface`
（>> 为层级大跳，> 为聚合内小跳，>> 为契约跨界面）

## 归属层级树

```
uml-model
├── package :: 架构层级
│   ├── diagram
│   ├── package …            （分组递归）
│   ├── subsystem :: 聚合对象
│   │   ├── diagram
│   │   ├── subsystem …      （聚合递归，实测深达 3 层）
│   │   ├── component :: 叶子对象
│   │   │   └── interface    （随宿主生灭）
│   │   └── interface
│   ├── component :: 叶子对象
│   │   └── interface
│   └── interface            （跨层契约可直挂 Package）
```

要点：
- Component 是叶子，不递归；唯一允许的子节点是 Interface。
- Subsystem 可递归嵌套（样板实证最深 3 层）。
- Interface 在 package/subsystem/component 三层均可直接挂载。

## 候选识别特征（建模资格）

凡具备以下任一特征的抽象对象，即获得至少 Component 的建模地位：

- 实体特征：状态上下文、数据 Ownership、I/O 接口
- 虚体特征：Runtime 调度与胶水逻辑

实体/虚体只是业务语义浓淡的标签，不影响建模资格。
