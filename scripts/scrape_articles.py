#!/usr/bin/env python3
"""
Scraper 30 Artikel Populer dari satu.xl.co.id/berita-dan-artikel
Menghasilkan /root/exelsatu/data/articles.json terstruktur
"""

import urllib.request
import re
import json
import time
import html
from concurrent.futures import ThreadPoolExecutor

SLUGS = [
    # Live Streaming & Gaming
    "kecepatan-internet-untuk-live-streaming",
    "cara-live-game-di-tiktok",
    "rekomendasi-aplikasi-cloud-gaming",
    "apa-itu-cloud-gaming",
    "perbedaan-streaming-4k-vs-8k",
    "peralatan-live-streaming",
    "cara-live-di-shopee",
    "rekomendasi-wifi-untuk-menonton-video-streaming",
    
    # Tips WiFi & Jaringan Rumah
    "memperkuat-sinyal-wifi",
    "cara-memperkuat-sinyal-wifi-hingga-ke-seluruh-sudut-rumah",
    "perbedaan-router-single-band-dan-dual-band",
    "perbedaan-dedicated-dan-up-to-bandwidth",
    "kenapa-wifi-tidak-ada-internet-ini-cara-mengatasinya",
    "penyebab-dan-cara-mengatasi-sinyal-wifi-naik-turun",
    "apa-itu-mbps-pada-wifi-penjelasan-singkat-dan-cara-memaksimalkannya",
    "apa-itu-bandwidth-wifi",
    "blank-spot-wifi",
    "manajemen-bandwidth",
    "interferensi-jaringan-wifi",
    "cara-menggunakan-wifi-extender-di-rumah",
    
    # Pemasangan & Keunggulan Fiber
    "biaya-pasang-wifi",
    "cara-memasang-wifi-di-rumah-untuk-kebutuhan-sehari-hari",
    "keuntungan-pasang-wifi-di-rumah",
    "apa-itu-internet-super-cepat",
    "wifi-terbaik-untuk-kantor",
    
    # Info Layanan XL SATU & First Media
    "metode-pembayaran-first-media",
    "xl-satu-raih-penghargaan-opensignal",
    
    # Tips Gadget & Digital Lifestyle
    "cara-download-file-besar-dengan-cepat",
    "cara-bersihkan-cache-di-iphone",
    "cara-share-screen-di-wa"
]

CATEGORY_MAP = {
    "kecepatan-internet-untuk-live-streaming": "Gaming & Streaming",
    "cara-live-game-di-tiktok": "Gaming & Streaming",
    "rekomendasi-aplikasi-cloud-gaming": "Gaming & Streaming",
    "apa-itu-cloud-gaming": "Gaming & Streaming",
    "perbedaan-streaming-4k-vs-8k": "Gaming & Streaming",
    "peralatan-live-streaming": "Gaming & Streaming",
    "cara-live-di-shopee": "Gaming & Streaming",
    "rekomendasi-wifi-untuk-menonton-video-streaming": "Gaming & Streaming",
    
    "memperkuat-sinyal-wifi": "Tips & Jaringan",
    "cara-memperkuat-sinyal-wifi-hingga-ke-seluruh-sudut-rumah": "Tips & Jaringan",
    "perbedaan-router-single-band-dan-dual-band": "Tips & Jaringan",
    "perbedaan-dedicated-dan-up-to-bandwidth": "Tips & Jaringan",
    "kenapa-wifi-tidak-ada-internet-ini-cara-mengatasinya": "Tips & Jaringan",
    "penyebab-dan-cara-mengatasi-sinyal-wifi-naik-turun": "Tips & Jaringan",
    "apa-itu-mbps-pada-wifi-penjelasan-singkat-dan-cara-memaksimalkannya": "Tips & Jaringan",
    "apa-itu-bandwidth-wifi": "Tips & Jaringan",
    "blank-spot-wifi": "Tips & Jaringan",
    "manajemen-bandwidth": "Tips & Jaringan",
    "interferensi-jaringan-wifi": "Tips & Jaringan",
    "cara-menggunakan-wifi-extender-di-rumah": "Tips & Jaringan",
    
    "biaya-pasang-wifi": "Panduan Pasang",
    "cara-memasang-wifi-di-rumah-untuk-kebutuhan-sehari-hari": "Panduan Pasang",
    "keuntungan-pasang-wifi-di-rumah": "Panduan Pasang",
    "apa-itu-internet-super-cepat": "Panduan Pasang",
    "wifi-terbaik-untuk-kantor": "Panduan Pasang",
    
    "metode-pembayaran-first-media": "Info XL SATU",
    "xl-satu-raih-penghargaan-opensignal": "Info XL SATU",
    
    "cara-download-file-besar-dengan-cepat": "Gadget & Trik",
    "cara-bersihkan-cache-di-iphone": "Gadget & Trik",
    "cara-share-screen-di-wa": "Gadget & Trik"
}

