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
                pub_date = a.get("published_at", now_date)[:10] if a.get("published_at") else now_date
                slug = a.get("slug")
                xml_lines.extend([
                    '  <url>',
                    f'    <loc>https://faridadamn.my.id/blog/{slug}</loc>',
                    f'    <lastmod>{pub_date}</lastmod>',
                    '    <changefreq>weekly</changefreq>',
                    '    <priority>0.8</priority>',
                    '  </url>'
                ])
                
        xml_lines.append('</urlset>')
        with open(SITEMAP_XML, "w", encoding="utf-8") as f:
            f.write("\n".join(xml_lines) + "\n")
        print(f"Generated sitemap at {SITEMAP_XML}")
    except Exception as e:
        print(f"Error generating sitemap: {e}", file=sys.stderr)

def generate_robots():
    try:
        content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /cms

Sitemap: https://faridadamn.my.id/sitemap.xml
"""
        with open(ROBOTS_TXT, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated robots.txt at {ROBOTS_TXT}")
    except Exception as e:
        print(f"Error generating robots.txt: {e}", file=sys.stderr)

def strip_tags(text):
    return re.sub(r'<[^>]*?>', ' ', text)

def count_words(html_text):
    clean = strip_tags(html_text)
    words = [w for w in clean.split() if w.strip()]
    return len(words)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text

class BlogHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
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
            token = auth[7:].strip()
            return token == AUTH_TOKEN
        # Also check custom header or query param
        if self.headers.get("X-Admin-Token") == AUTH_TOKEN:
            return True
        return False

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")
        # Normalize path if behind proxy
        path = path.replace("/api/blog", "")
        if not path:
            path = "/"

        articles = load_articles()

        # Route: /articles or /
        if path in ("", "/", "/articles"):
            is_auth = self._is_authenticated()
            if is_auth:
                self._send_json({"ok": True, "articles": articles})
            else:
                published = [a for a in articles if a.get("status") == "published"]
                self._send_json({"ok": True, "articles": published})
            return

        # Route: /articles/<slug>
        parts = path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "articles":
            slug = parts[1]
            found = next((a for a in articles if a.get("slug") == slug or a.get("id") == slug), None)
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
