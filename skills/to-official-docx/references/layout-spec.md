# 版式规格（来自公司模板《2026绿化养护面积核准报告(格式统一版)》）

`scripts/render_docx.py` 直接复用该模板的样式表、字体表、页眉页脚，下列数值即模板原值。

## 页面

```xml
<w:pgSz w:w="11906" w:h="16838"/>                       <!-- A4 -->
<w:pgMar w:top="1587" w:right="1417" w:bottom="1814" w:left="1417"
         w:header="720" w:footer="720" w:gutter="0"/>
```

可用正文高度 = 16838 − 1587 − 1814 = **13437 twips ≈ 23.7cm**。
封面的安全上限也按这个算：段落数 × 30pt < 23.7cm。

## 样式 ID 对照

模板 `styles.xml` 用数字 styleId，不是 `Heading1` 这种名字。写自定义 XML 时用这些 ID：

| 用途 | styleId | 字体 | 字号 | 说明 |
|---|---|---|---|---|
| 正文 | `1`（Normal） | 方正仿宋_GB2312 | 32 半磅 = 16pt | 固定行距 600 twips = 30pt，首行缩进 1040 twips / 200 字符单位 |
| 一级标题 | `3`（heading 1） | 方正黑体 | 16pt | `keepNext` + `outlineLvl 0` |
| 二级标题 | `4`（heading 2） | 方正楷体_GBK | 16pt | `outlineLvl 1` |
| 目录一级 | `26`（toc 1） | 方正楷体 | 16pt | 右对齐点线制表位 `pos=9072` |
| 目录二级 | `29`（toc 2） | 方正楷体 | 16pt | 同上，需加左缩进 |
| 表格 | `35`（Normal Table） | 仿宋 | 10.5pt | 表格正文另用 run 级 `sz=21` |
| 页脚 | `24` | 宋体 | 8.5pt | 「— 页码 —」 |

## 字体

模板指定四类中文字体，均随文档嵌入（`word/fonts/font1..3.odttf`）：

| 用途 | 指定字体 | altName 回退 |
|---|---|---|
| 正文 | 方正仿宋_GB2312 | 仿宋-简 / 仿宋_GB2312 |
| 一级标题 | 方正黑体 | 黑体-简 |
| 二级标题 | 方正楷体_GBK / 方正楷体 | 楷体_GB2312 |
| 封面标题 | 方正小标宋简体 | 华文楷体 |

**每个 run 必须显式写 `w:eastAsia="字体名"`。** 模板 `docDefaults` 里写的是 `eastAsiaTheme="minorEastAsia"`，会把中文回退到主题字体，落在一个不存在的字体上，表现为整篇方块。

## 表格

```xml
<w:tblW w:w="9751" w:type="dxa"/>          <!-- 与正文宽度一致 -->
<w:jc w:val="center"/>
<tblBorders … sz="4"/>                      <!-- 全框线 0.5pt -->
<w:tblLayout w:type="fixed"/>
<w:tblCellMar left=108 right=108 top=0 bottom=0/>
```

首行 `<w:tblHeader/>` + `trHeight 397 atLeast`，其余行 `340 atLeast`。
单元格段落：`snapToGrid=0`、`line=280 exact`、`jc=center|both`。

## 封面标题行距

封面大标题用**单倍行距**：

```xml
<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>
```

不要用正文的固定 30 磅（`line="600" lineRule="exact"`）——36pt 的字放在 30pt 固定行距里会上下压字。封面其余空段仍用 30pt，便于按段数算高度。

## 图片段落行距

图片段落同样用单倍行距 + 零段前后间距。写成固定 30pt 时，锚点段落会先占 30pt，再遭到图下方环绕，导致图与图题之间出现一条空白带，看上去像「图题浮在图上」。

## 题注

```
表 1　存量服务器续费清单        ← 黑体 9pt 居中，全角空格分隔编号与题名
图 1　新平台服务拓扑与新增服务器定位
```

题注段落必须 `firstLine=0 firstLineChars=0`，且**紧随对象，中间不插空段落**。

## 分页

只用两种分页方式，总数固定 2：

1. 封面末尾：`<w:p><w:pPr>…</w:pPr><w:r><w:br w:type="page"/></w:r></w:p>`
2. 目录末尾：同上

不要用 `pageBreakBefore`，不要两段连续分页（会产生空白页）。

## 图片

`wp:anchor` + `wp:wrapTopAndBottom`（上下环绕），水平 `align=center`，垂直 `posOffset=0`。
宽 3500000 EMU（≈9.7cm）时，竖版图（宽高比约 0.46）高约 21cm，正好一页放下。
`cx/cy` 必须等于 PNG 实际宽高比。
