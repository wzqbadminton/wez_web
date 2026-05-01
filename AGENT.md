# AGENT.md — WZQ Badminton Club website

Guidance for AI coding agents (and humans) working in this repo.

## Project

Static marketing site for **WZQ Badminton Club** (Pomona, CA).

- Live: https://wzqbadminton.com
- Repo: https://github.com/wzqbadminton/wez_web (public, branch `main`)
- Hosting: Netlify with continuous deployment from `main`.
- Registration app (separate, not in this repo): https://app.wzqbadminton.com

## File layout

```
.
├── index.html              # Single-page site, Chinese + English content
├── assets/
│   ├── css/styles.css      # All styles
│   └── js/main.js          # Scroll-reveal IntersectionObserver
├── logo.jpg                # Brand logo (also favicon)
├── wzq.png                 # About-section image
├── poster_wzq.pdf          # Printable poster with QR code (generated)
├── tools/
│   └── generate_poster.py  # Regenerates poster_wzq.pdf
├── netlify.toml            # Headers, redirects, cache rules
├── robots.txt
├── sitemap.xml
└── README.md
```

## Local preview

```powershell
python -m http.server 8000
# open http://localhost:8000
```

## Deploy

Push to `main` — Netlify auto-deploys in ~1 min.

```powershell
git add -A
git commit -m "describe change"
git push
```

## ⚠️ Encoding rule (CRITICAL)

`index.html` contains Chinese (UTF-8). **Never** edit via PowerShell pipelines such as `Get-Content | Set-Content` without explicit `[System.Text.UTF8Encoding]` — they corrupt UTF-8 multi-byte characters.

Safe edit methods:
- VS Code editor directly
- `replace_string_in_file` / `multi_replace_string_in_file` tools
- `create_file` for new files
- `[System.IO.File]::ReadAllText/WriteAllText` with `New-Object System.Text.UTF8Encoding $false` (no BOM)

## ⚠️ Python rule (CRITICAL)

**Never** install Python packages globally (`pip install ...` or `pip install --user ...`).
**Always** use the project virtual environment at `./.venv/`.

```powershell
# One-time setup
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tools\requirements.txt

# Run any project script
.\.venv\Scripts\python.exe tools\<script>.py
```

When adding a new Python dependency:
1. `.\.venv\Scripts\python.exe -m pip install <package>`
2. Add it to [tools/requirements.txt](tools/requirements.txt) with a version pin.

## Conventions

- **Brand colors:** `--court: #1f7a4d` (green), `--accent: #e63946` (red), `--ink: #14181f`. Defined in [assets/css/styles.css](assets/css/styles.css) `:root`.
- **Fonts:** Bebas Neue (display), Manrope (body), Noto Sans SC (Chinese). Loaded from Google Fonts with `preconnect`.
- **Spacing scale:** sections use `padding: 90px 24px` desktop, `60px 18px` mobile (≤760px).
- **All external links** use `target="_blank" rel="noopener"`.
- **Images** below the fold use `loading="lazy" decoding="async"`.

## Common tasks

### Add / edit player results
Edit the `#results` section directly in [index.html](index.html). Each `.player` card contains a `.player-head` (avatar initials + name + age category) and a `.achievements` `<ul>` with `gold | silver | bronze | none` class on each `<li>`.

### Add a nav link
Add an `<a>` inside `.nav-links` in [index.html](index.html). The `.nav-cta` class makes it a red CTA button.

### Regenerate the poster PDF

**Always use the project virtual environment — never `pip install` globally.**

First-time setup (once):
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tools\requirements.txt
```

Run the generator:
```powershell
.\.venv\Scripts\python.exe tools\generate_poster.py
```

Output: `poster_wzq.pdf` in the workspace root.

The `.venv/` folder is gitignored. Dependencies are pinned in [tools/requirements.txt](tools/requirements.txt).

### Add a redirect / header
Edit [netlify.toml](netlify.toml). Format docs: https://docs.netlify.com/configure-builds/file-based-configuration/

## Things NOT to do

- Don't introduce a build step (no Webpack/Vite/Tailwind compile). The repo deploys as-is — Netlify build command is empty, publish dir is `.`.
- Don't add tracking/analytics scripts without asking.
- Don't commit secrets — repo is public.
- Don't modify the JSON-LD `SportsClub` block in [index.html](index.html) without verifying it stays valid (https://search.google.com/test/rich-results).
- Don't rename `index.html`, `logo.jpg`, or `wzq.png` — they're referenced from CSS, the manifest, and the poster generator.

## Contact info (single source of truth)

If any of these change, update everywhere:
- Phone: `626-265-5766` → nav, contact card, CTA, footer, JSON-LD, poster
- Address: `2780 S Reservoir St, Pomona, CA` → contact card, footer, JSON-LD, poster
- Instagram: `@wzqbadmintonclub` → nav, contact card, footer, JSON-LD
- Registration: `https://app.wzqbadminton.com` → nav, hero, contact card, CTA banner, poster

## Footer attribution

The footer carries `Powered by D&G`. Keep it.