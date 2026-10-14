"""Build the static DermDesk site from the unpacked Claude Design templates.

Usage: python3 build.py   (writes ./site)
"""
import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "_unpacked")
OUT = os.path.join(ROOT, "site")
ACCENT = "#6f7460"

PAGES = {
    "index.html": {
        "dir": "member",
        "title": "DermDesk | Online skin consultations with dermal professionals",
        "desc": "See a qualified dermal professional over video, from home. Get a treatment plan made for your skin, track your progress and message your dermal professional between consults.",
        "assets": {
            "2ac21878-e10a-444c-bb74-fcc6feff3a8a": "assets/logo-sage.svg",
            "bca02ea1-8953-4ed5-92ba-01e134b1ec19": "assets/mark-sage.svg",
            "cb02e7a0-f23a-47e0-a251-cd7e5889a173": "assets/member-hero.jpg",
            "2925046c-943e-4c72-86c5-abbddaebaf5e": "assets/member-routine.jpg",
            "1ccd2869-e560-4af2-9c42-beeddf19e776": "assets/fonts/fraunces-latin.woff2",
            "dd0182c3-46f7-4712-81d1-076df342d303": "assets/fonts/inter-latin.woff2",
        },
    },
    "clinicians.html": {
        "dir": "clinician",
        "title": "DermDesk for dermal professionals | Consult clients online",
        "desc": "The telehealth platform for dermal professionals. Consult clients over video, build treatment plans and get paid through Stripe, on your own hours.",
        "assets": {
            "7f8c9a0c-f69d-4359-8cd1-33b67ee0f11d": "assets/logo-cream.svg",
            "2e06af46-89b6-401c-92f2-84a1fba0cdbf": "assets/mark-sage.svg",
            "663cddf2-ef1e-4626-99a9-f774f89d4137": "assets/pro-consult.jpg",
            # replaced per client feedback 2026-10-14 (Pexels, Gustavo Fring #7446685)
            "f6b283ac-38dc-4d69-bb40-790b2bee8beb": ("assets/pro-facial.jpg", "pro-facial.jpg"),
            "749df01e-8fc6-40f1-8a88-f18c50dc63b8": "assets/fonts/fraunces-latin.woff2",
            "3ba2876c-b44f-43fe-b774-cf0ad8321cc5": "assets/fonts/inter-latin.woff2",
        },
    },
}

# Client feedback (Karlee, Oct 2026). Specific phrases first; DCT is protected from
# the generic "clinician" -> "dermal professional" rules below.
DCT = "\x00DCT\x00"
COPY = [
    (r"Qualified skin clinicians who have applied", f"Qualified {DCT} who have applied"),
    (r"qualified clinicians, across Australia", f"qualified {DCT}, across Australia"),
    (r"The telehealth platform for skin clinicians", f"The telehealth platform for {DCT}"),
    (r"Qualified skin clinicians, whether", f"Qualified {DCT}, whether"),
    (r"Cosmetic injectables", "Cosmetic treatments"),
    (r"A smiling clinician in a white coat holding her stethoscope",
     "A dermal professional applying a face mask during a facial treatment"),
    (r"\bskin clinicians\b", "dermal professionals"),
    (r"\bskin clinician\b", "dermal professional"),
    (r"\bDermal Clinician\b", "Dermal Professional"),
    (r"\bClinic-based clinicians\b", "Clinic-based dermal professionals"),
    (r"\bclinician’s\b", "dermal professional’s"),
    (r"\bClinicians\b", "Dermal professionals"),
    (r"\bClinician\b", "Dermal professional"),
    (r"\bclinicians\b", "dermal professionals"),
    (r"\bclinician\b", "dermal professional"),
]


def recopy(text):
    for pat, rep in COPY:
        text = re.sub(pat, rep, text)
    return text.replace(DCT, "dermal clinicians and therapists")


def apply_copy(html):
    # Text nodes
    html = re.sub(r">([^<]+)<", lambda m: ">" + recopy(m.group(1)) + "<", html)
    # Human-readable attributes
    html = re.sub(r'\b(alt|aria-label|title)="([^"]*)"',
                  lambda m: f'{m.group(1)}="{recopy(m.group(2))}"', html)
    return html


SC_IF_CLASS = {
    "navFull": "dd-navfull",
    "navCompact": "dd-navcompact",
    "moreShown": "dd-more",
    "menuShown": "dd-menu-open",
    "menuClosed": "dd-menu-closed",
    "wide": "dd-wide",
}


