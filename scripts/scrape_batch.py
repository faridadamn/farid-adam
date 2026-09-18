#!/usr/bin/env python3
"""
Batch Scraper untuk artikel berita-dan-artikel satu.xl.co.id
Mengambil artikel unik berikutnya yang belum ada di data/articles.json
"""

import urllib.request
import xml.etree.ElementTree as ET
import re
import json
import time
import html
from concurrent.futures import ThreadPoolExecutor

DATA_PATH = "/root/exelsatu/data/articles.json"
SITEMAP_URL = "https://satu.xl.co.id/sitemap.xml"

def get_category_for_slug(slug, title=""):
    text = (slug + " " + title).lower()
    
    # Priority matching
    if any(k in text for k in ['xl-satu', 'xl satu', 'xl-home', 'first media', 'first-media', 'opensignal', 'kuota-hp', 'tagihan', 'pembayaran']):
        return "Info XL SATU"
    if any(k in text for k in ['pasang', 'biaya-pasang', 'daftar', 'keuntungan-pasang', 'kantor', 'syarat']):
        return "Panduan Pasang"
    if any(k in text for k in ['game', 'gaming', 'stream', 'streaming', 'youtube', 'netflix', 'tiktok', 'twitch', '4k', '8k', 'video', 'film', 'nonton', 'siaran']):
        return "Gaming & Streaming"
    if any(k in text for k in ['wifi', 'router', 'bandwidth', 'jaringan', 'sinyal', 'ip-address', 'ping', 'latensi', 'koneksi', 'connect', 'interferensi', 'blank-spot', 'extender', 'mesh', 'modem', 'vpn', 'dns', 'protokol', 'internet-positif', 'adblock', 'mbps']):
        return "Tips & Jaringan"
    return "Gadget & Trik"

def clean_content_html(raw_html):
    if not raw_html:
        return ""
    cleaned = re.sub(r'href="https://satu\.xl\.co\.id/berita-dan-artikel/([^"]+)"', r'href="artikel.html?slug=\1"', raw_html)
    cleaned = re.sub(r'href="/berita-dan-artikel/([^"]+)"', r'href="artikel.html?slug=\1"', cleaned)
    cleaned = re.sub(r'href="https://satu\.xl\.co\.id/?"', r'href="index.html#cakupan"', cleaned)
    cleaned = re.sub(r'href="/bantuan"', r'href="bantuan.html"', cleaned)
    cleaned = re.sub(r'href="/paket"', r'href="paket.html"', cleaned)
    cleaned = re.sub(r'href="/promo"', r'href="promo.html"', cleaned)
    cleaned = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', cleaned)
    cleaned = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', cleaned)
    cleaned = re.sub(r'\n\s*\n', '\n', cleaned)
    return cleaned.strip()

def scrape_one_article(slug):
    url = f"https://satu.xl.co.id/berita-dan-artikel/{slug}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            page_html = resp.read().decode('utf-8', errors='replace')
        
        # Title
        title_m = re.search(r'<title>(.*?)</title>', page_html, re.I)
        title = title_m.group(1).split('|')[0].strip() if title_m else slug.replace('-', ' ').title()
        title = html.unescape(title)
        
        # H1
        h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', page_html, re.DOTALL | re.I)
        h1 = re.sub(r'<[^>]+>', '', h1_m.group(1)).strip() if h1_m else title
        h1 = html.unescape(h1)
        
        # Description
        desc_m = re.search(r'<meta name="description" content="(.*?)"', page_html, re.I)
        desc = html.unescape(desc_m.group(1).strip()) if desc_m else ""
        
        # OG Image
        img_m = re.search(r'<meta property="og:image" content="(.*?)"', page_html, re.I)
        image = img_m.group(1).strip() if img_m else "https://static-xlsatu.xl.co.id/images/og-image.jpg"
        
        # Date
        date_m = re.search(r'(\d{1,2}\s+(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s+\d{4})', page_html)
        date_str = date_m.group(1) if date_m else "18 September 2026"
        
        # Content from safe-html
        content_m = re.search(r'<div class="[^"]*safe-html[^"]*">([\s\S]*?)</div>\s*</div>', page_html)
        if not content_m:
            content_m = re.search(r'<div class="[^"]*safe-html[^"]*">([\s\S]*?)</div>\s*(?:<div|<section|</main)', page_html)
        
        raw_content = content_m.group(1) if content_m else ""
        cleaned_content = clean_content_html(raw_content)
        
        # Hitung waktu baca (200 kata/menit)
        plain_text = re.sub(r'<[^>]+>', ' ', cleaned_content)
        word_count = len(plain_text.split())
        read_time = max(2, round(word_count / 200))
        
        category = get_category_for_slug(slug, title)
        
        print(f"✓ [{category}] {title[:40]}... ({word_count} kata, {read_time} min)")
        
        return {
            "slug": slug,
            "title": title,
            "h1": h1,
            "description": desc,
            "image": image,
            "date": date_str,
            "category": category,
            "read_time": f"{read_time} menit",
            "word_count": word_count,
            "content": cleaned_content,
            "url": f"/blog/{slug}"
        }
    except Exception as e:
        print(f"✗ Gagal scrape {slug}: {e}")
        return None

def main(batch_count=70):
    # 1. Baca artikel yang sudah ada
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            existing_articles = json.load(f)
    except Exception:
        existing_articles = []
    
    existing_slugs = set(a['slug'] for a in existing_articles)
    print(f"📦 Artikel yang sudah ada di database: {len(existing_articles)}")
    
    # 2. Ambil seluruh URL sitemap
    req = urllib.request.Request(SITEMAP_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=12) as resp:
        xml_data = resp.read()
    
    root = ET.fromstring(xml_data)
    all_urls = [elem.text for elem in root.iter() if elem.tag.endswith('loc') and '/berita-dan-artikel/' in (elem.text or '')]
    
    # Filter unik yang belum ada
    seen = set(existing_slugs)
    remaining_slugs = []
    for u in all_urls:
        slug = u.split('/')[-1].strip()
        if slug and slug not in seen:
            seen.add(slug)
            remaining_slugs.append(slug)
    
    total_in_sitemap = len(set(u.split('/')[-1].strip() for u in all_urls if u.split('/')[-1].strip()))
    print(f"🌐 Total artikel unik di sitemap: {total_in_sitemap}")
    print(f"⏳ Artikel tersisa yang belum diproses: {len(remaining_slugs)}")
    
    target_slugs = remaining_slugs[:batch_count]
    print(f"🚀 Memproses batch baru sebanyak {len(target_slugs)} artikel...")
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(scrape_one_article, target_slugs))
    
    added_count = 0
    for r in results:
        if r and r['content']:
            existing_articles.append(r)
            added_count += 1
            
    # Simpan kembali ke JSON
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_articles, f, ensure_ascii=False, indent=2)
        
    duration = time.time() - start_time
    total_now = len(existing_articles)
    print(f"\n🎉 Berhasil menambahkan {added_count} artikel baru dalam {duration:.1f} detik!")
    print(f"📊 Total artikel sekarang: {total_now} / {total_in_sitemap} artikel ({total_now/total_in_sitemap*100:.1f}%)")

if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 70
    main(count)
