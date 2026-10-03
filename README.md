# Xicheng Gong — Academic Homepage

Personal academic homepage: https://gxccc123.github.io/

The site is a small static page with English and Chinese text, selected papers,
research figures, education, and email contact links.

## Update

1. Edit paper metadata and contact details in `content.json`.
2. Edit the biography or page structure in `build.py`.
3. Edit the style and language switcher in `docs/styles.css` and `docs/app.js`.
4. Run `python3 build.py` and review `docs/index.html`.
5. Commit and push the changes to `main`.

GitHub Pages publishes the `/docs` directory from `main`. The `.nojekyll` file
keeps the generated HTML and assets unchanged. No runtime dependencies or
server-side services are needed.

The repository intentionally contains only homepage source files and the paper
assets used on the site.
