# DermDesk site: launch checklist

## Done
- [x] Business details confirmed and filled in `CONFIG` in `build.py`: legal name, ABN, address, contact emails, effective date, video recording, data location, overseas countries, GST note, cancellation window, platform fee, governing state. No placeholders remain on the site.
- [x] SEO basics: unique titles and descriptions, canonical links, Open Graph and Twitter tags with preview images, JSON-LD (Organization, WebSite, FAQPage), `sitemap.xml` and `robots.txt`.

## Still open
- [ ] Privacy Policy and Terms reviewed by an Australian lawyer (they're drafts written to match the site, not legal advice).
- [ ] Confirm the defaults set without the client: reply time "two business days", minimum age 18, refunds take 5–10 business days. Change them in `CONFIG` if wrong.
- [ ] Contact form: without `FORM_ENDPOINT` it opens the visitor's email app. A real endpoint (e.g. Formspree or a serverless function) is better.
- [ ] Hosting and dermdesk.com.au DNS.
- [ ] Credit or licence check for the new Pexels photo (Gustavo Fring, #7446685). Pexels licence allows commercial use without attribution.
- [ ] After go-live: test the pages in Google's Rich Results Test, check link previews on social media, and submit `https://dermdesk.com.au/sitemap.xml` in Google Search Console.
