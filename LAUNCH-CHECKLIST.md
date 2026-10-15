# DermDesk site: launch checklist

## Done
- [x] Business details confirmed and filled in `CONFIG` in `build.py`: legal name, ABN, address, contact emails, effective date, video recording, data location, overseas countries, GST note, cancellation window, platform fee, governing state. No placeholders remain on the site.
- [x] Defaults confirmed by the client: reply time "two business days", minimum age 18, refunds take 5–10 business days.
- [x] Pexels photo (Gustavo Fring, #7446685) checked: the Pexels licence allows commercial use without attribution.
- [x] SEO basics: unique titles and descriptions, canonical links, Open Graph and Twitter tags with preview images, JSON-LD (Organization, WebSite, FAQPage), `sitemap.xml` and `robots.txt`.
- [x] Contact form sends to Formspree (`FORM_ENDPOINT` in `CONFIG`).

## Still open
- [ ] Privacy Policy and Terms reviewed by an Australian lawyer (they're drafts written to match the site, not legal advice).
- [ ] Hosting and dermdesk.com.au DNS.
- [ ] After go-live: send a test message through the contact form and check it arrives in the inbox set up in Formspree (Formspree may ask to confirm the form on the first submission).
- [ ] After go-live: test the pages in Google's Rich Results Test, check link previews on social media, and submit `https://dermdesk.com.au/sitemap.xml` in Google Search Console.
