#!/usr/bin/env python3
"""Markdown → 公文式 Word（绿地扫描版式）。

用法:
    python3 render_docx.py <输入.md> <输出.docx> [--template <骨架目录>]

输入 Markdown 约定
------------------
# 标题                       → 封面大标题（可写成两行：用 " | " 分隔）
## 一、章节                   → 一级标题（方正黑体 16pt，首行缩进 2 字符）
### 6.1 小节                  → 二级标题（方正楷体 16pt）
普通段落                     → 方正仿宋_GB2312 16pt，固定行距 30pt，首行缩进 2 字符
- / 1. 列表                  → 同正文段落（去掉列表符号）
| a | b |                    → 三线表格，表题自动编号「表 N　…」
```mermaid ... ```             → 图（表题自动编号「图 N　…」）
> 表题/图题                   → 用引用块显式指定题注文字

元数据（写在文件开头的引用块里）
    > 编制：姓名
    > 编制单位：公司全称
    > 编制日期：2026年11月
    > 标题行2：与新增采购的请示      ← 可选，封面第二行

骨架目录默认取技能根目录下的 template/，其中含样式表、字体表、内嵌字体与页眉页脚。
"""
import re, os, sys, zipfile, shutil
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(os.path.dirname(HERE), 'template')

# 与模板样式表一致的字体声明；{cn} 为 esatAsia 字体名
def _fr(cn):
    return (f'<w:rFonts w:hint="eastAsia" w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
            f'w:eastAsia="{cn}" w:cs="Times New Roman"/>')

RPR_BODY = _fr('方正仿宋_GB2312') + '<w:sz w:val="32"/><w:szCs w:val="32"/>'
RPR_H1 = _fr('方正黑体') + '<w:sz w:val="32"/><w:szCs w:val="32"/>'
RPR_H2 = _fr('方正楷体') + '<w:sz w:val="32"/><w:szCs w:val="32"/>'
RPR_CAP = _fr('方正黑体') + '<w:sz w:val="18"/><w:szCs w:val="18"/>'
SP600 = '<w:spacing w:before="0" w:after="0" w:line="600" w:lineRule="exact"/>'

NS = ('xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
      'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
      'xmlns:o="urn:schemas-microsoft-com:office:office" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
      'xmlns:v="urn:schemas-microsoft-com:vml" '
      'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:w10="urn:schemas-microsoft-com:office:word" '
      'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
      'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" '
      'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
      'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
      'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
      'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
      'mc:Ignorable="w14 w15 wp14"')


def run(text, rpr):
    return (f'<w:r><w:rPr>{rpr}<w:color w:val="000000"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r>')


def inline(text, rpr):
    out = []
    for i, seg in enumerate(re.split(r'\*\*(.+?)\*\*', text)):
        if seg:
            out.append(run(seg, rpr + ('<w:b/>' if i % 2 == 1 else '')))
    return ''.join(out)


def p_blank(n=1):
    return f'<w:p><w:pPr>{SP600}</w:pPr></w:p>' * n


def body_para(text):
    return (f'<w:p><w:pPr><w:bidi w:val="0"/>{SP600}'
            f'<w:ind w:firstLine="640" w:firstLineChars="200"/>'
            f'<w:rPr><w:rFonts w:hint="eastAsia"/></w:rPr></w:pPr>{inline(text, RPR_BODY)}</w:p>')


_bm = {'n': 100}
def heading(text, level):
    _bm['n'] += 1
    name = f'_Toc{_bm["n"]}'
    ppr = (f'<w:pStyle w:val="3"/><w:bidi w:val="0"/>{SP600}'
           f'<w:ind w:firstLine="640" w:firstLineChars="200"/>' if level == 1 else
           f'<w:pStyle w:val="4"/><w:bidi w:val="0"/>{SP600}'
           f'<w:ind w:firstLine="640" w:firstLineChars="200"/>')
    rpr = RPR_H1 if level == 1 else RPR_H2
    x = (f'<w:p><w:pPr>{ppr}</w:pPr><w:bookmarkStart w:id="{_bm["n"]}" w:name="{name}"/>'
         f'{run(text, rpr)}<w:bookmarkEnd w:id="{_bm["n"]}"/></w:p>')
    return x, (name, text, level)


