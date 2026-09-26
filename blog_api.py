#!/usr/bin/env python3
import json
import os
import re
import sys
import shutil
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8656
AUTH_TOKEN = "cWST8dH8B45Yme38m4Acsg"

# Adjust paths based on environment
BASE_DIR = "/var/www/faridadamn-landing" if os.path.exists("/var/www/faridadamn-landing") else "/root/faridadamn"
DATA_DIR = os.path.join(BASE_DIR, "data")
ARTICLES_JSON = os.path.join(DATA_DIR, "articles.json")
SITEMAP_XML = os.path.join(BASE_DIR, "sitemap.xml")
ROBOTS_TXT = os.path.join(BASE_DIR, "robots.txt")

def ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(ARTICLES_JSON):
        with open(ARTICLES_JSON, "w", encoding="utf-8") as f:
            json.dump([], f)
    generate_sitemap()
    generate_robots()

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
        print("Sitemap successfully regenerated.", file=sys.stderr)
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
    primary_model = "gemini-2.5-flash"
    fallback_model = "gemini-2.0-flash"

    system_prompt = """Kamu adalah 'AI Kopilot SEO & Anti-Slop Writing Partner' untuk Farid Adamn (Solo Builder, Software & Automasi AI).
Gaya komunikasimu: Cerdas, santai, akrab (panggil user 'bre'), praktis, to-the-point, dan berbobot tanpa basa-basi korporat.

PRINSIP ARTIKEL SEO RANKING TINGGI FARID ADAMN:
1. H1 Judul: Mengandung focus keyword, bikin penasaran, tidak clickbait murahan.
2. Meta Deskripsi: 130-155 karakter, memancing klik di hasil pencarian Google, mengandung focus keyword.
3. Paragraf Pembuka (Hook): Langsung to the point ke inti masalah dalam 100 kata pertama, sebutkan keyword secara natural.
4. Struktur Heading: Hierarki jelas H2 dan H3. Hindari bab terlalu panjang tanpa pemecah visual.
5. Daging & Kedalaman (>800 kata): Berikan perbandingan nyata, arsitektur, cara kerja, checklist, atau skenario konkret. Bukan teori mengambang.
6. Format Kaya: Gunakan bullet points, callout box (<div class="article-callout"><div class="callout-title">...</div><p>...</p></div>), dan tabel perbandingan jika relevan.
7. Bagian FAQ: 2-3 pertanyaan umum yang dicari audiens di Google (People Also Ask).
8. CTA Penutup: Selalu sediakan ajakan konsultasi WhatsApp direct (https://wa.me/6281212686654).
9. ANTI-SLOP RULE: Dilarang menggunakan frasa klise AI seperti: "Di era digital yang serba cepat", "Mari kita selami", "Bukan rahasia lagi bahwa", "Sebagai kesimpulan", "Menapaki jalan". Gunakan bahasa Indonesia lugas, tajam, dan natural.

FORMAT OUTPUT:
Kembalikan JSON valid dengan struktur:
{
  "title": "Judul H1 lengkap...",
  "slug": "slug-url-ramah-seo",
  "category": "Bisnis & Software / AI & Otomasi / UI/UX & Desain / DevOps & Server",
  "focus_keyword": "keyword utama",
  "description": "Meta deskripsi 130-155 karakter...",
  "content": "Konten artikel lengkap dalam format HTML...",
  "summary_notes": "Rangkuman singkat perbaikan SEO yang dilakukan..."
}"""

    user_msg = (
        f"Aksi: {action}\n"
        f"Instruksi Khusus: {prompt or 'Optimasi penuh untuk standar SEO Google'}\n\n"
        f"Draft Saat Ini:\n"
        f"- Judul: {article.get('title', '')}\n"
        f"- Kategori: {article.get('category', 'Bisnis & Software')}\n"
        f"- Focus Keyword: {article.get('focus_keyword', '')}\n"
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

        self._send_json({"ok": False, "error": "Not Found"}, 404)

    def do_POST(self):
        path = self.path.split("?")[0].rstrip("/")
        path = path.replace("/api/blog", "")
        if not path:
            path = "/"

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
                    import uuid
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
                    "author": data.get("author", "Farid Adam"),
                    "date": data.get("date") or datetime.now().strftime("%d %b %Y"),
                    "published_at": data.get("published_at") or datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "read_time": read_time,
                    "word_count": word_count,
                    "status": data.get("status", "published"),
                    "image": data.get("image", "/assets/previews/payu.webp"),
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

        self._send_json({"ok": False, "error": "Endpoint not found"}, 404)

if __name__ == "__main__":
    ensure_files()
    server = HTTPServer(("0.0.0.0", PORT), BlogHandler)
    print(f"Blog API daemon running on port {PORT}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
