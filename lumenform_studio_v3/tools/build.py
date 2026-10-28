#!/usr/bin/env python3
"""Lumen&Form — static page generator (developer convenience only).

The deployable site in ../site is plain static HTML/CSS/JS and needs NO build
step. This script just regenerates those HTML files from one place, reading
prices, projects and contacts from site/assets/js/data.js — the same file the
browser uses — so Home, Pricing and Contact can never disagree.

    python3 tools/build.py
"""
import json, html, datetime, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SRC = (SITE / "assets/js/data.js").read_text(encoding="utf-8")
_start = SRC.index("{", SRC.index("window.LF_DATA"))
D = json.loads(SRC[_start: SRC.rindex("}") + 1])
C = D["contacts"]
BASE = "https://lumenform.studio"
YEAR = datetime.date.today().year
ASSET_V = "5"

def e(s):
    return html.escape(str(s), quote=True)

def pkg(i):
    return next(p for p in D["packages"] if p["id"] == i)

def proj(i):
    return next(p for p in D["projects"] if p["id"] == i)

def host(url):
    return re.sub(r"^https?://|/$", "", url)

NEWTAB = '<span class="visually-hidden"> (opens in a new tab)</span>'
ARROW = '<span class="arrow" aria-hidden="true">→</span>'
EXT = 'target="_blank" rel="noopener noreferrer"'
MAIL_ICON = ('<svg class="notice__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="1.5" aria-hidden="true" focusable="false"><rect x="3" y="5" width="18" height="14" rx="2"/>'
             '<path d="m3.5 6.5 8.5 6.5 8.5-6.5"/></svg>')

# ---------------------------------------------------------------- layout --
def head(title, desc, path, *, noindex=False, preload_hero=False, og_alt=None):
    canonical = BASE + path
    robots = "noindex, follow" if noindex else "index, follow"
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Lumen&Form",
        "url": BASE + "/",
        "logo": BASE + "/assets/img/brand/logo.svg",
        "email": C["studioEmail"],
        "description": "An independent web studio run by Mark Kalenchik, building websites for small businesses and personal brands.",
        "founder": {"@type": "Person", "name": "Mark Kalenchik", "email": C["personalEmail"], "sameAs": [C["linkedin"]]},
        "sameAs": [C["linkedin"]],
    }
    pre = ""
    if preload_hero:
        pre = ('<link rel="preload" as="image" type="image/webp" '
               'imagesrcset="/assets/img/work/alexboylan-960.webp 960w, /assets/img/work/alexboylan-1600.webp 1600w" '
               'imagesizes="(min-width: 1101px) 44vw, (min-width: 901px) 38vw, 86vw" fetchpriority="high">\n')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#F4F1EA">
<meta name="color-scheme" content="light">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lumen&amp;Form">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{BASE}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_alt or 'Lumen&Form — We build it first. You pay when you have seen it.')}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="{e(C['xHandle'])}">
<link rel="icon" href="/assets/img/brand/favicon.svg" type="image/svg+xml">
<script>
(function () {{
  var d = document.documentElement;
  d.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) {{
    d.classList.add('motion');
    /* Failsafe: if main.js never starts, drop motion so nothing stays hidden. */
    window.setTimeout(function () {{ if (!window.__lfReady) d.classList.remove('motion', 'io'); }}, 2000);
  }}
}})();
</script>
<link rel="preload" href="/assets/fonts/instrument-serif-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/golos-text-latin-var.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="/assets/css/styles.css?v={ASSET_V}">
<script src="/assets/js/data.js?v={ASSET_V}" defer></script>
<script src="/assets/js/main.js?v={ASSET_V}" defer></script>
<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

def header(active=None):
    def link(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<li><a class="site-nav__link" href="{href}"{cur}>{label}</a></li>'
    return f"""<header class="site-header" id="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="Lumen&amp;Form — home">
      <img class="brand__mono" src="/assets/img/brand/logo.svg" width="54" height="27" alt="">
      <span class="brand__name">Lumen&amp;Form</span>
    </a>
    <nav class="site-nav" aria-label="Primary">
      <ul class="site-nav__list">
        {link('/work/', 'Work', 'work')}
        {link('/pricing/', 'Pricing', 'pricing')}
        {link('/about/', 'About', 'about')}
      </ul>
    </nav>
    <div class="site-header__cta">
      <a class="btn btn--sm btn--accent" href="/contact/#enquiry">Request your preview</a>
    </div>
  </div>
</header>
"""

def footer():
    return f"""<footer class="site-footer on-dark">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="brand" href="/" aria-label="Lumen&amp;Form — home">
          <img class="brand__mono" src="/assets/img/brand/logo.svg" width="54" height="27" alt="">
          <span class="brand__name">Lumen&amp;Form</span>
        </a>
        <p class="footer-tagline">Independent web studio by Mark Kalenchik.</p>
      </div>
      <nav class="footer-col" aria-label="Footer">
        <h2>Studio</h2>
        <ul>
          <li><a href="/work/">Work</a></li>
          <li><a href="/pricing/">Pricing</a></li>
          <li><a href="/about/">About</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/privacy/">Privacy</a></li>
        </ul>
      </nav>
      <div class="footer-col">
        <h2>Get in touch</h2>
        <ul>
          <li><a href="mailto:{C['studioEmail']}">{C['studioEmail']}</a></li>
          <li><a href="{C['linkedin']}" {EXT}>LinkedIn{NEWTAB}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© <span data-year>{YEAR}</span> Lumen&amp;Form</p>
      <p>Websites for small businesses and personal brands.</p>
    </div>
  </div>
</footer>
</body>
</html>
"""

def page(name, body, **kw):
    active = kw.pop("active", None)
    out = head(**kw) + header(active) + '<main id="main" tabindex="-1">\n' + body + "\n</main>\n" + footer()
    target = SITE / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    print("wrote", target.relative_to(ROOT))

# ------------------------------------------------------------- snippets --
EXISTING = f"""<aside class="notice" aria-label="If you already received a preview">
  {MAIL_ICON}
  <p><strong>Already received your preview?</strong> Reply to my email with your changes or questions. No need to fill out another form. <a href="mailto:{C['personalEmail']}">{C['personalEmail']}</a></p>
</aside>"""

def picture_desktop(p, sizes, *, eager=False):
    k = p["id"]
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="/assets/img/work/{k}-960.webp 960w, /assets/img/work/{k}-1600.webp 1600w" sizes="{sizes}">'
            f'<img src="/assets/img/work/{k}-960.webp" width="1600" height="1000" {load} decoding="async" '
            f'alt="{e(p["name"])} preview homepage, desktop view"></picture>')

