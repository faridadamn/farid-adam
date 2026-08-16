# Farid Adamn — Living Portfolio

Halaman profil yang **hidup**: berisi value prop, bukti proyek (ApotekKilat), dan build log yang bertambah otomatis tiap minggu dari Notion Task Manager (via Hermes cron, tanpa LLM di tiap tick).

- Live: `https://faridadamn.github.io/farid-adam/`
- Proyek utama: [ApotekKilat](https://apotekkilat.vercel.app) — web app manajemen apotek, dikerjakan solo, kode [public](https://github.com/faridadamn/apotekkilat)
- Build log: update mingguan via script deterministik `farid_build_log.py` (task Done 7 hari dari Task Manager → append ke `index.html`)

Arsitektur: single-file static HTML (tanpa dependency), ditulis & dirawat manual + agent.