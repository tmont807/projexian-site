# projexian-site

Source for projexian.com. `build.py` generates the static site into `dist/`; GitHub Actions rebuilds and deploys it to GitHub Pages on every push and every morning with fresh opportunity data.

- Pages, copy and layout: `build.py`
- Styles and scripts: `assets/`
- Photos (web sizes): `img_out/`, credits in `credits.json`
- Live data: `data/` (refreshed by the workflow from tmont807/sam-packages)