def picture_mobile(p, sizes, *, eager=False):
    k = p["id"]
    load = 'loading="eager"' if eager else 'loading="lazy"'
    return (f'<img src="/assets/img/work/{k}-m-360.webp" srcset="/assets/img/work/{k}-m-360.webp 360w, /assets/img/work/{k}-m-600.webp 600w" '
            f'sizes="{sizes}" width="600" height="1298" {load} decoding="async" alt="{e(p["name"])} preview homepage, mobile view">')

def frame(p, sizes, *, eager=False):
    return (f'<div class="frame"><div class="frame__bar" aria-hidden="true"><i></i><i></i><i></i><span>{e(host(p["url"]))}</span></div>'
            f'{picture_desktop(p, sizes, eager=eager)}</div>')

def work_item(p, idx, *, heading="h3"):
    return f"""<article class="work reveal">
  <a class="work__media" href="{p['url']}" {EXT} tabindex="-1" aria-hidden="true">
    <div class="work__desk">{frame(p, '(min-width: 901px) 52vw, 88vw')}</div>
    <div class="work__phone phone">{picture_mobile(p, '(min-width: 901px) 12vw, 24vw')}</div>
  </a>
  <div class="work__meta">
    <p class="work__index">{idx:02d}</p>
    <p class="work__cat">{e(p['category'])}</p>
    <{heading} class="work__name serif">{e(p['name'])}</{heading}>
    <p class="work__desc">{e(p['description'])}</p>
    <div class="work__foot">
      <span class="tag">{e(p['label'])}</span>
      <a class="link-arrow" href="{p['url']}" {EXT}>Explore preview{NEWTAB} {ARROW}</a>
    </div>
  </div>
</article>"""

def currency_switch(scope):
    opts = []
    for c in D["currencies"]:
        chk = " checked" if c["code"] == D["defaultCurrency"] else ""
        opts.append(f'<span class="currency__opt"><input type="radio" name="currency-{scope}" id="cur-{scope}-{c["code"]}" value="{c["code"]}"{chk}>'
                    f'<label for="cur-{scope}-{c["code"]}"><span class="visually-hidden">{e(c["name"])} </span><span aria-hidden="true">{c["label"]}</span></label></span>')
    return (f'<fieldset class="currency js-only" data-currency-switch><legend>Show prices in</legend>'
            f'<div class="currency__opts">{"".join(opts)}</div></fieldset>'
            f'<p class="visually-hidden" aria-live="polite" data-currency-live></p>')

def package_card(p, *, full=False):
    featured = p["id"] == "business"
    cls = "package package--featured" if featured else "package"
    label = f'<p class="package__label">{e(p["label"])}</p>' if p.get("label") else ""
    frm = '<span class="package__from">from</span>' if p["from"] else ""
    pay_cls = "package__pay package__pay--staged" if p["id"] == "extended" else "package__pay"
    pay_text = "30% after homepage approval, balance after final approval." if p["id"] == "extended" else p["payment"]
    feats = p["features"] if full else p["features"][: (4 if p["id"] != "extended" else 4)]
    items = "".join(f"<li>{e(f)}</li>" for f in feats)
    note = f'<p class="package__note">{e(p["featuresNote"])}</p>' if p.get("featuresNote") else ""
    btn = "btn--accent" if featured else "btn--ghost"
    return f"""<article class="{cls}">
  {label}
  <h3 class="package__name">{e(p['name'])}</h3>
  <p class="package__price">{frm}<span class="package__amount" data-price="{p['id']}">{p['prices'][D['defaultCurrency']]}</span><span class="package__unit">one-time build</span></p>
  <p class="package__summary">{e(p['summary'])}</p>
  <p class="{pay_cls}">{e(pay_text)}</p>
  <ul class="package__features">{items}</ul>
  {note}
  <div class="package__cta"><a class="btn {btn} btn--block" data-package-cta="{p['id']}" href="/contact/?package={p['id']}&amp;currency={D['defaultCurrency']}#enquiry">Choose {e(p['name'])} {ARROW}</a></div>
</article>"""

FAQ = [
    ("Is it really built before I pay?",
     "For One page and Business websites, yes: you review the complete preview and approve the final version before payment. Extended projects use staged payment: 30% after homepage approval and the balance after final approval."),
    ("Where is the site hosted? Who owns it?",
     "First-year hosting is included, and you receive the website files. Your domain remains yours. You can move to another host; any forms, booking tools or other third-party services may need to be reconnected."),
    ("How do I make changes later?",
     "Send the changes in writing. Small edits are included for 30 days after launch. Straightforward updates are normally handled within 48 hours once the content is available. Later work is scoped separately or covered by an agreed care arrangement."),
    ("Can I edit it myself?",
     "These websites are not drag-and-drop builders. You or another developer can edit the files, or you can send changes to me. If daily drag-and-drop editing is essential, a builder may be a better fit."),
    ("What do you need from me?",
     "To start, send your current website or business page and what you want the new site to do. For launch, we'll confirm the content, enquiry email and domain access. Never send passwords through the enquiry form."),
    ("How do I pay?",
     "Payment instructions and invoice details are confirmed before approval. One page and Business websites are paid after final approval; Extended projects use the staged terms shown above."),
    ("What about my domain?",
     "You keep ownership of it. I'll guide you through the required settings or use delegated access where your provider supports it. We'll preserve existing email-related records and confirm the connection before launch."),
    ("How will we work together?",
     "You work directly with Mark, remotely and in writing, so the scope, changes and decisions stay clear. Enquiries receive a reply within one business day."),
]
CARE_TEXT = ("First-year hosting is included. Small edits are included for 30 days. Later changes are scoped separately. "
             "From year two, optional hosting and care starts at US$9/month, or you can take the files and host elsewhere.")

