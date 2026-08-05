#!/usr/bin/env python3
"""
Full brand showcase builder.
Each brand = unique visual system + full multi-section brand homepage (≈20 sections),
not a thin 4-block demo.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs" / "showcase"


def img(seed: str, w=1200, h=1500) -> str:
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


JS = r"""(() => {
  const top = document.querySelector("[data-top]");
  if (top) {
    const on = () => top.classList.toggle("scrolled", scrollY > 8);
    on(); addEventListener("scroll", on, { passive: true });
  }
  const io = new IntersectionObserver(
    (es) => es.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
    { threshold: 0.1 }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  document.querySelectorAll("[data-tabs] button, .sizes button").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.parentElement.querySelectorAll("button").forEach((b) => b.classList.remove("on","active"));
      btn.classList.add("on");
      btn.classList.add("active");
    });
  });
  document.querySelectorAll("[data-gal]").forEach((gal) => {
    const main = gal.querySelector("[data-main]");
    gal.querySelectorAll(".thumbs button").forEach((btn) => {
      btn.addEventListener("click", () => {
        gal.querySelectorAll(".thumbs button").forEach((b) => b.classList.remove("on"));
        btn.classList.add("on");
        const i = btn.querySelector("img");
        if (main && i) main.src = i.src.replace(/\/\d+\/\d+/, "/1200/1500");
      });
    });
  });
  const sticky = document.querySelector(".sticky-atc");
  const atc = document.querySelector("[data-atc]");
  if (sticky && atc) {
    new IntersectionObserver(([e]) => sticky.classList.toggle("show", !e.isIntersecting), { threshold: 0 }).observe(atc);
  }
})();"""


# ── Shared section HTML builders (brand-agnostic markup, themed via CSS) ──────

def cards(seed, products, href="product/", n=4, start=0):
    out = []
    for i, (name, price) in enumerate(products[start:start + n]):
        out.append(
            f'<a class="card" href="{href}"><div class="ph"><img src="{img(seed + "-p" + str(start+i), 800, 1000)}" alt="" loading="lazy" /></div>'
            f"<div class='meta'><h3>{name}</h3><p class='price'>{price}</p></div></a>"
        )
    return "".join(out)


def cats(seed, links, href="collection/"):
    return "".join(
        f'<a class="cat" href="{href}"><div class="ph"><img src="{img(seed + "-c" + str(i), 700, 900)}" alt="" loading="lazy" /></div><h3>{name}</h3></a>'
        for i, name in enumerate(links[:4])
    )


def reviews(items):
    return "".join(
        f'<article class="review"><div class="stars">★★★★★</div><p>{t}</p><cite>{c}</cite></article>'
        for t, c in items
    )


def faq(items):
    return "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items
    )


def page(title, fonts, body, depth=0):
    pre = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="{pre}brand.css" />
</head>
<body>
<div class="demo">Concept demo</div>
{body}
<script src="{pre}brand.js"></script>
</body>
</html>"""


def base_css(vars_block: str, extras: str = "") -> str:
    """Full brand-site component library + brand tokens."""
    return f"""
{vars_block}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font-b);background:var(--bg);color:var(--ink);line-height:1.55;-webkit-font-smoothing:antialiased}}
img{{display:block;width:100%;height:100%;object-fit:cover}}
a{{color:inherit;text-decoration:none}}
button,input,select{{font:inherit}}
.wrap{{width:min(100% - 2*var(--g),var(--max));margin-inline:auto}}
.demo{{position:fixed;bottom:12px;left:12px;z-index:200;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--ink);color:var(--bg);opacity:.75}}
.ann{{text-align:center;font-size:12px;font-weight:600;padding:10px var(--g);background:var(--ann-bg,var(--accent));color:var(--ann-ink,#fff)}}
.ann a{{text-decoration:underline;text-underline-offset:3px}}
.top{{position:sticky;top:0;z-index:100;background:color-mix(in srgb,var(--bg) 90%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid transparent}}
.top.scrolled{{border-color:var(--line);box-shadow:0 8px 24px rgba(0,0,0,.06)}}
.nav{{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:68px}}
.logo{{font-family:var(--font-d);font-size:clamp(22px,2.4vw,30px);font-weight:var(--logo-w,600);letter-spacing:var(--logo-track,0)}}
.links{{display:flex;gap:clamp(12px,2vw,24px);font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}}
.links a{{opacity:.75}}.links a:hover{{opacity:1}}
.bag{{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:9px 12px;border:1px solid var(--ink)}}
@media(max-width:820px){{.links{{display:none}}}}
.eye{{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);font-weight:700;margin-bottom:10px}}
.h1{{font-family:var(--font-d);font-size:clamp(36px,6vw,68px);line-height:1.02;font-weight:var(--h-w,600);letter-spacing:var(--h-track,-.02em)}}
.h2{{font-family:var(--font-d);font-size:clamp(26px,3.8vw,44px);line-height:1.1;font-weight:var(--h-w,600)}}
.h3{{font-family:var(--font-d);font-size:clamp(18px,2vw,24px)}}
.lead{{color:var(--muted);font-size:15px;line-height:1.65;max-width:42ch;margin-top:12px}}
.sec{{padding-block:clamp(40px,7vw,80px)}}
.sec.tight{{padding-block:clamp(28px,4vw,48px)}}
.head{{display:flex;justify-content:space-between;align-items:end;gap:16px;margin-bottom:24px;flex-wrap:wrap}}
.head a{{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid currentColor}}
.btn{{display:inline-flex;align-items:center;justify-content:center;padding:13px 22px;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;border:1px solid transparent;transition:transform .25s var(--e),background .2s,color .2s}}
.btn:hover{{transform:translateY(-1px)}}
.btn-solid{{background:var(--accent);color:var(--accent-ink,#fff);border-color:var(--accent)}}
.btn-ghost{{background:transparent;border-color:var(--ink);color:var(--ink)}}
.btn-ink{{background:var(--ink);color:var(--bg);border-color:var(--ink)}}
.btns{{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}}
.reveal{{opacity:0;transform:translateY(22px);transition:opacity .75s var(--e),transform .75s var(--e)}}
.reveal.in{{opacity:1;transform:none}}
.trust{{display:flex;flex-wrap:wrap;gap:10px 16px;justify-content:center;padding:18px var(--g);border-block:1px solid var(--line);background:var(--panel,#fff);font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}}
.trust span{{padding:8px 12px;border:1px solid var(--line)}}
.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}
.grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
@media(max-width:900px){{.grid4,.grid3{{grid-template-columns:1fr 1fr}}}}
@media(max-width:560px){{.grid4,.grid3,.grid2{{grid-template-columns:1fr}}}}
.card .ph{{aspect-ratio:var(--card-ratio,1);background:var(--panel,#eee);overflow:hidden;position:relative;border:1px solid var(--line)}}
.card .ph img{{transition:transform .7s var(--e)}}.card:hover .ph img{{transform:scale(1.04)}}
.card .meta{{padding:12px 2px 0}}.card h3{{font-size:14px;font-weight:700}}.card .price{{margin-top:6px;font-weight:800;font-size:14px}}
.badge{{position:absolute;top:10px;left:10px;background:var(--accent);color:var(--accent-ink,#fff);font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;padding:5px 8px}}
.cats{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.cat .ph{{aspect-ratio:1;overflow:hidden;border:1px solid var(--line);margin-bottom:10px}}
.cat h3{{font-size:13px;font-weight:800;letter-spacing:.04em;text-transform:uppercase}}
@media(max-width:800px){{.cats{{grid-template-columns:1fr 1fr}}}}
.chips{{display:flex;flex-wrap:wrap;gap:8px}}.chips a{{padding:12px 16px;border:1px solid var(--line);background:var(--panel,#fff);font-size:13px;font-weight:700;transition:background .2s,color .2s,border-color .2s}}
.chips a:hover{{background:var(--accent);border-color:var(--accent);color:var(--accent-ink,#fff)}}
.split{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(20px,4vw,48px);align-items:center}}
@media(max-width:800px){{.split{{grid-template-columns:1fr}}}}
.look{{display:grid;grid-template-columns:1.1fr .9fr;gap:12px}}.look .tall{{aspect-ratio:3/4;border:1px solid var(--line)}}.look .stack{{display:grid;gap:12px}}.look .stack>div{{aspect-ratio:4/3;border:1px solid var(--line)}}
@media(max-width:800px){{.look{{grid-template-columns:1fr}}}}
.film{{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:8px}}.film .shot{{flex:0 0 min(240px,70vw);aspect-ratio:3/4;scroll-snap-align:start;border:1px solid var(--line)}}
.steps{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
.steps article{{padding:20px;border:1px solid var(--line);background:var(--panel,#fff)}}
.steps .n{{font-family:var(--font-d);font-size:28px;color:var(--accent);margin-bottom:8px}}
@media(max-width:800px){{.steps{{grid-template-columns:1fr 1fr}}}}
.reviews{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.review{{padding:22px;border:1px solid var(--line);background:var(--panel,#fff)}}
.stars{{color:#c4a035;letter-spacing:2px;margin-bottom:10px;font-size:13px}}
.review p{{font-size:14px;color:var(--muted)}}.review cite{{display:block;margin-top:14px;font-style:normal;font-size:12px;font-weight:700}}
@media(max-width:800px){{.reviews{{grid-template-columns:1fr}}}}
.press{{display:flex;flex-wrap:wrap;gap:18px 28px;justify-content:center;align-items:center;opacity:.55;font-family:var(--font-d);font-size:18px;letter-spacing:.04em}}
.faq details{{border-bottom:1px solid var(--line);padding:14px 0}}
.faq summary{{cursor:pointer;font-weight:700;list-style:none;display:flex;justify-content:space-between}}
.faq summary::-webkit-details-marker{{display:none}}.faq summary::after{{content:"+";opacity:.45}}
.faq details[open] summary::after{{content:"–"}}.faq p{{margin-top:8px;color:var(--muted);font-size:14px}}
.news{{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;align-items:center;padding:clamp(32px,5vw,52px);background:var(--ink);color:var(--bg)}}
.news .lead{{color:color-mix(in srgb,var(--bg) 70%,transparent)}}
.news form{{display:flex;gap:8px;flex-wrap:wrap}}
.news input{{flex:1;min-width:160px;padding:13px 14px;border:1px solid color-mix(in srgb,var(--bg) 30%,transparent);background:transparent;color:var(--bg)}}
@media(max-width:800px){{.news{{grid-template-columns:1fr}}}}
.quote{{padding:clamp(48px,8vw,96px) var(--g);text-align:center}}
.quote blockquote{{font-family:var(--font-d);font-size:clamp(24px,4vw,40px);line-height:1.2;max-width:18ch;margin-inline:auto}}
.quote cite{{display:block;margin-top:18px;font-style:normal;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line)}}
.stats div{{padding:22px;border-right:1px solid var(--line)}}.stats div:last-child{{border:0}}
.stats strong{{display:block;font-family:var(--font-d);font-size:32px;margin-bottom:4px}}
@media(max-width:800px){{.stats{{grid-template-columns:1fr 1fr}}.stats div:nth-child(2){{border-right:0}}}}
.bundle{{display:grid;grid-template-columns:1fr 1.1fr;border:1px solid var(--line);overflow:hidden;background:var(--panel,#fff)}}
.bundle .ph{{min-height:260px}}.bundle .copy{{padding:clamp(22px,4vw,36px);display:flex;flex-direction:column;justify-content:center}}
@media(max-width:800px){{.bundle{{grid-template-columns:1fr}}}}
.foot{{background:var(--ink);color:color-mix(in srgb,var(--bg) 70%,transparent);padding:48px 0 24px;margin-top:24px}}
.foot .grid{{display:grid;grid-template-columns:1.4fr repeat(3,1fr);gap:24px;margin-bottom:32px}}
.foot .logo{{color:var(--bg)}}.foot h4{{color:var(--bg);font-size:11px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:12px}}
.foot a{{display:block;font-size:13px;margin-bottom:7px;opacity:.75}}.foot a:hover{{opacity:1}}
.foot .bar{{border-top:1px solid color-mix(in srgb,var(--bg) 15%,transparent);padding-top:14px;font-size:12px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}}
@media(max-width:800px){{.foot .grid{{grid-template-columns:1fr 1fr}}}}
.col-hero{{padding:clamp(36px,6vw,56px) 0 16px}}
.tabs{{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}}
.tabs button{{padding:9px 14px;border:1px solid var(--line);background:var(--panel,#fff);font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;cursor:pointer}}
.tabs button.on,.tabs button.active{{background:var(--ink);color:var(--bg);border-color:var(--ink)}}
.pdp{{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(20px,4vw,40px);padding:clamp(24px,4vw,40px) 0 56px;align-items:start}}
.pdp-info{{position:sticky;top:88px}}.pdp-info .price{{font-size:24px;font-weight:800;margin:10px 0 14px}}
.sizes{{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 18px}}
.sizes button{{min-width:44px;padding:10px 12px;border:1px solid var(--line);background:var(--panel,#fff);cursor:pointer;font-weight:700}}
.sizes button.on,.sizes button.active{{background:var(--ink);color:var(--bg);border-color:var(--ink)}}
.gal{{display:grid;gap:8px}}.gal .main{{aspect-ratio:1;border:1px solid var(--line);background:var(--panel,#eee)}}
.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}
.thumbs button{{aspect-ratio:1;border:1px solid var(--line);padding:0;overflow:hidden;cursor:pointer;opacity:.55;background:var(--panel,#fff)}}
.thumbs button.on{{opacity:1;outline:2px solid var(--ink)}}
@media(max-width:900px){{.pdp{{grid-template-columns:1fr}}.pdp-info{{position:static}}}}
.sticky-atc{{position:fixed;bottom:0;left:0;right:0;z-index:90;display:none;justify-content:space-between;align-items:center;gap:12px;padding:12px var(--g);background:var(--bg);border-top:1px solid var(--line)}}
.sticky-atc.show{{display:flex}}
.rail{{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;padding:4px 0 16px}}
.rail .card{{flex:0 0 min(260px,75vw);scroll-snap-align:start}}
{extras}
"""


