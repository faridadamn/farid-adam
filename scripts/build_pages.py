#!/usr/bin/env python3
"""
Clean Builder untuk blog.html dan artikel.html
Menghasilkan katalog artikel dan dynamic reader dengan visual 1:1 XL SATU
"""

import json
import os

def get_catalog_data():
    with open('/root/exelsatu/data/articles.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)

    catalog = []
    for a in articles:
        catalog.append({
            'slug': a['slug'],
            'title': a['title'],
            'description': a['description'],
            'image': a['image'],
            'date': a['date'],
            'category': a['category'],
            'read_time': a['read_time']
        })
    return catalog, articles

def build_blog():
    catalog, articles = get_catalog_data()
    catalog_json = json.dumps(catalog, ensure_ascii=False)

    html = r"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Berita & Artikel Seputar Internet Rumah, WiFi & Tips Digital — XL SATU Fiber</title>
  <meta name="description" content="Kumpulan artikel edukasi dan tips trik internet rumah: solusi WiFi lemot, panduan live streaming & cloud gaming, rekomendasi router, serta info promo XL SATU Fiber." />
  <link rel="canonical" href="https://exelsatu.my.id/blog" />
  <meta property="og:title" content="Berita & Artikel XL SATU Fiber" />
  <meta property="og:description" content="Tips trik internet kencang, panduan gaming & streaming, dan solusi jaringan rumah bebas lag." />
  <meta property="og:url" content="https://exelsatu.my.id/blog" />
  <meta property="og:type" content="website" />

  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon.png" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

  <style>
    @font-face {
      font-family: 'XLSmart';
      src: url('/fonts/xlsmart-regular.otf') format('opentype');
      font-weight: 400;
      font-style: normal;
      font-display: swap;
    }
    @font-face {
      font-family: 'XLSmart';
      src: url('/fonts/xlsmart-medium.otf') format('opentype');
      font-weight: 500;
      font-style: normal;
      font-display: swap;
    }
    @font-face {
      font-family: 'XLSmart';
      src: url('/fonts/xlsmart-bold.otf') format('opentype');
      font-weight: 700;
      font-style: normal;
      font-display: swap;
    }

    :root {
      --primary: #18448A;
      --secondary: #05A986;
      --soft-xl-home: #ECF9FF;
      --sky-blue: #1D90C9;
      --chip-blue: #0284C7;
      --accent: #E11D48;
      --bg-main: #FFFFFF;
      --text-dark: #131313;
      --text-muted: #64748B;
      --border-color: #E2E8F0;
      --card-bg: #FFFFFF;
      --font-family: 'XLSmart', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --radius: 16px;
      --container: 1180px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: var(--font-family);
    }

    body {
      background-color: #F8FAFC;
      color: var(--text-dark);
      line-height: 1.5;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
      padding-top: 102px;
    }

    a {
      text-decoration: none;
      color: inherit;
    }

    .container {
      max-width: var(--container);
      margin: 0 auto;
      padding: 0 20px;
      width: 100%;
    }

    .icon {
      display: inline-block;
      width: 20px;
      height: 20px;
      stroke-width: 2;
      stroke: currentColor;
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
      vertical-align: middle;
      flex-shrink: 0;
    }

    /* Top Announcement Bar (Fixed) */
    .top-bar-sticky {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      width: 100%;
      height: 38px;
      z-index: 1000;
      background: var(--soft-xl-home);
      border-bottom: 1px solid #daeeff;
      padding: 0 16px;
      text-align: center;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-size: 13.5px;
      color: var(--primary);
      font-weight: 600;
    }
    .top-bar-link {
      color: var(--secondary);
      font-weight: 700;
      text-decoration: underline;
      cursor: pointer;
    }

    /* Navbar (Fixed) */
    .navbar {
      background: #ffffff;
      border-bottom: 1px solid var(--border-color);
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
      position: fixed;
      top: 38px;
      left: 0;
      right: 0;
      width: 100%;
      height: 64px;
      z-index: 999;
    }
    .nav-inner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 64px;
    }
    .brand-logo-img {
      height: 32px;
      width: auto;
      object-fit: contain;
      display: block;
    }
    .nav-links {
      display: flex;
      align-items: center;
      gap: 26px;
      font-size: 14.5px;
      font-weight: 600;
      color: var(--text-muted);
    }
    .nav-links a:hover {
      color: var(--primary);
    }
    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-weight: 700;
      border-radius: 999px;
      padding: 11px 22px;
      font-size: 14px;
      cursor: pointer;
      border: none;
      transition: all 0.2s ease;
      text-align: center;
      justify-content: center;
    }
    .btn-primary {
      background: var(--primary);
      color: #ffffff;
    }
    .btn-primary:hover {
      background: #0f2e62;
      box-shadow: 0 4px 14px rgba(24, 68, 138, 0.25);
    }
    .btn-secondary {
      background: var(--secondary);
      color: #ffffff;
    }
    .btn-secondary:hover {
      background: #048a6d;
      box-shadow: 0 4px 14px rgba(5, 169, 134, 0.25);
    }

    /* Hero Blog Header */
    .blog-hero {
      padding: 46px 0 32px;
      background: linear-gradient(180deg, var(--soft-xl-home) 0%, #F8FAFC 100%);
      text-align: center;
      border-bottom: 1px solid var(--border-color);
    }
    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      background: rgba(24, 68, 138, 0.08);
      color: var(--primary);
      padding: 5px 15px;
      border-radius: 999px;
      margin-bottom: 14px;
    }
    .hero-title {
      font-size: 34px;
      font-weight: 700;
      color: var(--primary);
      line-height: 1.25;
      margin-bottom: 12px;
    }
    .hero-subtitle {
      font-size: 15.5px;
      color: var(--text-muted);
      max-width: 660px;
      margin: 0 auto;
    }

    /* Controls Bar: Search & Filter Chips */
    .blog-controls {
      padding: 24px 0 16px;
      position: sticky;
      top: 102px;
      background: #F8FAFC;
      z-index: 90;
      border-bottom: 1px solid rgba(226, 232, 240, 0.7);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
    }
    .search-box-wrap {
      max-width: 580px;
      margin: 0 auto 18px;
      position: relative;
    }
    .search-input {
      width: 100%;
      height: 48px;
      padding: 10px 44px 10px 46px;
      border-radius: 999px;
      border: 1.5px solid var(--border-color);
      background: #ffffff;
      font-size: 15px;
      color: var(--text-dark);
      outline: none;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
      transition: all 0.2s ease;
    }
    .search-input:focus {
      border-color: var(--primary);
      box-shadow: 0 4px 18px rgba(24, 68, 138, 0.12);
    }
    .search-icon {
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      pointer-events: none;
    }
    .search-clear-btn {
      position: absolute;
      right: 14px;
      top: 50%;
      transform: translateY(-50%);
      background: #f1f5f9;
      border: none;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      display: none;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--text-muted);
    }
    .search-clear-btn:hover {
      background: #e2e8f0;
      color: var(--text-dark);
    }

    /* Category Filter Pills */
    .filter-pills {
      display: flex;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      gap: 10px;
    }
    .pill-btn {
      background: #ffffff;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      font-size: 13.5px;
      font-weight: 600;
      padding: 7px 18px;
      border-radius: 999px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .pill-btn:hover {
      border-color: var(--primary);
      color: var(--primary);
      background: var(--soft-xl-home);
    }
    .pill-btn.active {
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
      box-shadow: 0 4px 12px rgba(24, 68, 138, 0.2);
    }

    /* Results Counter */
    .results-meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin: 24px 0 16px;
      font-size: 13.5px;
      color: var(--text-muted);
      font-weight: 600;
    }

    /* Featured Article Card */
    .featured-card {
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: 20px;
      overflow: hidden;
      margin-bottom: 34px;
      box-shadow: 0 10px 30px rgba(24, 68, 138, 0.06);
      display: grid;
      grid-template-columns: 1.15fr 1fr;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      cursor: pointer;
    }
    .featured-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 14px 36px rgba(24, 68, 138, 0.12);
    }
    .featured-img-wrap {
      position: relative;
      width: 100%;
      height: 100%;
      min-height: 300px;
      background: #0f172a;
      overflow: hidden;
    }
    .featured-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
      display: block;
    }
    .featured-card:hover .featured-img {
      transform: scale(1.03);
    }
    .featured-body {
      padding: 34px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .featured-tag-row {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 14px;
    }
    .badge-category {
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      background: rgba(24, 68, 138, 0.1);
      color: var(--primary);
      padding: 3px 10px;
      border-radius: 6px;
    }
    .featured-title {
      font-size: 24px;
      font-weight: 700;
      color: var(--primary);
      line-height: 1.35;
      margin-bottom: 12px;
      transition: color 0.15s ease;
    }
    .featured-card:hover .featured-title {
      color: var(--secondary);
    }
    .featured-desc {
      font-size: 14.5px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 20px;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .featured-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 16px;
      border-top: 1px solid var(--border-color);
      font-size: 13px;
      color: var(--text-muted);
    }
    .read-btn-link {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--primary);
      font-weight: 700;
      font-size: 13.5px;
    }

    /* Articles Grid */
    .articles-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-bottom: 50px;
    }
    .article-card {
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
      display: flex;
      flex-direction: column;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      cursor: pointer;
    }
    .article-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 28px rgba(24, 68, 138, 0.09);
    }
    .card-thumb-wrap {
      position: relative;
      width: 100%;
      padding-top: 56.25%;
      background: #f1f5f9;
      overflow: hidden;
    }
    .card-thumb {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }
    .article-card:hover .card-thumb {
      transform: scale(1.05);
    }
    .card-body {
      padding: 20px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }
    .card-meta-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 10px;
      font-size: 11.5px;
    }
    .card-title {
      font-size: 16.5px;
      font-weight: 700;
      color: var(--text-dark);
      line-height: 1.4;
      margin-bottom: 10px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      transition: color 0.15s ease;
    }
    .article-card:hover .card-title {
      color: var(--primary);
    }
    .card-desc {
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.55;
      margin-bottom: 16px;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
      flex: 1;
    }
    .card-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 14px;
      border-top: 1px solid #f1f5f9;
      font-size: 12px;
      color: var(--text-muted);
    }
    .card-read-link {
      font-weight: 700;
      color: var(--primary);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    /* Empty State */
    .empty-state {
      text-align: center;
      padding: 60px 20px;
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: 18px;
      margin: 20px 0 50px;
      display: none;
    }
    .empty-icon {
      width: 54px;
      height: 54px;
      color: var(--text-muted);
      margin-bottom: 14px;
    }
    .empty-title {
      font-size: 18px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 6px;
    }
    .empty-desc {
      font-size: 14px;
      color: var(--text-muted);
      margin-bottom: 18px;
    }

    /* Bottom Sales CTA Box */
    .cta-banner {
      background: linear-gradient(135deg, var(--primary) 0%, #0c2b5c 100%);
      border-radius: 24px;
      padding: 44px 36px;
      color: #ffffff;
      margin-bottom: 70px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 16px 40px rgba(24, 68, 138, 0.2);
    }
    .cta-banner::after {
      content: "";
      position: absolute;
      top: -50%;
      right: -10%;
      width: 400px;
      height: 400px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(5, 169, 134, 0.3) 0%, rgba(5, 169, 134, 0) 70%);
      pointer-events: none;
    }
    .cta-content {
      position: relative;
      z-index: 2;
      max-width: 680px;
    }
    .cta-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      background: rgba(255, 255, 255, 0.15);
      color: #ffffff;
      padding: 4px 12px;
      border-radius: 999px;
      margin-bottom: 12px;
    }
    .cta-title {
      font-size: 28px;
      font-weight: 700;
      line-height: 1.3;
      margin-bottom: 10px;
    }
    .cta-desc {
      font-size: 15px;
      color: #cbd5e1;
      line-height: 1.6;
      margin-bottom: 24px;
    }
    .cta-actions {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }

    /* Floating WhatsApp Button */
    .floating-wa-btn {
      position: fixed;
      bottom: 28px;
      right: 28px;
      z-index: 998;
      background: #25D366;
      color: #ffffff;
      width: 58px;
      height: 58px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 6px 20px rgba(37, 211, 102, 0.45);
      transition: all 0.25s ease;
    }
    .floating-wa-btn:hover {
      transform: scale(1.1);
      box-shadow: 0 10px 28px rgba(37, 211, 102, 0.6);
    }
    .floating-wa-icon {
      width: 32px;
      height: 32px;
    }

    /* Side Menu Drawer */
    .nav-toggle-btn {
      background: #f1f5f9;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      width: 38px;
      height: 38px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--primary);
      transition: all 0.15s ease;
    }
    .nav-toggle-btn:hover {
      background: var(--soft-xl-home);
      border-color: #bee3f8;
    }
    .drawer-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.5);
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
      z-index: 1000;
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.25s ease, visibility 0.25s ease;
    }
    .drawer-backdrop.active {
      opacity: 1;
      visibility: visible;
    }
    .side-drawer {
      position: fixed;
      top: 0;
      right: -320px;
      width: 300px;
      max-width: 85vw;
      height: 100%;
      background: #ffffff;
      z-index: 1001;
      box-shadow: -8px 0 28px rgba(0, 0, 0, 0.15);
      display: flex;
      flex-direction: column;
      transition: right 0.28s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .side-drawer.active {
      right: 0;
    }
    .drawer-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-color);
    }
    .drawer-logo-img {
      height: 28px;
      width: auto;
      display: block;
    }
    .drawer-close-btn {
      background: #f1f5f9;
      border: none;
      border-radius: 8px;
      width: 34px;
      height: 34px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--text-dark);
      transition: background 0.15s ease;
    }
    .drawer-close-btn:hover {
      background: #e2e8f0;
    }
    .drawer-body {
      flex: 1;
      overflow-y: auto;
      padding: 18px 16px;
    }
    .drawer-menu-label {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 8px;
      padding-left: 6px;
    }
    .drawer-nav-list {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .drawer-nav-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 11px 14px;
      border-radius: 10px;
      font-size: 14.5px;
      font-weight: 600;
      color: var(--text-dark);
      text-decoration: none;
      transition: background 0.15s ease, color 0.15s ease;
    }
    .drawer-nav-item:hover, .drawer-nav-item.active {
      background: var(--soft-xl-home);
      color: var(--primary);
    }
    .drawer-nav-item .icon {
      width: 18px;
      height: 18px;
      color: var(--primary);
    }
    .drawer-badge {
      margin-left: auto;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 999px;
      background: rgba(24, 68, 138, 0.08);
      color: var(--primary);
    }
    .drawer-divider {
      height: 1px;
      background: var(--border-color);
      margin: 14px 0 12px;
    }
    .drawer-footer {
      padding: 16px 18px;
      border-top: 1px solid var(--border-color);
      background: #f8fafc;
    }
    .drawer-wa-box {
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 12px;
      text-align: center;
    }
    .drawer-wa-title {
      font-size: 13px;
      font-weight: 700;
      color: var(--primary);
    }
    .drawer-wa-desc {
      font-size: 11.5px;
      color: var(--text-muted);
      margin: 2px 0 10px;
    }
    .drawer-wa-btn {
      width: 100%;
      justify-content: center;
      padding: 8px 12px;
      font-size: 13px;
    }

    /* Footer */
    .footer {
      padding: 40px 0 30px;
      background: #ffffff;
      border-top: 1px solid var(--border-color);
      font-size: 13.5px;
      color: var(--text-muted);
    }

    /* Responsive Reflow */
    @media (max-width: 1024px) {
      .articles-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
      }
      .featured-card {
        grid-template-columns: 1fr;
      }
      .featured-img-wrap {
        min-height: 240px;
      }
    }
    @media (max-width: 768px) {
      body { padding-top: 94px; }
      .nav-links { display: none; }
      .hero-title { font-size: 26px; }
      .top-bar-sticky { height: 34px; font-size: 12px; padding: 0 12px; }
      .navbar { top: 34px; height: 60px; }
      .blog-controls { top: 94px; }
      .featured-body { padding: 22px; }
      .featured-title { font-size: 20px; }
      .cta-banner { padding: 30px 22px; }
      .cta-title { font-size: 22px; }
    }
    @media (max-width: 640px) {
      .container { padding: 0 14px; }
      .articles-grid {
        grid-template-columns: 1fr;
      }
      .floating-wa-btn { width: 50px; height: 50px; bottom: 20px; right: 16px; }
      .floating-wa-icon { width: 28px; height: 28px; }
      .filter-pills { justify-content: flex-start; overflow-x: auto; flex-wrap: nowrap; padding-bottom: 6px; }
      .pill-btn { white-space: nowrap; }
    }
  </style>