def faq_list(items, heading="h3"):
    out = []
    for q, a in items:
        out.append(f"""<details class="faq__item">
  <summary><{heading} class="faq__q" style="font:inherit;margin:0">{e(q)}</{heading}><span class="faq__icon" aria-hidden="true"></span></summary>
  <div class="faq__answer"><p>{e(a)}</p></div>
</details>""")
    return '<div class="faq">' + "\n".join(out) + "</div>"

FINAL_CTA = f"""<section class="section final-cta on-dark" aria-labelledby="final-cta-title">
  <div class="container final-cta__grid">
    <h2 class="final-cta__title display reveal" id="final-cta-title">Let’s look at your <em>website.</em></h2>
    <div class="final-cta__body">
      <p>Send your current site, business page or a short description of what you need.</p>
      <div class="final-cta__actions">
        <a class="btn btn--accent" href="/contact/#enquiry">Request your preview {ARROW}</a>
        <a class="btn btn--ghost" href="mailto:{C['personalEmail']}">Email Mark</a>
      </div>
    </div>
    <p class="final-cta__aside">Already received your preview? Just reply to my email — or write to <a href="mailto:{C['personalEmail']}">{C['personalEmail']}</a>.</p>
  </div>
</section>"""

INCLUDED = [
    ("Your own domain", "The site launches on the domain you already own or register. It stays in your name, not the studio’s."),
    ("First-year hosting", "Hosting for the first twelve months is part of the build price. After that, optional care from US$9/month, or host it wherever you like."),
    ("Website files delivered", "You receive the site files at handover. Third-party tools such as booking or form services may need their own accounts if you move."),
    ("Mobile-first pages", "Layouts are designed for phones first, then composed for tablets and desktops — not squeezed down afterwards."),
    ("Contact and agreed booking integrations", "Contact forms are routed to your email at launch, and an existing booking tool can be connected where agreed."),
    ("Thirty days of small edits", "For 30 days after launch, changes to existing text, prices or supplied images are included."),
]

AUDIENCES = [
    ("Trades & construction", "Show the work and turn interest into quote requests."),
    ("Healthcare & professional services", "Explain services clearly and make the next enquiry easier."),
    ("Coaches, speakers & authors", "Give each offer a clear place and a clear next step."),
    ("Hospitality & venues", "Help guests explore the space and find the booking route."),
    ("Local services", "Make service areas, contact details and requests easy to find."),
    ("Bands & creators", "Bring the work together and make bookings easier to request."),
]

MARK_COPY = ("I’m Mark Kalenchik, the person behind Lumen&Form. I build websites for small businesses and personal brands. "
             "I prefer showing you the work to asking you to imagine it from a proposal. You’ll deal directly with me, "
             "with the scope, changes and payment terms agreed in writing.")

def identity_block(cls="identity reveal"):
    return f"""<div class="{cls}" aria-hidden="true">
  <!-- Founder portrait: add <img class="identity__portrait" src="/assets/img/mark.webp" width="800" height="1000" alt="Mark Kalenchik">
       as the first child of this block and remove aria-hidden. See README. -->
  <img class="identity__mono" src="/assets/img/brand/logo.svg" width="899" height="456" alt="">
  <div>
    <p class="identity__name">Mark<br><em>Kalenchik</em></p>
    <p class="identity__role"><span>Founder &amp; sole operator</span><span>Lumen&amp;Form</span></p>
  </div>
</div>"""

