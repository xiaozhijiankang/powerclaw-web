#!/usr/bin/env python3
"""Update both homepages without adding browser-side JavaScript."""
import argparse
from html import escape
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description='同步设置中英文首页的下载按钮')
action = parser.add_mutually_exclusive_group(required=True)
action.add_argument('--disable', action='store_true', help='置灰全部下载按钮，不保留可点击链接')
action.add_argument('--url', help='使用已核实的 App Store HTTPS 地址启用全部下载按钮')
args = parser.parse_args()
if args.url:
    parsed = urlsplit(args.url)
    if (parsed.scheme != 'https' or parsed.netloc != 'apps.apple.com'
            or not re.search(r'/id\d+(?:/|$)', parsed.path)
            or any(char.isspace() or ord(char) < 32 for char in args.url)):
        parser.error('请提供有效的 https://apps.apple.com/.../id数字 地址')

icon = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg>'
pattern = re.compile(r'<!-- DOWNLOAD_BUTTON_START -->.*?<!-- DOWNLOAD_BUTTON_END -->', re.S)
updates = []
for language, filename in [('zh', 'index.html'), ('en', 'en/index.html')]:
    path = ROOT / filename
    original = path.read_text()
    zh = language == 'zh'
    if args.disable:
        label = 'iOS 下载暂未开放' if zh else 'iOS download is not yet available'
        small = '暂未开放' if zh else 'Not yet available'
        element = f'<button type="button" class="store-btn" disabled aria-label="{label}">{icon}<span class="meta"><small>{small}</small><strong>App Store</strong></span></button>'
    else:
        label = '在 App Store 下载 PowerClaw' if zh else 'Download PowerClaw on the App Store'
        small = '前往下载' if zh else 'Download on the'
        element = f'<a class="store-btn" href="{escape(args.url, quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="{label}">{icon}<span class="meta"><small>{small}</small><strong>App Store</strong></span></a>'
    updated, count = pattern.subn(lambda _: '<!-- DOWNLOAD_BUTTON_START -->\n        '+element+'\n        <!-- DOWNLOAD_BUTTON_END -->', original)
    if count != 2:
        parser.error(f'{filename}: 应有两个下载区域，实际为 {count}；未写入任何页面')
    updates.append((path, updated))
for path, updated in updates:
    path.write_text(updated)
print('已同步更新中英文首页的 4 个下载按钮：'+('置灰，不可点击' if args.disable else '启用'))
