# 序列图查看器：设计说明

记录为什么长这样，以及踩过的坑。改模板前先看这里。

## 1. 为什么要 HTML 而不是对话里贴源码

OpenCode 把 mermaid 渲染成**一张固定尺寸的图片**贴进对话：

- 横向**能**滚 ✓
- 纵向**不能**滚 ✗ —— 图的下半截永远看不到

序列图的高度随消息条数线性增长（实测 26 条消息 + 7 注释 = **1625 px**），
终端的可见高度大概 800 px，所以**必然被裁** ✓。

`~/.config/opencode/cli.json` 的完整设置表核对过：**没有**任何跟内联图片尺寸、
高度、滚动相关的项 ✗。这不是配置问题，是它的显示方式。

## 2. 紧凑配置：省 18% 高（实测）

同一张图（26 条消息），只改 mermaid 的 sequence 配置：

| 配置 | SVG 尺寸 |
|---|---|
| 默认 | `2403 × 1984` |
| 紧凑 | `2189 × 1625` |

省下的是两块：

- `mirrorActors: false` —— 默认会在图**底部再画一遍**参与者条，纯属浪费
- `messageMargin / noteMargin / boxMargin / actorMargin` 收紧

**关键：写进图源码的 `%%{init: ...}%%` 指令，而不是只写进查看器的 JS。**
实测两种方式渲染结果**逐像素一致** ✓，但指令版的好处是**任何** mermaid 渲染器
（包括 OpenCode 自己的）都会吃到 ✓。

## 3. 查看器的四个能力

### 3.1 缩放平移

两个必须做的处理：

```css
#stage svg { max-width:none !important; height:auto !important; }
```

mermaid 渲染时会给 `<svg>` 加 `style="max-width: ...px"` —— **不压掉就放不大** ✓。

滚轮缩放以光标为中心（不是以图心）✓；拖动用 `pointerdown/move/up` + `setPointerCapture` ✓。

### 3.2 固定参与者头栏 ★

长图往下看会忘了哪条生命线是谁 —— 头栏把参与者那一行钉在顶部 ✓。

**做法不是把参与者抽出来重画** ✗（那样缩放时对不齐）✓，而是：

1. `svg.cloneNode(true)` 整份克隆进头栏，去掉 `id`（避免重复 id）
2. 用 `.actor-top` 元素的 `getBBox()` 量出参与者带的上下边界
3. 头栏 `overflow:hidden`，高度 = `(bandBot - bandTop) * s + 2*PAD`，**封顶 120 px**
4. 头栏与主图用**同一个** `translate(tx, ·) scale(s)` —— 只有纵向不同：
   `ty_head = PAD - bandTop * s`（把参与者带钉在头栏顶部）
5. 头栏 `pointer-events:none` —— 鼠标划过它照样能拖动主图

### 3.3 纵向钳位 ★（防"两条标题栏"）

**这是踩过的坑**：滚轮缩小会以光标为中心重算 `ty`，把图整体往下推，
于是图**自己**那条参与者行从固定头栏底下钻出来，看起来像**两条标题栏** ✗。

修法：

```js
function tyMax() { return headOn ? (PAD - bandTop * s) : Infinity; }
function apply() { if (ty > tyMax()) { ty = tyMax(); } ... }
```

图的纵向平移有上限 —— 图的参与者带顶端不能低于头栏里那条的位置 ✓。
头栏关掉时钳位解除 ✓（自由平移）✓。

### 3.4 源码开关

**坑**：`mermaid.run()` 会把 `<pre class="mermaid">` 的内容**替换成 SVG**，
渲染完就再也拿不到源码了 ✗。

修法：**渲染之前**先 `textContent` 存一份到变量里，`#srcbox` 用那份 ✓。

用途：往 StarUML / PlantUML 抄的时候要文本 ✓ —— 注意**删掉第一行 `%%{init}%%`** ✓。

## 4. 交付前的校验（无头 Chrome）

```sh
"/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" \
  --headless=new --disable-gpu --no-sandbox --virtual-time-budget=10000 \
  --dump-dom "file:///C:/tmp_atk/seq.html" > /tmp/dom.html
```

然后数元素（这些 class 是 mermaid 自己给的）：

| 元素 | 含义 |
|---|---|
| `class="messageText"` | 消息条数（**注意**：头栏克隆会把计数翻倍 ✓）|
| `class="noteText"` | 注释条数 |
| `class="loopText"` | `loop` + `opt` 片段数 |
| `class="actor actor-top"` | 参与者数 |
| `<svg` | 1 主图 + 1 头栏克隆 = 2 ✓ |

**这是唯一能证明"图真的渲染出来了、条数没漏"的手段** ✓ —— 不看图也能验 ✓。

## 5. 依赖钉版

| | |
|---|---|
| mermaid | **11.17.2**（`cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.min.js`）|
| md5 | `e1399ce98467ce048863d2ffaabf01ba`（2026-10-05 取的 3.5 MB 那份）|
| 许可 | mermaid 为 MIT；`mermaid.min.js` 尾部带全部内联依赖的许可注释 ✓ |

**为什么不把 js 提交进仓库**：`sm_skills` 是纯文本仓库，最大文件 49 KB ✗ ——
3.5 MB 会大出 70 倍 ✗。改成 `scripts/mmd2html.py` 按需取 + 缓存到
`~/.cache/mermaid-master/` ✓，输出目录里再放一份给查看器用 ✓。

## 6. 其他坑

| 现象 | 原因 |
|---|---|
| 断网打开是白屏 | 早期版本从 CDN 取 mermaid ✗ —— 现在本地 ✓ |
| `file://` 下 `<script type="module">` 失败 | ES module 走 CORS，`file://` 被拒 ✗ —— 必须用普通脚本（UMD）✓ |
| 图放大不了 | mermaid 的 `max-width` ✗ —— 见 3.1 ✓ |
| 缩小时两条标题栏 | 见 3.3 ✓ |
| 源码按钮是空的 | 见 3.4 ✓ |
| 抄进 StarUML 报语法错 | 忘了删 `%%{init}%%` 那行 ✗ |