# ================================================================= HOME ==
def build_home():
    hero_p = proj("alexboylan")
    business = [p for p in D["projects"] if p["group"] == "business"]
    works = "\n".join(work_item(p, i + 1) for i, p in enumerate(business))
    packages = "\n".join(package_card(p) for p in D["packages"])
    included = "\n".join(
        f'<div class="included__item reveal"><span class="included__mark" aria-hidden="true">{i+1:02d}</span>'
        f'<h3 class="included__title">{e(t)}</h3><p class="included__text">{e(x)}</p></div>'
        for i, (t, x) in enumerate(INCLUDED))
    audiences = "\n".join(
        f'<div class="audience"><h3 class="audience__name">{e(n)}</h3><p class="audience__text">{e(t)}</p></div>'
        for n, t in AUDIENCES)
    home_faq = [FAQ[0], ("Who owns the website?", FAQ[1][1]), FAQ[3], ("What happens after the first year?", CARE_TEXT + " Care scope is agreed in writing.")]

    body = f"""
<section class="hero" aria-labelledby="hero-title">
  <div class="container hero__grid">
    <div class="hero__copy">
      <p class="eyebrow">Independent web studio · Mark Kalenchik</p>
      <h1 class="hero__title display" id="hero-title"><span class="line anim-line">We build it first.</span> <span class="line anim-line">You pay when <em>you’ve seen it.</em></span></h1>
      <p class="hero__lead lead anim-fade">Complete websites for small businesses and personal brands. Explore your working preview, request changes, and approve the final version before payment.</p>
      <p class="hero__qual anim-fade">For One page and Business websites. Extended projects use staged payments.</p>
      <div class="hero__actions anim-fade">
        <a class="btn btn--accent" href="/contact/#enquiry">Request your preview {ARROW}</a>
        <a class="btn btn--ghost" href="#selected-work">See the websites</a>
      </div>
      <p class="hero__support anim-fade">First-year hosting included. Files are yours. No required care plan.</p>
      <div class="hero__existing anim-fade">{EXISTING}</div>
    </div>
    <div class="hero__visual">
      <div class="light-reveal">
        <div class="hero__desk">{frame(hero_p, '(min-width: 1101px) 44vw, (min-width: 901px) 38vw, 86vw', eager=True)}</div>
        <div class="hero__phone phone">{picture_mobile(hero_p, '(min-width: 901px) 12vw, 28vw', eager=True)}</div>
      </div>
      <p class="hero__caption"><span class="meta"><strong style="color:var(--ink);font-weight:500">Alex Boylan</strong> · Independent preview · real desktop and mobile captures</span>
        <a class="link-arrow" href="{hero_p['url']}" {EXT}>Explore{NEWTAB} {ARROW}</a></p>
    </div>
  </div>
</section>

<div class="reveal-stage">
  <div class="reveal-stage__field" aria-hidden="true"></div>
  <section class="section reveal-stage__content on-dark" style="background:transparent" id="selected-work" aria-labelledby="work-title">
    <div class="container">
      <div class="section-head">
        <h2 class="h2" id="work-title">Real websites <em>you can explore.</em></h2>
        <p class="section-intro">Independent previews built from publicly available business materials. Open the sites, explore the pages and see the work for yourself.</p>
      </div>
      <div class="works">
{works}
      </div>
      <div class="works-note">
        <p class="meta">These previews are not official business websites or client endorsements.</p>
        <a class="link-arrow" href="/work/">All work, including concepts {ARROW}</a>
      </div>
    </div>
  </section>
</div>

<section class="section" id="process" aria-labelledby="process-title">
  <div class="container">
    <div class="section-head">
      <h2 class="h2 reveal" id="process-title">See the work. <em>Then decide.</em></h2>
      <p class="section-intro">Three steps, agreed in writing, with one person accountable from first message to launch.</p>
    </div>
    <ol class="steps" role="list">
      <li class="step reveal"><p class="step__num" aria-hidden="true">01</p><h3 class="step__title">We build it first.</h3><p class="step__text">We use your existing website and other agreed public materials to create a complete preview you can explore.</p></li>
      <li class="step reveal"><p class="step__num" aria-hidden="true">02</p><h3 class="step__title">You review. We refine.</h3><p class="step__text">Send one consolidated list of changes. One revision round is included before final approval, with straightforward changes usually turned around the same business day.</p></li>
      <li class="step reveal"><p class="step__num" aria-hidden="true">03</p><h3 class="step__title">Approve. Pay. Launch.</h3><p class="step__text">Once the final version is approved and payment and access are in place, we connect your domain and hand over the files.</p></li>
    </ol>
    <div class="process-note"><p class="notice notice--accent"><span><strong>Payment timing:</strong> One page and Business websites are paid after final approval. Extended projects have a 30% payment after homepage approval.</span></p></div>
  </div>
</section>

<section class="section section--ruled" id="included" aria-labelledby="included-title" style="border-top:1px solid var(--line)">
  <div class="container">
    <div class="section-head">
      <h2 class="h2 reveal" id="included-title">What every build <em>includes.</em></h2>
      <p class="section-intro">The practical things that make a website yours to run — explained, not just listed.</p>
    </div>
    <div class="included">
{included}
    </div>
  </div>
</section>

<section class="section" id="pricing" aria-labelledby="pricing-title" style="background:var(--paper-2)">
  <div class="container">
    <div class="section-head">
      <h2 class="h2 reveal" id="pricing-title">Clear prices, <em>agreed upfront.</em></h2>
      <p class="section-intro">One-time build prices. Regional prices are set for each currency — they are not live conversions.</p>
    </div>
    <div class="pricing-bar">
      {currency_switch('home')}
      <a class="link-arrow" href="/pricing/">Full pricing details and terms {ARROW}</a>
    </div>
    <div class="packages">
{packages}
    </div>
    <div class="terms-strip">
      <p><strong>Payment.</strong> One page and Business websites are paid after final approval. Extended projects: 30% after homepage approval, with the balance after final approval.</p>
      <p><strong>After launch.</strong> First-year hosting included. From year two, optional hosting and care starts at US$9/month — or take the files and host elsewhere.</p>
    </div>
  </div>
</section>

<section class="section" id="who" aria-labelledby="who-title">
  <div class="container">
    <div class="section-head">
      <h2 class="h2 reveal" id="who-title">Who it’s <em>for.</em></h2>
      <p class="section-intro">Small businesses and personal brands that need a clear, credible website and a simple route to an enquiry.</p>
    </div>
    <div class="audiences">
{audiences}
    </div>
    <p class="audiences-note meta">These describe who the studio is set up to help — not a list of past clients.</p>
  </div>
</section>

<section class="section" id="mark" aria-labelledby="mark-title" style="border-top:1px solid var(--line)">
  <div class="container mark">
    {identity_block()}
    <div class="mark__body">
      <h2 class="h2 reveal" id="mark-title">You’ll work <em>directly with me.</em></h2>
      <p class="mark__text">{e(MARK_COPY)}</p>
      <div class="mark__links">
        <a class="link-arrow" href="{C['linkedin']}" {EXT}>LinkedIn{NEWTAB} {ARROW}</a>
        <a class="link-arrow" href="mailto:{C['personalEmail']}">{C['personalEmail']}</a>
        <a class="link-arrow" href="/about/">More about the studio {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="faq" aria-labelledby="faq-title" style="border-top:1px solid var(--line)">
  <div class="container faq-wrap">
    <div class="faq-side">
      <h2 class="h2" id="faq-title">Straight <em>answers.</em></h2>
      <p class="section-intro" style="margin-top:20px">The questions owners usually ask first.</p>
      <p style="margin-top:20px"><a class="link-arrow" href="/pricing/#faq">All eight questions on Pricing {ARROW}</a></p>
    </div>
    {faq_list(home_faq)}
  </div>
</section>

{FINAL_CTA}
"""
    page("index.html", body,
         title="Lumen&Form — Websites built before you pay | Independent web studio",
         desc="An independent web studio run by Mark Kalenchik. Complete websites for small businesses and personal brands — explore your working preview and approve it before payment.",
         path="/", preload_hero=True)