def nav_block(b):
    links = "".join(f'<a href="collection/">{l}</a>' for l in b["links"])
    return f"""
<div class="ann">{b["ann"]}</div>
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="./">{b["logo"]}</a>
  <nav class="links">{links}</nav>
  <span class="bag">Bag 0</span>
</div></header>"""


def footer_block(b):
    return f"""
<footer class="foot"><div class="wrap">
  <div class="grid">
    <div><div class="logo">{b["logo"]}</div><p style="margin-top:12px;max-width:30ch;font-size:13px;opacity:.75">{b["lead"]}</p></div>
    <div><h4>Shop</h4>{"".join(f'<a href="collection/">{l}</a>' for l in b["links"][:4])}</div>
    <div><h4>Help</h4><a href="#">Shipping</a><a href="#">Returns</a><a href="#">FAQ</a></div>
    <div><h4>Brand</h4><a href="#">About</a><a href="#">Contact</a><a href="product/">Featured</a></div>
  </div>
  <div class="bar"><span>© 2026 {b["full"]}</span><span>Concept / not a live store</span></div>
</div></footer>"""


def full_home_sections(b, hero_html: str, mid_unique: str = "") -> str:
    """Standard rich brand spine around a unique hero + optional mid block."""
    s = b["seed"]
    rev = reviews(b["reviews"])
    fa = faq(b["faq"])
    return f"""
{nav_block(b)}
{hero_html}
<div class="trust reveal">{"".join(f"<span>{t}</span>" for t in b["trust"])}</div>

<!-- 3 featured -->
<section class="sec reveal"><div class="wrap">
  <div class="head"><div><p class="eye">Bestsellers</p><h2 class="h2">{b["feat_title"]}</h2></div><a href="collection/">View all</a></div>
  <div class="grid4">{cards(s, b["products"], n=4)}</div>
</div></section>

<!-- 4 categories -->
<section class="sec tight reveal" style="background:var(--panel);border-block:1px solid var(--line)"><div class="wrap">
  <div class="head"><div><p class="eye">Shop by category</p><h2 class="h2">{b["cat_title"]}</h2></div></div>
  <div class="cats">{cats(s, b["links"])}</div>
</div></section>

<!-- 5 chips -->
<section class="sec reveal"><div class="wrap">
  <div class="head"><div><p class="eye">{b["chip_eye"]}</p><h2 class="h2">{b["chip_title"]}</h2></div></div>
  <div class="chips">{"".join(f'<a href="collection/">{c}</a>' for c in b["chips"])}</div>
</div></section>

{mid_unique}

<!-- 6 story -->
<section class="sec reveal"><div class="wrap">
  <div class="split">
    <div class="ph" style="aspect-ratio:4/5;border:1px solid var(--line)"><img src="{img(s+"-story",1000,1250)}" alt="" /></div>
    <div>
      <p class="eye">Our story · {b["locale"]}</p>
      <h2 class="h2">{b["story_title"]}</h2>
      <p class="lead" style="max-width:none">{b["story"]}</p>
      <div class="btns"><a class="btn btn-ghost" href="collection/">Shop the line</a></div>
    </div>
  </div>
</div></section>

<!-- 7 lookbook -->
<section class="sec tight reveal"><div class="wrap">
  <div class="head"><div><p class="eye">Lookbook</p><h2 class="h2">{b["look_title"]}</h2></div></div>
  <div class="look">
    <div class="tall"><img src="{img(s+"-lb1",1000,1400)}" alt="" /></div>
    <div class="stack"><div><img src="{img(s+"-lb2",900,700)}" alt="" /></div><div><img src="{img(s+"-lb3",900,700)}" alt="" /></div></div>
  </div>
</div></section>

<!-- 8 film -->
<section class="sec reveal"><div class="wrap">
  <div class="head"><div><p class="eye">More to explore</p><h2 class="h2">In the frame</h2></div></div>
  <div class="film">
    {"".join(f'<div class="shot"><img src="{img(s+"-f"+str(i),700,900)}" alt="" loading="lazy" /></div>' for i in range(6))}
  </div>
</div></section>

<!-- 9 new -->
<section class="sec tight reveal"><div class="wrap">
  <div class="head"><div><p class="eye">New &amp; noteworthy</p><h2 class="h2">Just in</h2></div><a href="collection/">Shop new</a></div>
  <div class="grid4">{cards(s, b["products"], n=4, start=4)}</div>
</div></section>

<!-- 10 bundles -->
<section class="sec reveal"><div class="wrap">
  <div class="head"><div><p class="eye">Value</p><h2 class="h2">{b["bundle_title"]}</h2></div></div>
  <div class="grid2">
    <a class="bundle" href="product/">
      <div class="ph"><img src="{img(s+"-bun1",900,700)}" alt="" /></div>
      <div class="copy"><p class="eye">{b["bundles"][0][0]}</p><h3 class="h3">{b["bundles"][0][1]}</h3><p class="lead">{b["bundles"][0][2]}</p><p class="price" style="margin-top:14px;font-weight:800">{b["bundles"][0][3]}</p></div>
    </a>
    <a class="bundle" href="product/">
      <div class="ph"><img src="{img(s+"-bun2",900,700)}" alt="" /></div>
      <div class="copy"><p class="eye">{b["bundles"][1][0]}</p><h3 class="h3">{b["bundles"][1][1]}</h3><p class="lead">{b["bundles"][1][2]}</p><p class="price" style="margin-top:14px;font-weight:800">{b["bundles"][1][3]}</p></div>
    </a>
  </div>
</div></section>

<!-- 11 how -->
<section class="sec tight reveal" style="background:var(--panel);border-block:1px solid var(--line)"><div class="wrap">
  <div class="head"><div><p class="eye">How it works</p><h2 class="h2">From browse to bag</h2></div></div>
  <div class="steps">
    <article><div class="n">01</div><h3 class="h3">Discover</h3><p class="lead" style="margin:0">Land on a brand-first hero with one clear path.</p></article>
    <article><div class="n">02</div><h3 class="h3">Browse</h3><p class="lead" style="margin:0">Collections shaped for how this category shops.</p></article>
    <article><div class="n">03</div><h3 class="h3">Decide</h3><p class="lead" style="margin:0">Product pages that prove fit, materials, and trust.</p></article>
    <article><div class="n">04</div><h3 class="h3">Checkout</h3><p class="lead" style="margin:0">Fast path — shipping clarity and payment confidence.</p></article>
  </div>
</div></section>

<!-- 12 stats -->
<section class="sec reveal"><div class="wrap">
  <div class="stats">
    {"".join(f"<div><strong>{k}</strong><span style='font-size:12px;color:var(--muted)'>{v}</span></div>" for k,v in b["stats"])}
  </div>
</div></section>

<!-- 13 quote -->
<section class="quote reveal">
  <blockquote>“{b["quote"]}”</blockquote>
  <cite>{b["quote_cite"]}</cite>
</section>

<!-- 14 reviews -->
<section class="sec reveal"><div class="wrap">
  <div class="head"><div><p class="eye">Reviews</p><h2 class="h2">From real customers</h2></div></div>
  <div class="reviews">{rev}</div>
</div></section>

<!-- 15 press -->
<section class="sec tight reveal"><div class="wrap">
  <p class="eye" style="text-align:center">As seen in</p>
  <div class="press">{"".join(f"<span>{p}</span>" for p in b["press"])}</div>
</div></section>

<!-- 16 visit -->
<section class="sec reveal"><div class="wrap">
  <div class="split">
    <div>
      <p class="eye">Visit</p>
      <h2 class="h2">{b["locale"]}</h2>
      <p class="lead" style="max-width:none">{b["visit"]}</p>
      <div class="btns"><a class="btn btn-solid" href="collection/">Shop online</a></div>
    </div>
    <div class="ph" style="aspect-ratio:4/3;border:1px solid var(--line)"><img src="{img(s+"-visit",1200,900)}" alt="" /></div>
  </div>
</div></section>

<!-- 17 before/after -->
<section class="sec tight reveal"><div class="wrap">
  <div class="grid2">
    <article style="padding:24px;border:1px solid var(--line)"><p class="eye">Before</p><h3 class="h3">Friction</h3><p class="lead" style="max-width:none">{b["before"]}</p></article>
    <article style="padding:24px;border:1px solid var(--line);background:var(--panel)"><p class="eye">After</p><h3 class="h3">Clearer path</h3><p class="lead" style="max-width:none">{b["after"]}</p></article>
  </div>
</div></section>

<!-- 18 faq -->
<section class="sec reveal"><div class="wrap">
  <div class="head"><div><p class="eye">FAQ</p><h2 class="h2">Before you buy</h2></div></div>
  <div class="faq">{fa}</div>
</div></section>

<!-- 19 newsletter -->
<section class="wrap" style="margin-bottom:48px">
  <div class="news reveal">
    <div>
      <p class="eye" style="color:color-mix(in srgb,var(--bg) 65%,transparent)">Newsletter</p>
      <h2 class="h2" style="color:var(--bg)">Stay close</h2>
      <p class="lead">Drops, restocks, and notes — no spam.</p>
    </div>
    <form onsubmit="return false"><input type="email" placeholder="Email address" aria-label="Email" /><button class="btn btn-solid" type="submit">Join</button></form>
  </div>
</section>

<!-- 20 rail encore -->
<section class="sec tight reveal"><div class="wrap">
  <div class="head"><div><p class="eye">Keep shopping</p><h2 class="h2">More from the line</h2></div></div>
  <div class="rail">{cards(s, b["products"], n=6)}</div>
</div></section>

{footer_block(b)}
"""


