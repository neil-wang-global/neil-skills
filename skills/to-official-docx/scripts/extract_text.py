#!/usr/bin/env python3
"""把任意文档抽成纯文本，供 to-official-docx 阶段一润色使用。

用法:
    python3 extract_text.py 输入文件 [输出.txt]

支持: .docx（直接读 word/document.xml）、.md/.txt/.markdown（直接读）、
     .pdf（调用 pdftotext，找不到时提示改用 wpscli pdf2txt）。

只抽文字，不保留原文档的字体、版式、表格结构——版式由 render_docx.py 重建。
"""
import os
import re
import subprocess
import sys
import zipfile
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def from_docx(path):
    z = zipfile.ZipFile(path)
    doc = ET.fromstring(z.read('word/document.xml'))
    lines = []
    for el in doc.find(W + 'body'):
        if el.tag == W + 'p':
            t = ''.join(x.text or '' for x in el.iter(W + 't')).strip()
            if t:
                lines.append(t)
        elif el.tag == W + 'tbl':
            for row in el.findall(W + 'tr'):
                cells = [''.join(x.text or '' for x in c.iter(W + 't')).strip()
                         for c in row.findall(W + 'tc')]
                lines.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(lines)


def from_pdf(path):
    for cmd in (['pdftotext', '-layout', path, '-'],):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if out.returncode == 0:
                return out.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    raise SystemExit(
        '未找到 pdftotext。可改用：'
        '/Applications/wpsoffice.app/Contents/MacOS/wpscli pdf2txt 输入.pdf -o 输出.txt'
    )


def extract(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.docx':
        return from_docx(path)
    if ext in ('.md', '.markdown', '.txt', '.text'):
        return open(path, encoding='utf-8', errors='replace').read()
    if ext == '.pdf':
        return from_pdf(path)
    raise SystemExit(f'不支持的格式: {ext}（请手动转成 txt 或 md 后再运行）')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    text = extract(sys.argv[1])
    if len(sys.argv) >= 3:
        open(sys.argv[2], 'w', encoding='utf-8').write(text)
        print(f'已抽取 {len(text)} 字 -> {sys.argv[2]}')
    else:
        print(text)
