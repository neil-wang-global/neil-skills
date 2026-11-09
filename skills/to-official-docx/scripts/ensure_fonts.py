#!/usr/bin/env python3
"""检查并安装公文排版所需字体。

用法:
    python3 ensure_fonts.py            # 只检查，列出缺什么、给出安装命令
    python3 ensure_fonts.py --install  # 检查并自动安装缺失字体

## 公文标准字体

中文公文用字有明确规范，本技能按下列四类取用；缺一类就会导致整篇显示为方块或字形走样：

| 用途 | 首选 | 等价/回退 |
|---|---|---|
| 标题 | 方正小标宋简体 | 方正小标宋_GBK、小标宋、宋体加粗 |
| 一级标题 | 方正黑体简体 | 黑体、思源黑体、苹方 |
| 二级标题 | 方正楷体简体 | 楷体_GB2312、楷体、华文楷体 |
| 正文 | 方正仿宋简体 / 仿宋_GB2312 | 仿宋、华文仿宋 |

## 安装方式

系统间差异很大，脚本按平台选择可行手段，都失败时打印可执行的安装指引，绝不静默跳过。
"""
import os
import platform
import shutil
import subprocess
import sys

# 每类字体：(用途, [候选字体族名...], 安装来源说明)
FONT_GROUPS = [
    ('标题', ['方正小标宋简体', '方正小标宋_GBK', '方正小标宋', 'FZXiaoBiaoSong-B05S'],
     '方正字库（商业授权）或排版软件随附字体包'),
    ('一级标题', ['方正黑体简体', '方正黑体_GBK', '方正黑体', '黑体', 'Heiti SC', 'Source Han Sans', '思源黑体'],
     '系统自带黑体，或方正字库'),
    ('二级标题', ['方正楷体简体', '方正楷体_GBK', '楷体_GB2312', '楷体', 'Kaiti SC', '华文楷体'],
     '系统自带楷体，或方正字库'),
    ('正文', ['方正仿宋简体', '方正仿宋_GB2312', '仿宋_GB2312', '仿宋', 'FangSong', '华文仿宋'],
     '系统自带仿宋，或方正字库'),
]

# 字体文件系统目录
MAC_FONT_DIRS = [os.path.expanduser('~/Library/Fonts'), '/Library/Fonts', '/System/Library/Fonts']
LINUX_FONT_DIRS = [os.path.expanduser('~/.local/share/fonts'), os.path.expanduser('~/.fonts'),
                   '/usr/local/share/fonts', '/usr/share/fonts']


def _run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def installed_families():
    """返回系统已安装的字体族集合（小写）。"""
    fams = set()
    if shutil.which('fc-list'):
        r = _run(['fc-list', '--format', '%{family}\n'])
        if r and r.returncode == 0:
            for line in r.stdout.splitlines():
                for name in line.split(','):
                    if name.strip():
                        fams.add(name.strip().lower())
    # macOS 兜底：直接扫字体目录文件名
    for d in MAC_FONT_DIRS:
        if os.path.isdir(d):
            for f in os.listdir(d):
                stem = os.path.splitext(f)[0]
                fams.add(stem.lower().replace('_', '').replace('-', ''))
    for d in LINUX_FONT_DIRS:
        if os.path.isdir(d):
            for root, _, files in os.walk(d):
                for f in files:
                    if f.lower().endswith(('.ttf', '.ttc', '.otf')):
                        fams.add(os.path.splitext(f)[0].lower().replace('_', '').replace('-', ''))
    return fams


def check(verbose=True):
    fams = installed_families()
    missing = []
    for role, candidates, source in FONT_GROUPS:
        hit = None
        for c in candidates:
            norm = c.lower().replace('_', '').replace('-', '')
            if any(norm == f or norm in f for f in fams):
                hit = c
                break
        if verbose:
            print(f'  {role:8s} {"✓ " + hit if hit else "✗ 缺失"}   候选: {", ".join(candidates[:3])}')
        if not hit:
            missing.append((role, candidates, source))
    return missing


def print_install_guide(missing):
    sysname = platform.system()
    print()
    print('缺失字体安装方式：')
    if sysname == 'Darwin':
        print('  1) 系统自带字体：仿宋、楷体、黑体在 macOS 上名称为 "FangSong" "Kaiti SC" "Heiti SC"，')
        print('     若被卸载，从「字体册」(Font Book) → 文件 → 恢复标准字体 还原。')
        print('  2) 方正系列字体需单独获取，放入 ~/Library/Fonts/ 后执行：')
        print('     atsutil databases -remove && atsutil server -ping')
        print('  3) 也可用 Homebrew 安装开源等价字体：')
        print('     brew install --cask font-source-han-sans font-source-han-serif')
    elif sysname == 'Linux':
        print('  sudo apt install fonts-wqy-zenhei fonts-arphic-uming fonts-arphic-ukai   # Debian/Ubuntu')
        print('  sudo dnf install wqy-zenhei-fonts                                       # Fedora')
        print('  或把 .ttf/.ttc 拷入 ~/.local/share/fonts/ 后执行 fc-cache -fv')
    else:
        print('  Windows：字体文件放入 C:\\Windows\\Fonts\\，或在「设置 → 字体」中拖入安装。')
    print()
    print('  方正字体系商业授权字体，脚本不会替你下载。没有授权时改用系统等价字体：')
    print('  标题→宋体加粗，一级标题→黑体，二级标题→楷体，正文→仿宋，字号与行距不变。')


def try_install():
    """尝试用包管理器安装开源等价字体；返回是否至少装了一套。"""
    sysname = platform.system()
    if sysname == 'Darwin' and shutil.which('brew'):
        pkgs = ['font-source-han-sans', 'font-source-han-serif']
        ok = False
        for p in pkgs:
            r = _run(['brew', 'install', '--cask', p])
            if r and r.returncode == 0:
                print(f'  已安装 {p}')
                ok = True
            else:
                print(f'  安装 {p} 失败（可能已安装或需要授权）')
        if ok:
            _run(['fc-cache', '-fv'])
        return ok
    if sysname == 'Linux':
        try:
            _run(['sudo', 'apt', 'install', '-y', 'fonts-wqy-zenhei'])
            _run(['fc-cache', '-fv'])
            return True
        except Exception:
            return False
    return False


if __name__ == '__main__':
    print('公文排版字体检查：')
    missing = check()
    if not missing:
        print('\n全部字体可用。')
        sys.exit(0)

    roles = ', '.join(m[0] for m in missing)
    print(f'\n缺失 {len(missing)} 类：{roles}')

    if '--install' in sys.argv:
        print('\n尝试自动安装开源等价字体 …')
        if not try_install():
            print_install_guide(missing)
            sys.exit(1)
        print('\n重新检查：')
        missing = check()
        if missing:
            print_install_guide(missing)
            sys.exit(1)
        print('\n安装完成，字体已可用。')
        sys.exit(0)

    print_install_guide(missing)
    print('\n加 --install 参数可让脚本尝试自动安装开源等价字体。')
    sys.exit(2)
