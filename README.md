# WZQ Badminton Club — Website

Static site for **WZQ Badminton Club** (Pomona, CA).
Live: https://wzqbadminton.com

## Structure

```
.
├── index.html          # Page markup
├── assets/
│   ├── css/styles.css  # All styles
│   └── js/main.js      # Scroll-reveal interactions
├── logo.jpg            # Brand logo
├── wzq.png             # About-section image
├── robots.txt
├── sitemap.xml
└── netlify.toml        # Hosting config (headers, redirects, caching)
```

## Local preview

Any static server works. Examples:

```bash
# Python 3
python -m http.server 8000

# Node (npx)
npx serve .
```

Then open http://localhost:8000.

## Deploy

Hosted on Netlify. Push to `main` (or drag-and-drop the folder in the Netlify UI):

```bash
git add .
git commit -m "describe change"
git push
```

## Editing notes

- `index.html` contains Chinese (UTF-8). Edit with a UTF-8-aware editor — do NOT pipe through PowerShell `Get-Content | Set-Content` without explicit UTF-8 encoding.
- Player results live directly in `index.html` under the `#results` section.