</head>
<body>

  <!-- Sticky Top Announcement Bar -->
  <aside class="top-bar-sticky">
    <span>Berita & Edukasi XL SATU:</span>
    <a href="https://wa.me/6287846560510?text=Halo%20Admin%20XL%20SATU,%20mau%20konsultasi%20pasang%20wifi%20rumah" target="_blank" class="top-bar-link">Konsultasi Gratis via WhatsApp!</a>
  </aside>

  <!-- Navbar -->
  <header class="navbar">
    <div class="container nav-inner">
      <div class="brand-logo-wrap">
        <a href="/">
          <img src="/assets/logo-xlsatu.png" alt="XL SATU" class="brand-logo-img" />
        </a>
      </div>

      <nav class="nav-links">
        <a href="/">Beranda</a>
        <a href="/paket">Paket</a>
        <a href="/promo">Promo</a>
        <a href="/blog" style="color:var(--primary);">Blog</a>
        <a href="/bantuan">Bantuan</a>
        <a href="/#coverage">Cek Jangkauan</a>
        <a href="/#kalkulator">Kalkulator</a>
      </nav>

      <div class="nav-actions">
        <button class="nav-toggle-btn" onclick="toggleSideDrawer()" aria-label="Buka Menu Samping">
          <svg class="icon" viewBox="0 0 24 24"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>
      </div>
    </div>
  </header>

  <!-- Hero Header -->
  <section class="blog-hero">
    <div class="container">
      <div class="hero-badge">
        <svg class="icon" style="width:14px; height:14px;" viewBox="0 0 24 24"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10"/><path d="M6 10h10"/></svg>
        Kabar & Edukasi Fiber
      </div>
      <h1 class="hero-title">Berita, Tips Jaringan & Solusi Internet Cepat</h1>
      <p class="hero-subtitle">Kumpulan artikel edukatif, panduan mengatasi WiFi lemot, tips streaming 4K & gaming tanpa lag, serta kabar terbaru layanan XL SATU Fiber.</p>
    </div>
  </section>

  <!-- Controls Bar: Sticky Search & Filter -->
  <section class="blog-controls">
    <div class="container">
      <div class="search-box-wrap">
        <svg class="icon search-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="searchInput" class="search-input" placeholder="Cari tips wifi, live streaming, cloud gaming, router..." oninput="handleSearch(this.value)" />
        <button id="searchClearBtn" class="search-clear-btn" onclick="clearSearch()" aria-label="Hapus Pencarian">
          <svg class="icon" style="width:14px; height:14px;" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>

      <div class="filter-pills" id="categoryPills">
        <button class="pill-btn active" data-cat="all" onclick="filterCategory('all', this)">Semua Artikel</button>
        <button class="pill-btn" data-cat="Tips & Jaringan" onclick="filterCategory('Tips & Jaringan', this)">Tips & Jaringan</button>
        <button class="pill-btn" data-cat="Gaming & Streaming" onclick="filterCategory('Gaming & Streaming', this)">Gaming & Streaming</button>
        <button class="pill-btn" data-cat="Panduan Pasang" onclick="filterCategory('Panduan Pasang', this)">Panduan Pasang</button>
        <button class="pill-btn" data-cat="Info XL SATU" onclick="filterCategory('Info XL SATU', this)">Info XL SATU</button>
        <button class="pill-btn" data-cat="Gadget & Trik" onclick="filterCategory('Gadget & Trik', this)">Gadget & Trik</button>
      </div>
    </div>
  </section>

  <!-- Main Content Area -->
  <main class="container" style="padding-top: 20px;">
    
    <!-- Meta Result Counter -->
    <div class="results-meta">
      <span id="resultsCount">Memuat artikel...</span>
      <span id="activeFilterLabel">Semua Kategori</span>
    </div>

    <!-- Featured Article Container -->
    <div id="featuredContainer"></div>

    <!-- Articles Grid Container -->
    <div class="articles-grid" id="articlesGrid"></div>

    <!-- Empty State -->
    <div class="empty-state" id="emptyState">
      <svg class="icon empty-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
      <h3 class="empty-title">Artikel Tidak Ditemukan</h3>
      <p class="empty-desc">Coba gunakan kata kunci lain seperti "wifi", "router", "streaming", atau "gaming".</p>
      <button class="btn btn-primary" onclick="resetFilters()">Lihat Semua Artikel</button>
    </div>

    <!-- Bottom Sales CTA Banner -->
    <section class="cta-banner">
      <div class="cta-content">
        <div class="cta-badge">Solusi Internet Rumah Juara</div>
        <h2 class="cta-title">Siap Nikmati Internet Fiber Super Stabil Tanpa Batas FUP?</h2>
        <p class="cta-desc">Dapatkan koneksi 100% full fiber optik mulai 50 Mbps hingga 1 Gbps, gratis sewa router Wi-Fi 6, plus bonus kuota HP bersama XL sekeluarga.</p>
        <div class="cta-actions">
          <a href="https://wa.me/6287846560510?text=Halo%20Admin%20XL%20SATU,%20saya%20tertarik%20pasang%20setelah%20baca%20artikel%20blog" target="_blank" class="btn btn-secondary">
            <svg class="icon" viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
            Daftar via WhatsApp (0878-4656-0510)
          </a>
          <a href="/#coverage" class="btn" style="background:rgba(255,255,255,0.15); color:#ffffff; border:1px solid rgba(255,255,255,0.3);">
            <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg>
            Cek Jangkauan Area
          </a>
        </div>
      </div>
    </section>

  </main>

  <!-- Floating WhatsApp Action -->
  <a href="https://wa.me/6287846560510?text=Halo%20Admin%20XL%20SATU,%20mau%20konsultasi%20paket%20wifi%20rumah" target="_blank" class="floating-wa-btn" aria-label="Hubungi WhatsApp Sales">
    <svg class="floating-wa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
    </svg>
  </a>

  <!-- Side Menu Drawer Backdrop -->
  <div class="drawer-backdrop" id="drawerBackdrop" onclick="closeSideDrawer()"></div>

  <!-- Side Menu Drawer Container -->
  <aside class="side-drawer" id="sideDrawer" aria-label="Menu Navigasi">
    <div class="drawer-header">
      <img src="/assets/logo-xlsatu.png" alt="XL SATU" class="drawer-logo-img" />
      <button class="drawer-close-btn" onclick="closeSideDrawer()" aria-label="Tutup Menu">
        <svg class="icon" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    </div>

    <div class="drawer-body">
      <div class="drawer-menu-label">Menu Utama</div>
      <nav class="drawer-nav-list">
        <a href="/" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
          <span>Beranda</span>
        </a>
        <a href="/paket" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
          <span>Daftar Paket</span>
          <span class="drawer-badge">Terlengkap</span>
        </a>
        <a href="/promo" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
          <span>Promo Spesial</span>
          <span class="drawer-badge" style="background:#fee2e2; color:#dc2626;">Hemat 30%</span>
        </a>
        <a href="/blog" class="drawer-nav-item active">
          <svg class="icon" viewBox="0 0 24 24"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10"/><path d="M6 10h10"/></svg>
          <span>Berita & Blog</span>
          <span class="drawer-badge">Baru</span>
        </a>
        <a href="/bantuan" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
          <span>Pusat Bantuan</span>
        </a>

        <div class="drawer-divider"></div>
        <div class="drawer-menu-label">Aksi Cepat</div>

        <a href="/#coverage" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg>
          <span>Cek Jangkauan Fiber</span>
        </a>
        <a href="/#kalkulator" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><rect width="16" height="20" x="4" y="2" rx="2"></rect><line x1="8" y1="6" x2="16" y2="6"></line><line x1="16" y1="14" x2="16" y2="18"></line><path d="M16 10h.01"></path><path d="M12 10h.01"></path><path d="M8 10h.01"></path><path d="M12 14h.01"></path><path d="M8 14h.01"></path><path d="M12 18h.01"></path><path d="M8 18h.01"></path></svg>
          <span>Kalkulator Hemat</span>
        </a>
      </nav>
    </div>

    <div class="drawer-footer">
      <div class="drawer-wa-box">
        <div class="drawer-wa-title">Konsultasi WhatsApp</div>
        <div class="drawer-wa-desc">Respon cepat & cek jangkauan langsung</div>
        <a href="https://wa.me/6287846560510?text=Halo%20Admin%20XL%20SATU,%20mau%20tanya%20info%20paket%20wifi" target="_blank" class="btn btn-secondary drawer-wa-btn">
          <svg class="icon" viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
          0878-4656-0510
        </a>
      </div>
    </div>
  </aside>

  <!-- Footer -->
  <footer class="footer">
    <div class="container" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
      <div>
        <div style="font-weight:700; color:var(--primary); margin-bottom:4px;">XL SATU Fiber — Authorized Sales Partner</div>
        <div>Pemasangan Internet Rumah Cepat & Hemat Area Jabodetabek & Seluruh Indonesia.</div>
      </div>
      <div style="font-size:12px; color:var(--text-muted);">
        &copy; 2026 exelsatu.my.id. Seluruh hak cipta dilindungi.
      </div>
    </div>
  </footer>

  <!-- Script Logic & Live Client Data -->
  <script>
    const ARTICLES_DATA = """ + catalog_json + r""";

    let currentCategory = 'all';
    let searchQuery = '';

    function openSideDrawer() {
      const drawer = document.getElementById('sideDrawer');
      const backdrop = document.getElementById('drawerBackdrop');
      if (drawer) drawer.classList.add('active');
      if (backdrop) backdrop.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeSideDrawer() {
      const drawer = document.getElementById('sideDrawer');
      const backdrop = document.getElementById('drawerBackdrop');
      if (drawer) drawer.classList.remove('active');
      if (backdrop) backdrop.classList.remove('active');
      document.body.style.overflow = '';
    }

    function toggleSideDrawer() {
      const drawer = document.getElementById('sideDrawer');
      if (drawer && drawer.classList.contains('active')) {
        closeSideDrawer();
      } else {
        openSideDrawer();
      }
    }

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeSideDrawer();
    });

    function renderArticles() {
      const q = searchQuery.toLowerCase().trim();
      const filtered = ARTICLES_DATA.filter(function(item) {
        const matchesCategory = currentCategory === 'all' || item.category === currentCategory;
        const matchesSearch = !q || 
          item.title.toLowerCase().indexOf(q) !== -1 || 
          item.description.toLowerCase().indexOf(q) !== -1 ||
          item.category.toLowerCase().indexOf(q) !== -1;
        return matchesCategory && matchesSearch;
      });

      const countEl = document.getElementById('resultsCount');
      const filterLabelEl = document.getElementById('activeFilterLabel');
      const emptyStateEl = document.getElementById('emptyState');
      const featuredContainer = document.getElementById('featuredContainer');
      const gridContainer = document.getElementById('articlesGrid');

      countEl.textContent = 'Menampilkan ' + filtered.length + ' dari ' + ARTICLES_DATA.length + ' artikel';
      filterLabelEl.textContent = currentCategory === 'all' ? 'Semua Kategori' : currentCategory;

      if (filtered.length === 0) {
        featuredContainer.innerHTML = '';
        gridContainer.innerHTML = '';
        emptyStateEl.style.display = 'block';
        return;
      }

      emptyStateEl.style.display = 'none';

      let featuredItem = null;
      let gridItems = filtered;

      if (!q && currentCategory === 'all' && filtered.length > 0) {
        featuredItem = filtered[0];
        gridItems = filtered.slice(1);
      }

      if (featuredItem) {
        featuredContainer.innerHTML = [
          '<div class="featured-card" onclick="location.href=\'/artikel.html?slug=' + featuredItem.slug + '\'">',
            '<div class="featured-img-wrap">',
              '<img src="' + featuredItem.image + '" alt="' + featuredItem.title + '" class="featured-img" loading="lazy" />',
            '</div>',
            '<div class="featured-body">',
              '<div class="featured-tag-row">',
                '<span class="badge-category">' + featuredItem.category + '</span>',
                '<span style="font-size:12px; color:var(--text-muted);">' + featuredItem.read_time + '</span>',
              '</div>',
              '<h2 class="featured-title">' + featuredItem.title + '</h2>',
              '<p class="featured-desc">' + featuredItem.description + '</p>',
              '<div class="featured-footer">',
                '<span>' + featuredItem.date + '</span>',
                '<span class="read-btn-link">',
                  'Baca Selengkapnya',
                  '<svg class="icon" style="width:16px; height:16px;" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"></polyline></svg>',
                '</span>',
              '</div>',
            '</div>',
          '</div>'
        ].join('');
      } else {
        featuredContainer.innerHTML = '';
      }

      const gridHtml = gridItems.map(function(item) {
        return [
          '<article class="article-card" onclick="location.href=\'/artikel.html?slug=' + item.slug + '\'">',
            '<div class="card-thumb-wrap">',
              '<img src="' + item.image + '" alt="' + item.title + '" class="card-thumb" loading="lazy" />',
            '</div>',
            '<div class="card-body">',
              '<div class="card-meta-top">',
                '<span class="badge-category">' + item.category + '</span>',
                '<span>' + item.read_time + '</span>',
              '</div>',
              '<h3 class="card-title">' + item.title + '</h3>',
              '<p class="card-desc">' + item.description + '</p>',
              '<div class="card-footer">',
                '<span>' + item.date + '</span>',
                '<span class="card-read-link">',
                  'Baca',
                  '<svg class="icon" style="width:14px; height:14px;" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"></polyline></svg>',
                '</span>',
              '</div>',
            '</div>',
          '</article>'
        ].join('');
      }).join('');

      gridContainer.innerHTML = gridHtml;
    }

    function filterCategory(cat, btn) {
      currentCategory = cat;
      document.querySelectorAll('.pill-btn').forEach(function(el) {
        el.classList.remove('active');
      });
      if (btn) btn.classList.add('active');
      renderArticles();
    }

    function handleSearch(val) {
      searchQuery = val;
      const clearBtn = document.getElementById('searchClearBtn');
      if (clearBtn) {
        clearBtn.style.display = val ? 'flex' : 'none';
      }
      renderArticles();
    }

    function clearSearch() {
      const input = document.getElementById('searchInput');
      if (input) input.value = '';
      searchQuery = '';
      const clearBtn = document.getElementById('searchClearBtn');
      if (clearBtn) clearBtn.style.display = 'none';
      renderArticles();
    }

    function resetFilters() {
      clearSearch();
      filterCategory('all', document.querySelector('.pill-btn[data-cat="all"]'));
    }

    window.addEventListener('DOMContentLoaded', function() {
      renderArticles();
    });
  </script>
