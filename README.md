# DermDesk marketing site

Plain static HTML/CSS with a little vanilla JS. There's no framework, no npm install and no build step needed to deploy.

## Deploy

Upload the contents of **`site/`** to the web root for `dermdesk.com.au`.

```
site/
  index.html          /             (clients)
  clinicians.html     /clinicians   (dermal professionals)
  about.html          /about
  contact.html        /contact
  privacy.html        /privacy
  terms.html          /terms
  assets/             images, fonts, pages.css, og-*.jpg social previews
  sitemap.xml         all public pages, for search engines
  robots.txt          allows crawling, points to the sitemap
  .htaccess           clean URLs on Apache
```

Links use clean URLs (`/about`, not `/about.html`) and root-relative paths, so the site must be served from the domain root.

- **Cloudflare Pages / Netlify / Vercel:** clean URLs work out of the box. Set the publish directory to `site`, with no build command.
- **Apache (cPanel etc.):** the included `.htaccess` handles it. Make sure hidden files are uploaded.
- **nginx:** add `try_files $uri $uri.html $uri/ =404;` to the `location /` block.

Links out to the app (`app.dermdesk.com.au/signup`, `/login`, `/apply`) are hard-coded and assume that subdomain.

## Before going live

See `LAUNCH-CHECKLIST.md`. All business details are filled in; any `CONFIG` value set back to `None` shows as a yellow placeholder on the Contact, Privacy and Terms pages.

- **Contact form:** it posts JSON `{role, name, email, subject, message}` to `FORM_ENDPOINT` (set it in `build.py` CONFIG). Any endpoint that returns 2xx works, e.g. Formspree or a serverless function. If it's left empty, the form opens the visitor's email app instead.

## Editing

`site/` is generated. Don't hand-edit it, or the changes will be lost on the next build.

```
python3 build.py      # Python 3.9+, no dependencies; regenerates site/
```

- `_unpacked/member|clinician/template.html` hold the home and dermal professionals pages, exported from the Claude Design file.
- `pages/*.html` and `pages/pages.css` hold the About, Contact, Privacy and Terms content.
- `build.py` contains:
  - `COPY`: client wording rules. "Clinician" never appears bare; use "dermal professional(s)" or "dermal clinicians and therapists".
  - `CONFIG`: business details used to fill the placeholders.
  - `PAGES` and `SUBPAGES`: titles and meta descriptions.
  - `SITE_URL`: the domain used for canonical links, Open Graph tags, JSON-LD and the sitemap.
- `_unpacked/og-home.jpg` and `_unpacked/og-pro.jpg` are 1200×630 social preview crops of the hero photos (`og-pro` is used on /clinicians).
- Structured data (JSON-LD) is generated: Organization and WebSite on the home page, and FAQPage from each page's own FAQ, so it always matches the visible text.