def collection_page(b):
    s = b["seed"]
    return f"""
<div class="ann">{b["ann"]}</div>
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="../">{b["logo"]}</a>
  <nav class="links">{"".join(f'<a href="./">{l}</a>' for l in b["links"][:4])}</nav>
  <span class="bag">Bag 0</span>
</div></header>
<header class="col-hero wrap">
  <p class="eye">Collection</p>
  <h1 class="h1">{b["full"]}</h1>
  <p class="lead">{b["lead"]}</p>
  <div class="tabs" data-tabs>{"".join(f'<button class="{"on" if i==0 else ""}">{x}</button>' for i,x in enumerate(["All"]+b["links"][:5]))}</div>
</header>
<section class="wrap" style="padding-bottom:56px">
  <div class="grid4">{cards(s, b["products"]*2, "../product/", 8)}</div>
</section>
<section class="sec tight wrap reveal">
  <div class="head"><div><p class="eye">Also browse</p><h2 class="h2">Categories</h2></div></div>
  <div class="cats">{cats(s, b["links"], "./")}</div>
</section>
<footer class="foot"><div class="wrap">
  <div class="grid">
    <div><div class="logo">{b["logo"]}</div></div>
    <div><h4>Shop</h4><a href="./">All</a><a href="../">Home</a></div>
    <div><h4>Help</h4><a href="#">Shipping</a></div>
    <div><h4>More</h4><a href="../product/">Product</a></div>
  </div>
  <div class="bar"><span>© 2026 {b["full"]}</span><span>Concept demo</span></div>
</div></footer>
"""


