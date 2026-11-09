---
name: to-official-docx
description: Use when a report must be delivered as a Chinese formal Word document with a company template layout — source may be Markdown, txt, an existing .docx, a PDF or rough notes. Triggers on "转成 word", "转公文格式", "转成正式文档", "输出 docx 汇报", "按模板出文档", "docx 转 docx".
---

# 任意来源转公文式 Word

## 输入

来源不限：Markdown、txt、已有的 .docx、PDF、网页或聊天记录整理稿、多份材料合并。

**无论来源是什么，中间产物都必须重建为标准 Markdown**，转换脚本只认这一种中间格式。已有 .docx 或 PDF 先取纯文本、丢掉原版式；中间文件写到临时目录，不覆盖原件。

```bash
python3 scripts/extract_text.py 输入.docx 素材.txt     # 支持 .docx / .md / .txt / .pdf
```

## 先做字体体检

公文排版对字体有明确规范：标题用大标宋、一级标题用黑体、二级标题用楷体、正文用仿宋。**缺一类，整篇就会显示为方块或字形走样。**

动手前先检查，缺字体就装上：

```bash
python3 scripts/ensure_fonts.py            # 检查，列出缺什么
python3 scripts/ensure_fonts.py --install  # 检查并自动安装开源等价字体
```

脚本按四类逐项核对，能找到系统等价字体就通过（例如正文接受仿宋、华文仿宋或系统仿宋），一个都找不到才算缺。安装失败时打印各平台的具体安装方式，不会静默跳过。

方正系列字体是商业授权字体，脚本不代为下载。没有授权时改用系统等价字体，字号与行距不变：标题→宋体加粗，一级标题→黑体，二级标题→楷体，正文→仿宋。

`render_docx.py` 生成文档后会自动再跑一次体检，缺字体时在输出里提示。

## 两个阶段，顺序不可颠倒

**阶段一 润色**：把正文改写成公文语体。先润色后转换——直接跑脚本只会把口语段落排进公文版式，格式对了读起来还是草稿。

**阶段二 转换**：调用 `scripts/render_docx.py`，复用模板的样式表、字体表、页眉页脚，只替换正文。

```bash
python3 scripts/render_docx.py 正文.md 输出.docx --figure 图.png
```

## 语体目标

| 项 | 要求 |
|---|---|
| 段落长度 | 60–90 字一段，一段只说一件事；超过 150 字拆开 |
| 人称 | 不用第一人称 |
| 用词 | 不用口语词，不用感叹号 |
| 枚举 | 用「一是…二是…三是…」「此外」「其中」串联，不列项目符号 |
| 数字 | 每个数字带单位与口径 |
| 边界说明 | 数据有估算或口径差异时，另起一段以「说明：」开头 |
| 结论 | 末章用「1. 2. 3.」逐条写，每条可独立引用 |

润色只改表达，不改数字、不改结论、不补原材料没有的事实。

## 版式规格

见 [references/layout-spec.md](references/layout-spec.md)：样式 ID、页面尺寸、字体与回退、表格、题注、分页、图片规格。

流程图用 Mermaid 渲染成白底黑线 PNG，配置见 [references/mermaid-white-theme.json](references/mermaid-white-theme.json)。

## 交付前强制校验

| 检查项 | 通过标准 |
|---|---|
| zip 完整性 | `ZipFile.testzip()` 返回 None |
| XML 可解析 | 所有 `.xml` / `.rels` 部件都能解析 |
| 分页 | 恰好 2 个分页符 |
| 题注 | 表题在表格上方、图题在图片下方，均紧贴对象，中间无空段落 |
| 目录 | HYPERLINK 与 PAGEREF 成对，数量等于标题总数 |
| 字体 | `word/fonts/*.odttf` 至少 3 个 |
| 封面 | 各段高度之和小于页面可用高度，否则会溢出到第二页 |
| 图片 | PNG 魔数正确，插入宽高比与原图一致 |

**只验证 XML 结构不算通过。** 乱码、空白页、被压扁的图，都是结构正常但一眼能看出来的问题。

```bash
python3 - <<'EOF'
import zipfile, re
from xml.etree import ElementTree as ET
z = zipfile.ZipFile('输出.docx')
assert z.testzip() is None
for n in z.namelist():
    if n.endswith('.xml') or n.endswith('.rels'):
        ET.fromstring(z.read(n))
x = z.read('word/document.xml').decode()
print('分页符', x.count('<w:br w:type="page"/>'))
print('目录域', x.count('HYPERLINK'), x.count('PAGEREF'))
print('内嵌字体', [n for n in z.namelist() if n.endswith('.odttf')])
EOF
```

## 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 打开全是方块 | 只复制了样式表，没复制字体文件；或字体走了主题引用 | 保留 `template/word/fonts/`，每处文字显式指定中文字体 |
| 多出空白页 | 封面或目录末尾重复放了分页符、空段落 | 分页符只有 2 个；封面高度先核算 |
| 题注和对象之间空一行 | 题注与对象之间插了空段落 | 紧贴，不加空段 |
| 图是一片空白框 | 图片实际不是 PNG（改了扩展名） | 检查 PNG 魔数 |
| 图题看着浮在图上方 | 图片段落用了正文的固定行距，先占掉行高 | 图片段落改单倍行距、零段前段后 |
| 目录页码全是 1 | 页码域未更新 | 交付时说明：右键目录 → 更新域 → 更新整个目录 |

## 边界

- 不臆造内容。缺数据就保留「待确认」。
- 不覆盖源文件，输出写新文件名。
- 图必须来自真实渲染，不用手画近似图替代。
- 模板字体在目标机器缺失时，依靠内嵌字体与回退名；两者都失败就把字体换成通用中文字体，字号行距不变。