# ================================================================= WORK ==
def build_work():
    business = [p for p in D["projects"] if p["group"] == "business"]
    fictional = [p for p in D["projects"] if p["group"] == "fictional"]
    experimental = [p for p in D["projects"] if p["group"] == "experimental"]
    works = "\n".join(work_item(p, i + 1) for i, p in enumerate(business))

    def mini(p, exp=False):
        cls = "mini-work mini-work--exp reveal" if exp else "mini-work reveal"
        return f"""<article class="{cls}">
  <a class="mini-work__media" href="{p['url']}" {EXT} tabindex="-1" aria-hidden="true">{frame(p, '(min-width: 761px) 46vw, 92vw')}</a>
  <div>
    <div class="mini-work__row"><p class="meta">{e(p['category'])}</p><span class="tag">{e(p['label'])}</span></div>
    <h3 class="mini-work__name serif" style="margin-top:8px">{e(p['name'])}</h3>
    <p style="margin-top:10px;color:var(--ink-2);max-width:30em">{e(p['description'])}</p>
    <p style="margin-top:8px"><a class="link-arrow" href="{p['url']}" {EXT}>Explore {('concept' if p['group']!='business' else 'preview')}{NEWTAB} {ARROW}</a></p>
  </div>
</article>"""

    body = f"""
<section class="page-head" aria-labelledby="page-title">
  <div class="container page-head__grid">
    <div class="page-head__title">
      <p class="eyebrow">Work</p>
      <h1 class="h1" id="page-title" style="margin-top:18px"><span class="anim-line" style="display:block">Websites you can open,</span> <em class="anim-line" style="display:block">not mockups.</em></h1>
    </div>
    <div class="page-head__intro anim-fade">
      <p>Every project below is a working website. Open it in a new tab, try it on your phone, click through the pages.</p>
      <p class="meta">Screens are real captures of each site as currently published.</p>
    </div>
  </div>
</section>

<section class="section on-dark" aria-labelledby="business-title">
  <div class="container">
    <div class="group-head">
      <h2 class="h3" id="business-title">Business previews</h2>
      <p class="meta">Independent previews built from publicly available business materials. They are not official business websites or client endorsements.</p>
    </div>
    <div class="works">
{works}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="fictional-title">
  <div class="container">
    <div class="group-head">
      <h2 class="h3" id="fictional-title">Business concepts</h2>
      <p class="meta">Fictional businesses, built to show how a service website can be structured for a specific trade.</p>
    </div>
    <div class="mini-works">
{chr(10).join(mini(p) for p in fictional)}
    </div>
  </div>
</section>

<section class="section section--tight" aria-labelledby="exp-title" style="border-top:1px solid var(--line)">
  <div class="container">
    <div class="group-head">
      <h2 class="h3" id="exp-title">Experimental concepts</h2>
      <p class="meta">Unofficial concepts exploring product and editorial design. Not affiliated with, or endorsed by, the projects they reference.</p>
    </div>
    <div class="mini-works">
{chr(10).join(mini(p) for p in experimental)}
    </div>
  </div>
</section>

{FINAL_CTA}
"""
    page("work/index.html", body, active="work",
         title="Work — Real websites you can explore | Lumen&Form",
         desc="Independent website previews and business concepts by Lumen&Form. Open each working site and explore the pages yourself.",
         path="/work/")

# ============================================================== PRICING ==
def build_pricing():
    packages = "\n".join(package_card(p, full=True) for p in D["packages"])
    rows = []
    for p in D["packages"]:
        cells = "".join(f'<td>{"from " if p["from"] else ""}{p["prices"][c["code"]]}</td>' for c in D["currencies"])
        rows.append(f'<tr><th scope="row">{e(p["name"])}</th>{cells}</tr>')
    heads = "".join(f'<th scope="col">{c["code"]}</th>' for c in D["currencies"])
    body = f"""
<section class="page-head" aria-labelledby="page-title">
  <div class="container page-head__grid">
    <div class="page-head__title">
      <p class="eyebrow">Pricing</p>
      <h1 class="h1" id="page-title" style="margin-top:18px"><span class="anim-line" style="display:block">One-time prices.</span> <em class="anim-line" style="display:block">Terms in plain sight.</em></h1>
    </div>
    <div class="page-head__intro anim-fade">
      <p>One page and Business websites are paid after you approve the final version. Extended projects use staged payments: 30% after homepage approval, the balance after final approval.</p>
    </div>
  </div>
</section>

<section class="section section--tight" style="padding-top:0" aria-labelledby="packages-title">
  <div class="container">
    <h2 class="visually-hidden" id="packages-title">Packages</h2>
    <div class="pricing-bar">
      {currency_switch('pricing')}
      <p class="currency-hint">Regional prices, not live currency conversions.</p>
    </div>
    <div class="packages">
{packages}
    </div>
  </div>
</section>

<section class="section section--tight" aria-labelledby="terms-title">
  <div class="container">
    <div class="section-head" style="margin-bottom:40px">
      <h2 class="h2" id="terms-title">The <em>terms.</em></h2>
      <p class="section-intro">Agreed in writing before anything is paid.</p>
    </div>
    <div class="term-blocks">
      <div class="term-block">
        <h3>Payment</h3>
        <p><strong>One-time build price.</strong> One page and Business websites are paid after final approval. <strong>Extended projects: 30% after homepage approval, with the balance after final approval.</strong></p>
        <p>Payment instructions and invoice details are confirmed before you approve.</p>
      </div>
      <div class="term-block">
        <h3>Launch</h3>
        <p>Standard launch is within 48 hours of final approval, payment and receiving the access needed for launch. Extended integrations may have a separately agreed schedule.</p>
        <p>The preview is a complete working website. Domain connection, authorised booking accounts and final form routing are completed at launch.</p>
      </div>
      <div class="term-block">
        <h3>Included in every package</h3>
        <ul>
          <li>The agreed website pages</li>
          <li>Mobile-first implementation</li>
          <li>Contact forms and agreed booking integrations</li>
          <li>First-year hosting</li>
          <li>Delivery of the website files</li>
          <li>One consolidated revision round before final approval</li>
          <li>Small edits for 30 days after launch</li>
        </ul>
      </div>
      <div class="term-block">
        <h3>Not included</h3>
        <ul>
          <li>Domain registration and renewal</li>
          <li>Paid third-party subscriptions and transaction fees</li>
          <li>New scope beyond the selected package</li>
        </ul>
        <p>Booking, form, payment or commerce services may need their own accounts, configuration or fees.</p>
      </div>
      <div class="term-block">
        <h3>Ownership</h3>
        <p>You keep your domain and receive the website files. There is no mandatory studio maintenance subscription — you can arrange hosting and development elsewhere.</p>
        <p>Third-party services may need to be reconnected under your own accounts if you move. Some photographs, fonts or other third-party assets come with their own licence terms.</p>
      </div>
      <div class="term-block">
        <h3>Extended projects</h3>
        <p>Scope and final price are agreed before the paid stage begins. Possible project types are not all included together at the starting price.</p>
        <p><strong>Shops:</strong> checkout, payment providers, shipping, tax configuration and other integrations are scoped individually — a catalogue alone is not a working shop.</p>
        <p><strong>Bilingual sites:</strong> translation responsibility and content supply are agreed upfront; professional translation is not included automatically.</p>
      </div>
    </div>

    <table class="region-table" style="margin-top:32px">
      <caption>All regional prices at a glance (one-time build)</caption>
      <thead><tr><th scope="col">Package</th>{heads}</tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
  </div>
</section>

<section class="section section--tight" id="faq" aria-labelledby="faq-title" style="border-top:1px solid var(--line)">
  <div class="container faq-wrap">
    <div class="faq-side">
      <h2 class="h2" id="faq-title">Questions, <em>answered.</em></h2>
      <div class="care" style="margin-top:32px;display:block" id="care" aria-labelledby="care-title">
        <h3 class="h3" id="care-title">After launch: hosting &amp; care</h3>
        <p class="care__price">from US$9<span style="font-size:1.1rem;font-family:var(--sans)">/month</span></p>
        <p class="meta" style="margin-top:6px">From year two · optional · always billed in USD</p>
        <p style="margin-top:16px;color:var(--ink-2)">{e(CARE_TEXT)}</p>
        <p style="margin-top:12px;color:var(--ink-2)">Care covers hosting, backups and small agreed content updates. <strong>Small edits</strong> mean changes to existing text, prices or supplied images. New pages, redesigns and new functionality are scoped separately. Care scope is confirmed in writing, and you can decline it and host elsewhere.</p>
      </div>
    </div>
    {faq_list(FAQ)}
  </div>
</section>

<section class="section section--tight" aria-labelledby="agency-title">
  <div class="container">
    <div class="agency">
      <div>
        <p class="meta">For studios and agencies</p>
        <h2 class="agency__title" id="agency-title" style="margin-top:8px">White-label builds for studios from US$100 per landing page.</h2>
        <p>For defined production-only scope using supplied design and content. Requirements and pricing are agreed separately.</p>
      </div>
      <a class="btn btn--ghost" href="mailto:{C['personalEmail']}?subject=White-label%20build">Discuss a white-label build</a>
    </div>
  </div>
</section>

{FINAL_CTA}
"""
    page("pricing/index.html", body, active="pricing",
         title="Pricing — One page, Business and Extended websites | Lumen&Form",
         desc="One-time website prices in USD, GBP and AUD. One page and Business sites are paid after final approval; Extended projects use staged payments. First-year hosting included.",
         path="/pricing/")