def product_page(b):
    s = b["seed"]
    name, price = b["products"][0]
    thumbs = "".join(
        f'<button class="{"on" if i==0 else ""}"><img src="{img(s+"-g"+str(i),300,300)}" alt="" /></button>'
        for i in range(4)
    )
    return f"""
<div class="ann">{b["ann"]}</div>
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="../">{b["logo"]}</a>
  <nav class="links"><a href="../collection/">Shop</a><a href="../collection/">{b["links"][0]}</a></nav>
  <span class="bag">Bag 0</span>
</div></header>
<section class="pdp wrap">
  <div class="gal" data-gal>
    <div class="main"><img src="{img(s+"-g0",1200,1500)}" alt="" data-main /></div>
    <div class="thumbs">{thumbs}</div>
  </div>
  <div class="pdp-info">
    <p class="eye">{b["links"][0]} · {b["locale"]}</p>
    <h1 class="h1" style="font-size:clamp(28px,4vw,44px)">{name}</h1>
    <div class="price">{price}</div>
    <p class="lead">{b["lead"]}</p>
    <p class="eye" style="margin-bottom:6px">Options</p>
    <div class="sizes">
      <button class="active on" type="button">S</button>
      <button type="button">M</button>
      <button type="button">L</button>
      <button type="button">XL</button>
    </div>
    <button class="btn btn-solid" style="width:100%" data-atc type="button">Add to bag — {price}</button>
    <p class="lead" style="margin-top:12px;font-size:13px">Free returns · Ships in 1–3 days · Concept demo</p>
    <div class="faq" style="margin-top:20px">
      <details open><summary>Details</summary><p>{b["story"]}</p></details>
      <details><summary>Shipping &amp; returns</summary><p>Standard shipping with easy returns on unused items.</p></details>
      <details><summary>Care</summary><p>Follow care label. Built for real use — not brochure photos only.</p></details>
    </div>
  </div>
</section>
<div class="sticky-atc"><strong>{name}</strong><button class="btn btn-solid" type="button">Add to bag</button></div>
<section class="sec wrap" style="border-top:1px solid var(--line)">
  <div class="head"><div><p class="eye">Pairs well with</p><h2 class="h2">Complete the look</h2></div></div>
  <div class="grid4">{cards(s, b["products"][1:], "./", 4)}</div>
</section>
<footer class="foot"><div class="wrap">
  <div class="grid">
    <div><div class="logo">{b["logo"]}</div></div>
    <div><h4>Shop</h4><a href="../collection/">All</a></div>
    <div><h4>Help</h4><a href="#">Returns</a></div>
    <div><h4>Home</h4><a href="../">Back</a></div>
  </div>
  <div class="bar"><span>© 2026 {b["full"]}</span><span>Concept demo</span></div>
</div></footer>
"""


# ── Hero variants (unique per brand family) ───────────────────────────────────

def hero_kinetic(b):
    s = b["seed"]
    return f"""
<section class="hero-kinetic">
  <div class="pane"><img src="{img(s+"-h1",1400,1600)}" alt="" /><div class="overlay"><p class="eye" style="color:rgba(255,255,255,.7)">{b["locale"]}</p><h1 class="h1" style="color:#fff">{b["logo"]}</h1><p class="lead" style="color:rgba(255,255,255,.8)">{b["tagline"]}</p></div></div>
  <div class="pane"><img src="{img(s+"-h2",1400,1600)}" alt="" /><div class="overlay"><p class="lead" style="color:rgba(255,255,255,.85)">{b["lead"]}</p><div class="btns"><a class="btn btn-solid" href="collection/">Shop now</a><a class="btn btn-ghost" href="product/" style="border-color:#fff;color:#fff">Featured</a></div></div></div>
</section>"""


def hero_split(b):
    s = b["seed"]
    return f"""
<section class="hero-split">
  <div class="media"><img src="{img(s+"-hero",1400,1600)}" alt="" /></div>
  <div class="copy">
    <p class="eye">{b["locale"]}</p>
    <h1 class="h1">{b["tagline"]}</h1>
    <p class="lead">{b["lead"]}</p>
    <div class="btns"><a class="btn btn-solid" href="collection/">Shop collection</a><a class="btn btn-ghost" href="product/">View featured</a></div>
  </div>
</section>"""


def hero_full(b):
    s = b["seed"]
    return f"""
<section class="hero-full">
  <div class="bg"><img src="{img(s+"-hero",1800,2200)}" alt="" /></div>
  <div class="copy">
    <p class="eye" style="color:rgba(255,255,255,.7)">{b["locale"]}</p>
    <h1 class="h1" style="color:#fff">{b["tagline"]}</h1>
    <p class="lead" style="color:rgba(255,255,255,.8)">{b["lead"]}</p>
    <div class="btns"><a class="btn btn-solid" href="collection/">Shop now</a><a class="btn btn-ghost" href="product/" style="border-color:#fff;color:#fff">Featured</a></div>
  </div>
</section>"""


def hero_center(b):
    s = b["seed"]
    return f"""
<section class="hero-center">
  <div class="still"><img src="{img(s+"-hero",900,900)}" alt="" /></div>
  <p class="eye">{b["locale"]}</p>
  <h1 class="h1">{b["tagline"]}</h1>
  <p class="lead" style="margin-inline:auto">{b["lead"]}</p>
  <div class="btns" style="justify-content:center"><a class="btn btn-solid" href="collection/">View collection</a></div>
</section>"""


def hero_tech(b):
    s = b["seed"]
    return f"""
<section class="hero-tech wrap">
  <div>
    <p class="eye">{b["locale"]}</p>
    <h1 class="h1">{b["tagline"]}</h1>
    <p class="lead">{b["lead"]}</p>
    <form class="search" action="collection/" method="get" onsubmit="return true">
      <input name="q" placeholder="Search products / SKU" aria-label="Search" />
      <button class="btn btn-solid" type="submit">Search</button>
    </form>
    <div class="btns"><a class="btn btn-ghost" href="collection/">Browse catalogue</a></div>
  </div>
  <div class="media"><img src="{img(s+"-hero",1200,1200)}" alt="" /></div>
</section>"""


HERO_EXTRAS = {
    "kinetic": """
.hero-kinetic{display:grid;grid-template-columns:1fr 1fr;min-height:88vh}
.hero-kinetic .pane{position:relative;overflow:hidden;min-height:42vh;isolation:isolate}
.hero-kinetic .overlay{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;padding:clamp(24px,4vw,48px);background:linear-gradient(transparent 35%,rgba(0,0,0,.72))}
@media(max-width:900px){.hero-kinetic{grid-template-columns:1fr}}
""",
    "split": """
.hero-split{display:grid;grid-template-columns:1.05fr .95fr;min-height:86vh;background:var(--panel)}
.hero-split .media{min-height:44vh}
.hero-split .copy{display:flex;flex-direction:column;justify-content:center;padding:clamp(32px,5vw,64px)}
@media(max-width:860px){.hero-split{grid-template-columns:1fr}}
""",
    "full": """
.hero-full{min-height:92vh;position:relative;display:grid;align-items:end;isolation:isolate;color:#fff}
.hero-full .bg{position:absolute;inset:0;z-index:-1}
.hero-full .bg img{filter:brightness(.58)}
.hero-full .copy{padding:clamp(40px,8vw,96px) var(--g);max-width:720px}
""",
    "center": """
.hero-center{text-align:center;padding:clamp(48px,8vw,88px) var(--g)}
.hero-center .still{width:min(380px,78vw);aspect-ratio:1;margin:0 auto 28px;border-radius:var(--still-radius,50%);overflow:hidden;border:1px solid var(--line)}
""",
    "tech": """
.hero-tech{display:grid;grid-template-columns:1.1fr .9fr;gap:28px;align-items:center;padding:clamp(36px,6vw,64px) 0;min-height:78vh}
.hero-tech .media{border:1px solid var(--line);min-height:360px}
.search{display:grid;grid-template-columns:1fr auto;gap:0;margin-top:20px;max-width:480px;border:1px solid var(--line);background:var(--panel,#fff)}
.search input{border:0;padding:14px 16px;background:transparent;outline:none}
@media(max-width:860px){.hero-tech{grid-template-columns:1fr}}
""",
}


def mid_marquee(b):
    return f"""
<section class="marquee reveal" aria-hidden="true"><div class="track">
  <span>{b["tagline"]}</span><span>·</span><span>{b["full"]}</span><span>·</span><span>{b["locale"]}</span><span>·</span>
  <span>{b["tagline"]}</span><span>·</span><span>{b["full"]}</span><span>·</span><span>{b["locale"]}</span><span>·</span>
</div></section>"""


MARQUEE_CSS = """
.marquee{overflow:hidden;border-block:1px solid var(--line);padding:14px 0;white-space:nowrap;background:var(--panel)}
.marquee .track{display:inline-flex;gap:40px;animation:mq 28s linear infinite;font-family:var(--font-d);font-size:14px;letter-spacing:.08em;text-transform:uppercase}
@keyframes mq{from{transform:translateX(0)}to{transform:translateX(-50%)}}
"""


# ── Brand data ────────────────────────────────────────────────────────────────

def brand(
    slug, logo, full, fonts, hero, locale, ann, links, tagline, lead, seed, products,
    trust, chips, chip_eye, chip_title, feat_title, cat_title, story_title, story,
    look_title, bundle_title, bundles, stats, quote, quote_cite, reviews_, press,
    visit, before, after, faq_, tokens, extras=""
):
    return {
        "slug": slug, "logo": logo, "full": full, "fonts": fonts, "hero": hero,
        "locale": locale, "ann": ann, "links": links, "tagline": tagline, "lead": lead,
        "seed": seed, "products": products, "trust": trust, "chips": chips,
        "chip_eye": chip_eye, "chip_title": chip_title, "feat_title": feat_title,
        "cat_title": cat_title, "story_title": story_title, "story": story,
        "look_title": look_title, "bundle_title": bundle_title, "bundles": bundles,
        "stats": stats, "quote": quote, "quote_cite": quote_cite, "reviews": reviews_,
        "press": press, "visit": visit, "before": before, "after": after, "faq": faq_,
        "tokens": tokens, "extras": extras,
    }