def convert(html):
    # sc-if blocks -> display:contents wrappers toggled by CSS (or unwrapped)
    def sc_if(m):
        key = m.group(1)
        if key in ("showTop", "showBottom"):
            return "<div style=\"display: contents;\">"
        return f'<div class="{SC_IF_CLASS[key]}">'
    html = re.sub(r'<sc-if value="\{\{(\w+)\}\}"[^>]*>', sc_if, html)
    html = html.replace("</sc-if>", "</div>")
    html = re.sub(r"<(/?)sc-raw-(\w+)", r"<\1\2", html)
    html = html.replace("sc-camel-view-box=", "viewBox=")
    html = html.replace('sc-camel-on-click="{{toggleMenu}}"', 'data-dd="toggle-menu"')
    html = html.replace('sc-camel-on-click="{{toggleMore}}"', 'data-dd="toggle-more"')
    html = html.replace('sc-camel-on-click="{{closeMenu}}"', 'data-dd="close-menu"')
    html = html.replace("{{accent}}", ACCENT)
    html = html.replace("{{menuExpanded}}", "false").replace("{{moreExpanded}}", "false")
    html = html.replace("{{menuLabel}}", "Open menu")
    html = html.replace('href="Main.dc.html"', 'href="/"')
    html = html.replace('href="Clinicians.dc.html"', 'href="/clinicians"')
    html = re.sub(r'href="https://dermdesk\.com\.au/(about|contact|privacy|terms)"', r'href="/\1"', html)
    # FAQ +/x icon: rotate via CSS on [open] instead of a baked-in rotation on the first item
    html = re.sub(r'(<summary[^>]*>.*?<span style="[^"]*?)\s*transform: rotate\(45deg\);', r'\1', html)
    left = re.findall(r"\{\{[^}]*\}\}|sc-[a-z-]+", html)
    assert not left, f"unconverted directives: {set(left)}"
    return html


CSS = """
.dd-navfull,.dd-navcompact,.dd-menu-closed,.dd-wide{display:contents}
.dd-more,.dd-menu-open{display:none}
.dd-more.is-open,[data-menu="open"] .dd-menu-open{display:contents}
[data-menu="open"] .dd-menu-closed{display:none}
@media (max-width:1179.98px){.dd-navfull{display:none}}
@media (min-width:1180px){.dd-navcompact,.dd-menu-open,[data-menu="open"] .dd-menu-open{display:none}}
@media (max-width:899.98px){.dd-wide{display:none}}
html{scroll-behavior:smooth;scroll-padding-top:88px}
details>summary::-webkit-details-marker{display:none}
details>summary>span:last-child{transition:transform .2s ease}
details[open]>summary>span:last-child{transform:rotate(45deg)}
"""

JS = """
(function(){
  var root=document.documentElement;
  function setMenu(open){
    if(open)root.setAttribute('data-menu','open');else root.removeAttribute('data-menu');
    document.querySelectorAll('[data-dd="toggle-menu"]').forEach(function(b){
      b.setAttribute('aria-expanded',open?'true':'false');
      b.setAttribute('aria-label',open?'Close menu':'Open menu');
    });
  }
  function setMore(open){
    document.querySelectorAll('.dd-more').forEach(function(m){m.classList.toggle('is-open',open)});
    document.querySelectorAll('[data-dd="toggle-more"]').forEach(function(b){b.setAttribute('aria-expanded',open?'true':'false')});
  }
  document.addEventListener('click',function(e){
    var t=e.target.closest('[data-dd]');
    var act=t&&t.getAttribute('data-dd');
    if(act==='toggle-menu'){setMenu(root.getAttribute('data-menu')!=='open');return}
    if(act==='close-menu'){setMenu(false);return}
    if(act==='toggle-more'){setMore(!document.querySelector('.dd-more.is-open'));return}
    if(!e.target.closest('.dd-more'))setMore(false);
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){setMenu(false);setMore(false)}});
  window.addEventListener('resize',function(){if(window.innerWidth>=1180)setMenu(false);else setMore(false)});
})();
"""