# ================================================================ ABOUT ==
def build_about():
    body = f"""
<section class="page-head" aria-labelledby="page-title">
  <div class="container page-head__grid">
    <div class="page-head__title">
      <p class="eyebrow">About</p>
      <h1 class="h1" id="page-title" style="margin-top:18px"><span class="anim-line" style="display:block">An independent web studio</span> <em class="anim-line" style="display:block">run by Mark Kalenchik.</em></h1>
    </div>
    <div class="page-head__intro anim-fade">
      <p>Lumen&amp;Form is one person, accountable for the whole job: building, revisions, launch and the small edits after it.</p>
    </div>
  </div>
</section>

<section class="section section--tight" style="padding-top:0" aria-labelledby="intro-title">
  <div class="container mark">
    {identity_block()}
    <div class="mark__body">
      <h2 class="h2" id="intro-title">Hello, <em>I’m Mark.</em></h2>
      <p class="mark__text">{e(MARK_COPY)}</p>
    </div>
  </div>
</section>

<section class="section section--tight" aria-labelledby="why-title" style="border-top:1px solid var(--line)">
  <div class="container about-grid">
    <div class="about-main prose">
      <h2 class="h2" id="why-title" style="margin:0 0 28px">Why show the <em>work first?</em></h2>
      <p class="lead">A proposal asks you to imagine a website. A preview lets you use one.</p>
      <p>You can open it on your phone, show it to a colleague and see whether your services, prices and contact routes make sense — before you commit to anything. It also makes feedback concrete: instead of debating a description, you point at the page and say what should change.</p>
      <p>For One page and Business websites, you only pay once you’ve approved the final version. Extended projects are larger, so they use staged payment: 30% after homepage approval and the balance after final approval.</p>
    </div>
    <aside class="about-aside">
      <h2 class="h3" style="margin-bottom:16px">Working together</h2>
      <p style="color:var(--ink-2)">Collaboration is remote and in writing — email first. Scope, revisions and payment terms are agreed in writing, so decisions are easy to look back on. Enquiries receive a reply within one business day.</p>
    </aside>
  </div>
</section>

<section class="section section--tight" aria-labelledby="stages-title">
  <div class="container">
    <h2 class="h2" id="stages-title" style="margin-bottom:40px">Preview, approval, <em>launch.</em></h2>
    <div class="stages">
      <div class="stage"><p class="stage__name"><em>Preview</em></p><p>A complete, working version of your website, hosted at a temporary address so you can explore every page. It isn’t connected to your domain yet, and forms or booking tools may still point to test settings.</p></div>
      <div class="stage"><p class="stage__name"><em>Approval</em></p><p>You send one consolidated list of changes, I apply them, and you confirm the final version in writing. That confirmation is the point where payment becomes due.</p></div>
      <div class="stage"><p class="stage__name"><em>Launch</em></p><p>Once payment and access are in place, I connect your domain, route the forms to your email, set up agreed integrations and hand over the files — usually within 48 hours.</p></div>
    </div>
  </div>
</section>

<section class="section section--tight" aria-labelledby="fit-title" style="border-top:1px solid var(--line)">
  <div class="container">
    <h2 class="h2" id="fit-title" style="margin-bottom:40px">An honest <em>fit.</em></h2>
    <div class="fit">
      <div class="fit__col fit__col--yes">
        <h3>A good fit</h3>
        <ul>
          <li>Business websites for small companies and local services</li>
          <li>Personal brands: coaches, speakers, authors, creators</li>
          <li>Clear service websites with a simple route to an enquiry or booking</li>
          <li>Owners who are happy to send changes in writing</li>
        </ul>
      </div>
      <div class="fit__col">
        <h3>Not the core offer</h3>
        <ul>
          <li>Complex web applications</li>
          <li>Customer portals, dashboards and account systems</li>
          <li>Sites that need daily drag-and-drop editing by the owner</li>
        </ul>
        <p>If daily drag-and-drop editing is essential, a website builder may suit you better — and that’s a perfectly good choice.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight" aria-labelledby="contact-title">
  <div class="container about-grid">
    <div class="about-main">
      <h2 class="h2" id="contact-title" style="margin-bottom:28px">Get in <em>touch.</em></h2>
      <ul class="channels" role="list">
        <li><span class="meta">Email Mark</span><a href="mailto:{C['personalEmail']}">{C['personalEmail']}</a></li>
        <li><span class="meta">LinkedIn</span><a href="{C['linkedin']}" {EXT}>linkedin.com/in/lumenform{NEWTAB}</a></li>
        <li><span class="meta">Studio email</span><a href="mailto:{C['studioEmail']}">{C['studioEmail']}</a></li>
      </ul>
      <p style="margin-top:28px"><a class="btn btn--accent" href="/contact/#enquiry">Request your preview {ARROW}</a></p>
    </div>
    <aside class="about-aside">
      <h2 class="h3" style="margin-bottom:16px">Elsewhere</h2>
      <ul class="channels channels--secondary" role="list">
        <li><span class="meta">Facebook</span><a href="{C['facebook']}" {EXT}>Mark Kalenchik{NEWTAB}</a></li>
        <li><span class="meta">X</span><a href="{C['x']}" {EXT}>{e(C['xHandle'])}{NEWTAB}</a></li>
        <li><span class="meta">Telegram</span><a href="{C['telegram']}" {EXT}>{e(C['telegramHandle'])}{NEWTAB}</a></li>
      </ul>
    </aside>
  </div>
</section>
"""
    page("about/index.html", body, active="about",
         title="About — Mark Kalenchik, independent web studio | Lumen&Form",
         desc="Lumen&Form is an independent web studio run by Mark Kalenchik. You work directly with one accountable person, remotely and in writing.",
         path="/about/")