BRANDS = [
    brand(
        "northline-athletics", "Northline", "Northline Athletics",
        "family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700", "kinetic", "Portland, OR",
        "Drop 07 live · Free shipping over $120",
        ["Run", "Train", "Outer", "Women", "Men"],
        "Move harder. Recover cleaner.",
        "Performance layers engineered for cold starts, wet miles, and city intervals.",
        "northline",
        [("NL Apex Jacket", "$248"), ("Stride Short 5\"", "$68"), ("Trail Pack Vest", "$180"), ("Recover Hood", "$120"),
         ("Pulse Tight", "$88"), ("Grip Sock Pro", "$24"), ("Altitude Shell", "$310"), ("Base Layer 01", "$54")],
        ["Cold tested", "Reflective", "Recycled yarn", "Free returns", "Drop 07", "Portland"],
        ["Morning run", "Tempo", "Trail", "Recovery", "Rain", "Gym", "Travel", "Race day"],
        "Shop by session", "What are you training?",
        "What athletes reorder", "Kit by discipline",
        "Built for intervals",
        "Northline designs layers that disappear when you move — and still look sharp on the walk home.",
        "Campaign stills", "Training kits",
        [("Save 10%", "Cold Start Kit", "Apex Jacket + Base Layer", "$286"), ("Save 12%", "Recover Duo", "Hood + Pulse Tight", "$188")],
        [("−12°", "Cold-start tested"), ("360g", "Shell class"), ("7", "Drop cycle"), ("30d", "Returns")],
        "The jacket disappears after mile three. That is the point.",
        "Alex · Portland · Apex Jacket",
        [("Warm without bulk on wet mornings.", "Jordan · Run club"), ("Vest stays put on long trail days.", "Sam · Ultramarathon"), ("Recover hood is my flight layer now.", "Riley · Travel")],
        ["Runner's World", "Outside", "Hypebeast", "Gear Patrol"],
        "Flagship fittings by appointment · Portland Pearl District.",
        "Scattered categories, weak mobile cart, brochure energy before product.",
        "Session-led browse, clear kits, and a path from drop to bag.",
        [("Is this a live store?", "No — portfolio concept for Shopify / rebuild conversations."), ("Can this run on Shopify?", "Yes — sections, metafields, and custom CSS map cleanly."), ("Do you migrate apps?", "We map subscriptions, reviews, and loyalty in launch QA.")],
        ':root{--bg:#0c0e10;--ink:#f2f4f6;--muted:#8b939c;--line:#252a30;--accent:#c8f542;--accent-ink:#111;--panel:#14181c;--ann-bg:#c8f542;--ann-ink:#111;--font-d:"Bebas Neue",sans-serif;--font-b:"DM Sans",sans-serif;--g:clamp(16px,4vw,40px);--max:1200px;--e:cubic-bezier(.22,1,.36,1);--logo-track:.06em;--h-track:.02em;--card-ratio:4/5}',
        MARQUEE_CSS + ".logo,.h1,.h2,.h3{text-transform:uppercase}",
    ),
    brand(
        "atelier-maris", "Atelier Maris", "Atelier Maris",
        "family=Cormorant+Garamond:wght@500;600;700&family=Figtree:wght@400;500;600;700", "center", "Lisbon",
        "Private appointments · Atelier open Thu–Sat",
        ["Rings", "Necklaces", "Earrings", "Bridal", "Objects"],
        "Quiet metal. Soft stone.",
        "Hand-finished jewelry for people who notice the weight of a clasp.",
        "maris",
        [("Lune Signet", "€420"), ("Tide Collar", "€680"), ("Pearl Drop II", "€290"), ("Sand Band", "€310"),
         ("Harbor Studs", "€180"), ("Citrine Halo", "€540"), ("Ribbon Cuff", "€390"), ("Vesper Chain", "€250")],
        ["Hand finished", "Recycled gold options", "Lisbon atelier", "Gift wrap", "Appointments", "Worldwide"],
        ["Everyday", "Evening", "Bridal", "Gift", "Stacking", "Statement", "Minimal", "Custom"],
        "Shop by moment", "How will you wear it?",
        "Pieces people return for", "By typology",
        "Made to be noticed in the hand",
        "Maris keeps metal quiet and stones soft — jewelry that rewards a closer look, not a louder logo.",
        "Atelier light", "Sets & rituals",
        [("Save 8%", "Daily Stack", "Sand Band + Harbor Studs", "€450"), ("Save 10%", "Evening Pair", "Tide Collar + Pearl Drop", "€870")],
        [("Thu–Sat", "Atelier hours"), ("18k", "Options"), ("2–4w", "Made pieces"), ("Lisbon", "Studio")],
        "The clasp weight told me more than any product photo.",
        "Elena · Lisbon · Lune Signet",
        [("Pearl Drop sits perfectly — no costume energy.", "Marta · Bridal"), ("Signet feels heirloom without shouting.", "João · Gift"), ("Appointments made choosing calm.", "Sofia · Stack")],
        ["Vogue", "Wallpaper*", "Dezeen", "Monocle"],
        "Atelier visits Thu–Sat · Alfama studio by appointment.",
        "Thin catalog, unclear CTAs, brochure jewelry site.",
        "Moment-led browse, appointment path, and product pages that prove craft.",
        [("Is this live commerce?", "Concept demo for rebuild conversations."), ("Shopify ready?", "Yes — Online Store 2.0 sections and metafields."), ("Custom pieces?", "RFQ / appointment patterns map to forms + calendars.")],
        ':root{--bg:#f7f1ea;--ink:#2a221c;--muted:#7a6e64;--line:#e4d8cc;--accent:#8b5e3c;--accent-ink:#fff;--panel:#fff;--font-d:"Cormorant Garamond",serif;--font-b:"Figtree",sans-serif;--g:clamp(18px,4vw,40px);--max:1000px;--e:cubic-bezier(.22,1,.36,1);--h-w:500;--logo-w:600;--still-radius:50%;--card-ratio:1}',
        MARQUEE_CSS + ".card .ph{border-radius:50%;overflow:hidden}.hero-center{background:radial-gradient(circle at 50% 0%,#fff8f0,transparent 55%)}",
    ),
    brand(
        "cedar-and-salt", "Cedar & Salt", "Cedar & Salt",
        "family=Fraunces:opsz,wght@9..144,500;600;700&family=Sora:wght@400;500;600;700", "full", "Cornwall",
        "New: Coastal Fig · Ships in recycled glass",
        ["Candles", "Diffusers", "Oils", "Sets", "Ritual"],
        "Rooms that smell like places.",
        "Botanical fragrance for homes that want atmosphere, not perfume fog.",
        "cedar",
        [("Coastal Fig", "$48"), ("Cedar Smoke", "$48"), ("Salt Air Diffuser", "$64"), ("Morning Resin", "$42"),
         ("Clay Vessel Set", "$96"), ("Travel Tin Trio", "$36"), ("Linen Mist", "$28"), ("Altar Oil", "$54")],
        ["Recycled glass", "Botanical", "Cornwall poured", "Gift ready", "Slow burn", "Refills"],
        ["Morning", "Evening", "Coast", "Forest", "Linen", "Travel", "Gift", "Altar"],
        "Shop by mood", "What room are you building?",
        "Scents people reorder", "By ritual",
        "Fragrance that behaves like furniture",
        "Cedar & Salt builds atmosphere you can live in — notes that settle into a room instead of announcing themselves.",
        "Material mood", "Ritual sets",
        [("Save 12%", "Coast Ritual", "Coastal Fig + Salt Air", "$98"), ("Save 10%", "Evening Pair", "Cedar Smoke + Altar Oil", "$92")],
        [("55h", "Burn time"), ("Glass", "Recycled"), ("8", "Core notes"), ("UK", "Ships from")],
        "It smells like a place I want to stay in.",
        "Hannah · Cornwall · Coastal Fig",
        [("Salt Air is our hallway now.", "Tom · Home"), ("Fig candle lasted the full claim.", "Priya · Gift"), ("Travel tins saved my suitcase.", "Leah · Travel")],
        ["Kinfolk", "Apartamento", "The Modern House", "Cereal"],
        "Cornwall studio pickup weekends · coastal shipping nationwide.",
        "Generic candle grid, weak scent storytelling, no ritual path.",
        "Mood-led rooms, clear sets, and product pages that explain notes.",
        [("Live store?", "Portfolio concept only."), ("Shopify?", "Yes — subscriptions for refills map well."), ("Wholesale?", "Trade login patterns available on request.")],
        ':root{--bg:#1a1814;--ink:#f3efe6;--muted:#a39a8c;--line:#2f2b24;--accent:#c4a574;--accent-ink:#1a1814;--panel:#221f1a;--font-d:"Fraunces",serif;--font-b:"Sora",sans-serif;--g:clamp(18px,4vw,40px);--max:1120px;--e:cubic-bezier(.22,1,.36,1);--h-w:500}',
        MARQUEE_CSS,
    ),
    brand(
        "volt-kitchen", "Volt", "Volt Kitchen",
        "family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700", "split", "Chicago",
        "Pro tools for home kitchens · 30-day heat test",
        ["Cookware", "Knives", "Tools", "Table", "Bundles"],
        "Heat. Speed. Control.",
        "Industrial-grade cookware scaled for serious home cooks.",
        "volt",
        [("Skillet 28cm", "$189"), ("Chef Knife 210", "$220"), ("Carbon Wok", "$160"), ("Therm Probe X", "$79"),
         ("Steel Tong Pro", "$34"), ("Dutch Oven 5L", "$280"), ("Board End-Grain", "$120"), ("Sauce Pan Set", "$310")],
        ["260°C tested", "Induction ready", "Full tang", "30-day heat test", "Chicago", "Pro grade"],
        ["Sear", "Slice", "Simmer", "Prep", "Serve", "Gift", "Starter", "Pro"],
        "Shop by job", "What are you cooking?",
        "Tools that stay on the rail", "By station",
        "Spec the wall",
        "Volt brings industrial heat control home — gear that earns a permanent place on the rail.",
        "Line check", "Station kits",
        [("Save 11%", "Sear Kit", "Skillet + Tong Pro", "$199"), ("Save 9%", "Knife + Board", "Chef 210 + End-Grain", "$310")],
        [("260°C", "Heat test"), ("28cm", "Skillet"), ("30d", "Returns"), ("Pro", "Spec")],
        "Finally a home skillet that behaves like line cookware.",
        "Chris · Chicago · Skillet 28cm",
        [("Knife geometry is serious.", "Dana · Prep"), ("Probe is stupid accurate.", "Lee · Roast"), ("Wok heats edge to edge.", "Morgan · Stir-fry")],
        ["Serious Eats", "Wirecutter", "Bon Appétit", "Food52"],
        "Demo kitchen events · Chicago Fulton Market.",
        "Pretty pans, weak specs, unclear heat ratings.",
        "Job-led browse, hard specs, kits for real stations.",
        [("Concept only?", "Yes — demo for rebuild pitches."), ("Shopify?", "Yes — metafields for specs shine here."), ("Bundles?", "Native or app-based kits both work.")],
        ':root{--bg:#111;--ink:#f5f5f0;--muted:#9a9a90;--line:#2a2a2a;--accent:#ffe600;--accent-ink:#111;--panel:#1a1a1a;--ann-bg:#ffe600;--ann-ink:#111;--font-d:"Space Grotesk",sans-serif;--font-b:"IBM Plex Sans",sans-serif;--g:clamp(16px,4vw,36px);--max:1180px;--e:cubic-bezier(.22,1,.36,1)}',
        MARQUEE_CSS + ".h1,.h2,.logo{text-transform:uppercase}.top{border-bottom:3px solid var(--accent)}",
    ),
    brand(
        "lumen-eyewear", "Lumen", "Lumen Eyewear",
        "family=Syne:wght@500;600;700;800&family=Outfit:wght@400;500;600;700", "split", "Berlin",
        "Virtual try-on · Free returns 30 days",
        ["Optical", "Sun", "Blue", "Fit Lab", "Lenses"],
        "Frames for faces, not mannequins.",
        "Precision optical DTC with fit data, blue-light options, and overnight lenses.",
        "lumen",
        [("Arc 02", "$168"), ("Nova Wire", "$148"), ("Halo Acetate", "$188"), ("Drift Sun", "$158"),
         ("Pulse Blue", "$138"), ("Studio Thin", "$178"), ("Night Shield", "$128"), ("Clip Module", "$48")],
        ["Fit lab", "AR try-on", "Blue light", "30-day returns", "Berlin", "Rx ready"],
        ["Narrow", "Average", "Wide", "Low bridge", "Sun", "Blue", "Night", "Clip-ons"],
        "Shop by fit", "Start with your face",
        "Frames that get reordered", "By lens need",
        "Fit first, then fashion",
        "Lumen treats PD and bridge width as product features — frames that actually match faces.",
        "Fit gallery", "Lens kits",
        [("Save 10%", "Desk Duo", "Pulse Blue + Clip Module", "$168"), ("Save 8%", "Sun + Optical", "Drift + Arc 02", "$300")],
        [("12", "Bridge widths"), ("AR", "Try-on"), ("30d", "Returns"), ("Rx", "Lenses")],
        "First pair that did not slide down my nose.",
        "Nina · Berlin · Arc 02",
        [("Blue lenses saved my screen days.", "Omar · Studio"), ("Try-on was accurate enough to buy.", "Grace · Optical"), ("Sun clip is genius.", "Felix · Travel")],
        ["Dezeen", "Highsnobiety", "GQ", "It's Nice That"],
        "Fit Lab appointments · Berlin Mitte.",
        "Pretty frames, weak fit guidance, returns friction.",
        "Fit-led browse, try-on confidence, clear lens options.",
        [("Demo?", "Yes — concept storefront."), ("Shopify?", "Yes — fit quizzes + apps."), ("Rx?", "Lens workflows via partner apps.")],
        ':root{--bg:#f4f6f8;--ink:#12141a;--muted:#667084;--line:#d5dae3;--accent:#5b7cfa;--accent-ink:#fff;--panel:#fff;--font-d:"Syne",sans-serif;--font-b:"Outfit",sans-serif;--g:clamp(18px,4vw,40px);--max:1120px;--e:cubic-bezier(.22,1,.36,1);--logo-track:-.04em;--h-track:-.04em}',
        MARQUEE_CSS + ".bag,.btn{border-radius:999px}.card{border-radius:16px;overflow:hidden;background:#fff;border:1px solid var(--line)}.card .meta{padding:12px 14px}",
    ),
    brand(
        "exclusive-living", "Exclusive Living", "Exclusive Living",
        "family=Libre+Baskerville:wght@400;700&family=Karla:wght@400;500;600;700", "split", "Germany",
        "Solid wood furniture · Showroom appointments available",
        ["Dining", "Living", "Bedroom", "Oak", "Walnut"],
        "Showroom craft. Shopable stock.",
        "Solid-wood furniture with clear lead times, finishes, and delivery — not just a gallery.",
        "exclive",
        [("Oak Dining Table 220", "€2,480"), ("Walnut Sideboard", "€1,890"), ("Lounge Chair Linen", "€980"), ("Bed Frame Queen", "€1,640"),
         ("Console Slim", "€720"), ("Bookshelf Bay", "€1,120"), ("Bench Seat", "€540"), ("Nightstand Pair", "€680")],
        ["Solid wood", "Finish samples", "Lead times shown", "White glove", "Germany", "In stock + MTO"],
        ["Oak", "Walnut", "In stock", "6–10 wks", "Dining", "Bedroom", "Living", "Outdoor"],
        "Shop by finish / timing", "How soon do you need it?",
        "Pieces with real availability", "By room",
        "Furniture you can actually buy",
        "Exclusive Living connects showroom craft to clear stock, finishes, and delivery windows.",
        "Room stories", "Room kits",
        [("Save 6%", "Dining Starter", "Table + Bench", "€2,850"), ("Save 7%", "Bedroom Pair", "Bed + Nightstands", "€2,150")],
        [("6–10w", "MTO oak"), ("In stock", "Showroom"), ("DE", "Delivery"), ("Samples", "Finishes")],
        "Lead time on the product page sold me more than the photo.",
        "Anke · Hamburg · Oak Table",
        [("Walnut sideboard finish matched sample.", "Lars · Living"), ("White glove was seamless.", "Mira · Bedroom"), ("Finally not just a lookbook.", "Otto · Dining")],
        ["AD Germany", "Schöne Wohnen", "Dezeen", "Interior Design"],
        "Showroom appointments · Germany.",
        "Gallery furniture site without buy path or lead times.",
        "Room + finish filters, stock clarity, delivery confidence.",
        [("Concept?", "Yes."), ("Shopify?", "Yes — delivery apps + metafields."), ("B2B trade?", "Trade pricing patterns available.")],
        ':root{--bg:#f3efe8;--ink:#1c1915;--muted:#6f675c;--line:#ddd4c6;--accent:#3d5a40;--accent-ink:#fff;--panel:#fff;--font-d:"Libre Baskerville",serif;--font-b:"Karla",sans-serif;--g:clamp(18px,4vw,40px);--max:1200px;--e:cubic-bezier(.22,1,.36,1);--h-w:400;--card-ratio:4/5}',
        MARQUEE_CSS,
    ),
    brand(
        "mican-industrial", "MiCan", "MiCan Industrial",
        "family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600;700", "tech", "South Africa",
        "Wholesale tools · Net terms for trade accounts",
        ["Power", "Hand", "Safety", "Consumables", "Trade"],
        "Tools that earn their keep.",
        "Industrial supply for workshops — fast SKU search, pack sizes, and trade checkout.",
        "mican",
        [("Impact Driver 18V", "R 2,450"), ("Torque Wrench Set", "R 1,180"), ("Cut-Resist Gloves", "R 89"), ("Angle Grinder", "R 1,650"),
         ("Drill Bit Pack 50", "R 320"), ("Safety Glasses Pro", "R 145"), ("Compressor 50L", "R 4,200"), ("Tape Measure 8m", "R 78")],
        ["Trade accounts", "Pack sizes", "Net terms", "Same-week dispatch", "SA stock", "SKU search"],
        ["Power", "Hand", "PPE", "Abrasives", "Consumables", "Bulk", "Site", "Workshop"],
        "Shop by job site", "What are you stocking?",
        "Fast movers for trade", "By category",
        "Workshop-first merchandising",
        "MiCan is built for buyers who know SKUs — pack sizes, trade path, and search that respects time on site.",
        "On the floor", "Trade packs",
        [("Trade save", "Impact + Bits", "Driver + Drill Bit Pack", "R 2,650"), ("Trade save", "Safety Pair", "Gloves + Glasses", "R 210")],
        [("Net", "Trade terms"), ("SKU", "Search"), ("Pack", "Sizes"), ("SA", "Stock")],
        "Finally a tool site that shows pack size before the pitch.",
        "Thabo · Joburg · Trade",
        [("Impact driver in stock same week.", "Lerato · Power"), ("Gloves pricing by pack is clear.", "Johan · PPE"), ("Trade checkout is faster now.", "Sipho · Workshop")],
        ["Engineering News", "Mining Weekly", "Tools SA", "Bizcommunity"],
        "Counter pickup · major metros.",
        "Brochure industrial site, weak SKU density.",
        "Search-led catalogue, pack clarity, trade checkout.",
        [("Demo?", "Yes."), ("Shopify?", "B2B apps + wholesale channels."), ("ERP?", "Feed / middleware scoped separately.")],
        ':root{--bg:#f0f2f0;--ink:#141414;--muted:#5c6360;--line:#c9d0cb;--accent:#e8a317;--accent-ink:#111;--panel:#fff;--ann-bg:#141414;--ann-ink:#e8a317;--font-d:"Barlow Condensed",sans-serif;--font-b:"Barlow",sans-serif;--g:clamp(16px,4vw,32px);--max:1200px;--e:cubic-bezier(.22,1,.36,1)}',
        MARQUEE_CSS + ".logo,.h1,.h2{text-transform:uppercase}.top{background:var(--ink);color:#fff}.top .logo{color:var(--accent)}.top .links a{color:#fff}.bag{background:var(--accent);color:#111;border:0}",
    ),
    brand(
        "german-industry-parts", "GIP", "German Industry Parts",
        "family=Archivo:wght@500;600;700&family=Source+Sans+3:wght@400;500;600;700", "tech", "Germany",
        "Spare parts search · RFQ in under 2 minutes",
        ["Bearings", "Seals", "Motors", "Hydraulics", "RFQ"],
        "Find the part. Quote the rest.",
        "B2B spare-parts commerce with cross-reference search and rapid RFQ workflows.",
        "giparts",
        [("Bearing 6205-2RS", "€12.40"), ("Oil Seal 35×52", "€4.80"), ("Motor Flange IEC", "€186"), ("Hydraulic Hose 2m", "€42"),
         ("Coupling Elastic", "€68"), ("Filter Cartridge", "€22"), ("V-Belt XPZ", "€9.50"), ("Sensor Proximity", "€54")],
        ["OEM cross-ref", "Alternatives", "RFQ <2m", "Export docs", "Germany", "Net terms"],
        ["OEM exact", "Alternative", "In stock", "Hydraulics", "Motors", "Seals", "Sensors", "Belts"],
        "Shop by match type", "How do you need to source?",
        "Common SKUs", "By family",
        "Cross-reference without the spreadsheet",
        "GIP turns spare-part hunting into search → confirm → RFQ — with OEM and alternative side by side.",
        "Parts context", "Maintenance kits",
        [("Quote pack", "Bearing + Seal", "6205 + 35×52", "€16.20"), ("Service", "Filter + Belt", "Cartridge + XPZ", "€30")],
        [("<2m", "RFQ"), ("OEM", "Cross-ref"), ("DE", "Dispatch"), ("Docs", "Export")],
        "Alternative pricing next to OEM saved the whole order.",
        "Plant buyer · NRW",
        [("Cross-ref actually matched.", "Maintenance lead"), ("RFQ reply same day.", "Purchasing"), ("Docs pack was complete.", "Logistics")],
        ["VDI", "Produktion", "MM Maschinenmarkt", "Industry Week"],
        "RFQ desk · Germany business hours.",
        "PDF catalogs and email-only quotes.",
        "Search, compare, multi-SKU RFQ on one path.",
        [("Concept?", "Yes."), ("Shopify?", "B2B + search apps."), ("PIM?", "Can integrate later.")],
        ':root{--bg:#eef1f4;--ink:#15202b;--muted:#5d6b7a;--line:#c5ced6;--accent:#0b6e4f;--accent-ink:#fff;--panel:#fff;--font-d:"Archivo",sans-serif;--font-b:"Source Sans 3",sans-serif;--g:clamp(16px,4vw,32px);--max:1180px;--e:cubic-bezier(.22,1,.36,1)}',
        MARQUEE_CSS,
    ),
    brand(
        "btt-vacuums", "BTT Vacuums", "BTT Vacuums",
        "family=Rajdhani:wght@500;600;700&family=Exo+2:wght@400;500;600;700", "tech", "Germany",
        "Industrial vacuum systems · Configure & request quote",
        ["Systems", "Accessories", "Filters", "Configure", "Support"],
        "Suction engineered for industry.",
        "Industrial vacuum equipment with configurator-style product pages and clear duty specs.",
        "bttvac",
        [("IVS-400 Mobile", "€3,200"), ("HEPA Module", "€680"), ("Hose Kit 10m", "€210"), ("Cyclone Presep", "€940"),
         ("ATEX Unit 2", "€5,800"), ("Nozzle Pack", "€145"), ("Filter Bag Case", "€96"), ("Wall Dock", "€420")],
        ["Duty classed", "HEPA options", "ATEX available", "BOM quote", "Germany", "Configure"],
        ["Dust", "Liquid", "ATEX", "Mobile", "Central", "Filters", "Hoses", "Docking"],
        "Shop by duty", "What are you extracting?",
        "Configured systems", "By module",
        "Configure before you call",
        "BTT makes industrial vacuum selection feel like engineering — duty, filters, and BOM in one flow.",
        "Systems in situ", "Module kits",
        [("Config save", "Mobile + HEPA", "IVS-400 + HEPA Module", "€3,700"), ("Config save", "Hose + Nozzles", "10m + Nozzle Pack", "€320")],
        [("400", "m³/h class"), ("HEPA", "Module"), ("ATEX", "Option"), ("BOM", "Quote")],
        "Duty class on the page stopped the wrong unit order.",
        "Facilities eng. · Bavaria",
        [("Configure flow is clear.", "Safety officer"), ("HEPA add-on pricing honest.", "Cleanroom"), ("Dock design is solid.", "Workshop")],
        ["Process Engineering", "MM", "Produktion", "Plant Engineering"],
        "Configure with sales · Germany.",
        "PDF spec sheets, no guided configure.",
        "Duty-led configure, module pricing, BOM RFQ.",
        [("Demo?", "Yes."), ("Shopify?", "Yes with custom options."), ("ATEX docs?", "Metafield / download pattern.")],
        ':root{--bg:#0f1419;--ink:#e8eef4;--muted:#8b9aab;--line:#243040;--accent:#39c0ba;--accent-ink:#0f1419;--panel:#15202b;--font-d:"Rajdhani",sans-serif;--font-b:"Exo 2",sans-serif;--g:clamp(16px,4vw,36px);--max:1160px;--e:cubic-bezier(.22,1,.36,1)}',
        MARQUEE_CSS + ".h1,.h2,.logo{text-transform:uppercase}",
    ),
    brand(
        "jkm-industrial", "JKM", "JKM Industrial Supplies",
        "family=Chivo:wght@500;600;700&family=Public+Sans:wght@400;500;600;700", "tech", "Johannesburg",
        "Fasteners & tools · Same-day Johannesburg metro",
        ["Fasteners", "Tools", "Abrasives", "PPE", "Bulk"],
        "Density without chaos.",
        "Industrial fasteners and tools with high-density catalog UX that still feels fast.",
        "jkmind",
        [("Hex Bolt M10×40", "R 2.40"), ("Socket Cap M8", "R 1.80"), ("Flat Washer M12", "R 0.45"), ("Nylon Nut M10", "R 0.90"),
         ("Cutting Disc 115", "R 12"), ("Safety Gloves", "R 48"), ("Drill Bit HSS", "R 18"), ("Cable Tie Pack", "R 35")],
        ["Same-day metro", "Bulk bins", "SKU dense", "Counter pickup", "Joburg", "Trade"],
        ["M6", "M8", "M10", "M12", "Hex", "Socket", "PPE", "Abrasives"],
        "Shop by size / type", "What are you picking?",
        "Counter favourites", "By family",
        "A catalog that respects the pick list",
        "JKM keeps fastener density usable — matrix browse, clear packs, metro speed.",
        "Bin reality", "Site packs",
        [("Bulk", "M10 Fastener Pack", "Bolt + Nut + Washer", "R 48"), ("Site", "Cut + Protect", "Disc + Gloves", "R 55")],
        [("Same day", "Metro"), ("Bulk", "Bins"), ("SKU", "Dense"), ("JHB", "Counter")],
        "Found M10×40 in two clicks. That is the product.",
        "Buyer · Midrand",
        [("Matrix is how we think.", "Storeman"), ("Bulk pricing visible.", "Contractor"), ("Pickup slots reliable.", "Site lead")],
        ["Engineering News", "Construction World", "Tools SA", "Bizcommunity"],
        "Counter · Johannesburg metro same-day.",
        "Unsearchable fastener lists.",
        "Size matrix, bulk clarity, metro promise.",
        [("Demo?", "Yes."), ("Shopify?", "Yes with dense collections."), ("EDI?", "Scoped separately.")],
        ':root{--bg:#f6f6f4;--ink:#111;--muted:#666;--line:#d0d0cc;--accent:#d62828;--accent-ink:#fff;--panel:#fff;--ann-bg:#111;--ann-ink:#fff;--font-d:"Chivo",sans-serif;--font-b:"Public Sans",sans-serif;--g:clamp(14px,3vw,28px);--max:1240px;--e:cubic-bezier(.22,1,.36,1)}',
        MARQUEE_CSS + ".logo,.h1,.h2{text-transform:uppercase}.top{background:#111;color:#fff}.bag{background:var(--accent);border:0}",
    ),
    brand(
        "night-market-archive", "Night Market", "Night Market Archive",
        "family=Special+Elite&family=IBM+Plex+Mono:wght@400;500;600", "kinetic", "Taipei",
        "After-dark drops · Archive stalls open nightly",
        ["Archive", "Stalls", "Vintage", "New", "Visit"],
        "After dark, the good racks open.",
        "A night-market energy for vintage and limited drops — browse like a reel, buy like a stall.",
        "nightmkt",
        [("Archive Denim", "$120"), ("Stall Tee", "$48"), ("Night Cap", "$36"), ("Market Tote", "$64"),
         ("Film Jacket", "$180"), ("Stamp Scarf", "$42"), ("Lantern Shirt", "$78"), ("Ticket Pin Set", "$18")],
        ["Archive graded", "Limited drops", "Night release", "Authentic", "Taipei", "Worldwide"],
        ["Denim", "Tees", "Outer", "Accessories", "Deadstock", "Reprint", "Local", "Import"],
        "Shop by stall", "Which rack tonight?",
        "Tonight's picks", "By stall type",
        "Racks with a pulse",
        "Night Market Archive borrows night-market rhythm — scarce drops, graded archive, and a browse that feels like walking stalls.",
        "Reel frames", "Stall sets",
        [("Night save", "Denim + Cap", "Archive Denim + Night Cap", "$140"), ("Stall save", "Tee + Tote", "Stall Tee + Market Tote", "$100")],
        [("Nightly", "Drops"), ("Graded", "Archive"), ("Taipei", "Root"), ("Ltd", "Runs")],
        "Felt like finding the good stall before the crowd.",
        "Mei · Taipei · Archive Denim",
        [("Grading notes were honest.", "Ken · Vintage"), ("Drop timing is addictive.", "Aya · New"), ("Tote is daily now.", "Rio · Stall")],
        ["Hypebeast", "It's Nice That", "Nowness", "Highsnobiety"],
        "Night pop-ups · Taipei weekends.",
        "Flat vintage grid, no drop energy.",
        "Reel browse, stall chapters, scarce drop clarity.",
        [("Demo?", "Yes."), ("Shopify?", "Yes — drop apps help."), ("Authenticity?", "Metafield grading works.")],
        ':root{--bg:#0a0a0b;--ink:#f0e6d8;--muted:#8a8074;--line:#222;--accent:#e8572a;--accent-ink:#fff;--panel:#121212;--font-d:"Special Elite",monospace;--font-b:"IBM Plex Mono",monospace;--g:clamp(16px,4vw,36px);--max:1080px;--e:cubic-bezier(.22,1,.36,1);--card-ratio:3/4}',
        MARQUEE_CSS + "img{filter:contrast(1.05) saturate(.9)}",
    ),
    brand(
        "sandton-atelier", "Sandton Atelier", "Sandton Atelier",
        "family=Bodoni+Moda:opsz,wght@6..96,500;600;700&family=Manrope:wght@400;500;600;700", "full", "Johannesburg",
        "SS edit online · Click & collect Sandton",
        ["New", "Day", "Evening", "Visit", "Edit"],
        "City polish. Soft light.",
        "A Sandton boutique rhythm — seasonal looks, clear stock, and a path from lookbook to bag.",
        "sandton",
        [("Column Dress", "R 2,800"), ("Soft Blazer", "R 3,200"), ("Pleat Skirt", "R 1,650"), ("Silk Cami", "R 980"),
         ("Tailored Trouser", "R 1,890"), ("Wrap Dress", "R 2,450"), ("Evening Tank", "R 1,200"), ("Leather Belt", "R 650")],
        ["Season edit", "Click & collect", "Size guide", "Sandton", "Lookbook", "In stock"],
        ["Day", "Evening", "Work", "Weekend", "Event", "Travel", "New", "Sale"],
        "Shop by occasion", "Where are you going?",
        "The edit that sells out", "By moment",
        "Lookbook with a buy button",
        "Sandton Atelier keeps boutique polish — but every look connects to size, stock, and collect.",
        "Season film", "Occasion sets",
        [("Edit save", "Day Set", "Blazer + Trouser", "R 4,600"), ("Edit save", "Evening Pair", "Column Dress + Belt", "R 3,200")],
        [("SS", "Edit"), ("C&C", "Sandton"), ("Sizes", "Guide"), ("JHB", "Boutique")],
        "Finally a lookbook where I could buy the skirt in my size.",
        "Naledi · Sandton · Pleat Skirt",
        [("Click & collect was easy.", "Thandi · Day"), ("Evening dress photos matched fabric.", "Aisha · Event"), ("Size guide saved a return.", "Zoe · New")],
        ["Elle SA", "Destiny", "Wanted", "House and Leisure"],
        "Boutique · Sandton City precinct.",
        "Lookbook without stock or size path.",
        "Occasion browse, clear sizes, click & collect.",
        [("Demo?", "Yes."), ("Shopify?", "Yes."), ("Appointments?", "Calendar apps fit.")],
        ':root{--bg:#faf8f5;--ink:#1a1512;--muted:#7a7168;--line:#e6e0d8;--accent:#1a1512;--accent-ink:#fff;--panel:#fff;--font-d:"Bodoni Moda",serif;--font-b:"Manrope",sans-serif;--g:clamp(18px,4vw,40px);--max:1200px;--e:cubic-bezier(.22,1,.36,1);--h-w:500;--card-ratio:3/4}',
        MARQUEE_CSS,
    ),
]


HERO_FN = {
    "kinetic": hero_kinetic,
    "split": hero_split,
    "full": hero_full,
    "center": hero_center,
    "tech": hero_tech,
}


def build(b: dict) -> None:
    hero = HERO_FN[b["hero"]](b)
    extras = HERO_EXTRAS[b["hero"]] + b["extras"]
    css = base_css(b["tokens"], extras)
    home = full_home_sections(b, hero, mid_marquee(b))
    base = ROOT / b["slug"]
    write(base / "brand.css", css)
    write(base / "brand.js", JS)
    write(base / "index.html", page(f"{b['full']} — Concept", b["fonts"], home, 0))
    write(base / "collection" / "index.html", page(f"{b['full']} — Shop", b["fonts"], collection_page(b), 1))
    write(base / "product" / "index.html", page(f"{b['full']} — Product", b["fonts"], product_page(b), 1))
    # rough section count
    n = home.count("<section") + home.count('class="trust') + home.count('class="ann')
    print(f"built {b['slug']} (~{n} blocks)")


def main() -> None:
    for b in BRANDS:
        build(b)
    print("done", len(BRANDS))


if __name__ == "__main__":
    main()
