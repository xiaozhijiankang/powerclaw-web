# PowerClaw Marketing Site

Static landing page for [powerclaw.app](https://powerclaw.app/), hosted on GitHub Pages.

## Structure

```
.
├── CNAME                 # GitHub Pages custom domain (powerclaw.app)
├── index.html            # Landing page (single-file, no build)
├── assets/
│   ├── logo.png          # App icon (96×96)
│   └── screenshots/      # iPhone 17 Pro Max captures (1320×2868)
├── privacy/index.html    # → /privacy
├── terms/index.html      # → /terms
└── support/index.html    # → /support
```

No build step. Pure static HTML + inline CSS. Edit files, commit, push — GitHub Pages serves the change in ~30 seconds.

## Local preview

```bash
open index.html
# or run a tiny server if you need clean URLs:
python3 -m http.server 8000
```

## Deploying

GitHub Pages is configured to serve from `main` branch root. Every push to `main` triggers a deploy.

## Custom domain (DNS)

`powerclaw.app` apex domain points to GitHub Pages via A records:

```
A  powerclaw.app  185.199.108.153
A  powerclaw.app  185.199.109.153
A  powerclaw.app  185.199.110.153
A  powerclaw.app  185.199.111.153
```

For `www` subdomain (optional, recommended):

```
CNAME  www.powerclaw.app  xiaozhijiankang.github.io
```

After DNS propagates, enable **Enforce HTTPS** in repo Settings → Pages. The `.app` TLD requires HTTPS by registry policy (HSTS preload).

## Updating screenshots

Source PNGs live in `PowerClaw-Native/.asc/screenshots/` (1320×2868 from iPhone 17 Pro Max simulator). Copy any updates into `assets/screenshots/` keeping filenames stable so the `<img src>` references in `index.html` keep working.

## Legal pages

Content is portable PowerClaw policy text (no platform / domain hardcoding). To update, edit `privacy/index.html`, `terms/index.html`, or `support/index.html` directly.

The PowerClaw iOS app links to `https://powerclaw.app/privacy` etc. Keep those URLs stable.
