# 正例语料

从样板工程 sm_tracer_tui 提炼的可复用建模模式。

## 接口三件套

每个承载元素按需配置三种角色的 Interface，命名 `<Element><Role>`：

| 角色 | 职责 | 样板实例 |
|---|---|---|
| Lifecycle | 构造、初始化、运行、销毁 | `IUIThreadLifecycle`（UI_init/UI_run）、`ISM_InputCmpsMngrLifecycle`（ctor/init/create/destroy/resize） |
| Ingress / EvtDispatch | 事件或调用进入 | `IUIEventIngress`（UI_postText/postPortList）、`ISM_InputCmpsMngrEvtDispatch` |
| Control | 配置与模式切换 | `ISM_InputCmpsMngrControl`（setActive） |

一个只有单一调用者且只被 owner 使用的方法不成其为边界，删。

## 并发域优先

先切并发域（线程 / Active Object / 中断上下文），每域一个 Subsystem；Package 分组最后贴。

样板：`Application` 下挂 `UIThread` / `SpThread` / `AO_SpMngr` / `AO_Blinky`，恰好对应五条 OS 线程的分类。

## 所有权词汇

依赖边必须标注语义，三词足够：

| 标注 | 含义 |
|---|---|
| `<<owns lifecycle>>` | 创建者兼销毁者 |
| `<<borrows>>` | owner 保证有效期内的使用 |
| `<<lends>>` | 把借来的对象交出去 |

样板实例：`UIThreadRuntime → NotcursesRuntime <<owns lifecycle>>`；`SMUI → NotcursesRuntime <<borrows>>`。

## 端口模式

平台差异收敛到叶子：每个真实存在 OS 契约差异的能力一个 Port Component（`ports/` 下按能力分七个），业务元素保持平台中立。原生分支只出现在 port 实现内。

## 序列图锁运行时契约

交互图消息名直接用信号名（`SPMNGR_PORT_OPENED`），lifeline 用 represent 绑定到结构元素，alt 片段表达成功/失败分支。结构图定"谁是谁"，序列图定"怎么来去"。