def clean_content_html(raw_html):
    if not raw_html:
        return ""
    # Ganti link internal berita
    cleaned = re.sub(r'href="https://satu\.xl\.co\.id/berita-dan-artikel/([^"]+)"', r'href="artikel.html?slug=\1"', raw_html)
    cleaned = re.sub(r'href="/berita-dan-artikel/([^"]+)"', r'href="artikel.html?slug=\1"', cleaned)
    # Ganti link satu.xl.co.id umum ke internal / WhatsApp sales
    cleaned = re.sub(r'href="https://satu\.xl\.co\.id/?"', r'href="index.html#cakupan"', cleaned)
    cleaned = re.sub(r'href="/bantuan"', r'href="bantuan.html"', cleaned)
    cleaned = re.sub(r'href="/paket"', r'href="paket.html"', cleaned)
    cleaned = re.sub(r'href="/promo"', r'href="promo.html"', cleaned)
    # Hapus tag script & style jika ada
    cleaned = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', cleaned)
    cleaned = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', cleaned)
    # Hapus whitespace berlebih
    cleaned = re.sub(r'\n\s*\n', '\n', cleaned)
    return cleaned.strip()

def scrape_article(slug):
    url = f"https://satu.xl.co.id/berita-dan-artikel/{slug}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
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
        image = img_m.group(1).strip() if img_m else "https://satu.xl.co.id/images/og-image.jpg"
        
        # Date
        date_m = re.search(r'(\d{1,2}\s+(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s+\d{4})', page_html)
        date_str = date_m.group(1) if date_m else "18 September 2026"
        
        # Content from safe-html
        content_m = re.search(r'<div class="[^"]*safe-html[^"]*">([\s\S]*?)</div>\s*</div>', page_html)
        if not content_m:
            # fallback jika format penutup berbeda
            content_m = re.search(r'<div class="[^"]*safe-html[^"]*">([\s\S]*?)</div>\s*(?:<div|<section|</main)', page_html)
        
        raw_content = content_m.group(1) if content_m else ""
        cleaned_content = clean_content_html(raw_content)
        
        # Hitung waktu baca (rata-rata 200 kata per menit)
        plain_text = re.sub(r'<[^>]+>', ' ', cleaned_content)
        word_count = len(plain_text.split())
        read_time = max(2, round(word_count / 200))
        
        category = CATEGORY_MAP.get(slug, "Tips & Jaringan")
        
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

def main():
    print(f"🚀 Memulai scraping {len(SLUGS)} artikel XL SATU...")
    start_time = time.time()
    articles = []
    
    # Gunakan ThreadPool 5 worker agar cepat tapi tetap ramah
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(scrape_article, SLUGS))
    
    for r in results:
        if r:
            articles.append(r)
            
    print(f"\n✨ Selesai! Berhasil mengambil {len(articles)} dari {len(SLUGS)} artikel dalam {time.time() - start_time:.1f} detik.")
    
    output_path = "/root/exelsatu/data/articles.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
        
    print(f"💾 Data tersimpan di {output_path} ({len(json.dumps(articles)) / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