# ============================================================== CONTACT ==
def build_contact():
    pk_opts = '<option value="">No package selected</option>' + "".join(
        f'<option value="{e(p["name"])}">{e(p["name"])}</option>' for p in D["packages"]) + '<option value="Not sure yet">Not sure yet</option>'
    cur_opts = "".join(f'<option value="{c["code"]}"{" selected" if c["code"]==D["defaultCurrency"] else ""}>{c["code"]} — {e(c["name"])}</option>' for c in D["currencies"])
    body = f"""
<section class="page-head" aria-labelledby="page-title" style="padding-bottom:clamp(32px,4vw,56px)">
  <div class="container page-head__grid">
    <div class="page-head__title">
      <p class="eyebrow">Contact</p>
      <h1 class="h1" id="page-title" style="margin-top:18px"><span class="anim-line" style="display:block">Tell me what your website</span> <em class="anim-line" style="display:block">needs to do.</em></h1>
    </div>
    <div class="page-head__intro anim-fade">
      <p>Send a few details. I’ll review the fit and reply within one business day.</p>
    </div>
  </div>
</section>

<section class="section section--tight" style="padding-top:0" id="enquiry" aria-labelledby="form-title">
  <div class="container contact-grid">
    <div class="contact-form-wrap">
      <h2 class="visually-hidden" id="form-title">Preview request form</h2>
      <p class="form-note" style="margin-bottom:24px">Tell me about your business. I’ll confirm whether the project is a fit and what happens next.</p>
      <form class="form" id="enquiry-form" name="preview-request" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="bot-field" accept-charset="UTF-8">
        <input type="hidden" name="form-name" value="preview-request">
        <p class="hp-field" aria-hidden="true"><label>Leave this field empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>

        <div class="selection" id="selection-banner" hidden>
          <p class="selection__text" id="selection-text" aria-live="polite"></p>
          <button type="button" class="selection__clear" id="selection-change">Change</button>
          <button type="button" class="selection__clear" id="selection-clear">Clear selection</button>
        </div>

        <div class="form-summary-error" id="form-errors" role="alert" hidden></div>

        <div class="form-row">
          <div class="field">
            <label for="f-name">Name <span class="req">(required)</span></label>
            <input class="input" id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="f-name-error">
            <p class="field__error" id="f-name-error"></p>
          </div>
          <div class="field">
            <label for="f-business">Business name <span class="req">(required)</span></label>
            <input class="input" id="f-business" name="business" type="text" autocomplete="organization" required aria-describedby="f-business-error">
            <p class="field__error" id="f-business-error"></p>
          </div>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="f-website">Current website or business page <span class="req">(optional)</span></label>
            <input class="input" id="f-website" name="website" type="text" inputmode="url" autocomplete="url" aria-describedby="f-website-hint" placeholder="yourbusiness.com or a social page">
            <p class="hint" id="f-website-hint">A website, Facebook, Instagram or directory link is fine.</p>
          </div>
          <div class="field">
            <label for="f-email">Email <span class="req">(required)</span></label>
            <input class="input" id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="f-email-error">
            <p class="field__error" id="f-email-error"></p>
          </div>
        </div>
        <div class="field">
          <label for="f-message">What should the new site do for you? <span class="req">(required)</span></label>
          <textarea class="textarea" id="f-message" name="message" required aria-describedby="f-message-hint f-message-error"></textarea>
          <p class="hint" id="f-message-hint">For example: get more quote requests, explain services clearly, take bookings. Please don’t include passwords or payment details.</p>
          <p class="field__error" id="f-message-error"></p>
        </div>

        <fieldset class="form-fieldset">
          <legend>Package interest <span class="req" style="font-weight:400;color:var(--meta)">(optional)</span></legend>
          <div class="form-row">
            <div class="field">
              <label for="f-package">Package</label>
              <select class="select" id="f-package" name="package">{pk_opts}</select>
            </div>
            <div class="field">
              <label for="f-currency">Pricing currency</label>
              <select class="select" id="f-currency" name="currency">{cur_opts}</select>
            </div>
          </div>
        </fieldset>

        <div class="form-actions">
          <button class="btn btn--accent" type="submit" id="form-submit">Request your preview</button>
          <p class="form-note">Your details are used only to reply to this enquiry. <a href="/privacy/">Privacy</a></p>
        </div>
        <p class="form-note">Already received a preview? Reply to my email instead, or write to <a href="mailto:{C['personalEmail']}">{C['personalEmail']}</a>.</p>
      </form>
    </div>

    <aside class="contact-aside" aria-label="About your enquiry">
      <div class="aside-block">
        <h2>What happens next</h2>
        <ol>
          <li>I read your enquiry and reply within one business day.</li>
          <li>If it’s a fit, I confirm the package, the scope and which materials I’ll build the preview from.</li>
          <li>You get a link to a complete working preview to review.</li>
        </ol>
      </div>
      <div class="aside-block">
        <h2>Prefer email?</h2>
        <p><a class="link-arrow" href="mailto:{C['personalEmail']}">{C['personalEmail']}</a></p>
        <p><a class="link-arrow" href="{C['linkedin']}" {EXT}>Message me on LinkedIn{NEWTAB} {ARROW}</a></p>
      </div>
      <div class="aside-block">
        <h2>Please don’t send</h2>
        <p>Passwords, domain logins, payment details or sensitive documents. Launch access is arranged separately and safely when the time comes.</p>
      </div>
    </aside>
  </div>
</section>
"""
    page("contact/index.html", body,
         title="Contact — Request your website preview | Lumen&Form",
         desc="Tell Mark what your website needs to do. Send a few details about your business and get a reply within one business day.",
         path="/contact/")