def build_page(name, cfg):
    d = os.path.join(SRC, cfg["dir"])
    tpl = open(os.path.join(d, "template.html"), encoding="utf-8").read()
    fonts = re.search(r"<helmet>\s*<style>(.*?)</style>", tpl, re.S).group(1)
    # keep only the latin @font-face blocks (served locally)
    blocks = re.findall(r"/\* latin \*/\s*(@font-face\s*\{.*?\})", fonts, re.S)
    body = re.search(r"</helmet>\s*(.*?)\s*</x-dc>", tpl, re.S).group(1)
    for uuid, path in cfg["assets"].items():
        if isinstance(path, tuple):
            path, src = path[0], os.path.join(SRC, path[1])
        else:
            src = os.path.join(d, next(f for f in os.listdir(d) if f.startswith(uuid)))
        dst = os.path.join(OUT, path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        body = body.replace(f'"{uuid}"', f'"/{path}"')
        blocks = [b.replace(f'"{uuid}"', f'"/{path}"') for b in blocks]
    body = apply_copy(convert(body))
    if name == "clinicians.html":
        body = body.replace('href="#how-it-works"', 'href="/#how-it-works"').replace('href="#pricing"', 'href="/#pricing"')
    font_css = "\n".join(blocks)
    write_html(name, cfg["title"], cfg["desc"], font_css, body)
    return body, font_css


def write_html(name, title, desc, font_css, body, extra_head=""):
    html = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#FFFCF5">
<link rel="icon" type="image/svg+xml" href="/assets/mark-sage.svg">
<link rel="preload" href="/assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>
{font_css}
body{{margin:0;background:#FFFCF5}}
{CSS.strip()}
</style>
{extra_head}</head>
<body>
{body}
<script>{JS.strip()}</script>
</body>
</html>
"""
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(html)


# ---- About / Contact / Privacy / Terms -------------------------------------
# Business details the client must confirm. None = not known yet: shown on the
# page as a yellow highlighted placeholder so it can't be missed before launch.
CONFIG = {
    "LEGAL_NAME": "Karlee Jayne Sandland",
    "ABN": "68 462 811 099",
    "ADDRESS": "3 Porter Road, Warrnambool VIC 3280",  # postal address for privacy requests / notices
    "EMAIL_SUPPORT": None,       # e.g. hello@dermdesk.com.au
    "EMAIL_PROS": None,          # e.g. partners@dermdesk.com.au
    "EMAIL_PRIVACY": None,       # e.g. privacy@dermdesk.com.au
    "EFFECTIVE_DATE": "14 October 2026",  # date the policies go live
    "FORM_ENDPOINT": "",         # contact form POST URL; empty = opens visitor's email app
    "REPLY_TIME": "two business days",
    "MIN_AGE": "18",
    "UNDER_AGE_POLICY": "If you are under 18, please don’t create an account or book a consultation.",
    "VIDEO_RECORDING": "Consultations are not recorded, and we do not store the audio or video of your consultation.",
    "DATA_LOCATION": "Your personal information, including health information, is stored on servers located in the United States.",
    "OVERSEAS_COUNTRIES": "the United States",
    "GST_NOTE": " and include GST where applicable",  # keep leading space
    "CANCEL_WINDOW": "48 hours",
    "REFUND_DAYS": "5–10 business days",
    "PLATFORM_FEE": "5% of each consultation fee",
    "GOVERNING_STATE": "Victoria",
}

SUBPAGES = {
    "about.html": ("About DermDesk", "DermDesk connects people across Australia with qualified dermal clinicians and therapists over video, with ongoing support after every consult."),
    "contact.html": ("Contact DermDesk", "Get in touch with DermDesk about your account, consultations or joining as a dermal professional."),
    "privacy.html": ("Privacy Policy | DermDesk", "How DermDesk collects, uses, shares and protects your personal and health information."),
    "terms.html": ("Terms of Service | DermDesk", "The terms that apply when you use DermDesk as a client or a dermal professional."),
}


def fill(html, todo):
    def val(key, in_text):
        v = CONFIG[key]
        if v is not None:
            return v
        todo.add(key)
        label = key.replace("_", " ").lower()
        return f'<mark class="dd-todo">[{label}]</mark>' if in_text else ""
    # attributes and scripts get plain values; text nodes get a visible marker
    def outside_text(m):
        return re.sub(r"\{\{(\w+)\}\}", lambda k: val(k.group(1), False), m.group(0))
    html = re.sub(r"<script.*?</script>|<[^>]+>", outside_text, html, flags=re.S)
    return re.sub(r"\{\{(\w+)\}\}", lambda k: val(k.group(1), True), html)


def build_subpages(home_body, font_css):
    wrapper = home_body[:home_body.index(">") + 1]
    header = home_body[home_body.index("<header"):home_body.index("</header>") + 9]
    footer = home_body[home_body.index("<footer"):home_body.index("</footer>") + 9]
    chrome = lambda h: re.sub(r'href="#', 'href="/#', h)
    header, footer = chrome(header), chrome(footer)
    shutil.copyfile(os.path.join(ROOT, "pages", "pages.css"), os.path.join(OUT, "assets", "pages.css"))
    todo = set()
    for name, (title, desc) in SUBPAGES.items():
        main = open(os.path.join(ROOT, "pages", name), encoding="utf-8").read()
        heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', main)
        toc = "".join('<li><a href="#%s">%s</a></li>' % (i, re.sub(r"^\d+\. ", "", t)) for i, t in heads)
        main = main.replace("<ol></ol>", f"<ol>{toc}</ol>")
        main = fill(main, todo)
        body = f"{wrapper}\n{header}\n<main>\n{main}\n</main>\n{footer}\n</div>"
        write_html(name, title, desc, font_css, body,
                   '<link rel="stylesheet" href="/assets/pages.css">\n')
    return todo


if __name__ == "__main__":
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    bodies = {}
    for name, cfg in PAGES.items():
        body, font_css = build_page(name, cfg)
        bodies[name] = body
        text = re.sub(r'href="[^"]*"', "", body).replace("dermal clinicians and therapists", "")
        left = re.findall(r"(?i)[^>]{0,40}clinician[^<]{0,40}", text)
        print(name, "remaining 'clinician' text:", left or "none")
    todo = build_subpages(bodies["index.html"], font_css)
    # Clean URLs (/about -> about.html) on Apache hosts; Netlify/Vercel/Cloudflare Pages do this already
    open(os.path.join(OUT, ".htaccess"), "w").write(
        "Options -MultiViews\nRewriteEngine On\n"
        "RewriteCond %{REQUEST_FILENAME} !-f\nRewriteCond %{REQUEST_FILENAME}.html -f\n"
        "RewriteRule ^(.+?)/?$ $1.html [L]\n")
    print("placeholders still to confirm:", ", ".join(sorted(todo)) or "none")
    print("built ->", OUT)
