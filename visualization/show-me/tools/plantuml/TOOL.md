# PlantUML

用户指定图类型时遵循指定；否则按表达需要选择。
源码使用 `@startuml` / `@enduml`；语法不确定时查 [官方文档](https://plantuml.com/)，并通过实际渲染验证。

## 环境依赖

- 生成图形：本地 PlantUML JAR 与兼容该版本的 Java 运行环境（JRE/JDK）；仓库尚未内置二者。先检查 `java -version` 和渲染器版本。
- 布局：默认布局下，类图、组件图、部署图、状态图等需要 Graphviz `dot`；序列图等不需要。Linux 通常需单独安装；Windows 部分发行版内置 `dot`，以所选 JAR 为准。使用 Smetana 等替代布局时需确认图类型支持情况，见 [官方依赖说明](https://plantuml.com/graphviz-dot)。
- 字体与扩展：渲染环境需有图中文字对应的字体；图中使用 `!include` 时需提供对应本地文件或可访问的网络资源。
- 查看成品：渲染后的 SVG 与 HTML 只需现代浏览器；内联或本地配套资源齐全时可离线打开，查看端无需 Java 或 Graphviz。

## 放入 HTML

未指定落地路径时，将 `.puml`、SVG 和 HTML 一起放到系统临时目录下的本任务独立子目录（`<tmp-task-dir>`）：Unix 使用 `$TMPDIR`，为空则 `/tmp`；Windows 使用 `%TEMP%`。

1. 检查环境中可用的 PlantUML 渲染器与命令选项。命令行用法见 [官方说明](https://plantuml.com/command-line)。
2. 将 `.puml` 渲染为 SVG。例如，支持传统参数的本地 JAR 可使用：

   ```sh
   java -jar "<plantuml.jar>" -tsvg "<tmp-task-dir>/diagram.puml"
   ```

3. 将生成的 SVG 内联到 HTML，或通过相对路径的 `<img src="diagram.svg" alt="图的含义">` 引用并一同交付。
4. 检查生成物确实是目标图而非错误图，再检查 HTML 中的文字、边界与阅读尺寸。

渲染器不可用时，选择能表达同一含义的其他工具；用户要求保留 PlantUML 时说明缺少的依赖。
保留可编辑的 `.puml` 源码；HTML 承载渲染结果与解释。