def caption(text):
    return (f'<w:p><w:pPr>{SP600}<w:jc w:val="center"/>'
            f'<w:ind w:left="0" w:leftChars="0" w:firstLine="0" w:firstLineChars="0"/></w:pPr>'
            f'{run(text, RPR_CAP)}</w:p>')


def table(rows):
    ncol = len(rows[0])
    widths = {2: [3000, 6751], 3: [2500, 5251, 2000], 4: [2100, 4251, 1750, 1650],
              5: [1800, 2600, 2000, 1800, 1551], 6: [1600, 1800, 1700, 1600, 1500, 1551]}.get(
                  ncol, [9751 // ncol] * ncol)
    bd = ('<w:tblBorders>' + ''.join(
        f'<w:{s} w:val="single" w:color="auto" w:sz="4" w:space="0"/>'
        for s in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']) + '</w:tblBorders>')
    pr = (f'<w:tblPr><w:tblW w:w="9751" w:type="dxa"/><w:jc w:val="center"/>{bd}'
          '<w:tblLayout w:type="fixed"/>'
          '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
          '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr>')
    grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>'
    trs = []
    for ri, cells in enumerate(rows):
        head = ri == 0
        trpr = ('<w:trPr><w:trHeight w:val="397" w:hRule="atLeast"/><w:tblHeader/></w:trPr>' if head
                else '<w:trPr><w:trHeight w:val="340" w:hRule="atLeast"/></w:trPr>')
        tcs = []
        for ci, cell in enumerate(cells):
            txt = cell.strip()
            align = 'center' if head or ci == 0 or (re.search(r'\d', txt) and len(txt) <= 16) else 'both'
            rpr = _fr('方正仿宋_GB2312') + '<w:sz w:val="21"/><w:szCs w:val="21"/>' + ('<w:b/>' if head else '')
            p = (f'<w:p><w:pPr><w:snapToGrid w:val="0"/>'
                 f'<w:spacing w:before="0" w:after="0" w:line="280" w:lineRule="exact"/>'
                 f'<w:ind w:left="0" w:leftChars="0" w:right="0" w:rightChars="0" '
                 f'w:firstLine="0" w:firstLineChars="0"/>'
                 f'<w:jc w:val="{align}"/><w:rPr>{rpr}</w:rPr></w:pPr>{inline(txt, rpr)}</w:p>')
            tcs.append(f'<w:tc><w:tcPr><w:tcW w:w="{widths[ci]}" w:type="dxa"/>'
                       f'<w:vAlign w:val="center"/></w:tcPr>{p}</w:tc>')
        trs.append(f'<w:tr>{trpr}{"".join(tcs)}</w:tr>')
    return f'<w:tbl>{pr}{grid}{"".join(trs)}</w:tbl>'


def _png_size(path):
    import struct
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    return struct.unpack('>II', head[16:24])


def image_anchor(cx, cy, rid, name):
    # 图片段落用单倍行距且零段前后间距，否则固定 30pt 行距会在图上方压出一条空白带
    return ('<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
            '<w:jc w:val="center"/>'
            '<w:ind w:left="0" w:leftChars="0" w:firstLine="0" w:firstLineChars="0"/></w:pPr>'
            '<w:r><w:drawing>'
            '<wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="2" '
            'behindDoc="0" locked="0" layoutInCell="1" allowOverlap="1">'
            '<wp:simplePos x="0" y="0"/>'
            '<wp:positionH relativeFrom="column"><wp:align>center</wp:align></wp:positionH>'
            '<wp:positionV relativeFrom="paragraph"><wp:posOffset>0</wp:posOffset></wp:positionV>'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
            '<wp:wrapTopAndBottom/>'
            f'<wp:docPr id="1" name="{name}"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic><pic:nvPicPr><pic:cNvPr id="1" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
            '</a:graphicData></a:graphic></wp:anchor></w:drawing></w:r></w:p>')


def cover(title_lines, meta):
    rpr_b = _fr('方正小标宋简体') + '<w:sz w:val="72"/><w:szCs w:val="72"/><w:b/>'
    rpr_m = _fr('方正楷体') + '<w:sz w:val="44"/><w:szCs w:val="44"/>'
    out = [p_blank(4)]
    single = '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'  # 单倍行距
    for line in title_lines:
        out.append(f'<w:p><w:pPr>{single}'
                   f'<w:ind w:left="0" w:leftChars="0" w:firstLine="0" w:firstLineChars="0"/>'
                   f'<w:jc w:val="center"/><w:rPr>{rpr_b}</w:rPr></w:pPr>{run(line, rpr_b)}</w:p>')
    out.append(p_blank(7))
    for t in meta:
        out.append(f'<w:p><w:pPr>{SP600}'
                   f'<w:ind w:left="0" w:leftChars="0" w:firstLine="0" w:firstLineChars="0"/>'
                   f'<w:jc w:val="center"/><w:rPr>{rpr_m}</w:rPr></w:pPr>{run(t, rpr_m)}</w:p>')
    out.append(p_blank(1))
    out.append(f'<w:p><w:pPr>{SP600}</w:pPr><w:r><w:br w:type="page"/></w:r></w:p>')
    # 高度核算：空段 30pt，标题行单倍行距约 43pt/行
    # 4*30 + 2*43 + 7*30 + 3*30 + 1*30 = 120+86+210+90+30 = 536pt = 18.9cm < 23.7cm
    return ''.join(out)


def toc(entries):
    rpr = _fr('方正楷体') + '<w:sz w:val="32"/><w:szCs w:val="32"/>'
    rpr_h = _fr('方正楷体') + '<w:sz w:val="44"/><w:szCs w:val="44"/>'
    out = [f'<w:p><w:pPr><w:spacing w:before="0" w:after="240" w:line="360" w:lineRule="auto"/>'
           f'<w:ind w:left="0" w:leftChars="0" w:firstLine="0" w:firstLineChars="0"/>'
           f'<w:jc w:val="center"/><w:rPr>{rpr_h}</w:rPr></w:pPr>{run("目　　录", rpr_h)}</w:p>']
    for name, text, level in entries:
        style = '26' if level == 1 else '29'
        ind = ('<w:ind w:left="0" w:leftChars="0" w:firstLine="640" w:firstLineChars="200"/>' if level == 1
               else '<w:ind w:left="640" w:leftChars="200" w:firstLine="0" w:firstLineChars="0"/>')
        fld = (f'<w:r><w:rPr>{rpr}</w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
               f'<w:r><w:rPr>{rpr}</w:rPr><w:instrText xml:space="preserve"> HYPERLINK \\l {name} </w:instrText></w:r>'
               f'<w:r><w:rPr>{rpr}</w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
               f'<w:r><w:rPr>{rpr}</w:rPr><w:t>{escape(text)}</w:t></w:r>'
               f'<w:r><w:rPr>{rpr}</w:rPr><w:tab/></w:r>'
               f'<w:r><w:rPr>{rpr}</w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
               f'<w:r><w:rPr>{rpr}</w:rPr><w:instrText xml:space="preserve"> PAGEREF {name} \\h </w:instrText></w:r>'
               f'<w:r><w:rPr>{rpr}</w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
               f'<w:r><w:rPr>{rpr}</w:rPr><w:t>1</w:t></w:r>'
               f'<w:r><w:rPr>{rpr}</w:rPr><w:fldChar w:fldCharType="end"/></w:r>'
               f'<w:r><w:rPr>{rpr}</w:rPr><w:fldChar w:fldCharType="end"/></w:r>')
        out.append(f'<w:p><w:pPr><w:pStyle w:val="{style}"/>'
                   f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="8400"/></w:tabs>'
                   f'<w:spacing w:before="0" w:after="0" w:line="360" w:lineRule="auto"/>{ind}</w:pPr>{fld}</w:p>')
    out.append(f'<w:p><w:pPr>{SP600}</w:pPr><w:r><w:rPr>{rpr}</w:rPr><w:br w:type="page"/></w:r></w:p>')
    return ''.join(out)


def build(md_path, out_path, template=DEFAULT_TEMPLATE, figure_png=None):
    lines = open(md_path, encoding='utf-8').read().split('\n')
    title = ''
    meta = []
    body, entries = [], []
    i, tbl_no, fig_no = 0, 0, 0
    # 表题映射：紧跟表格前的 > 引用块，或按 n 号顺序取
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        if not s:
            i += 1
            continue
        if s.startswith('# ') and not title:
            title = s[2:].strip()
            i += 1
            continue
        if s.startswith('> '):
            meta.append(s[2:].strip())
            i += 1
            continue
        if s.startswith('## '):
            h, e = heading(s[3:].strip(), 1)
            body.append(h); entries.append(e); i += 1; continue
        if s.startswith('### '):
            h, e = heading(s[4:].strip(), 2)
            body.append(h); entries.append(e); i += 1; continue
        if s.startswith('```'):
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith('```'):
                j += 1
            fig_no += 1
            cap = ''
            block = '\n'.join(lines[i + 1:j])
            m = re.search(r'%%\s*图题[:：]\s*(.+)', block)
            if m:
                cap = m.group(1).strip()
            label = f'图 {fig_no}' + (f'\u3000{cap}' if cap else '')
            cx = 3500000
            size = _png_size(figure_png) if figure_png else None
            cy = int(cx * size[1] / size[0]) if size else 3000000
            body.append(image_anchor(cx, cy, 'rId8', 'figure'))
            body.append(caption(label))   # 图题必须在锚点段落之后，且中间不得插入任何段落
            i = j + 1
            continue
        if s.startswith('|'):
            rows, j = [], i
            while j < len(lines) and lines[j].strip().startswith('|'):
                cells = [c.strip() for c in lines[j].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
                    rows.append(cells)
                j += 1
            tbl_no += 1
            cap = f'表 {tbl_no}'
            m = re.search(r'%%\s*表题[:：]\s*(.+)', rows[0][0] if rows else '')
            if m:
                cap += '\u3000' + m.group(1).strip()
                rows[0][0] = re.sub(r'%%\s*表题[:：].*', '', rows[0][0]).strip()
            body.append(caption(cap))
            body.append(table(rows))
            i = j
            continue
        if re.match(r'^([-*]|\d+\.)\s', s):
            body.append(body_para(re.sub(r'^([-*])\s+', '', s)))
            i += 1
            continue
        body.append(body_para(s))
        i += 1

    title_lines = [t.strip() for t in title.split('|')] if title else ['（未命名文档）']
    meta_lines = [m for m in meta if re.match(r'(编制|日期|单位|作者)', m)]
    if not meta_lines:
        meta_lines = ['编制日期：' + __import__('datetime').date.today().isoformat()]

    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
           f'<w:document {NS}><w:body>{cover(title_lines, meta_lines)}{toc(entries)}'
           f'{"".join(body)}'
           '<w:sectPr><w:headerReference w:type="default" r:id="rId5"/>'
           '<w:footerReference w:type="default" r:id="rId6"/>'
           '<w:pgSz w:w="11906" w:h="16838"/>'
           '<w:pgMar w:top="1587" w:right="1417" w:bottom="1814" w:left="1417" '
           'w:header="720" w:footer="720" w:gutter="0"/>'
           '<w:cols w:space="720" w:num="1"/><w:docGrid w:linePitch="360" w:charSpace="0"/>'
           '</w:sectPr></w:body></w:document>')

    # 字体表补齐 altName 回退（缺回退时缺字体会整篇方块）
    import re as _re
    ft_path = os.path.join(template, 'word', 'fontTable.xml')
    if os.path.exists(ft_path):
        ft = open(ft_path, encoding='utf-8').read()
        fallback = {
            '方正仿宋_GB2312': '仿宋_GB2312', '方正黑体': '黑体-简',
            '方正楷体': '楷体_GB2312', '方正楷体_GBK': '楷体_GB2312',
            '方正黑体_GBK': '黑体-简', '方正小标宋简体': '宋体',
            '方正小标宋': '宋体',
        }
        for fam, alt in fallback.items():
            pat = f'<w:font w:name="{fam}">'
            if pat in ft:
                head, tail = ft.split(pat, 1)
                seg, rest = tail.split('</w:font>', 1)
                if '<w:altName' not in seg:
                    ft = head + pat + f'<w:altName w:val="{alt}"/>' + seg + '</w:font>' + rest
        open(ft_path, 'w', encoding='utf-8').write(ft)

    # 从骨架打包
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(template):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, template).replace(os.sep, '/')
                if rel in ('word/document.xml', 'word/_rels/document.xml.rels',
                           '[Content_Types].xml', '_rels/.rels'):
                    continue
                if not rel:
                    continue
                z.write(full, rel)
        z.writestr('word/document.xml', doc.encode('utf-8'))
        rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
                '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" Target="footnotes.xml"/>'
                '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/endnotes" Target="endnotes.xml"/>'
                '<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>'
                '<Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>'
                '<Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
                '<Relationship Id="rId8" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/figure.png"/>'
                '<Relationship Id="rId24" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
                '<Relationship Id="rId26" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/>'
                '</Relationships>')
        z.writestr('word/_rels/document.xml.rels', rels)
        ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
              '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
              '<Default Extension="xml" ContentType="application/xml"/>'
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
              '<Default Extension="png" ContentType="image/png"/>'
              '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
              '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
              '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
              '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
              '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
              '<Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/>'
              '<Override PartName="/word/endnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml"/>'
              '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
              '<Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>'
              '<Override PartName="/word/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
              '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
              '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
              '</Types>')
        z.writestr('[Content_Types].xml', ct)
        pkg_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
                    '</Relationships>')
        z.writestr('_rels/.rels', pkg_rels)
        # 占位图片（调用方应先写真实 PNG 到 template/media/figure.png 或在此替换）
        ph = figure_png or os.path.join(template, 'media', 'figure.png')
        if ph and os.path.exists(ph):
            z.write(ph, 'word/media/figure.png')
    print(f'已生成 {out_path}  表 {tbl_no} 张，图 {fig_no} 张，目录 {len(entries)} 条')

    # 字体体检：缺字体时文档在别人机器上会显示为方块
    try:
        import subprocess as _sp
        r = _sp.run([sys.executable, os.path.join(HERE, 'ensure_fonts.py')],
                    capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            print()
            print('⚠ 本机缺少公文排版字体，文档在他人机器上可能显示为方块：')
            print(r.stdout.rstrip())
            print()
            print('  自动安装开源等价字体：python3 scripts/ensure_fonts.py --install')
    except Exception:
        pass


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    tpl = DEFAULT_TEMPLATE
    if '--template' in sys.argv:
        tpl = sys.argv[sys.argv.index('--template') + 1]
    fig = None
    if '--figure' in sys.argv:
        fig = sys.argv[sys.argv.index('--figure') + 1]
    build(sys.argv[1], sys.argv[2], tpl, fig)