</body>
</html>
"""
    with open('/root/exelsatu/blog.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ blog.html berhasil di-generate ({len(catalog)} artikel)")

def build_artikel():
    catalog, articles = get_catalog_data()
    summary_list = []
    for a in articles:
        summary_list.append({
            'slug': a['slug'],
            'title': a['title'],
            'image': a['image'],
            'category': a['category'],
            'date': a['date'],
            'read_time': a['read_time']
        })

    summary_json = json.dumps(summary_list, ensure_ascii=False)
    first_article = articles[0]
    first_article_json = json.dumps(first_article, ensure_ascii=False)

    html = r"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title id="pageTitle">Detail Artikel — XL SATU Fiber</title>
  <meta name="description" id="pageMetaDesc" content="Baca ulasan lengkap tips internet rumah, panduan gaming streaming, dan solusi koneksi WiFi stabil dari XL SATU Fiber." />
  <link rel="canonical" id="pageCanonical" href="https://exelsatu.my.id/blog" />
  <meta property="og:title" id="pageOgTitle" content="Artikel XL SATU Fiber" />
  <meta property="og:description" id="pageOgDesc" content="Baca ulasan lengkap tips internet rumah dari XL SATU Fiber." />
  <meta property="og:image" id="pageOgImage" content="https://exelsatu.my.id/assets/logo-xlsatu.png" />
  <meta property="og:type" content="article" />

  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon.png" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

  <style>
    @font-face {
      font-family: 'XLSmart';
      src: url('/fonts/xlsmart-regular.otf') format('opentype');
      font-weight: 400;
      font-style: normal;
      font-display: swap;
    }
    @font-face {
      font-family: 'XLSmart';
      src: url('/fonts/xlsmart-medium.otf') format('opentype');
      font-weight: 500;
      font-style: normal;
      font-display: swap;
    }
    @font-face {
      font-family: 'XLSmart';
      src: url('/fonts/xlsmart-bold.otf') format('opentype');
      font-weight: 700;
      font-style: normal;
      font-display: swap;
    }

    :root {
      --primary: #18448A;
      --secondary: #05A986;
      --soft-xl-home: #ECF9FF;
      --sky-blue: #1D90C9;
      --chip-blue: #0284C7;
      --accent: #E11D48;
      --bg-main: #FFFFFF;
      --text-dark: #0f172a;
      --text-body: #334155;
      --text-muted: #64748B;
      --border-color: #E2E8F0;
      --card-bg: #FFFFFF;
      --font-family: 'XLSmart', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --radius: 16px;
      --container: 1180px;
      --reader-width: 820px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: var(--font-family);
    }

    body {
      background-color: #FFFFFF;
      color: var(--text-dark);
      line-height: 1.6;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
      padding-top: 102px;
    }

    a {
      text-decoration: none;
      color: inherit;
    }

    .container {
      max-width: var(--container);
      margin: 0 auto;
      padding: 0 20px;
      width: 100%;
    }

    .reader-container {
      max-width: var(--reader-width);
      margin: 0 auto;
      padding: 0 20px;
      width: 100%;
    }

    .icon {
      display: inline-block;
      width: 20px;
      height: 20px;
      stroke-width: 2;
      stroke: currentColor;
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
      vertical-align: middle;
      flex-shrink: 0;
    }

    /* Top Announcement Bar (Fixed) */
    .top-bar-sticky {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      width: 100%;
      height: 38px;
      z-index: 1000;
      background: var(--soft-xl-home);
      border-bottom: 1px solid #daeeff;
      padding: 0 16px;
      text-align: center;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-size: 13.5px;
      color: var(--primary);
      font-weight: 600;
    }
    .top-bar-link {
      color: var(--secondary);
      font-weight: 700;
      text-decoration: underline;
      cursor: pointer;
    }

    /* Navbar (Fixed) */
    .navbar {
      background: #ffffff;
      border-bottom: 1px solid var(--border-color);
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
      position: fixed;
      top: 38px;
      left: 0;
      right: 0;
      width: 100%;
      height: 64px;
      z-index: 999;
    }
    .nav-inner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 64px;
    }
    .brand-logo-img {
      height: 32px;
      width: auto;
      object-fit: contain;
      display: block;
    }
    .nav-links {
      display: flex;
      align-items: center;
      gap: 26px;
      font-size: 14.5px;
      font-weight: 600;
      color: var(--text-muted);
    }
    .nav-links a:hover {
      color: var(--primary);
    }
    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-weight: 700;
      border-radius: 999px;
      padding: 11px 22px;
      font-size: 14px;
      cursor: pointer;
      border: none;
      transition: all 0.2s ease;
      text-align: center;
      justify-content: center;
    }
    .btn-primary {
      background: var(--primary);
      color: #ffffff;
    }
    .btn-primary:hover {
      background: #0f2e62;
      box-shadow: 0 4px 14px rgba(24, 68, 138, 0.25);
    }
    .btn-secondary {
      background: var(--secondary);
      color: #ffffff;
    }
    .btn-secondary:hover {
      background: #048a6d;
      box-shadow: 0 4px 14px rgba(5, 169, 134, 0.25);
    }

    /* Breadcrumbs */
    .breadcrumbs-bar {
      padding: 20px 0 10px;
      font-size: 13px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .breadcrumbs-bar a:hover {
      color: var(--primary);
      text-decoration: underline;
    }
    .breadcrumbs-sep {
      color: #cbd5e1;
    }

    /* Article Header */
    .article-header {
      padding: 14px 0 28px;
    }
    .article-badge-row {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }
    .badge-category {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      background: rgba(24, 68, 138, 0.1);
      color: var(--primary);
      padding: 4px 12px;
      border-radius: 6px;
    }
    .badge-time {
      font-size: 12.5px;
      color: var(--text-muted);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .article-main-title {
      font-size: 36px;
      font-weight: 700;
      color: var(--primary);
      line-height: 1.3;
      margin-bottom: 16px;
    }
    .article-author-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 14px 0;
      border-top: 1px solid var(--border-color);
      border-bottom: 1px solid var(--border-color);
      font-size: 13.5px;
      color: var(--text-muted);
      flex-wrap: wrap;
    }
    .author-info {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .author-avatar {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: var(--soft-xl-home);
      color: var(--primary);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .share-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .share-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid var(--border-color);
      background: #ffffff;
      color: var(--text-dark);
      transition: all 0.15s ease;
    }
    .share-btn:hover {
      background: var(--soft-xl-home);
      border-color: var(--primary);
      color: var(--primary);
    }
    .share-btn-wa {
      background: #25D366;
      color: #ffffff;
      border-color: #25D366;
    }
    .share-btn-wa:hover {
      background: #20ba59;
      color: #ffffff;
    }

    /* Featured Hero Banner */
    .article-hero-banner {
      width: 100%;
      margin: 24px 0 34px;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
      background: #0f172a;
    }
    .article-hero-banner img {
      width: 100%;
      height: auto;
      max-height: 480px;
      object-fit: cover;
      display: block;
    }

    /* Article Content Typography */
    .article-content {
      font-size: 17px;
      color: var(--text-body);
      line-height: 1.8;
      margin-bottom: 40px;
    }
    .article-content p {
      margin-bottom: 20px;
    }
    .article-content h2 {
      font-size: 24px;
      font-weight: 700;
      color: var(--primary);
      line-height: 1.35;
      margin: 36px 0 16px;
      padding-bottom: 8px;
      border-bottom: 2px solid var(--soft-xl-home);
    }
    .article-content h3 {
      font-size: 20px;
      font-weight: 700;
      color: #0f2e62;
      line-height: 1.4;
      margin: 28px 0 12px;
    }
    .article-content ul, .article-content ol {
      margin: 16px 0 24px 24px;
    }
    .article-content li {
      margin-bottom: 8px;
    }
    .article-content strong {
      color: var(--text-dark);
      font-weight: 700;
    }
    .article-content em {
      font-style: italic;
    }
    .article-content a {
      color: var(--primary);
      font-weight: 600;
      text-decoration: underline;
      text-underline-offset: 3px;
    }
    .article-content a:hover {
      color: var(--secondary);
    }
    .article-content img {
      max-width: 100%;
      height: auto;
      border-radius: 14px;
      margin: 20px 0;
    }

    /* In-Article Sales CTA Box */
    .in-article-cta {
      margin: 36px 0;
      padding: 30px 28px;
      border-radius: 20px;
      background: linear-gradient(135deg, #ECF9FF 0%, #E0F2FE 100%);
      border: 1.5px solid #BAE6FD;
      box-shadow: 0 8px 24px rgba(24, 68, 138, 0.07);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
      flex-wrap: wrap;
    }
    .in-cta-text {
      flex: 1;
      min-width: 260px;
    }
    .in-cta-badge {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--primary);
      background: rgba(24, 68, 138, 0.1);
      padding: 3px 10px;
      border-radius: 999px;
      display: inline-block;
      margin-bottom: 8px;
    }
    .in-cta-title {
      font-size: 20px;
      font-weight: 700;
      color: var(--primary);
      line-height: 1.35;
      margin-bottom: 6px;
    }
    .in-cta-desc {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.5;
    }
    .in-cta-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    /* End-of-Article Author & Share Box */
    .article-end-box {
      padding: 24px;
      background: #f8fafc;
      border: 1px solid var(--border-color);
      border-radius: 18px;
      margin: 40px 0 60px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      flex-wrap: wrap;
    }

    /* Related Articles Section */
    .related-section {
      padding: 40px 0 70px;
      background: #f8fafc;
      border-top: 1px solid var(--border-color);
    }
    .related-title {
      font-size: 24px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 24px;
      text-align: center;
    }
    .related-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
    }
    .related-card {
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: 16px;
      overflow: hidden;
      cursor: pointer;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      display: flex;
      flex-direction: column;
    }
    .related-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 24px rgba(24, 68, 138, 0.08);
    }
    .related-thumb-wrap {
      position: relative;
      width: 100%;
      padding-top: 56.25%;
      background: #e2e8f0;
    }
    .related-thumb {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .related-body {
      padding: 16px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }
    .related-card-title {
      font-size: 15px;
      font-weight: 700;
      color: var(--text-dark);
      line-height: 1.4;
      margin-bottom: 8px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .related-card:hover .related-card-title {
      color: var(--primary);
    }
    .related-meta {
      margin-top: auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11.5px;
      color: var(--text-muted);
      padding-top: 10px;
      border-top: 1px solid #f1f5f9;
    }

    /* Floating WhatsApp Button */
    .floating-wa-btn {
      position: fixed;
      bottom: 28px;
      right: 28px;
      z-index: 998;
      background: #25D366;
      color: #ffffff;
      width: 58px;
      height: 58px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 6px 20px rgba(37, 211, 102, 0.45);
      transition: all 0.25s ease;
    }
    .floating-wa-btn:hover {
      transform: scale(1.1);
      box-shadow: 0 10px 28px rgba(37, 211, 102, 0.6);
    }
    .floating-wa-icon {
      width: 32px;
      height: 32px;
    }

    /* Side Menu Drawer */
    .nav-toggle-btn {
      background: #f1f5f9;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      width: 38px;
      height: 38px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--primary);
      transition: all 0.15s ease;
    }
    .nav-toggle-btn:hover {
      background: var(--soft-xl-home);
      border-color: #bee3f8;
    }
    .drawer-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.5);
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
      z-index: 1000;
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.25s ease, visibility 0.25s ease;
    }
    .drawer-backdrop.active {
      opacity: 1;
      visibility: visible;
    }
    .side-drawer {
      position: fixed;
      top: 0;
      right: -320px;
      width: 300px;
      max-width: 85vw;
      height: 100%;
      background: #ffffff;
      z-index: 1001;
      box-shadow: -8px 0 28px rgba(0, 0, 0, 0.15);
      display: flex;
      flex-direction: column;
      transition: right 0.28s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .side-drawer.active {
      right: 0;
    }
    .drawer-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-color);
    }
    .drawer-logo-img {
      height: 28px;
      width: auto;
      display: block;
    }
    .drawer-close-btn {
      background: #f1f5f9;
      border: none;
      border-radius: 8px;
      width: 34px;
      height: 34px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--text-dark);
      transition: background 0.15s ease;
    }
    .drawer-close-btn:hover {
      background: #e2e8f0;
    }
    .drawer-body {
      flex: 1;
      overflow-y: auto;
      padding: 18px 16px;
    }
    .drawer-menu-label {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 8px;
      padding-left: 6px;
    }
    .drawer-nav-list {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .drawer-nav-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 11px 14px;
      border-radius: 10px;
      font-size: 14.5px;
      font-weight: 600;
      color: var(--text-dark);
      text-decoration: none;
      transition: background 0.15s ease, color 0.15s ease;
    }
    .drawer-nav-item:hover, .drawer-nav-item.active {
      background: var(--soft-xl-home);
      color: var(--primary);
    }
    .drawer-nav-item .icon {
      width: 18px;
      height: 18px;
      color: var(--primary);
    }
    .drawer-badge {
      margin-left: auto;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 999px;
      background: rgba(24, 68, 138, 0.08);
      color: var(--primary);
    }
    .drawer-divider {
      height: 1px;
      background: var(--border-color);
      margin: 14px 0 12px;
    }
    .drawer-footer {
      padding: 16px 18px;
      border-top: 1px solid var(--border-color);
      background: #f8fafc;
    }
    .drawer-wa-box {
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 12px;
      text-align: center;
    }
    .drawer-wa-title {
      font-size: 13px;
      font-weight: 700;
      color: var(--primary);
    }
    .drawer-wa-desc {
      font-size: 11.5px;
      color: var(--text-muted);
      margin: 2px 0 10px;
    }
    .drawer-wa-btn {
      width: 100%;
      justify-content: center;
      padding: 8px 12px;
      font-size: 13px;
    }

    /* Footer */
    .footer {
      padding: 40px 0 30px;
      background: #ffffff;
      border-top: 1px solid var(--border-color);
      font-size: 13.5px;
      color: var(--text-muted);
    }

    /* Responsive */
    @media (max-width: 768px) {
      body { padding-top: 94px; }
      .nav-links { display: none; }
      .article-main-title { font-size: 26px; }
      .top-bar-sticky { height: 34px; font-size: 12px; padding: 0 12px; }
      .navbar { top: 34px; height: 60px; }
      .in-article-cta { padding: 22px; }
      .in-cta-title { font-size: 18px; }
      .related-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 640px) {
      .reader-container { padding: 0 16px; }
      .floating-wa-btn { width: 50px; height: 50px; bottom: 20px; right: 16px; }
      .floating-wa-icon { width: 28px; height: 28px; }
    }
  </style>
</head>
<body>

  <!-- Sticky Top Announcement Bar -->
  <aside class="top-bar-sticky">
    <span>Konsultasi Pasang Baru XL SATU:</span>
    <a href="https://wa.me/6287846560510?text=Halo%20Admin%20XL%20SATU,%20mau%20konsultasi%20pasang%20wifi%20rumah" target="_blank" class="top-bar-link">Chat WhatsApp 0878-4656-0510!</a>
  </aside>

  <!-- Navbar -->
  <header class="navbar">
    <div class="container nav-inner">
      <div class="brand-logo-wrap">
        <a href="/">
          <img src="/assets/logo-xlsatu.png" alt="XL SATU" class="brand-logo-img" />
        </a>
      </div>

      <nav class="nav-links">
        <a href="/">Beranda</a>
        <a href="/paket">Paket</a>
        <a href="/promo">Promo</a>
        <a href="/blog" style="color:var(--primary);">Blog</a>
        <a href="/bantuan">Bantuan</a>
        <a href="/#coverage">Cek Jangkauan</a>
        <a href="/#kalkulator">Kalkulator</a>
      </nav>

      <div class="nav-actions">
        <button class="nav-toggle-btn" onclick="toggleSideDrawer()" aria-label="Buka Menu Samping">
          <svg class="icon" viewBox="0 0 24 24"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>
      </div>
    </div>
  </header>

  <!-- Article View Container -->
  <main class="reader-container">

    <!-- Breadcrumbs -->
    <nav class="breadcrumbs-bar" aria-label="Breadcrumb">
      <a href="/">Beranda</a>
      <span class="breadcrumbs-sep">/</span>
      <a href="/blog">Blog</a>
      <span class="breadcrumbs-sep">/</span>
      <span id="breadcrumbCategory" style="color:var(--primary); font-weight:600;">Edukasi</span>
      <span class="breadcrumbs-sep">/</span>
      <span id="breadcrumbTitle" style="color:var(--text-dark); max-width:320px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">Detail Artikel</span>
    </nav>

    <!-- Article Header -->
    <header class="article-header">
      <div class="article-badge-row">
        <span class="badge-category" id="articleCategoryBadge">Tips & Jaringan</span>
        <span class="badge-time">
          <svg class="icon" style="width:14px; height:14px;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          <span id="articleReadTime">4 menit baca</span>
        </span>
      </div>

      <h1 class="article-main-title" id="articleTitle">Memuat Judul Artikel...</h1>

      <div class="article-author-row">
        <div class="author-info">
          <div class="author-avatar">
            <svg class="icon" style="width:20px; height:20px;" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
          </div>
          <div>
            <div style="font-weight:700; color:var(--text-dark);">Tim Edukasi XL SATU</div>
            <div style="font-size:12px; color:var(--text-muted);" id="articleDate">18 September 2026</div>
          </div>
        </div>

        <div class="share-actions">
          <button class="share-btn share-btn-wa" onclick="shareToWhatsApp()" aria-label="Bagikan ke WhatsApp">
            <svg class="icon" style="width:14px; height:14px;" viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
            <span>Share WA</span>
          </button>
          <button class="share-btn" onclick="copyArticleLink()" id="copyLinkBtn" aria-label="Salin Tautan Artikel">
            <svg class="icon" style="width:14px; height:14px;" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
            <span id="copyLinkText">Salin Link</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Article Featured Image -->
    <div class="article-hero-banner" id="articleImageWrap">
      <img src="/assets/logo-xlsatu.png" alt="Featured Banner" id="articleFeaturedImg" />
    </div>

    <!-- Article Body HTML -->
    <article class="article-content" id="articleBody">
      <p>Memuat konten artikel...</p>
    </article>

    <!-- High-Converting Sales CTA Box -->
    <section class="in-article-cta" id="salesCtaBox">
      <div class="in-cta-text">
        <span class="in-cta-badge">Rekomendasi Terbaik</span>
        <h3 class="in-cta-title">Ingin WiFi Rumah Kencang Tanpa Mikirin Batas FUP?</h3>
        <p class="in-cta-desc">Pakai XL SATU Fiber: kecepatan 100% simetris, gratis instalasi & router Wi-Fi 6, plus bonus kuota HP bersama sekeluarga.</p>
      </div>
      <div class="in-cta-actions">
        <a id="ctaWaLink" href="https://wa.me/6287846560510?text=Halo%20Admin%20XL%20SATU,%20mau%20konsultasi%20pasang%20wifi%20rumah" target="_blank" class="btn btn-secondary">
          <svg class="icon" viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
          Chat WhatsApp Sales
        </a>
        <a href="/#coverage" class="btn btn-primary">
          Cek Jangkauan
        </a>
      </div>
    </section>

    <!-- End of Article Footer Box -->
    <div class="article-end-box">
      <div>
        <div style="font-weight:700; color:var(--primary); font-size:15px; margin-bottom:4px;">Punya Pertanyaan Seputar Artikel Ini?</div>
        <div style="font-size:13.5px; color:var(--text-muted);">Konsultasikan gratis dengan tim resmi XL SATU via WhatsApp kami.</div>
      </div>
      <a href="https://wa.me/6287846560510?text=Halo%20Admin%20XL%20SATU,%20mau%20tanya%20seputar%20artikel%20wifi%20rumah" target="_blank" class="btn btn-secondary" style="padding:9px 18px; font-size:13.5px;">
        Hubungi WhatsApp (0878-4656-0510)
      </a>
    </div>

  </main>

  <!-- Related Articles Section -->
  <section class="related-section">
    <div class="container">
      <h2 class="related-title">Artikel Pilihan Lainnya</h2>
      <div class="related-grid" id="relatedGrid">
        <!-- Injected dynamically -->
      </div>
    </div>
  </section>

  <!-- Floating WhatsApp Action -->
  <a href="https://wa.me/6287846560510?text=Halo%20Admin%20XL%20SATU,%20mau%20konsultasi%20paket%20wifi%20rumah" target="_blank" class="floating-wa-btn" aria-label="Hubungi WhatsApp Sales">
    <svg class="floating-wa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
    </svg>
  </a>

  <!-- Side Menu Drawer Backdrop -->
  <div class="drawer-backdrop" id="drawerBackdrop" onclick="closeSideDrawer()"></div>

  <!-- Side Menu Drawer Container -->
  <aside class="side-drawer" id="sideDrawer" aria-label="Menu Navigasi">
    <div class="drawer-header">
      <img src="/assets/logo-xlsatu.png" alt="XL SATU" class="drawer-logo-img" />
      <button class="drawer-close-btn" onclick="closeSideDrawer()" aria-label="Tutup Menu">
        <svg class="icon" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    </div>

    <div class="drawer-body">
      <div class="drawer-menu-label">Menu Utama</div>
      <nav class="drawer-nav-list">
        <a href="/" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
          <span>Beranda</span>
        </a>
        <a href="/paket" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
          <span>Daftar Paket</span>
          <span class="drawer-badge">Terlengkap</span>
        </a>
        <a href="/promo" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
          <span>Promo Spesial</span>
          <span class="drawer-badge" style="background:#fee2e2; color:#dc2626;">Hemat 30%</span>
        </a>
        <a href="/blog" class="drawer-nav-item active">
          <svg class="icon" viewBox="0 0 24 24"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10"/><path d="M6 10h10"/></svg>
          <span>Berita & Blog</span>
          <span class="drawer-badge">Baru</span>
        </a>
        <a href="/bantuan" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
          <span>Pusat Bantuan</span>
        </a>

        <div class="drawer-divider"></div>
        <div class="drawer-menu-label">Aksi Cepat</div>

        <a href="/#coverage" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg>
          <span>Cek Jangkauan Fiber</span>
        </a>
        <a href="/#kalkulator" class="drawer-nav-item">
          <svg class="icon" viewBox="0 0 24 24"><rect width="16" height="20" x="4" y="2" rx="2"></rect><line x1="8" y1="6" x2="16" y2="6"></line><line x1="16" y1="14" x2="16" y2="18"></line><path d="M16 10h.01"></path><path d="M12 10h.01"></path><path d="M8 10h.01"></path><path d="M12 14h.01"></path><path d="M8 14h.01"></path><path d="M12 18h.01"></path><path d="M8 18h.01"></path></svg>
          <span>Kalkulator Hemat</span>
        </a>
      </nav>
    </div>

    <div class="drawer-footer">
      <div class="drawer-wa-box">
        <div class="drawer-wa-title">Konsultasi WhatsApp</div>
        <div class="drawer-wa-desc">Respon cepat & cek jangkauan langsung</div>
        <a href="https://wa.me/6287846560510?text=Halo%20Admin%20XL%20SATU,%20mau%20tanya%20info%20paket%20wifi" target="_blank" class="btn btn-secondary drawer-wa-btn">
          <svg class="icon" viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
          0878-4656-0510
        </a>
      </div>
    </div>
  </aside>

  <!-- Footer -->
  <footer class="footer">
    <div class="container" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
      <div>
        <div style="font-weight:700; color:var(--primary); margin-bottom:4px;">XL SATU Fiber — Authorized Sales Partner</div>
        <div>Pemasangan Internet Rumah Cepat & Hemat Area Jabodetabek & Seluruh Indonesia.</div>
      </div>
      <div style="font-size:12px; color:var(--text-muted);">
        &copy; 2026 exelsatu.my.id. Seluruh hak cipta dilindungi.
      </div>
    </div>
  </footer>

  <!-- Script Logic -->
  <script>
    const SUMMARY_DATA = """ + summary_json + r""";
    const DEFAULT_ARTICLE = """ + first_article_json + r""";
    let CURRENT_ARTICLE = DEFAULT_ARTICLE;

    function openSideDrawer() {
      const drawer = document.getElementById('sideDrawer');
      const backdrop = document.getElementById('drawerBackdrop');
      if (drawer) drawer.classList.add('active');
      if (backdrop) backdrop.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeSideDrawer() {
      const drawer = document.getElementById('sideDrawer');
      const backdrop = document.getElementById('drawerBackdrop');
      if (drawer) drawer.classList.remove('active');
      if (backdrop) backdrop.classList.remove('active');
      document.body.style.overflow = '';
    }

    function toggleSideDrawer() {
      const drawer = document.getElementById('sideDrawer');
      if (drawer && drawer.classList.contains('active')) {
        closeSideDrawer();
      } else {
        openSideDrawer();
      }
    }

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeSideDrawer();
    });

    function getTargetSlug() {
      const params = new URLSearchParams(window.location.search);
      const querySlug = params.get('slug');
      if (querySlug) return querySlug.trim();

      const pathSegments = window.location.pathname.split('/').filter(Boolean);
      if (pathSegments.length >= 2 && pathSegments[0] === 'blog') {
        const lastPart = pathSegments[1].replace('.html', '');
        if (lastPart && lastPart !== 'index' && lastPart !== 'baca') {
          return lastPart;
        }
      }
      return DEFAULT_ARTICLE.slug;
    }

    function renderArticleDetail(art) {
      CURRENT_ARTICLE = art;

      document.title = art.title + ' — XL SATU Fiber';
      const metaDesc = document.getElementById('pageMetaDesc');
      if (metaDesc && art.description) metaDesc.setAttribute('content', art.description);

      const bcCat = document.getElementById('breadcrumbCategory');
      const bcTitle = document.getElementById('breadcrumbTitle');
      if (bcCat) bcCat.textContent = art.category;
      if (bcTitle) bcTitle.textContent = art.title;

      const catBadge = document.getElementById('articleCategoryBadge');
      const readTime = document.getElementById('articleReadTime');
      const titleEl = document.getElementById('articleTitle');
      const dateEl = document.getElementById('articleDate');
      const imgEl = document.getElementById('articleFeaturedImg');
      const bodyEl = document.getElementById('articleBody');

      if (catBadge) catBadge.textContent = art.category;
      if (readTime) readTime.textContent = art.read_time;
      if (titleEl) titleEl.textContent = art.title;
      if (dateEl) dateEl.textContent = art.date;
      if (imgEl) {
        imgEl.src = art.image;
        imgEl.alt = art.title;
      }
      if (bodyEl) {
        bodyEl.innerHTML = art.content || '<p>' + art.description + '</p>';
      }

      const ctaWaLink = document.getElementById('ctaWaLink');
      if (ctaWaLink) {
        const waText = 'Halo Admin XL SATU, saya baru saja membaca artikel "' + art.title + '" dan tertarik konsultasi pasang wifi rumah.';
        ctaWaLink.href = 'https://wa.me/6287846560510?text=' + encodeURIComponent(waText);
      }

      renderRelatedArticles(art.slug, art.category);
    }

    function renderRelatedArticles(currentSlug, currentCat) {
      const relatedGrid = document.getElementById('relatedGrid');
      if (!relatedGrid) return;

      let sameCat = SUMMARY_DATA.filter(function(item) {
        return item.slug !== currentSlug && item.category === currentCat;
      });
      let otherCat = SUMMARY_DATA.filter(function(item) {
        return item.slug !== currentSlug && item.category !== currentCat;
      });

      const related = sameCat.concat(otherCat).slice(0, 3);

      relatedGrid.innerHTML = related.map(function(item) {
        return [
          '<div class="related-card" onclick="location.href=\'/artikel.html?slug=' + item.slug + '\'">',
            '<div class="related-thumb-wrap">',
              '<img src="' + item.image + '" alt="' + item.title + '" class="related-thumb" loading="lazy" />',
            '</div>',
            '<div class="related-body">',
              '<div style="font-size:11px; font-weight:700; color:var(--primary); text-transform:uppercase; margin-bottom:6px;">' + item.category + '</div>',
              '<h3 class="related-card-title">' + item.title + '</h3>',
              '<div class="related-meta">',
                '<span>' + item.date + '</span>',
                '<span>' + item.read_time + '</span>',
              '</div>',
            '</div>',
          '</div>'
        ].join('');
      }).join('');
    }

    function shareToWhatsApp() {
      const url = window.location.href;
      const title = CURRENT_ARTICLE ? CURRENT_ARTICLE.title : document.title;
      const text = title + '\n\n' + url;
      window.open('https://api.whatsapp.com/send?text=' + encodeURIComponent(text), '_blank');
    }

    function copyArticleLink() {
      const url = window.location.href;
      if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(function() {
          const txt = document.getElementById('copyLinkText');
          if (txt) {
            txt.textContent = 'Tersalin!';
            setTimeout(function() { txt.textContent = 'Salin Link'; }, 2000);
          }
        });
      }
    }

    async function initArticle() {
      const targetSlug = getTargetSlug();

      if (targetSlug === DEFAULT_ARTICLE.slug) {
        renderArticleDetail(DEFAULT_ARTICLE);
        return;
      }

      try {
        const res = await fetch('/data/articles.json');
        if (!res.ok) throw new Error('Failed to fetch articles');
        const list = await res.json();
        const found = list.find(function(item) { return item.slug === targetSlug; });
        if (found) {
          renderArticleDetail(found);
        } else {
          renderArticleDetail(DEFAULT_ARTICLE);
        }
      } catch (err) {
        console.error('Error loading article:', err);
        renderArticleDetail(DEFAULT_ARTICLE);
      }
    }

    window.addEventListener('DOMContentLoaded', function() {
      initArticle();
    });
  </script>
</body>
</html>
"""
    with open('/root/exelsatu/artikel.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ artikel.html berhasil di-generate")

if __name__ == '__main__':
    build_blog()
    build_artikel()
