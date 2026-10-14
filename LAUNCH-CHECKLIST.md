# DermDesk site: details needed from the client before launch

Fill these in `CONFIG` at the top of the subpage section in `build.py`, then run `python3 build.py`.
Until then they show on the site as yellow highlighted placeholders.

| Key | What we need | Example |
|---|---|---|
| LEGAL_NAME | Registered business name | DermDesk Pty Ltd |
| ABN | ABN | 12 345 678 901 |
| ADDRESS | Postal address for privacy requests and notices | PO Box 123, Sydney NSW 2000 |
| EMAIL_SUPPORT | General / account help inbox | hello@dermdesk.com.au |
| EMAIL_PROS | Inbox for dermal professionals and applications | partners@dermdesk.com.au |
| EMAIL_PRIVACY | Privacy Officer inbox | privacy@dermdesk.com.au |
| EFFECTIVE_DATE | Date the policies take effect | 1 November 2026 |
| VIDEO_RECORDING | Are video consults recorded? | Consultations are not recorded. |
| DATA_LOCATION | Where app data is hosted | We store your information on servers in Australia. |
| OVERSEAS_COUNTRIES | Countries where providers may hold data | the United States |
| GST_NOTE | Do prices include GST? | " and include GST where it applies" |
| CANCEL_WINDOW | Free cancellation cut-off | 24 hours |
| PLATFORM_FEE | DermDesk's cut of each consult | 15% of each consultation fee |
| GOVERNING_STATE | State whose law governs the terms | New South Wales |
| FORM_ENDPOINT | Where the contact form posts (optional) | Formspree / Cloudflare function URL |

Already set as sensible defaults (change if wrong): reply time "two business days", minimum age 18, refunds take 5–10 business days.

## Before go-live
- [ ] Privacy Policy and Terms reviewed by an Australian lawyer (they're drafts written to match the site, not legal advice).
- [ ] Contact form: without FORM_ENDPOINT it opens the visitor's email app. A real endpoint is better.
- [ ] Hosting and dermdesk.com.au DNS.
- [ ] Credit or licence check for the new Pexels photo (Gustavo Fring, #7446685). Pexels licence allows commercial use without attribution.
