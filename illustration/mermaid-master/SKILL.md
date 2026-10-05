---
name: mermaid-master
description: 把 mermaid 序列图落成可交互的 HTML 查看器（滚轮缩放、固定参与者头栏、源码开关）。当需要给用户看时序图、或图太长在 OpenCode 对话里显示不全时使用。
---

# Mermaid Master（序列图）

## 为什么不直接在对话里贴 mermaid

OpenCode 把 mermaid 渲染成**一张固定尺寸的图片**贴进对话 ✗ —— 横向能滚、**纵向不能** ✗。
序列图按消息条数线性变高（26 条消息约 1600 px），必然被裁 ✗。
`cli.json` 里**没有**任何跟内联图片尺寸/滚动相关的设置 ✓（整份设置表核对过）。

**所以：图一律落成 HTML 文件，让用户在浏览器里看。**

## 工作流

1. **写 mermaid 源码** —— 存成 `.mmd`。只要序列图语法。
2. **转 HTML**：

```sh
python3 scripts/mmd2html.py seq.mmd -o /mnt/c/tmp_atk/seq.html
```

脚本会自动把紧凑配置指令插到图源码前面（见下），并在输出目录备好 `mermaid.min.js`。

3. **给用户打开命令**（脚本会打印，落在 `/mnt/c/...` 时自动给 Windows 形式）：

```sh
/mnt/c/Windows/System32/cmd.exe /c start "" "C:\tmp_atk\seq.html"
```

4. **（可选）无头校验** —— 交付前数一数消息/注释条数对不对：

```sh
"/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" \
  --headless=new --disable-gpu --no-sandbox --virtual-time-budget=10000 \
  --dump-dom "file:///C:/tmp_atk/seq.html" > /tmp/dom.html
grep -o 'class="messageText' /tmp/dom.html | wc -l    # 应等于消息条数
grep -o 'class="noteText'    /tmp/dom.html | wc -l    # 应等于注释条数
```

其它平台换成 `chromium --headless --dump-dom`。

5. **要抄进 StarUML / PlantUML 时** —— 点查看器的 `源码` 按钮拿原文，
   **删掉第一行 `%%{init: ...}%%`** ✓（那是 mermaid 专用，别的工具会当成语法错误）。

## 紧凑配置：省 18% 高

脚本会自动注入这一行（已在图上就跳过）：

```
%%{init: {"sequence": {"mirrorActors": false, "messageMargin": 22,
 "noteMargin": 5, "boxMargin": 5, "actorMargin": 36,
 "diagramMarginX": 6, "diagramMarginY": 6}}}%%
```

**实测同一张图**：默认配置 `2403×1984` → 紧凑配置 `2189×1625`（矮 359 px，−18%）。

**写进图源码而不是只写进查看器的 JS** ✓ —— 这样**任何** mermaid 渲染器（包括 OpenCode 自己）
都吃到 ✓。用户要在别处（mermaid.live 等）渲染时，把这一行留着 ✓。

## 约定

| | |
|---|---|
| 输出位置 | WSL 下放 `/mnt/c/tmp_atk/` ✓ —— Windows 侧才能双击打开 ✓ |
| 文件名 | 和源码同名 `.html` ✓ |
| 同目录两件 | `xxx.html` + `mermaid.min.js` ✓ —— 多张图**共用一个 js** ✓，不用重复 ✓ |
| 离线 | 查看器用本地 mermaid ✓，断网可开 ✓；脚本首次取 js 需要联网一次 ✓ |
| 与 OpenCode 无关的图 | 不是序列图就别用这个技能 ✗（头栏依赖 `.actor-top`，是序列图专有）|

## 参考

- `references/sequence-viewer.md` —— 查看器为什么这么设计：固定头栏的钳位原理、
  实测数字、踩过的坑（两条标题栏、CDN 白屏、mermaid 的 max-width 挡住缩放）
- `assets/viewer.html.tpl` —— 查看器模板（两个占位符 `{{TITLE}}` / `{{SOURCE}}`）
- `scripts/mmd2html.py` —— 填模板 + 找/取 `mermaid.min.js`
