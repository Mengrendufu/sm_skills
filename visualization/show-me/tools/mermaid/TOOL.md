# Mermaid

按表达需要选择 Mermaid 图表类型，可直接将渲染器接入 HTML。
浏览器加载方案以 [官方用法](https://mermaid.js.org/config/usage.html) 和实际运行环境为准。

## 环境依赖

- 生成现成查看器：Python 3，仅使用标准库，无需安装 Node.js 或 npm 包。
- 渲染与查看：支持 JavaScript 和 SVG 的现代浏览器，以及 `mermaid.min.js`。现有脚本使用 `11.17.2`，仓库尚未内置该文件。
- 下载：本地没有渲染器时，需要访问 jsDelivr；离线生成可通过 `--mermaid` 指定已有文件。成品 HTML 与本地 JS 一起交付后可离线打开。
- 自定义页面若使用 ES module 加载渲染器，按浏览器要求通过本地 HTTP 服务打开；现成查看器使用普通脚本，可直接打开本地 HTML。

## 现成查看器

未指定落地路径时，将源码、HTML 和配套 JS 放到系统临时目录下的本任务独立子目录（`<tmp-task-dir>`）：Unix 使用 `$TMPDIR`，为空则 `/tmp`；Windows 使用 `%TEMP%`。

需要单张图的缩放、拖动和源码开关时，使用已有脚本：

```sh
python3 "<skill-dir>/tools/mermaid/scripts/mmd2html.py" "<tmp-task-dir>/diagram.mmd" -o "<tmp-task-dir>/diagram.html"
```

`<skill-dir>` 为 `show-me/SKILL.md` 所在目录。交付 `diagram.html` 与同目录的 `mermaid.min.js`，打开时无需联网。
脚本优先读取 `--mermaid <本地JS路径>`、输出目录或缓存中的渲染器；都没有时会下载固定版本。
缓存位于系统临时目录下的 `show-me-mermaid/`。省略 `-o` 时，脚本自动在系统临时目录中创建独立子目录，保留源码文件名作为 HTML 文件名，并打印实际输出位置。

查看器会为序列图添加紧凑布局和固定参与者头栏；其他图没有参与者头栏。
需要多图、说明面板或定制交互时，直接编写 HTML，不必套用这个单图模板。

## 修改查看器时

- 脚本通过相对路径加载 `assets/viewer.html.tpl`；移动时保持两者的相对结构。
- SVG 的自然尺寸与缩放变换要一致，避免 Mermaid 的 `max-width` 限制放大。
- 固定头栏与主图共用缩放和平移；检查长序列图向下查看及缩小时的对齐。
- 渲染前保存 Mermaid 源码，渲染后从保存的副本提供源码查看。Mermaid 与 PlantUML 是不同语法，不能直接互换。