# ======================================================== SIMPLE PAGES ==
def build_thanks():
    body = f"""
<section class="simple" aria-labelledby="page-title">
  <div class="container"><div class="simple__inner">
    <p class="eyebrow">Enquiry received</p>
    <h1 class="h1" id="page-title">Thanks.</h1>
    <p class="lead">Thanks. Your enquiry has been received. I’ll review it and reply within one business day.</p>
    <p style="margin-top:16px;color:var(--ink-2)">If you need to add anything, email <a href="mailto:{C['personalEmail']}">{C['personalEmail']}</a>.</p>
    <div class="simple__actions">
      <a class="btn btn--ghost" href="/work/">Look through the work</a>
      <a class="btn btn--ghost" href="/pricing/">Review pricing &amp; terms</a>
    </div>
  </div></div>
</section>
"""
    page("thank-you/index.html", body, noindex=True,
         title="Thank you — Enquiry received | Lumen&Form",
         desc="Your enquiry has been received. Mark will reply within one business day.",
         path="/thank-you/")

def build_privacy():
    body = f"""
<section class="simple" aria-labelledby="page-title">
  <div class="container"><div class="simple__inner prose">
    <p class="eyebrow">Privacy</p>
    <h1 class="h1" id="page-title">Privacy</h1>
    <p class="lead">A short, plain description of what this website does with your information.</p>

    <h2>Enquiries</h2>
    <p>When you send the contact form, the details you enter — your name, business name, email, website link, message and any package or currency you select — are used to review and respond to your request. Nothing else is collected through the form.</p>

    <h2>Form processing</h2>
    <p>This website is hosted on Netlify, and enquiry form submissions are processed and stored by Netlify Forms so they can be delivered to the studio. Netlify’s own privacy practices apply to that processing.</p>

    <h2>No tracking, no sale</h2>
    <p>This website does not use advertising pixels or analytics tools. Enquiry data is not sold or shared for marketing.</p>
    <p>If you choose a pricing currency, that choice is remembered in your browser for the current visit only (session storage), so the contact form can show it. It isn’t sent anywhere unless you submit the form.</p>

    <h2>Portfolio websites</h2>
    <p>The preview and concept websites linked from this site are separate websites with their own practices. Please review each site before submitting information through it.</p>

    <h2>Questions</h2>
    <p>For any privacy question, or to ask about an enquiry you have sent, email <a href="mailto:{C['studioEmail']}">{C['studioEmail']}</a>.</p>
  </div></div>
</section>
"""
    page("privacy/index.html", body,
         title="Privacy | Lumen&Form",
         desc="How Lumen&Form handles enquiry information: used only to reply, processed by Netlify Forms, never sold. No tracking.",
         path="/privacy/")

def build_404():
    body = """
<section class="simple" aria-labelledby="page-title">
  <div class="container"><div class="simple__inner">
    <p class="eyebrow">404 · Page not found</p>
    <h1 class="h1" id="page-title">This page isn’t <em>here.</em></h1>
    <p class="lead">The link may be old or mistyped. Here’s where most people are heading:</p>
    <nav class="simple__links" aria-label="Helpful links">
      <a href="/work/"><strong>Work</strong><span>Real websites you can explore</span></a>
      <a href="/pricing/"><strong>Pricing</strong><span>Packages, payment and terms</span></a>
      <a href="/contact/"><strong>Contact</strong><span>Request your preview</span></a>
    </nav>
    <div class="simple__actions"><a class="btn btn--accent" href="/">Back to the homepage</a></div>
  </div></div>
</section>
"""
    page("404.html", body, noindex=True,
         title="Page not found | Lumen&Form",
         desc="This page could not be found.",
         path="/404.html")

def build_meta_files():
    urls = ["/", "/work/", "/pricing/", "/about/", "/contact/", "/privacy/"]
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod></url>")
    sm.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    print("wrote site/sitemap.xml, site/robots.txt")

if __name__ == "__main__":
    build_home(); build_work(); build_pricing(); build_about(); build_contact()
    build_thanks(); build_privacy(); build_404(); build_meta_files()
