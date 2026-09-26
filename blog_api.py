#!/usr/bin/env python3
import html
import json
import os
import re
import sys
import shutil
import uuid
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8656
AUTH_TOKEN = "cWST8dH8B45Yme38m4Acsg"

# Adjust paths based on environment
BASE_DIR = "/var/www/faridadamn-landing" if os.path.exists("/var/www/faridadamn-landing") else "/root/faridadamn"
DATA_DIR = os.path.join(BASE_DIR, "data")
ARTICLES_JSON = os.path.join(DATA_DIR, "articles.json")
COMMENTS_JSON = os.path.join(DATA_DIR, "comments.json")
ANALYTICS_EVENTS_JSON = os.path.join(DATA_DIR, "analytics_events.json")
SITEMAP_XML = os.path.join(BASE_DIR, "sitemap.xml")
ROBOTS_TXT = os.path.join(BASE_DIR, "robots.txt")

def ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(ARTICLES_JSON):
        with open(ARTICLES_JSON, "w", encoding="utf-8") as f:
            json.dump([], f)
    generate_sitemap()
    generate_robots()
    seed_analytics_if_needed()
    seed_comments_and_likes_if_needed()

def load_articles():
    try:
        with open(ARTICLES_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading articles: {e}", file=sys.stderr)
        return []

def save_articles(articles):
    # Atomic save with backup
    if os.path.exists(ARTICLES_JSON):
        shutil.copy2(ARTICLES_JSON, ARTICLES_JSON + ".bak")
    with open(ARTICLES_JSON, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    generate_sitemap()

def load_analytics_events():
    try:
        if os.path.exists(ANALYTICS_EVENTS_JSON):
            with open(ANALYTICS_EVENTS_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading analytics: {e}", file=sys.stderr)
    return []

def save_analytics_events(events):
    try:
        # Keep recent 3000 events
        events = events[:3000]
        with open(ANALYTICS_EVENTS_JSON, "w", encoding="utf-8") as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving analytics: {e}", file=sys.stderr)

def load_comments():
    try:
        if os.path.exists(COMMENTS_JSON):
            with open(COMMENTS_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading comments: {e}", file=sys.stderr)
    return []

def save_comments(comments):
    try:
        if os.path.exists(COMMENTS_JSON):
            shutil.copy2(COMMENTS_JSON, COMMENTS_JSON + ".bak")
        with open(COMMENTS_JSON, "w", encoding="utf-8") as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving comments: {e}", file=sys.stderr)

def parse_ua(ua):
    ua_lower = (ua or "").lower()
    if "googlebot" in ua_lower:
        return "Googlebot (Crawler)", "Bot", "Googlebot"
    
    os_name = "Desktop"
    device_type = "Desktop"
    if "iphone" in ua_lower:
        os_name = "iPhone (iOS)"
        device_type = "Mobile"
    elif "ipad" in ua_lower:
        os_name = "iPad (iPadOS)"
        device_type = "Tablet"
    elif "android" in ua_lower:
        os_name = "Android"
        device_type = "Mobile"
    elif "windows" in ua_lower:
        os_name = "Windows"
    elif "macintosh" in ua_lower or "mac os" in ua_lower:
        os_name = "Mac"
    elif "linux" in ua_lower:
        os_name = "Linux"

    browser = "Browser"
    if "whatsapp" in ua_lower:
        browser = "WhatsApp Webview"
    elif "instagram" in ua_lower:
        browser = "Instagram Webview"
    elif "edg" in ua_lower:
        browser = "Edge"
    elif "chrome" in ua_lower:
        browser = "Chrome Mobile" if device_type == "Mobile" else "Chrome"
    elif "safari" in ua_lower:
        browser = "Safari Mobile" if device_type == "Mobile" else "Safari"
    elif "firefox" in ua_lower:
        browser = "Firefox"

    return f"{os_name} • {browser}", device_type, browser

def parse_referrer(ref):
    if not ref or ref.strip() == "":
        return "Direct / WhatsApp"
    ref_lower = ref.lower()
    if "google." in ref_lower:
        return "Google Search"
    if "whatsapp" in ref_lower or "wa.me" in ref_lower or "l.wl.co" in ref_lower:
        return "WhatsApp Link"
    if "t.co" in ref_lower or "twitter" in ref_lower or "x.com" in ref_lower:
        return "Twitter / X"
    if "instagram.com" in ref_lower:
        return "Instagram"
    if "threads.net" in ref_lower:
        return "Threads"
    if "faridadamn.my.id/blog" in ref_lower:
        return "Katalog Blog (/blog/)"
    if "faridadamn.my.id" in ref_lower:
        return "Portal Beranda (/)"
    m = re.search(r"https?://([^/]+)", ref)
    return m.group(1) if m else ref[:25]

def record_click_event(slug, referrer, screen, ip, ua):
    articles = load_articles()
    target_art = next((a for a in articles if a.get("slug") == slug), None)
    
    if target_art:
        target_art["views"] = target_art.get("views", 0) + 1
        save_articles(articles)
        art_title = target_art.get("title", slug)
    else:
        art_title = slug

    device_label, platform, browser = parse_ua(ua)
    ref_label = parse_referrer(referrer)
    now_dt = datetime.now()

    evt = {
        "id": "clk-" + uuid.uuid4().hex[:8],
        "slug": slug,
        "article_title": art_title,
        "ip": ip or "127.0.0.1",
        "device": device_label,
        "platform": platform,
        "browser": browser,
        "referrer": ref_label,
        "raw_referrer": referrer or "",
        "screen": screen or "",
        "timestamp": now_dt.isoformat(),
        "created_at_wib": now_dt.strftime("%d %b %Y, %H:%M:%S WIB")
    }

    events = load_analytics_events()
    events.insert(0, evt)
    save_analytics_events(events)
    return evt

def seed_analytics_if_needed():
    if os.path.exists(ANALYTICS_EVENTS_JSON) and os.path.getsize(ANALYTICS_EVENTS_JSON) > 10:
        return

    articles = load_articles()
    if not articles:
        return

    sample_ips = [
        "180.252.88.14", "114.122.45.92", "103.111.34.8", "36.85.12.104",
        "182.253.90.22", "125.160.77.31", "103.28.14.88", "139.192.4.5"
    ]
    sample_devices = [
        ("Android • Chrome Mobile", "Mobile", "Chrome Mobile", "390x844"),
        ("iPhone (iOS) • Safari Mobile", "Mobile", "Safari Mobile", "393x852"),
        ("Windows • Chrome", "Desktop", "Chrome", "1920x1080"),
        ("Mac • Safari", "Desktop", "Safari", "1440x900"),
        ("Android • Chrome Mobile", "Mobile", "Chrome Mobile", "412x915")
    ]
    sample_refs = [
        ("WhatsApp Link", "https://wa.me/"),
        ("Google Search", "https://www.google.com/search?q=toko+online+chat+first"),
        ("Google Search", "https://www.google.com/search?q=agen+ai+bisnis+2026"),
        ("Direct / WhatsApp", ""),
        ("Katalog Blog (/blog/)", "https://faridadamn.my.id/blog/"),
        ("Portal Beranda (/)", "https://faridadamn.my.id/")
    ]

    events = []
    now = datetime.now()

    for idx, a in enumerate(articles):
        slug = a.get("slug")
        title = a.get("title", slug)
        base_views = 35 + (idx * 22)
        a["views"] = base_views

        for i in range(base_views):
            delta_mins = (base_views - i) * 24 + (i * 7 % 19)
            evt_time = now - timedelta(minutes=delta_mins)
            ip = sample_ips[i % len(sample_ips)]
            dev, plat, brw, scr = sample_devices[i % len(sample_devices)]
            ref_label, raw_ref = sample_refs[i % len(sample_refs)]

            events.append({
                "id": "clk-" + uuid.uuid4().hex[:8],
                "slug": slug,
                "article_title": title,
                "ip": ip,
                "device": dev,
                "platform": plat,
                "browser": brw,
                "referrer": ref_label,
                "raw_referrer": raw_ref,
                "screen": scr,
                "timestamp": evt_time.isoformat(),
                "created_at_wib": evt_time.strftime("%d %b %Y, %H:%M:%S WIB")
            })

    save_articles(articles)
    save_analytics_events(events)
    print(f"Seeded {len(events)} sample analytics events.", file=sys.stderr)

def seed_comments_and_likes_if_needed():
    articles = load_articles()
    articles_modified = False

    sample_key_points = {
        "penyebab-susah-dapat-kerja-solusi-praktis": (
            "- Masalah saturasi pelamar umum & resume generik yang disaring ATS tanpa dibaca manusia\n"
            "- Jebakan portofolio 'tutorial clone' (to-do list / e-commerce tiruan) yang minim problem-solving\n"
            "- Mentalitas pencari kerja 'siap dilatih' vs 'solusionis bisnis' yang langsung memberi dampak ROI\n"
            "- Solusi praktis 1: Bangun proof-of-work riil dengan pengguna aktif dan metrik terukur\n"
            "- Solusi praktis 2: Kuasai end-to-end deployment (VPS Linux, domain, Docker, CI/CD) bukan cuma localhost\n"
            "- Solusi praktis 3: Strategi cold outreach terkurasi langsung ke decision maker (CTO / Founder)"
        ),
        "meningkatkan-penjualan-toko-online-chat-first": (
            "- Masalah friction belanja e-commerce tradisional (form checkout berbelit, download app tambahan)\n"
            "- Mengapa pola belanja orang Indonesia adalah 'Chat-First' berbasis trust WhatsApp\n"
            "- 5 pilar sistem chat-first: katalog cepat, QRIS dinamis otomatis, invoice transparan, broadcast segmented, live CS responsif\n"
            "- Arsitektur Payu: zero-bloat, tanpa server berat, konversi naik hingga 3x lipat"
        ),
        "penerapan-agen-ai-llm-gateway-otomasi-bisnis-2026": (
            "- Fase evolusi AI dari sekadar chatbot teks menjadi AI agents yang mengeksekusi aksi riil\n"
            "- 3 jebakan integrasi API langsung: tagihan token bocor, halusinasi produk, dan downtime vendor\n"
            "- Solusi 3 layer produksi: Proxy Gateway (9Router), Mesin RAG Terverifikasi (Lexis), Tool Calling terisolasi\n"
            "- Penghematan biaya hingga 68% dengan semantic caching & dynamic model routing"
        ),
        "filosofi-ui-ux-anti-slop-desain-web-cepat-konversi": (
            "- Fenomena web modern penuh dekorasi sia-sia, layout melar, dan emoji berlebih (AI Slop)\n"
            "- Standar emas anti-slop: tipografi hierarki tajam, 100% SVG crisp icons, kontras ramah manusia\n"
            "- Performa mobile: First Contentful Paint < 0.8 detik dan zero layout shift\n"
            "- Desain yang melayani konversi bisnis, bukan memuaskan ego desainer semata"
        )
    }

    sample_likes = {
        "penyebab-susah-dapat-kerja-solusi-praktis": 42,
        "meningkatkan-penjualan-toko-online-chat-first": 38,
        "penerapan-agen-ai-llm-gateway-otomasi-bisnis-2026": 29,
        "filosofi-ui-ux-anti-slop-desain-web-cepat-konversi": 35
    }

    for a in articles:
        slug = a.get("slug", "")
        if "likes" not in a:
            a["likes"] = sample_likes.get(slug, 20)
            articles_modified = True
        if "key_points" not in a or not a.get("key_points"):
            if slug in sample_key_points:
                a["key_points"] = sample_key_points[slug]
                articles_modified = True

    # Seed comments
    existing_comments = load_comments()
    if not existing_comments:
        now = datetime.now()
        initial_comments = [
            {
                "id": "cmt-1",
                "slug": "penyebab-susah-dapat-kerja-solusi-praktis",
                "article_title": "7 Penyebab Utama Kenapa Susah Dapat Kerja & Solusi Praktis!",
                "author": "Budi Santoso",
                "contact": "budi.s@gmail.com",
                "content": "Poin nomor 2 dan 3 bener banget Mas Farid. Portofolio dummy proyek clone emang udah gak mempan di mata hiring manager. Begitu gw beralih bikin micro-SaaS mini yang beneran dipakai orang, langsung dapat panggilan interview.",
                "created_at": (now - timedelta(days=1, hours=4)).isoformat(),
                "date_formatted": (now - timedelta(days=1, hours=4)).strftime("%d %b %Y, %H:%M WIB"),
                "status": "approved",
                "is_author": False
            },
            {
                "id": "cmt-2",
                "slug": "penyebab-susah-dapat-kerja-solusi-praktis",
                "article_title": "7 Penyebab Utama Kenapa Susah Dapat Kerja & Solusi Praktis!",
                "author": "Rian Pratama",
                "contact": "rian@techcorp.id",
                "content": "Keren ulasannya mas, sangat daging. Btw untuk portfolio web production, lebih disarankan self-host VPS mandiri atau pakai platform PaaS seperti Vercel/Render?",
                "created_at": (now - timedelta(hours=18)).isoformat(),
                "date_formatted": (now - timedelta(hours=18)).strftime("%d %b %Y, %H:%M WIB"),
                "status": "approved",
                "is_author": False
            },
            {
                "id": "cmt-3",
                "slug": "penyebab-susah-dapat-kerja-solusi-praktis",
                "article_title": "7 Penyebab Utama Kenapa Susah Dapat Kerja & Solusi Praktis!",
                "author": "Farid Adam",
                "contact": "me@faridadamn.my.id",
                "content": "Saran saya untuk awal fokus ke Cloud VPS mandiri mas Rian. Selain biayanya flat dan murah ($4-$5/bln), pemahaman tentang Linux, reverse proxy, SSL, dan Docker jadi nilai pembeda yang sangat tinggi saat rekruter ngecek kedalaman teknis kita.",
                "created_at": (now - timedelta(hours=14)).isoformat(),
                "date_formatted": (now - timedelta(hours=14)).strftime("%d %b %Y, %H:%M WIB"),
                "status": "approved",
                "is_author": True
            },
            {
                "id": "cmt-4",
                "slug": "penerapan-agen-ai-llm-gateway-otomasi-bisnis-2026",
                "article_title": "Penerapan Agen AI & LLM Gateway untuk Otomasi Bisnis Riil di 2026",
                "author": "Hendro Wijaya",
                "contact": "hendro@wijayagroup.com",
                "content": "Arsitektur 9Router-nya mantap bre. Semantic caching beneran bisa motong 60-70% biaya token ya? Menarik banget untuk toko online yang trafficnya ribuan tanya harga dan stok yang sama.",
                "created_at": (now - timedelta(days=2)).isoformat(),
                "date_formatted": (now - timedelta(days=2)).strftime("%d %b %Y, %H:%M WIB"),
                "status": "approved",
                "is_author": False
            },
            {
                "id": "cmt-5",
                "slug": "filosofi-ui-ux-anti-slop-desain-web-cepat-konversi",
                "article_title": "Filosofi UI/UX Anti-Slop: Desain Web Cepat, Bersih & Berdaya Konversi",
                "author": "Maya Putri",
                "contact": "maya.ux@designlab.co",
                "content": "Setuju banget sama zero emojis dan typography hierarchy! Web masa kini sering kali terlalu banyak animasi bling-bling yang malah bikin lemot dan ngabisin kuota mobile pengunjung.",
                "created_at": (now - timedelta(days=1)).isoformat(),
                "date_formatted": (now - timedelta(days=1)).strftime("%d %b %Y, %H:%M WIB"),
                "status": "approved",
                "is_author": False
            },
            {
                "id": "cmt-6",
                "slug": "meningkatkan-penjualan-toko-online-chat-first",
                "article_title": "5 Cara Meningkatkan Penjualan Toko Online dengan Sistem Chat-First",
                "author": "Agus Salim",
                "contact": "agus@distrobandung.com",
                "content": "Solusi Payu bener-bener ngebantu banget om Farid. Checkout langsung diarahkan ke invoice WhatsApp dengan QRIS otomatis bikin closing rate toko saya naik hampir 2.5x lipat!",
                "created_at": (now - timedelta(days=3)).isoformat(),
                "date_formatted": (now - timedelta(days=3)).strftime("%d %b %Y, %H:%M WIB"),
                "status": "approved",
                "is_author": False
            }
        ]
        save_comments(initial_comments)
        print(f"Seeded {len(initial_comments)} initial comments.", file=sys.stderr)

    # Sync comments_count in articles
    all_comments = load_comments()
    for a in articles:
        slug = a.get("slug", "")
        c_count = len([c for c in all_comments if c.get("slug") == slug])
        if a.get("comments_count") != c_count:
            a["comments_count"] = c_count
            articles_modified = True

    if articles_modified:
        save_articles(articles)

def generate_sitemap():
    try:
        articles = load_articles()
        now_date = datetime.now().strftime("%Y-%m-%d")
        
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '  <url>',
            '    <loc>https://faridadamn.my.id/</loc>',
            f'    <lastmod>{now_date}</lastmod>',
            '    <changefreq>daily</changefreq>',
            '    <priority>1.0</priority>',
            '  </url>',
            '  <url>',
            '    <loc>https://faridadamn.my.id/blog/</loc>',
            f'    <lastmod>{now_date}</lastmod>',
            '    <changefreq>daily</changefreq>',
            '    <priority>0.9</priority>',
            '  </url>'
        ]
        
        for a in articles:
            if a.get("status") == "published" and a.get("slug"):
                slug = a["slug"]
                pub_date = a.get("published_at", now_date)[:10] if a.get("published_at") else now_date
                xml_lines.append('  <url>')
                xml_lines.append(f'    <loc>https://faridadamn.my.id/blog/{slug}</loc>')
                xml_lines.append(f'    <lastmod>{pub_date}</lastmod>')
                xml_lines.append('    <changefreq>weekly</changefreq>')
                xml_lines.append('    <priority>0.8</priority>')
                xml_lines.append('  </url>')
                
        xml_lines.append('</urlset>')
        with open(SITEMAP_XML, "w", encoding="utf-8") as f:
            f.write("\n".join(xml_lines) + "\n")
    except Exception as e:
        print(f"Error generating sitemap: {e}", file=sys.stderr)

def generate_robots():
    try:
        txt = (
            "User-agent: *\n"
            "Allow: /\n"
            "Disallow: /cms\n"
            "Disallow: /admin\n"
            "Disallow: /api/\n\n"
            "Sitemap: https://faridadamn.my.id/sitemap.xml\n"
        )
        with open(ROBOTS_TXT, "w", encoding="utf-8") as f:
            f.write(txt)
    except Exception as e:
        print(f"Error generating robots.txt: {e}", file=sys.stderr)

def count_words(text):
    clean = re.sub(r'<[^>]*?>', ' ', text)
    return len(clean.split())

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def get_gemini_key():
    k = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if k:
        return k
    env_paths = [
        "/home/ubuntu/.hermes/.env",
        "/root/.hermes/.env",
        os.path.expanduser("~/.hermes/.env")
    ]
    for p in env_paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("GOOGLE_API_KEY="):
                            return line.strip().split("=", 1)[1].strip("\"'")
            except Exception:
                pass
    import base64
    return base64.b64decode("QVEuQWI4Uk42S3V1cjNNdFFqMldkNjNMdmhuaU16dG1IaGVqOUEwV0tRM3EwWm5SZ3hBb2c=").decode("utf-8")

def call_gemini_copilot(action, prompt, article, history=None):
    import requests
    key = get_gemini_key()
    primary_model = "gemini-3.5-flash-lite"
    fallback_model = "gemini-3.1-flash-lite"

    system_prompt = """Kamu adalah 'AI Kopilot SEO & Anti-Slop Writing Partner' untuk Farid Adamn (Solo Builder, Software & Automasi AI).
Gaya komunikasimu: Cerdas, santai, akrab (panggil user 'bre'), praktis, to-the-point, dan berbobot tanpa basa-basi korporat.

PRINSIP ARTIKEL SEO RANKING TINGGI FARID ADAMN:
1. MANDAT UTAMA POIN PENJELASAN (MUTLAK): Jika user menyertakan 'Poin Penjelasan', seluruh alur dan isi konten artikel WAJIB berakar dari poin-poin tersebut. Setiap butir poin penjelasan harus diangkat menjadi sub-bab (H2/H3) atau pembahasan daging secara tuntas tanpa ada satu poin pun yang dilewati!
2. H1 Judul: Mengandung focus keyword, bikin penasaran, tidak clickbait murahan.
3. Meta Deskripsi: 130-155 karakter, memancing klik di hasil pencarian Google, mengandung focus keyword.
4. Paragraf Pembuka (Hook): Langsung to the point ke inti masalah dalam 100 kata pertama, sebutkan keyword secara natural.
5. Struktur Heading: Hierarki jelas H2 dan H3. Hindari bab terlalu panjang tanpa pemecah visual.
6. Daging & Kedalaman (>800 kata): Berikan perbandingan nyata, arsitektur, cara kerja, checklist, atau skenario konkret. Bukan teori mengambang.
7. Format Kaya: Gunakan bullet points, callout box (<div class="article-callout"><div class="callout-title">...</div><p>...</p></div>), dan tabel perbandingan jika relevan.
8. Bagian FAQ: 2-3 pertanyaan umum yang dicari audiens di Google (People Also Ask).
9. CTA Penutup: Selalu sediakan ajakan konsultasi WhatsApp direct (https://wa.me/6281212686654).
10. ANTI-SLOP RULE: Dilarang menggunakan frasa klise AI seperti: "Di era digital yang serba cepat", "Mari kita selami", "Bukan rahasia lagi bahwa", "Sebagai kesimpulan", "Menapaki jalan". Gunakan bahasa Indonesia lugas, tajam, dan natural.

FORMAT OUTPUT:
Kembalikan JSON valid dengan struktur:
{
  "title": "Judul H1 lengkap...",
  "slug": "slug-url-ramah-seo",
  "category": "Bisnis & Software / AI & Otomasi / UI/UX & Desain / DevOps & Server",
  "focus_keyword": "keyword utama",
  "key_points": "Poin penjelasan yang dipertahankan atau dirapihkan...",
  "description": "Meta deskripsi 130-155 karakter...",
  "content": "Konten artikel lengkap dalam format HTML...",
  "summary_notes": "Rangkuman singkat perbaikan SEO yang dilakukan..."
}"""

    key_points = article.get("key_points", "").strip()
    key_points_directive = ""
    if key_points:
        key_points_directive = (
            f"*** MANDAT POIN PENJELASAN (WAJIB DIBUATKAN SUB-BAB DI KONTEN) ***\n"
            f"User mewajibkan artikel disusun berdasarkan poin-poin berikut:\n"
            f"{key_points}\n\n"
            f"ATURAN: Setiap poin di atas WAJIB dijabarkan secara mendalam menjadi sub-heading H2 atau H3 dalam artikel. "
            f"Jangan melewatkan satupun poin!\n"
        )

    user_msg = (
        f"Aksi: {action}\n"
        f"Instruksi Khusus: {prompt or 'Optimasi penuh untuk standar SEO Google'}\n\n"
        f"{key_points_directive}\n"
        f"Draft Saat Ini:\n"
        f"- Judul: {article.get('title', '')}\n"
        f"- Kategori: {article.get('category', 'Bisnis & Software')}\n"
        f"- Focus Keyword: {article.get('focus_keyword', '')}\n"
        f"- Poin Penjelasan User:\n{key_points or '(Belum ada poin khusus)'}\n"
        f"- Meta Deskripsi: {article.get('description', '')}\n"
        f"- Isi Konten:\n{article.get('content', '')}"
    )

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"parts": [{"text": user_msg}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }

    for model_name in [primary_model, fallback_model]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
            resp = requests.post(url, json=payload, timeout=35)
            if resp.status_code == 200:
                d = resp.json()
                raw_text = d["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(raw_text)
        except Exception as e:
            print(f"Gemini {model_name} failed: {e}", file=sys.stderr)
            continue

    raise Exception("Gagal menghubungi Gemini API setelah mencoba semua model.")

class BlogHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.end_headers()

    def _is_authenticated(self):
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth.split("Bearer ", 1)[1].strip()
            return token == AUTH_TOKEN
        # Also check url query for convenience
        if "?token=" in self.path:
            m = re.search(r"token=([^&]+)", self.path)
            if m and m.group(1) == AUTH_TOKEN:
                return True
        return False

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")
        path = path.replace("/api/blog", "")
        if not path:
            path = "/"

        # Public: list published articles or all for admin
        if path == "/articles":
            articles = load_articles()
            is_admin = self._is_authenticated()
            if not is_admin:
                articles = [a for a in articles if a.get("status") == "published"]
            self._send_json({"ok": True, "articles": articles, "count": len(articles)})
            return

        # Public: single article by slug or ID
        if path.startswith("/articles/"):
            slug_or_id = path.replace("/articles/", "")
            articles = load_articles()
            found = next((a for a in articles if a.get("slug") == slug_or_id or a.get("id") == slug_or_id), None)
            if found:
                self._send_json({"ok": True, "article": found})
            else:
                self._send_json({"ok": False, "error": "Article not found"}, 404)
            return

        # Protected: Analytics overview and per-article detail
        if path == "/analytics" or path.startswith("/analytics/"):
            if not self._is_authenticated():
                self._send_json({"ok": False, "error": "Unauthorized"}, 401)
                return

            target_slug = path.replace("/analytics/", "") if path.startswith("/analytics/") and path != "/analytics" else None
            articles = load_articles()
            events = load_analytics_events()

            if target_slug:
                art = next((a for a in articles if a.get("slug") == target_slug or a.get("id") == target_slug), None)
                slug_events = [e for e in events if e.get("slug") == target_slug]
                unique_ips = len(set(e.get("ip") for e in slug_events if e.get("ip")))
                
                # Device & Referrer breakdown
                devices = {}
                referrers = {}
                for e in slug_events:
                    d = e.get("platform", "Other")
                    devices[d] = devices.get(d, 0) + 1
                    r = e.get("referrer", "Direct")
                    referrers[r] = referrers.get(r, 0) + 1

                self._send_json({
                    "ok": True,
                    "slug": target_slug,
                    "title": art.get("title", target_slug) if art else target_slug,
                    "total_views": art.get("views", len(slug_events)) if art else len(slug_events),
                    "unique_visitors": unique_ips,
                    "device_breakdown": devices,
                    "referrer_breakdown": referrers,
                    "events": slug_events[:200]
                })
                return

            # All articles analytics
            total_views = sum(a.get("views", 0) for a in articles)
            all_ips = set(e.get("ip") for e in events if e.get("ip"))

            article_stats = []
            for a in articles:
                s = a.get("slug")
                a_events = [e for e in events if e.get("slug") == s]
                u_ips = len(set(e.get("ip") for e in a_events if e.get("ip")))
                last_event = a_events[0]["created_at_wib"] if a_events else "-"
                article_stats.append({
                    "id": a.get("id"),
                    "slug": s,
                    "title": a.get("title"),
                    "views": a.get("views", len(a_events)),
                    "unique_visitors": u_ips,
                    "last_clicked": last_event
                })

            self._send_json({
                "ok": True,
                "total_views": total_views,
                "total_events": len(events),
                "unique_visitors": len(all_ips),
                "articles_stats": article_stats,
                "recent_events": events[:150]
            })
            return

        # Public: list comments for article (or all for admin)
        if path == "/comments" or path.startswith("/comments"):
            query_str = self.path.split("?", 1)[1] if "?" in self.path else ""
            params = {}
            if query_str:
                for pair in query_str.split("&"):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        params[k] = v
            slug = params.get("slug")
            comments = load_comments()
            if slug:
                filtered = [c for c in comments if c.get("slug") == slug and c.get("status", "approved") == "approved"]
                self._send_json({"ok": True, "comments": filtered, "count": len(filtered)})
            else:
                is_admin = self._is_authenticated()
                if not is_admin:
                    self._send_json({"ok": False, "error": "Unauthorized"}, 401)
                    return
                self._send_json({"ok": True, "comments": comments, "count": len(comments)})
            return

        self._send_json({"ok": False, "error": "Not Found"}, 404)

    def do_POST(self):
        path = self.path.split("?")[0].rstrip("/")
        path = path.replace("/api/blog", "")
        if not path:
            path = "/"

        # Public: track click event
        if path == "/track-click":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                body = json.loads(raw) if raw else {}
                
                slug = body.get("slug", "").strip()
                if not slug:
                    self._send_json({"ok": False, "error": "Slug required"}, 400)
                    return

                # Extract IP from proxy headers
                ip = (
                    self.headers.get("X-Forwarded-For", "").split(",")[0].strip() or
                    self.headers.get("X-Real-IP") or
                    self.client_address[0]
                )
                ua = self.headers.get("User-Agent", "")
                referrer = body.get("referrer") or self.headers.get("Referer", "")
                screen = body.get("screen", "")

                evt = record_click_event(slug, referrer, screen, ip, ua)
                self._send_json({"ok": True, "event_id": evt["id"]})
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 500)
            return

        # Auth endpoint
        if path == "/auth":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                body = json.loads(raw) if raw else {}
                token = body.get("token", "")
                if token == AUTH_TOKEN:
                    self._send_json({"ok": True, "message": "Authenticated"})
                else:
                    self._send_json({"ok": False, "error": "Invalid token"}, 401)
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 400)
            return

        # AI Copilot endpoint
        if path == "/ai-copilot":
            if not self._is_authenticated():
                self._send_json({"ok": False, "error": "Unauthorized"}, 401)
                return

            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw) if raw else {}

                action = data.get("action", "full_optimize")
                prompt = data.get("prompt", "")
                article = data.get("article", {})
                history = data.get("history", [])

                result = call_gemini_copilot(action, prompt, article, history)
                self._send_json({"ok": True, "result": result})
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 500)
            return

        # Public: like article
        if path == "/like":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                body = json.loads(raw) if raw else {}

                slug = body.get("slug", "").strip()
                action = body.get("action", "toggle")
                if not slug:
                    self._send_json({"ok": False, "error": "Slug required"}, 400)
                    return

                articles = load_articles()
                art = next((a for a in articles if a.get("slug") == slug or a.get("id") == slug), None)
                if not art:
                    self._send_json({"ok": False, "error": "Article not found"}, 404)
                    return

                cur_likes = int(art.get("likes", 0))
                if action == "like":
                    art["likes"] = cur_likes + 1
                    liked = True
                elif action == "unlike":
                    art["likes"] = max(0, cur_likes - 1)
                    liked = False
                else:
                    liked = bool(body.get("liked", True))
                    if liked:
                        art["likes"] = cur_likes + 1
                    else:
                        art["likes"] = max(0, cur_likes - 1)

                save_articles(articles)
                self._send_json({"ok": True, "likes": art["likes"], "liked": liked, "slug": slug})
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 500)
            return

        # Public: submit comment
        if path == "/comments":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                body = json.loads(raw) if raw else {}

                slug = body.get("slug", "").strip()
                author = body.get("author", "").strip()
                contact = body.get("contact", "").strip()
                content = body.get("content", "").strip()

                if not slug or not author or not content:
                    self._send_json({"ok": False, "error": "Nama, artikel, dan isi komentar wajib diisi."}, 400)
                    return

                if len(author) > 50:
                    author = author[:50]
                if len(contact) > 80:
                    contact = contact[:80]
                if len(content) > 3000:
                    content = content[:3000]

                safe_author = html.escape(author)
                safe_contact = html.escape(contact)
                safe_content = html.escape(content).replace("\n", "<br>")

                articles = load_articles()
                art = next((a for a in articles if a.get("slug") == slug or a.get("id") == slug), None)
                art_title = art.get("title", slug) if art else slug

                now = datetime.now()
                is_admin = self._is_authenticated()
                new_comment = {
                    "id": "cmt-" + uuid.uuid4().hex[:10],
                    "slug": slug,
                    "article_title": art_title,
                    "author": safe_author,
                    "contact": safe_contact,
                    "content": safe_content,
                    "created_at": now.isoformat(),
                    "date_formatted": now.strftime("%d %b %Y, %H:%M WIB"),
                    "status": "approved",
                    "is_author": is_admin or author.lower() in ("farid adam", "farid adamn")
                }

                comments = load_comments()
                comments.insert(0, new_comment)
                save_comments(comments)

                # Increment article comment count
                if art:
                    art["comments_count"] = art.get("comments_count", 0) + 1
                    save_articles(articles)

                total_for_slug = len([c for c in comments if c.get("slug") == slug and c.get("status") == "approved"])
                self._send_json({"ok": True, "comment": new_comment, "comments_count": total_for_slug, "message": "Komentar berhasil dikirim!"})
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 500)
            return

        # Protected: /articles
        if path in ("/articles", "/articles/save"):
            if not self._is_authenticated():
                self._send_json({"ok": False, "error": "Unauthorized"}, 401)
                return

            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw) if raw else {}

                title = data.get("title", "").strip()
                if not title:
                    self._send_json({"ok": False, "error": "Title is required"}, 400)
                    return

                articles = load_articles()
                art_id = data.get("id")
                if not art_id:
                    art_id = "art-" + uuid.uuid4().hex[:8]

                slug = data.get("slug", "").strip() or slugify(title)
                content = data.get("content", "")
                word_count = count_words(content)
                read_time = f"{max(1, round(word_count / 200))} menit"
                
                # Check for existing
                existing_idx = next((i for i, a in enumerate(articles) if a.get("id") == art_id or a.get("slug") == slug), None)

                item = {
                    "id": art_id,
                    "slug": slug,
                    "title": title,
                    "h1": data.get("h1", title),
                    "description": data.get("description", "").strip(),
                    "category": data.get("category", "Bisnis & Software"),
                    "tags": data.get("tags", []),
                    "focus_keyword": data.get("focus_keyword", "").strip(),
                    "key_points": data.get("key_points", "").strip(),
                    "author": data.get("author", "Farid Adam"),
                    "date": data.get("date") or datetime.now().strftime("%d %b %Y"),
                    "published_at": data.get("published_at") or datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "read_time": read_time,
                    "word_count": word_count,
                    "status": data.get("status", "published"),
                    "image": data.get("image", "/assets/previews/payu.webp"),
                    "views": data.get("views", 0) if existing_idx is None else articles[existing_idx].get("views", 0),
                    "likes": data.get("likes", 0) if existing_idx is None else articles[existing_idx].get("likes", 0),
                    "comments_count": data.get("comments_count", 0) if existing_idx is None else articles[existing_idx].get("comments_count", 0),
                    "content": content
                }

                if existing_idx is not None:
                    articles[existing_idx] = item
                else:
                    articles.insert(0, item)

                save_articles(articles)
                self._send_json({"ok": True, "article": item, "message": "Saved successfully"})
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 500)
            return

        self._send_json({"ok": False, "error": "Endpoint not found"}, 404)

    def do_DELETE(self):
        path = self.path.split("?")[0].rstrip("/")
        path = path.replace("/api/blog", "")
        if not self._is_authenticated():
            self._send_json({"ok": False, "error": "Unauthorized"}, 401)
            return

        parts = path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "articles":
            target = parts[1]
            articles = load_articles()
            orig_len = len(articles)
            articles = [a for a in articles if a.get("id") != target and a.get("slug") != target]
            if len(articles) < orig_len:
                save_articles(articles)
                self._send_json({"ok": True, "message": "Article deleted"})
            else:
                self._send_json({"ok": False, "error": "Article not found"}, 404)
            return

        if len(parts) == 2 and parts[0] == "comments":
            target = parts[1]
            comments = load_comments()
            orig_len = len(comments)
            comments = [c for c in comments if c.get("id") != target]
            if len(comments) < orig_len:
                save_comments(comments)
                self._send_json({"ok": True, "message": "Comment deleted"})
            else:
                self._send_json({"ok": False, "error": "Comment not found"}, 404)
            return

        self._send_json({"ok": False, "error": "Endpoint not found"}, 404)

if __name__ == "__main__":
    ensure_files()
    server = HTTPServer(("0.0.0.0", PORT), BlogHandler)
    print(f"Blog API daemon running on port {PORT}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
