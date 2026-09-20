#!/usr/bin/env python3
"""
Update navigation across all HTML pages and build_pages.py to add Speed Test link.
"""

import re

# 1. Update index.html
with open('/root/exelsatu/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Desktop nav
if '/speedtest' not in c:
    c = c.replace(
        '<a href="/promo">Promo</a>\n        <a href="/blog">Blog</a>',
        '<a href="/promo">Promo</a>\n        <a href="/speedtest">Speed Test</a>\n        <a href="/blog">Blog</a>'
    )
    # Drawer nav
    drawer_item = """        <a href="/speedtest" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          <span>Speed Test WiFi</span>
          <span class="drawer-badge drawer-badge-hot">Cek</span>
        </a>\n"""
    c = re.sub(r'(<a href="/promo"[^>]*>[\s\S]*?</a>\s*)(\n\s*<a href="/blog")', r'\1\n' + drawer_item + r'\2', c)

    with open('/root/exelsatu/index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("✓ Updated index.html")

# 2. Update paket.html
with open('/root/exelsatu/paket.html', 'r', encoding='utf-8') as f:
    c = f.read()

if '/speedtest' not in c:
    c = c.replace(
        '<a href="/promo">Promo</a>\n        <a href="/blog">Blog</a>',
        '<a href="/promo">Promo</a>\n        <a href="/speedtest">Speed Test</a>\n        <a href="/blog">Blog</a>'
    )
    drawer_item = """        <a href="/speedtest" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          <span>Speed Test WiFi</span>
          <span class="drawer-badge drawer-badge-hot">Cek</span>
        </a>\n"""
    c = re.sub(r'(<a href="/promo"[^>]*>[\s\S]*?</a>\s*)(\n\s*<a href="/blog")', r'\1\n' + drawer_item + r'\2', c)

    with open('/root/exelsatu/paket.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("✓ Updated paket.html")

# 3. Update promo.html
with open('/root/exelsatu/promo.html', 'r', encoding='utf-8') as f:
    c = f.read()

if '/speedtest' not in c:
    c = c.replace(
        '<a href="/promo" style="color:var(--primary);">Promo</a>\n        <a href="/blog">Blog</a>',
        '<a href="/promo" style="color:var(--primary);">Promo</a>\n        <a href="/speedtest">Speed Test</a>\n        <a href="/blog">Blog</a>'
    )
    if '/speedtest' not in c:
        c = c.replace(
            '<a href="/promo">Promo</a>\n        <a href="/blog">Blog</a>',
            '<a href="/promo">Promo</a>\n        <a href="/speedtest">Speed Test</a>\n        <a href="/blog">Blog</a>'
        )
    drawer_item = """        <a href="/speedtest" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          <span>Speed Test WiFi</span>
          <span class="drawer-badge drawer-badge-hot">Cek</span>
        </a>\n"""
    c = re.sub(r'(<a href="/promo"[^>]*>[\s\S]*?</a>\s*)(\n\s*<a href="/blog")', r'\1\n' + drawer_item + r'\2', c)

    with open('/root/exelsatu/promo.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("✓ Updated promo.html")

# 4. Update bantuan.html
with open('/root/exelsatu/bantuan.html', 'r', encoding='utf-8') as f:
    c = f.read()

if '/speedtest' not in c:
    c = c.replace(
        '<a href="/promo">Promo</a>\n        <a href="/blog">Blog</a>',
        '<a href="/promo">Promo</a>\n        <a href="/speedtest">Speed Test</a>\n        <a href="/blog">Blog</a>'
    )
    drawer_item = """        <a href="/speedtest" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          <span>Speed Test WiFi</span>
          <span class="drawer-badge drawer-badge-hot">Cek</span>
        </a>\n"""
    c = re.sub(r'(<a href="/promo"[^>]*>[\s\S]*?</a>\s*)(\n\s*<a href="/blog")', r'\1\n' + drawer_item + r'\2', c)

    with open('/root/exelsatu/bantuan.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("✓ Updated bantuan.html")

# 5. Update build_pages.py
with open('/root/exelsatu/scripts/build_pages.py', 'r', encoding='utf-8') as f:
    bp = f.read()

if '/speedtest' not in bp:
    # Desktop nav in blog and artikel
    bp = bp.replace(
        '<a href="/promo">Promo</a>\n        <a href="/blog"',
        '<a href="/promo">Promo</a>\n        <a href="/speedtest">Speed Test</a>\n        <a href="/blog"'
    )
    drawer_item_bp = """        <a href="/speedtest" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          <span>Speed Test WiFi</span>
          <span class="drawer-badge drawer-badge-hot">Cek</span>
        </a>\n"""
    bp = re.sub(r'(<a href="/promo"[^>]*>[\s\S]*?</a>\s*)(\n\s*<a href="/blog")', r'\1\n' + drawer_item_bp + r'\2', bp)

    with open('/root/exelsatu/scripts/build_pages.py', 'w', encoding='utf-8') as f:
        f.write(bp)
    print("✓ Updated build_pages.py")
