#!/usr/bin/env python3
"""Build distinct showcase storefronts — one unique layout system per brand.

Skips handcrafted: river-quarter, im-naturkosmetik, fieldpaw, ips-germany.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs" / "showcase"


def img(seed: str, w=1200, h=1500) -> str:
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


# ─── Shared tiny JS ───────────────────────────────────────────────────────────

JS = """(() => {
  const top = document.querySelector("[data-top]");
  if (top) {
    const on = () => top.classList.toggle("scrolled", scrollY > 8);
    on(); addEventListener("scroll", on, { passive: true });
  }
  const io = new IntersectionObserver(
    (es) => es.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
    { threshold: 0.12 }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  document.querySelectorAll("[data-tabs] button").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.parentElement.querySelectorAll("button").forEach((b) => b.classList.remove("on"));
      btn.classList.add("on");
    });
  });
  document.querySelectorAll("[data-gal]").forEach((gal) => {
    const main = gal.querySelector("[data-main]");
    gal.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        gal.querySelectorAll("button").forEach((b) => b.classList.remove("on"));
        btn.classList.add("on");
        const i = btn.querySelector("img");
        if (main && i) main.src = i.src.replace(/\\/\\d+\\/\\d+/, "/1200/1500");
      });
    });
  });
})();"""


def page(title: str, fonts: str, css: str, body: str, js_depth: int = 0) -> str:
    prefix = "../" * js_depth
    js = "brand.js" if js_depth == 0 else "../brand.js"
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
<link rel="stylesheet" href="{prefix}brand.css" />
</head>
<body>
<div class="demo">Concept demo</div>
{body}
<script src="{js}"></script>
</body>
</html>"""


def cards(seed: str, products: list[tuple[str, str]], href="product/", n=4) -> str:
    out = []
    for i, (name, price) in enumerate(products[:n]):
        out.append(
            f'<a class="card" href="{href}"><div class="ph"><img src="{img(seed + "-p" + str(i), 800, 1000)}" alt="" /></div>'
            f"<h3>{name}</h3><p>{price}</p></a>"
        )
    return "".join(out)


def simple_collection(b: dict, extra_css_note: str = "") -> str:
    prods = cards(b["seed"], b["products"], "../product/", 8)
    return f"""
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="../">{b["name"]}</a>
  <nav>{"".join(f'<a href="./">{x}</a>' for x in b["links"][:4])}</nav>
  <span class="bag">Bag 0</span>
</div></header>
<section class="col-hero wrap">
  <p class="eye">Collection</p>
  <h1>{b["full"]}</h1>
  <p class="lead">{b["lead"]}</p>
  <div class="tabs" data-tabs>{"".join(f'<button class="{"on" if i==0 else ""}">{x}</button>' for i,x in enumerate(["All"]+b["links"][:4]))}</div>
</section>
<section class="wrap grid-shop reveal">{prods}</section>
<footer class="foot wrap"><div><strong>{b["name"]}</strong></div><div>© 2026 · Concept demo</div></footer>
"""


def simple_product(b: dict) -> str:
    name, price = b["products"][0]
    s = b["seed"]
    thumbs = "".join(
        f'<button class="{"on" if i==0 else ""}"><img src="{img(s+"-g"+str(i), 300, 300)}" alt="" /></button>'
        for i in range(4)
    )
    more = cards(s, b["products"][1:], "./", 4)
    return f"""
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="../">{b["name"]}</a>
  <nav><a href="../collection/">Shop</a></nav>
  <span class="bag">Bag 0</span>
</div></header>
<section class="pdp wrap">
  <div class="gal" data-gal>
    <div class="main"><img src="{img(s+"-g0", 1200, 1500)}" alt="" data-main /></div>
    <div class="thumbs">{thumbs}</div>
  </div>
  <div class="info">
    <p class="eye">{b["locale"]}</p>
    <h1>{name}</h1>
    <p class="price">{price}</p>
    <p class="lead">{b["lead"]}</p>
    <button class="btn">Add to bag</button>
  </div>
</section>
<section class="wrap"><p class="eye">Also consider</p><div class="grid-shop">{more}</div></section>
<footer class="foot wrap"><div><strong>{b["name"]}</strong></div><div>© 2026 · Concept demo</div></footer>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# BRAND LAYOUTS — each returns (css, home_html)
# ═══════════════════════════════════════════════════════════════════════════════

def layout_northline(b):
    """Athletic sprint — dark, ticker, side index, horizontal rail."""
    s = b["seed"]
    css = f"""
:root{{--bg:#0c0e10;--ink:#f2f4f6;--muted:#8b939c;--line:#252a30;--acc:#c8f542;--font-d:"Bebas Neue",sans-serif;--font-b:"DM Sans",sans-serif;--g:clamp(16px,4vw,40px);--max:1200px;--e:cubic-bezier(.22,1,.36,1)}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink);line-height:1.5}}
img{{display:block;width:100%;height:100%;object-fit:cover}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),var(--max));margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--acc);color:#111}}
.top{{position:sticky;top:0;z-index:50;background:rgba(12,14,16,.9);backdrop-filter:blur(12px);border-bottom:1px solid transparent}}.top.scrolled{{border-color:var(--line)}}
.nav{{display:flex;align-items:center;justify-content:space-between;min-height:64px;gap:16px}}
.logo{{font-family:var(--font-d);font-size:28px;letter-spacing:.06em}}nav{{display:flex;gap:18px;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}}@media(max-width:800px){{nav{{display:none}}}}
.bag{{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--acc);padding:8px 12px;color:var(--acc)}}
.ticker{{overflow:hidden;border-block:1px solid var(--line);padding:10px 0;white-space:nowrap}}.ticker b{{display:inline-block;animation:t 22s linear infinite;font-family:var(--font-d);font-size:18px;letter-spacing:.08em}}
@keyframes t{{from{{transform:translateX(0)}}to{{transform:translateX(-50%)}}}}
.hero{{display:grid;grid-template-columns:80px 1fr;min-height:88vh}}
.side{{writing-mode:vertical-rl;transform:rotate(180deg);display:flex;align-items:center;justify-content:center;gap:24px;border-right:1px solid var(--line);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}}
.hero-main{{position:relative;display:grid;align-items:end;padding:var(--g);isolation:isolate}}
.hero-main img{{position:absolute;inset:0;z-index:-1;filter:brightness(.55)}}
.hero-main h1{{font-family:var(--font-d);font-size:clamp(64px,14vw,140px);line-height:.85;letter-spacing:.02em;max-width:8ch}}
.hero-main p{{max-width:36ch;color:rgba(242,244,246,.75);margin:14px 0 22px}}
.btn{{display:inline-flex;padding:14px 22px;background:var(--acc);color:#111;font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:12px;border:0}}
.rail{{display:flex;gap:12px;overflow-x:auto;padding:28px var(--g);scroll-snap-type:x mandatory}}.rail .card{{flex:0 0 240px;scroll-snap-align:start}}
.card .ph{{aspect-ratio:4/5;background:#1a1e22;margin-bottom:10px}}
.card h3{{font-size:14px;font-weight:700}}.card p{{color:var(--acc);font-weight:800;margin-top:4px}}
.sec{{padding:clamp(40px,7vw,80px) 0}}.eye{{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);font-weight:700;margin-bottom:10px}}
.h2{{font-family:var(--font-d);font-size:clamp(36px,6vw,64px);letter-spacing:.02em}}
.split{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}@media(max-width:800px){{.hero{{grid-template-columns:1fr}}.side{{display:none}}.split{{grid-template-columns:1fr}}}}
.stat{{border:1px solid var(--line);padding:24px}}.stat strong{{font-family:var(--font-d);font-size:48px;color:var(--acc);display:block}}
.grid-shop{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding-block:32px}}@media(max-width:900px){{.grid-shop{{grid-template-columns:1fr 1fr}}}}
.col-hero{{padding:48px 0 16px}}.col-hero h1{{font-family:var(--font-d);font-size:clamp(40px,8vw,72px)}}
.tabs{{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}}.tabs button{{padding:9px 14px;background:transparent;border:1px solid var(--line);color:var(--ink);font-weight:700;cursor:pointer}}.tabs button.on{{background:var(--acc);color:#111;border-color:var(--acc)}}
.pdp{{display:grid;grid-template-columns:1.1fr .9fr;gap:32px;padding:48px 0}}@media(max-width:900px){{.pdp{{grid-template-columns:1fr}}}}
.gal .main{{aspect-ratio:4/5;background:#1a1e22}}.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px}}.thumbs button{{aspect-ratio:1;border:1px solid var(--line);padding:0;opacity:.5;background:0;cursor:pointer}}.thumbs button.on{{opacity:1;outline:2px solid var(--acc)}}
.info h1{{font-family:var(--font-d);font-size:clamp(32px,5vw,48px)}}.price{{font-size:24px;color:var(--acc);font-weight:800;margin:12px 0}}.lead{{color:var(--muted);margin-bottom:20px}}
.foot{{display:flex;justify-content:space-between;padding:40px 0;border-top:1px solid var(--line);margin-top:40px;font-size:13px;color:var(--muted)}}
.reveal{{opacity:0;transform:translateY(20px);transition:.7s var(--e)}}.reveal.in{{opacity:1;transform:none}}
"""
    home = f"""
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="./">{b["name"].upper()}</a>
  <nav>{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"])}</nav>
  <span class="bag">Bag 0</span>
</div></header>
<div class="ticker"><b>{b["ann"]} · {b["tagline"]} · {b["ann"]} · {b["tagline"]} · </b></div>
<section class="hero">
  <aside class="side"><span>01 Run</span><span>02 Train</span><span>03 Outer</span></aside>
  <div class="hero-main">
    <img src="{img(s+'-hero',1600,2000)}" alt="" />
    <div>
      <h1>{b["tagline"]}</h1>
      <p>{b["lead"]}</p>
      <a class="btn" href="collection/">Shop Drop 07</a>
    </div>
  </div>
</section>
<section class="reveal">
  <div class="wrap" style="padding-top:40px"><p class="eye">Sprint edit</p><h2 class="h2">Move next</h2></div>
  <div class="rail">{cards(s, b["products"], n=6)}</div>
</section>
<section class="sec wrap reveal">
  <div class="split">
    <div class="stat"><strong>−12°</strong><span>Cold-start tested</span></div>
    <div class="stat"><strong>360g</strong><span>Shell weight class</span></div>
  </div>
</section>
<section class="sec wrap reveal">
  <div class="split">
    <div><p class="eye">{b["locale"]}</p><h2 class="h2">Built for intervals</h2><p class="lead" style="margin-top:12px">{b["lead"]}</p><a class="btn" href="product/" style="margin-top:20px">View apex jacket</a></div>
    <div style="aspect-ratio:4/5;background:#1a1e22"><img src="{img(s+'-story',1000,1250)}" alt="" /></div>
  </div>
</section>
<footer class="foot wrap"><div><strong>{b["full"]}</strong></div><div>© 2026 · Concept / not a live store</div></footer>
"""
    return css, home


def layout_maris(b):
    """Jewelry atelier — centered, soft, chapter scrolls."""
    s = b["seed"]
    css = f"""
:root{{--bg:#f7f1ea;--ink:#2a221c;--muted:#7a6e64;--line:#e4d8cc;--acc:#8b5e3c;--font-d:"Cormorant Garamond",serif;--font-b:"Figtree",sans-serif;--g:clamp(18px,4vw,40px);--max:980px;--e:cubic-bezier(.22,1,.36,1)}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink);text-align:center}}
img{{display:block;width:100%;height:100%;object-fit:cover}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),var(--max));margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--ink);color:var(--bg);text-align:left}}
.top{{padding:28px var(--g) 12px}}.logo{{font-family:var(--font-d);font-size:32px;font-weight:600}}.nav{{display:flex;justify-content:center;gap:28px;margin-top:18px;font-size:12px;letter-spacing:.16em;text-transform:uppercase}}@media(max-width:700px){{.nav{{display:none}}}}
.hero{{padding:48px var(--g) 64px}}.hero .still{{width:min(420px,78vw);aspect-ratio:1;margin:0 auto 28px;border-radius:50%;overflow:hidden;border:1px solid var(--line)}}
.hero h1{{font-family:var(--font-d);font-size:clamp(40px,7vw,68px);font-weight:500;line-height:1.05}}
.hero p{{color:var(--muted);max-width:34ch;margin:14px auto 24px;line-height:1.7}}
.btn{{display:inline-flex;padding:13px 26px;border:1px solid var(--ink);font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:700}}
.chapter{{padding:72px var(--g);border-top:1px solid var(--line)}}.chapter h2{{font-family:var(--font-d);font-size:clamp(28px,4vw,40px);font-weight:500;margin-bottom:8px}}
.chapter .eye{{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}}
.stack{{display:grid;gap:40px;margin-top:36px}}.stack article{{display:grid;gap:14px;justify-items:center}}
.stack .ph{{width:min(280px,70vw);aspect-ratio:1;background:#efe6dc}}
.stack h3{{font-family:var(--font-d);font-size:24px;font-weight:500}}.stack p{{color:var(--muted);font-size:14px}}
.grid-shop{{display:grid;grid-template-columns:repeat(2,1fr);gap:28px;padding:40px 0;text-align:left}}@media(max-width:600px){{.grid-shop{{grid-template-columns:1fr}}}}
.card .ph{{aspect-ratio:1;background:#efe6dc;margin-bottom:12px;border-radius:50%;overflow:hidden}}.card h3{{font-family:var(--font-d);font-size:22px;font-weight:500}}.card p{{color:var(--muted);margin-top:4px}}
.col-hero{{padding:48px 0 20px;text-align:center}}.col-hero h1{{font-family:var(--font-d);font-size:clamp(36px,6vw,56px);font-weight:500}}
.tabs{{display:flex;justify-content:center;flex-wrap:wrap;gap:8px;margin-top:18px}}.tabs button{{padding:8px 14px;border:1px solid var(--line);background:0;cursor:pointer;font-size:11px;letter-spacing:.1em;text-transform:uppercase}}.tabs button.on{{border-color:var(--ink)}}
.pdp{{display:grid;grid-template-columns:1fr 1fr;gap:40px;padding:48px 0;text-align:left}}@media(max-width:800px){{.pdp{{grid-template-columns:1fr}}}}
.gal .main{{aspect-ratio:1;border-radius:50%;overflow:hidden;background:#efe6dc}}.thumbs{{display:flex;justify-content:center;gap:8px;margin-top:12px}}.thumbs button{{width:56px;height:56px;border-radius:50%;border:1px solid var(--line);padding:0;overflow:hidden;opacity:.5;cursor:pointer}}.thumbs button.on{{opacity:1}}
.info h1{{font-family:var(--font-d);font-size:40px;font-weight:500}}.price{{font-size:20px;margin:12px 0}}.lead{{color:var(--muted)}}
.foot{{padding:40px 0;border-top:1px solid var(--line);margin-top:40px;display:flex;justify-content:space-between;font-size:13px;color:var(--muted);text-align:left}}
.bag{{display:none}}.reveal{{opacity:0;transform:translateY(16px);transition:.8s var(--e)}}.reveal.in{{opacity:1;transform:none}}
"""
    arts = "".join(
        f'<article><div class="ph"><img src="{img(s+"-c"+str(i),700,700)}" alt="" /></div><h3>{n}</h3><p>{p}</p></article>'
        for i, (n, p) in enumerate(b["products"][:4])
    )
    home = f"""
<header class="top">
  <a class="logo" href="./">{b["name"]}</a>
  <nav class="nav">{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"])}</nav>
</header>
<section class="hero">
  <div class="still"><img src="{img(s+'-hero',900,900)}" alt="" /></div>
  <h1>{b["tagline"]}</h1>
  <p>{b["lead"]}</p>
  <a class="btn" href="collection/">View collection</a>
</section>
<section class="chapter reveal">
  <p class="eye">Chapter I · {b["locale"]}</p>
  <h2>Pieces made to be noticed in the hand</h2>
  <div class="stack">{arts}</div>
</section>
<section class="chapter reveal">
  <p class="eye">Appointments</p>
  <h2>Private viewing Thu–Sat</h2>
  <p style="color:var(--muted);max-width:36ch;margin:12px auto 24px">Try weight, clasp, and stone under atelier light — then buy online with the same finish notes.</p>
  <a class="btn" href="product/">Featured: {b["products"][0][0]}</a>
</section>
<footer class="foot wrap"><div>{b["full"]}</div><div>© 2026 · Concept demo</div></footer>
"""
    return css, home


def layout_cedar(b):
    """Atmosphere rooms — full-bleed scent chapters."""
    s = b["seed"]
    css = f"""
:root{{--bg:#1a1814;--ink:#f3efe6;--muted:#a39a8c;--line:#2f2b24;--acc:#c4a574;--font-d:"Fraunces",serif;--font-b:"Sora",sans-serif;--g:clamp(18px,4vw,40px);--e:cubic-bezier(.22,1,.36,1)}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink)}}
img{{display:block;width:100%;height:100%;object-fit:cover}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),1100px);margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--acc);color:#1a1814}}
.top{{position:fixed;inset:0 0 auto;z-index:40;padding:20px var(--g);display:flex;justify-content:space-between;mix-blend-mode:difference}}
.logo{{font-family:var(--font-d);font-size:22px}}.nav{{display:flex;gap:20px;font-size:12px;letter-spacing:.12em;text-transform:uppercase}}@media(max-width:700px){{.nav{{display:none}}}}
.room{{min-height:100vh;position:relative;display:grid;align-items:end;padding:var(--g);isolation:isolate}}
.room img{{position:absolute;inset:0;z-index:-1;filter:brightness(.45)}}
.room h1,.room h2{{font-family:var(--font-d);font-weight:500;font-size:clamp(40px,8vw,80px);line-height:1;max-width:10ch}}
.room p{{max-width:34ch;color:rgba(243,239,230,.75);margin:14px 0 22px}}
.btn{{display:inline-flex;padding:13px 20px;background:var(--acc);color:#1a1814;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}}
.notes{{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}}.notes span{{border:1px solid rgba(243,239,230,.35);padding:8px 12px;font-size:11px;letter-spacing:.1em;text-transform:uppercase}}
.strip{{display:grid;grid-template-columns:repeat(3,1fr)}}@media(max-width:800px){{.strip{{grid-template-columns:1fr}}}}
.strip a{{position:relative;min-height:50vh;display:flex;align-items:flex-end;padding:24px;isolation:isolate;border:1px solid var(--line)}}
.strip a img{{position:absolute;inset:0;z-index:-1;filter:brightness(.4)}}
.strip h3{{font-family:var(--font-d);font-size:28px;font-weight:500}}
.grid-shop{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;padding:48px 0}}@media(max-width:900px){{.grid-shop{{grid-template-columns:1fr 1fr}}}}
.card .ph{{aspect-ratio:1;background:#2a2620;margin-bottom:10px}}.card h3{{font-size:14px}}.card p{{color:var(--acc);margin-top:4px}}
.col-hero{{padding:120px 0 20px}}.col-hero h1{{font-family:var(--font-d);font-size:clamp(40px,7vw,64px);font-weight:500}}
.tabs{{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}}.tabs button{{padding:8px 12px;background:0;border:1px solid var(--line);color:var(--ink);cursor:pointer}}.tabs button.on{{border-color:var(--acc);color:var(--acc)}}
.pdp{{display:grid;grid-template-columns:1fr 1fr;gap:32px;padding:120px 0 48px}}@media(max-width:800px){{.pdp{{grid-template-columns:1fr;padding-top:100px}}}}
.gal .main{{aspect-ratio:1;background:#2a2620}}.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px}}.thumbs button{{border:1px solid var(--line);padding:0;aspect-ratio:1;opacity:.5;cursor:pointer;background:0}}.thumbs button.on{{opacity:1}}
.info h1{{font-family:var(--font-d);font-size:40px;font-weight:500}}.price{{color:var(--acc);font-size:22px;margin:12px 0}}.lead{{color:var(--muted)}}
.bag{{font-size:11px;letter-spacing:.1em;text-transform:uppercase}}.foot{{padding:40px var(--g);border-top:1px solid var(--line);display:flex;justify-content:space-between;color:var(--muted);font-size:13px}}
.reveal{{opacity:0;transition:1s var(--e)}}.reveal.in{{opacity:1}}
.eye{{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}}
"""
    rooms = "".join(
        f'<a href="product/"><img src="{img(s+"-r"+str(i),1000,1400)}" alt="" /><div><h3>{n}</h3><p style="opacity:.7;margin-top:4px">{p}</p></div></a>'
        for i, (n, p) in enumerate(b["products"][:3])
    )
    home = f"""
<header class="top">
  <a class="logo" href="./">{b["name"]}</a>
  <nav class="nav">{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"][:4])}<span class="bag">Bag</span></nav>
</header>
<section class="room">
  <img src="{img(s+'-hero',1800,2200)}" alt="" />
  <div>
    <p class="eye">{b["locale"]}</p>
    <h1>{b["tagline"]}</h1>
    <p>{b["lead"]}</p>
    <div class="notes"><span>Fig</span><span>Cedar</span><span>Salt air</span><span>Resin</span></div>
    <div style="margin-top:22px"><a class="btn" href="collection/">Enter the rooms</a></div>
  </div>
</section>
<section class="strip reveal">{rooms}</section>
<section class="wrap" style="padding:64px 0">
  <p class="eye">Ritual</p>
  <h2 style="font-family:var(--font-d);font-size:clamp(28px,4vw,44px);font-weight:500;max-width:16ch">Fragrance that behaves like furniture</h2>
  <div class="grid-shop">{cards(s, b["products"], n=4)}</div>
</section>
<footer class="foot"><div>{b["full"]}</div><div>© 2026 · Concept</div></footer>
"""
    return css, home


def layout_volt(b):
    """Kitchen utility — bold yellow/black spec grid."""
    s = b["seed"]
    css = f"""
:root{{--bg:#111;--ink:#f5f5f0;--muted:#9a9a90;--line:#2a2a2a;--acc:#ffe600;--font-d:"Space Grotesk",sans-serif;--font-b:"IBM Plex Sans",sans-serif;--g:clamp(16px,4vw,36px);--max:1180px}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink)}}
img{{display:block;width:100%;height:100%;object-fit:cover}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),var(--max));margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--acc);color:#111}}
.top{{border-bottom:3px solid var(--acc)}}.nav{{display:flex;align-items:center;justify-content:space-between;min-height:64px}}
.logo{{font-family:var(--font-d);font-weight:700;font-size:24px;text-transform:uppercase}}nav{{display:flex;gap:16px;font-size:12px;font-weight:700;text-transform:uppercase}}@media(max-width:800px){{nav{{display:none}}}}
.bag{{background:var(--acc);color:#111;padding:8px 12px;font-weight:800;font-size:11px;text-transform:uppercase}}
.hero{{display:grid;grid-template-columns:1.2fr .8fr;border-bottom:3px solid var(--acc)}}
.hero .copy{{padding:clamp(32px,6vw,64px);background:var(--acc);color:#111}}
.hero h1{{font-family:var(--font-d);font-size:clamp(40px,7vw,72px);line-height:.95;text-transform:uppercase}}
.hero p{{margin:14px 0 22px;max-width:36ch;font-weight:500}}
.btn{{display:inline-flex;padding:12px 18px;background:#111;color:var(--acc);font-weight:800;text-transform:uppercase;font-size:12px;letter-spacing:.06em}}
.hero .media{{min-height:50vh}}
.specs{{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid var(--line)}}
.specs div{{padding:20px;border-right:1px solid var(--line);font-size:12px;text-transform:uppercase;letter-spacing:.06em}}.specs div:last-child{{border:0}}
.specs strong{{display:block;font-family:var(--font-d);font-size:28px;color:var(--acc);margin-bottom:4px}}
@media(max-width:800px){{.hero{{grid-template-columns:1fr}}.specs{{grid-template-columns:1fr 1fr}}}}
.sec{{padding:48px 0}}.eye{{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}}
.h2{{font-family:var(--font-d);font-size:clamp(28px,4vw,44px);text-transform:uppercase}}
.grid-shop{{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:var(--line)}}
.card{{background:var(--bg);padding:0 0 14px}}.card .ph{{aspect-ratio:1;background:#1a1a1a;margin-bottom:10px}}.card h3{{padding:0 12px;font-size:14px;font-weight:700}}.card p{{padding:0 12px;color:var(--acc);font-weight:800;margin-top:4px}}
@media(max-width:900px){{.grid-shop{{grid-template-columns:1fr 1fr}}}}
.col-hero{{padding:40px 0 16px}}.col-hero h1{{font-family:var(--font-d);font-size:48px;text-transform:uppercase}}
.tabs{{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}}.tabs button{{padding:8px 12px;background:0;border:1px solid var(--line);color:var(--ink);cursor:pointer;text-transform:uppercase;font-size:11px;font-weight:700}}.tabs button.on{{background:var(--acc);color:#111;border-color:var(--acc)}}
.pdp{{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:40px 0}}@media(max-width:800px){{.pdp{{grid-template-columns:1fr}}}}
.gal .main{{aspect-ratio:1;background:#1a1a1a;border:3px solid var(--acc)}}.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}}.thumbs button{{border:1px solid var(--line);padding:0;aspect-ratio:1;opacity:.5;cursor:pointer;background:0}}.thumbs button.on{{opacity:1;border-color:var(--acc)}}
.info h1{{font-family:var(--font-d);font-size:36px;text-transform:uppercase}}.price{{color:var(--acc);font-size:28px;font-weight:800;margin:10px 0}}.lead{{color:var(--muted)}}
.foot{{border-top:3px solid var(--acc);padding:28px 0;display:flex;justify-content:space-between;font-size:13px;color:var(--muted)}}
.reveal{{opacity:0;transform:translateY(12px);transition:.5s}}.reveal.in{{opacity:1;transform:none}}
"""
    home = f"""
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="./">{b["name"]}</a>
  <nav>{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"])}</nav>
  <span class="bag">Bag 0</span>
</div></header>
<section class="hero">
  <div class="copy">
    <h1>{b["tagline"]}</h1>
    <p>{b["lead"]}</p>
    <a class="btn" href="collection/">Shop cookware</a>
  </div>
  <div class="media"><img src="{img(s+'-hero',1200,1400)}" alt="" /></div>
</section>
<div class="specs wrap" style="width:100%;max-width:none">
  <div><strong>260°C</strong>Heat test</div>
  <div><strong>28cm</strong>Skillet class</div>
  <div><strong>30d</strong>Return window</div>
  <div><strong>{b["locale"]}</strong>Built for</div>
</div>
<section class="sec wrap reveal">
  <p class="eye">Tool wall</p>
  <h2 class="h2">Spec the line</h2>
  <div class="grid-shop" style="margin-top:20px">{cards(s, b["products"], n=8)}</div>
</section>
<footer class="foot wrap"><div>{b["full"]}</div><div>© 2026 · Concept</div></footer>
"""
    return css, home


def layout_lumen(b):
    """Eyewear — orbit frames, try-on mock UI."""
    s = b["seed"]
    css = f"""
:root{{--bg:#f4f6f8;--ink:#12141a;--muted:#667084;--line:#d5dae3;--acc:#5b7cfa;--font-d:"Syne",sans-serif;--font-b:"Outfit",sans-serif;--g:clamp(18px,4vw,40px);--max:1120px}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink)}}
img{{display:block;width:100%;height:100%;object-fit:cover}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),var(--max));margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--ink);color:#fff}}
.top{{position:sticky;top:0;background:rgba(244,246,248,.92);backdrop-filter:blur(10px);z-index:40}}
.nav{{display:flex;align-items:center;justify-content:space-between;min-height:68px}}
.logo{{font-family:var(--font-d);font-weight:800;font-size:26px;letter-spacing:-.04em}}nav{{display:flex;gap:18px;font-size:13px;font-weight:600}}@media(max-width:800px){{nav{{display:none}}}}
.bag{{border:1px solid var(--ink);padding:8px 12px;border-radius:999px;font-size:11px;font-weight:700}}
.hero{{display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:center;padding:48px 0;min-height:80vh}}
.hero h1{{font-family:var(--font-d);font-size:clamp(40px,6vw,64px);font-weight:800;letter-spacing:-.05em;line-height:1}}
.hero p{{color:var(--muted);margin:14px 0 22px;max-width:36ch}}
.btn{{display:inline-flex;padding:13px 20px;background:var(--acc);color:#fff;border-radius:999px;font-weight:700;font-size:13px}}
.orbit{{aspect-ratio:1;border-radius:50%;border:1px dashed var(--line);display:grid;place-items:center;position:relative;background:radial-gradient(circle at 30% 30%,#fff,#e8ecf3)}}
.orbit .frame{{width:55%;aspect-ratio:16/7;border-radius:40px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.12)}}
.fit{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:28px}}
.fit div{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;text-align:center;font-size:12px;font-weight:700}}
.fit strong{{display:block;font-family:var(--font-d);font-size:22px;margin-bottom:4px}}
@media(max-width:800px){{.hero{{grid-template-columns:1fr}}.fit{{grid-template-columns:1fr}}}}
.sec{{padding:48px 0}}.eye{{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);font-weight:700;margin-bottom:8px}}
.h2{{font-family:var(--font-d);font-size:clamp(28px,4vw,40px);font-weight:800;letter-spacing:-.04em}}
.grid-shop{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}.card{{background:#fff;border-radius:20px;overflow:hidden;border:1px solid var(--line)}}.card .ph{{aspect-ratio:1}}.card h3,.card p{{padding:0 14px}}.card h3{{margin-top:12px;font-size:14px}}.card p{{color:var(--acc);font-weight:700;margin:6px 0 14px}}
@media(max-width:900px){{.grid-shop{{grid-template-columns:1fr 1fr}}}}
.col-hero{{padding:40px 0 16px}}.col-hero h1{{font-family:var(--font-d);font-size:48px;font-weight:800;letter-spacing:-.04em}}
.tabs{{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}}.tabs button{{padding:8px 14px;border-radius:999px;border:1px solid var(--line);background:#fff;cursor:pointer}}.tabs button.on{{background:var(--ink);color:#fff}}
.pdp{{display:grid;grid-template-columns:1fr 1fr;gap:32px;padding:40px 0}}@media(max-width:800px){{.pdp{{grid-template-columns:1fr}}}}
.gal .main{{aspect-ratio:1;border-radius:24px;overflow:hidden;background:#fff;border:1px solid var(--line)}}.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px}}.thumbs button{{border-radius:12px;border:1px solid var(--line);padding:0;aspect-ratio:1;opacity:.55;cursor:pointer;background:#fff}}.thumbs button.on{{opacity:1;outline:2px solid var(--acc)}}
.info h1{{font-family:var(--font-d);font-size:36px;font-weight:800;letter-spacing:-.04em}}.price{{font-size:24px;font-weight:800;margin:10px 0}}.lead{{color:var(--muted)}}
.foot{{padding:40px 0;border-top:1px solid var(--line);display:flex;justify-content:space-between;color:var(--muted);font-size:13px;margin-top:40px}}
.reveal{{opacity:0;transform:translateY(16px);transition:.7s}}.reveal.in{{opacity:1;transform:none}}
"""
    home = f"""
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="./">{b["name"]}</a>
  <nav>{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"])}</nav>
  <span class="bag">Bag 0</span>
</div></header>
<section class="wrap hero">
  <div>
    <p class="eye">{b["locale"]} · Fit lab</p>
    <h1>{b["tagline"]}</h1>
    <p>{b["lead"]}</p>
    <a class="btn" href="collection/">Try the edit</a>
    <div class="fit"><div><strong>12</strong>Bridge widths</div><div><strong>AR</strong>Try-on ready</div><div><strong>30d</strong>Free returns</div></div>
  </div>
  <div class="orbit"><div class="frame"><img src="{img(s+'-hero',900,400)}" alt="" /></div></div>
</section>
<section class="wrap sec reveal">
  <p class="eye">Frames</p>
  <h2 class="h2">Optical + sun</h2>
  <div class="grid-shop" style="margin-top:20px">{cards(s, b["products"], n=4)}</div>
</section>
<footer class="foot wrap"><div>{b["full"]}</div><div>© 2026 · Concept</div></footer>
"""
    return css, home


def layout_exclusive(b):
    """Furniture rooms — horizontal room chapters + finish chips."""
    s = b["seed"]
    css = f"""
:root{{--bg:#f3efe8;--ink:#1c1915;--muted:#6f675c;--line:#ddd4c6;--acc:#3d5a40;--font-d:"Libre Baskerville",serif;--font-b:"Karla",sans-serif;--g:clamp(18px,4vw,40px);--max:1200px}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink)}}
img{{display:block;width:100%;height:100%;object-fit:cover}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),var(--max));margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--ink);color:var(--bg)}}
.top{{border-bottom:1px solid var(--line);background:rgba(243,239,232,.94);position:sticky;top:0;z-index:40}}
.nav{{display:flex;align-items:center;justify-content:space-between;min-height:70px}}.logo{{font-family:var(--font-d);font-size:22px}}nav{{display:flex;gap:20px;font-size:13px}}@media(max-width:800px){{nav{{display:none}}}}
.bag{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700}}
.hero{{display:grid;grid-template-columns:.9fr 1.1fr;min-height:85vh}}
.hero .copy{{padding:clamp(36px,6vw,64px);display:flex;flex-direction:column;justify-content:center}}
.hero h1{{font-family:var(--font-d);font-size:clamp(36px,5vw,56px);line-height:1.1;font-weight:400}}
.hero p{{color:var(--muted);margin:16px 0 24px;max-width:38ch;line-height:1.7}}
.btn{{display:inline-flex;padding:13px 20px;background:var(--acc);color:#fff;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}}
.finishes{{display:flex;gap:10px;margin-top:28px}}.finishes i{{width:28px;height:28px;border-radius:50%;border:1px solid var(--line);display:block}}
.room-row{{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;border-block:1px solid var(--line)}}
.room-row a{{flex:0 0 min(78vw,640px);scroll-snap-align:start;min-height:70vh;position:relative;display:flex;align-items:flex-end;padding:28px;color:#fff;isolation:isolate}}
.room-row a img{{position:absolute;inset:0;z-index:-2}}.room-row a::before{{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(transparent,rgba(0,0,0,.65))}}
.room-row h3{{font-family:var(--font-d);font-size:32px;font-weight:400}}
.sec{{padding:56px 0}}.eye{{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}}
.h2{{font-family:var(--font-d);font-size:clamp(28px,4vw,40px);font-weight:400}}
.grid-shop{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}.card .ph{{aspect-ratio:4/5;background:#e8e0d4;margin-bottom:10px}}.card h3{{font-size:14px}}.card p{{color:var(--muted);margin-top:4px}}
@media(max-width:900px){{.hero{{grid-template-columns:1fr}}.grid-shop{{grid-template-columns:1fr 1fr}}}}
.meta-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:28px}}.meta-row div{{border:1px solid var(--line);padding:18px;background:#fff}}
.meta-row strong{{display:block;font-family:var(--font-d);font-size:20px;margin-bottom:4px}}
.col-hero{{padding:40px 0 16px}}.col-hero h1{{font-family:var(--font-d);font-size:44px;font-weight:400}}
.tabs{{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}}.tabs button{{padding:8px 14px;border:1px solid var(--line);background:#fff;cursor:pointer}}.tabs button.on{{background:var(--ink);color:#fff}}
.pdp{{display:grid;grid-template-columns:1.15fr .85fr;gap:32px;padding:40px 0}}@media(max-width:800px){{.pdp{{grid-template-columns:1fr}}}}
.gal .main{{aspect-ratio:4/5;background:#e8e0d4}}.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px}}.thumbs button{{border:1px solid var(--line);padding:0;aspect-ratio:1;opacity:.55;cursor:pointer;background:#fff}}.thumbs button.on{{opacity:1}}
.info h1{{font-family:var(--font-d);font-size:34px;font-weight:400}}.price{{font-size:22px;margin:12px 0}}.lead{{color:var(--muted)}}
.foot{{padding:40px 0;border-top:1px solid var(--line);display:flex;justify-content:space-between;color:var(--muted);font-size:13px;margin-top:40px}}
.reveal{{opacity:0;transform:translateY(16px);transition:.7s}}.reveal.in{{opacity:1;transform:none}}
"""
    rooms = "".join(
        f'<a href="collection/"><img src="{img(s+"-room"+str(i),1400,1600)}" alt="" /><div><p class="eye" style="color:rgba(255,255,255,.7)">{b["links"][i] if i < len(b["links"]) else "Room"}</p><h3>{n}</h3></div></a>'
        for i, (n, _) in enumerate(b["products"][:4])
    )
    home = f"""
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="./">{b["name"]}</a>
  <nav>{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"])}</nav>
  <span class="bag">Bag 0</span>
</div></header>
<section class="hero">
  <div class="copy">
    <p class="eye">{b["locale"]}</p>
    <h1>{b["tagline"]}</h1>
    <p>{b["lead"]}</p>
    <a class="btn" href="collection/">Shop in stock</a>
    <div class="finishes"><i style="background:#c4a574"></i><i style="background:#5c4033"></i><i style="background:#d9d2c5"></i><i style="background:#2f2a24"></i></div>
  </div>
  <div><img src="{img(s+'-hero',1400,1600)}" alt="" style="height:100%;min-height:50vh" /></div>
</section>
<div class="room-row reveal">{rooms}</div>
<section class="sec wrap reveal">
  <p class="eye">Lead times · finishes · delivery</p>
  <h2 class="h2">Not just a photo gallery</h2>
  <div class="meta-row">
    <div><strong>6–10 wks</strong>Made-to-order oak</div>
    <div><strong>In stock</strong>Showroom pieces</div>
    <div><strong>DE</strong>White-glove option</div>
  </div>
  <div class="grid-shop" style="margin-top:32px">{cards(s, b["products"], n=4)}</div>
</section>
<footer class="foot wrap"><div>{b["full"]}</div><div>© 2026 · Concept</div></footer>
"""
    return css, home


def layout_mican(b):
    """Trade supply — dense SKU table + pack sizes."""
    s = b["seed"]
    css = f"""
:root{{--bg:#f0f2f0;--ink:#141414;--muted:#5c6360;--line:#c9d0cb;--acc:#e8a317;--font-d:"Barlow Condensed",sans-serif;--font-b:"Barlow",sans-serif;--g:clamp(16px,4vw,32px);--max:1200px}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink)}}
img{{display:block;width:100%;height:100%;object-fit:cover}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),var(--max));margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--ink);color:#fff}}
.top{{background:var(--ink);color:#fff}}.nav{{display:flex;align-items:center;justify-content:space-between;min-height:60px}}.logo{{font-family:var(--font-d);font-size:28px;font-weight:700;text-transform:uppercase;color:var(--acc)}}
nav{{display:flex;gap:16px;font-size:12px;font-weight:700;text-transform:uppercase}}@media(max-width:800px){{nav{{display:none}}}}
.bag{{background:var(--acc);color:#111;padding:8px 12px;font-weight:800;font-size:11px;text-transform:uppercase}}
.hero{{display:grid;grid-template-columns:1fr 1fr;background:var(--ink);color:#fff}}
.hero .copy{{padding:clamp(28px,5vw,48px)}}.hero h1{{font-family:var(--font-d);font-size:clamp(40px,7vw,64px);text-transform:uppercase;line-height:.95}}
.hero p{{color:#aab2ae;margin:12px 0 20px;max-width:40ch}}.search{{display:grid;grid-template-columns:1fr auto}}.search input{{padding:12px;border:0}}.search button{{padding:12px 16px;background:var(--acc);border:0;font-weight:800;text-transform:uppercase}}
.hero .media{{min-height:40vh}}
.table{{width:100%;border-collapse:collapse;font-size:14px;background:#fff;margin-top:20px}}
.table th,.table td{{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left}}.table th{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);background:#e8ece9}}
.table tr:hover td{{background:#f7f9f7}}.sku{{font-family:ui-monospace,monospace;font-size:12px;color:var(--muted)}}
.btn{{display:inline-flex;padding:10px 14px;background:var(--acc);color:#111;font-weight:800;font-size:11px;text-transform:uppercase}}
.sec{{padding:40px 0}}.eye{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:700}}.h2{{font-family:var(--font-d);font-size:36px;text-transform:uppercase}}
.grid-shop{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}.card{{background:#fff;border:1px solid var(--line)}}.card .ph{{aspect-ratio:1;background:#dde3df}}.card h3{{padding:10px 12px 0;font-size:14px}}.card p{{padding:4px 12px 12px;font-weight:800}}
@media(max-width:800px){{.hero{{grid-template-columns:1fr}}.grid-shop{{grid-template-columns:1fr 1fr}}.table{{font-size:12px}}}}
.col-hero{{padding:32px 0 12px}}.col-hero h1{{font-family:var(--font-d);font-size:42px;text-transform:uppercase}}
.tabs{{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}}.tabs button{{padding:8px 12px;border:1px solid var(--line);background:#fff;cursor:pointer;font-weight:700;text-transform:uppercase;font-size:11px}}.tabs button.on{{background:var(--ink);color:#fff}}
.pdp{{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:32px 0}}@media(max-width:800px){{.pdp{{grid-template-columns:1fr}}}}
.gal .main{{aspect-ratio:1;background:#dde3df;border:1px solid var(--line)}}.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}}.thumbs button{{border:1px solid var(--line);padding:0;aspect-ratio:1;opacity:.5;cursor:pointer;background:#fff}}.thumbs button.on{{opacity:1}}
.info h1{{font-family:var(--font-d);font-size:36px;text-transform:uppercase}}.price{{font-size:24px;font-weight:800;margin:10px 0}}.lead{{color:var(--muted)}}
.foot{{background:var(--ink);color:#aab2ae;padding:28px 0;margin-top:40px}}.foot .wrap{{display:flex;justify-content:space-between}}
.reveal{{opacity:0;transition:.5s}}.reveal.in{{opacity:1}}
"""
    rows = "".join(
        f"<tr><td class='sku'>{b['seed'].upper()}-{100+i}</td><td>{n}</td><td>Pack 1 / 5 / 10</td><td>{p}</td><td><a class='btn' href='product/'>Add</a></td></tr>"
        for i, (n, p) in enumerate(b["products"][:6])
    )
    home = f"""
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="./">{b["name"]}</a>
  <nav>{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"])}</nav>
  <span class="bag">Trade</span>
</div></header>
<section class="hero">
  <div class="copy">
    <h1>{b["tagline"]}</h1>
    <p>{b["lead"]}</p>
    <form class="search" action="collection/" method="get"><input name="q" placeholder="SKU / tool name" /><button type="submit">Search</button></form>
  </div>
  <div class="media"><img src="{img(s+'-hero',1200,1200)}" alt="" /></div>
</section>
<section class="sec wrap reveal">
  <p class="eye">{b["locale"]} · Net terms</p>
  <h2 class="h2">Fast movers</h2>
  <table class="table"><thead><tr><th>SKU</th><th>Product</th><th>Pack</th><th>Price</th><th></th></tr></thead><tbody>{rows}</tbody></table>
</section>
<section class="sec wrap reveal">
  <div class="grid-shop">{cards(s, b["products"], n=4)}</div>
</section>
<footer class="foot"><div class="wrap"><div>{b["full"]}</div><div>© 2026 · Concept</div></div></footer>
"""
    return css, home


def layout_gip(b):
    """Cross-ref B2B — search + compare columns."""
    s = b["seed"]
    css = f"""
:root{{--bg:#eef1f4;--ink:#15202b;--muted:#5d6b7a;--line:#c5ced6;--acc:#0b6e4f;--font-d:"Archivo",sans-serif;--font-b:"Source Sans 3",sans-serif;--g:clamp(16px,4vw,32px);--max:1180px}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink)}}
img{{display:block;width:100%;height:100%;object-fit:cover}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),var(--max));margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--ink);color:#fff}}
.top{{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:40}}
.nav{{display:flex;align-items:center;justify-content:space-between;min-height:60px}}.logo{{font-family:var(--font-d);font-weight:700;font-size:22px}}nav{{display:flex;gap:16px;font-size:12px;font-weight:700;text-transform:uppercase}}@media(max-width:800px){{nav{{display:none}}}}
.bag{{background:var(--acc);color:#fff;padding:8px 12px;font-size:11px;font-weight:800;text-transform:uppercase}}
.hero{{padding:40px 0;background:#fff;border-bottom:1px solid var(--line)}}
.hero h1{{font-family:var(--font-d);font-size:clamp(32px,5vw,48px);font-weight:700}}
.hero p{{color:var(--muted);margin:10px 0 20px;max-width:48ch}}
.xref{{display:grid;grid-template-columns:1fr 1fr auto;gap:8px}}.xref input,.xref select{{padding:12px;border:1px solid var(--line)}}
.xref button{{padding:12px 18px;background:var(--acc);color:#fff;border:0;font-weight:800;text-transform:uppercase}}
@media(max-width:800px){{.xref{{grid-template-columns:1fr}}}}
.compare{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:28px}}@media(max-width:800px){{.compare{{grid-template-columns:1fr}}}}
.compare article{{background:#fff;border:1px solid var(--line);padding:18px}}.compare h3{{font-family:var(--font-d);font-size:18px;margin-bottom:8px}}.compare ul{{list-style:none;font-size:13px;color:var(--muted)}}.compare li{{padding:6px 0;border-bottom:1px solid var(--line)}}
.sec{{padding:40px 0}}.eye{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:700}}.h2{{font-family:var(--font-d);font-size:32px}}
.grid-shop{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}.card{{background:#fff;border:1px solid var(--line)}}.card .ph{{aspect-ratio:1;background:#dde3ea}}.card h3{{padding:10px;font-size:14px}}.card p{{padding:0 10px 12px;font-weight:800;color:var(--acc)}}
@media(max-width:900px){{.grid-shop{{grid-template-columns:1fr 1fr}}}}
.col-hero{{padding:32px 0 12px}}.col-hero h1{{font-family:var(--font-d);font-size:40px}}
.tabs{{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}}.tabs button{{padding:8px 12px;border:1px solid var(--line);background:#fff;cursor:pointer;font-size:11px;font-weight:700;text-transform:uppercase}}.tabs button.on{{background:var(--ink);color:#fff}}
.pdp{{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:32px 0}}@media(max-width:800px){{.pdp{{grid-template-columns:1fr}}}}
.gal .main{{aspect-ratio:1;background:#dde3ea;border:1px solid var(--line)}}.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}}.thumbs button{{border:1px solid var(--line);padding:0;aspect-ratio:1;opacity:.5;cursor:pointer;background:#fff}}.thumbs button.on{{opacity:1}}
.info h1{{font-family:var(--font-d);font-size:32px}}.price{{font-size:22px;font-weight:800;margin:10px 0;color:var(--acc)}}.lead{{color:var(--muted)}}
.btn{{display:inline-flex;padding:12px 16px;background:var(--acc);color:#fff;font-weight:800;text-transform:uppercase;font-size:12px;border:0}}
.foot{{padding:28px 0;border-top:1px solid var(--line);display:flex;justify-content:space-between;color:var(--muted);font-size:13px;margin-top:32px}}
.reveal{{opacity:0;transition:.5s}}.reveal.in{{opacity:1}}
"""
    home = f"""
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="./">{b["name"]}</a>
  <nav>{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"])}</nav>
  <span class="bag">RFQ</span>
</div></header>
<section class="hero"><div class="wrap">
  <p class="eye">{b["locale"]} · Cross-reference</p>
  <h1>{b["tagline"]}</h1>
  <p>{b["lead"]}</p>
  <form class="xref" action="collection/" method="get">
    <input name="oem" placeholder="OEM / part number" />
    <select name="cat"><option>Category</option>{"".join(f"<option>{x}</option>" for x in b["links"][:4])}</select>
    <button type="submit">Find part</button>
  </form>
  <div class="compare">
    <article><h3>OEM</h3><ul><li>Exact match</li><li>Lead time shown</li><li>Docs pack</li></ul></article>
    <article><h3>Alternative</h3><ul><li>Checked equivalent</li><li>Price delta</li><li>Stock flag</li></ul></article>
    <article><h3>RFQ</h3><ul><li>Multi-SKU cart</li><li>Net terms</li><li>&lt;2 min send</li></ul></article>
  </div>
</div></section>
<section class="sec wrap reveal">
  <p class="eye">Catalogue</p>
  <h2 class="h2">Common SKUs</h2>
  <div class="grid-shop" style="margin-top:16px">{cards(s, b["products"], n=8)}</div>
</section>
<footer class="foot wrap"><div>{b["full"]}</div><div>© 2026 · Concept</div></footer>
"""
    return css, home


def layout_btt(b):
    """Vacuum configurator — steps + duty ratings."""
    s = b["seed"]
    css = f"""
:root{{--bg:#0f1419;--ink:#e8eef4;--muted:#8b9aab;--line:#243040;--acc:#39c0ba;--font-d:"Rajdhani",sans-serif;--font-b:"Exo 2",sans-serif;--g:clamp(16px,4vw,36px);--max:1160px}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink)}}
img{{display:block;width:100%;height:100%;object-fit:cover}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),var(--max));margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--acc);color:#0f1419}}
.top{{border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(15,20,25,.92);backdrop-filter:blur(10px);z-index:40}}
.nav{{display:flex;align-items:center;justify-content:space-between;min-height:64px}}.logo{{font-family:var(--font-d);font-size:28px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}}
nav{{display:flex;gap:16px;font-size:12px;font-weight:600;text-transform:uppercase}}@media(max-width:800px){{nav{{display:none}}}}
.bag{{border:1px solid var(--acc);color:var(--acc);padding:8px 12px;font-size:11px;font-weight:800;text-transform:uppercase}}
.hero{{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:48px 0;align-items:center}}
.hero h1{{font-family:var(--font-d);font-size:clamp(40px,6vw,64px);text-transform:uppercase;line-height:.95}}
.hero p{{color:var(--muted);margin:12px 0 20px;max-width:40ch}}
.btn{{display:inline-flex;padding:12px 18px;background:var(--acc);color:#0f1419;font-weight:800;text-transform:uppercase;font-size:12px}}
.steps{{display:grid;gap:10px;margin-top:24px}}.steps div{{display:grid;grid-template-columns:40px 1fr;gap:12px;align-items:center;border:1px solid var(--line);padding:12px}}
.steps b{{font-family:var(--font-d);font-size:22px;color:var(--acc)}}
.duty{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:20px}}.duty div{{background:#15202b;border:1px solid var(--line);padding:16px;text-align:center}}.duty strong{{display:block;font-family:var(--font-d);font-size:28px;color:var(--acc)}}
@media(max-width:800px){{.hero{{grid-template-columns:1fr}}.duty{{grid-template-columns:1fr}}}}
.sec{{padding:40px 0}}.eye{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}.h2{{font-family:var(--font-d);font-size:36px;text-transform:uppercase}}
.grid-shop{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}.card{{border:1px solid var(--line);background:#15202b}}.card .ph{{aspect-ratio:1;background:#1c2a38}}.card h3{{padding:10px;font-size:14px}}.card p{{padding:0 10px 12px;color:var(--acc);font-weight:800}}
@media(max-width:900px){{.grid-shop{{grid-template-columns:1fr 1fr}}}}
.col-hero{{padding:32px 0 12px}}.col-hero h1{{font-family:var(--font-d);font-size:42px;text-transform:uppercase}}
.tabs{{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}}.tabs button{{padding:8px 12px;border:1px solid var(--line);background:0;color:var(--ink);cursor:pointer;text-transform:uppercase;font-size:11px}}.tabs button.on{{border-color:var(--acc);color:var(--acc)}}
.pdp{{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:32px 0}}@media(max-width:800px){{.pdp{{grid-template-columns:1fr}}}}
.gal .main{{aspect-ratio:1;background:#1c2a38;border:1px solid var(--line)}}.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}}.thumbs button{{border:1px solid var(--line);padding:0;aspect-ratio:1;opacity:.5;cursor:pointer;background:0}}.thumbs button.on{{opacity:1;border-color:var(--acc)}}
.info h1{{font-family:var(--font-d);font-size:36px;text-transform:uppercase}}.price{{font-size:24px;color:var(--acc);font-weight:800;margin:10px 0}}.lead{{color:var(--muted)}}
.foot{{padding:28px 0;border-top:1px solid var(--line);display:flex;justify-content:space-between;color:var(--muted);font-size:13px;margin-top:32px}}
.reveal{{opacity:0;transition:.5s}}.reveal.in{{opacity:1}}
"""
    home = f"""
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="./">BTT</a>
  <nav>{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"])}</nav>
  <span class="bag">Configure</span>
</div></header>
<section class="wrap hero">
  <div>
    <p class="eye">{b["locale"]}</p>
    <h1>{b["tagline"]}</h1>
    <p>{b["lead"]}</p>
    <a class="btn" href="product/">Start configure</a>
    <div class="steps">
      <div><b>01</b><span>Duty class · dust / liquid / ATEX</span></div>
      <div><b>02</b><span>Hose · filter · docking</span></div>
      <div><b>03</b><span>Quote with BOM attached</span></div>
    </div>
  </div>
  <div>
    <img src="{img(s+'-hero',1200,1200)}" alt="" style="border:1px solid var(--line)" />
    <div class="duty"><div><strong>400</strong>m³/h class</div><div><strong>HEPA</strong>Module</div><div><strong>ATEX</strong>Option</div></div>
  </div>
</section>
<section class="sec wrap reveal">
  <p class="eye">Systems</p>
  <h2 class="h2">Units &amp; modules</h2>
  <div class="grid-shop" style="margin-top:16px">{cards(s, b["products"], n=4)}</div>
</section>
<footer class="foot wrap"><div>{b["full"]}</div><div>© 2026 · Concept</div></footer>
"""
    return css, home


def layout_jkm(b):
    """Fastener density — matrix catalog."""
    s = b["seed"]
    css = f"""
:root{{--bg:#f6f6f4;--ink:#111;--muted:#666;--line:#d0d0cc;--acc:#d62828;--font-d:"Chivo",sans-serif;--font-b:"Public Sans",sans-serif;--g:clamp(14px,3vw,28px);--max:1240px}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink);font-size:14px}}
img{{display:block;width:100%;height:100%;object-fit:cover}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),var(--max));margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--acc);color:#fff}}
.top{{background:#111;color:#fff}}.nav{{display:flex;align-items:center;justify-content:space-between;min-height:52px;font-size:12px}}
.logo{{font-family:var(--font-d);font-weight:700;font-size:20px;text-transform:uppercase}}nav{{display:flex;gap:14px;text-transform:uppercase;font-weight:700}}@media(max-width:800px){{nav{{display:none}}}}
.bag{{background:var(--acc);padding:6px 10px;font-weight:800}}
.hero{{padding:28px 0;border-bottom:2px solid #111}}
.hero h1{{font-family:var(--font-d);font-size:clamp(28px,4vw,40px);text-transform:uppercase}}
.hero p{{color:var(--muted);margin:8px 0 16px}}
.matrix{{display:grid;grid-template-columns:repeat(8,1fr);gap:4px}}.matrix a{{aspect-ratio:1;background:#fff;border:1px solid var(--line);display:grid;place-items:center;font-size:10px;font-weight:700;text-align:center;padding:4px}}
.matrix a:hover{{border-color:var(--acc);color:var(--acc)}}
@media(max-width:900px){{.matrix{{grid-template-columns:repeat(4,1fr)}}}}
.sec{{padding:28px 0}}.eye{{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:700}}.h2{{font-family:var(--font-d);font-size:28px;text-transform:uppercase}}
.grid-shop{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}.card{{background:#fff;border:1px solid var(--line)}}.card .ph{{aspect-ratio:1;background:#e8e8e4}}.card h3{{padding:8px;font-size:13px}}.card p{{padding:0 8px 10px;font-weight:800;color:var(--acc)}}
@media(max-width:900px){{.grid-shop{{grid-template-columns:1fr 1fr}}}}
.col-hero{{padding:24px 0 10px}}.col-hero h1{{font-family:var(--font-d);font-size:32px;text-transform:uppercase}}
.tabs{{display:flex;flex-wrap:wrap;gap:4px;margin-top:10px}}.tabs button{{padding:6px 10px;border:1px solid var(--line);background:#fff;cursor:pointer;font-size:10px;font-weight:700;text-transform:uppercase}}.tabs button.on{{background:#111;color:#fff}}
.pdp{{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:24px 0}}@media(max-width:800px){{.pdp{{grid-template-columns:1fr}}}}
.gal .main{{aspect-ratio:1;background:#e8e8e4;border:1px solid var(--line)}}.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-top:4px}}.thumbs button{{border:1px solid var(--line);padding:0;aspect-ratio:1;opacity:.5;cursor:pointer;background:#fff}}.thumbs button.on{{opacity:1}}
.info h1{{font-family:var(--font-d);font-size:28px;text-transform:uppercase}}.price{{font-size:20px;font-weight:800;margin:8px 0;color:var(--acc)}}.lead{{color:var(--muted)}}
.btn{{display:inline-flex;padding:10px 14px;background:var(--acc);color:#fff;font-weight:800;text-transform:uppercase;font-size:11px;border:0}}
.foot{{background:#111;color:#999;padding:20px 0;margin-top:28px}}.foot .wrap{{display:flex;justify-content:space-between;font-size:12px}}
.reveal{{opacity:0;transition:.4s}}.reveal.in{{opacity:1}}
"""
    cells = "".join(
        f"<a href='collection/'>{x}</a>" for x in [
            "M6","M8","M10","M12","M16","M20","Hex","Socket",
            "Washer","Nut","Anchor","Screw","Bolt","Pin","Rivet","Clip",
            "PPE","Glove","Mask","Boot","Lens","Ear","Vest","Hardhat",
            "Disc","Belt","Wheel","Bit","Tap","Die","Drill","Blade",
        ]
    )
    home = f"""
<header class="top" data-top><div class="wrap nav">
  <a class="logo" href="./">{b["name"]}</a>
  <nav>{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"])}</nav>
  <span class="bag">Bulk</span>
</div></header>
<section class="hero wrap">
  <p class="eye">{b["locale"]} · Same-day metro</p>
  <h1>{b["tagline"]}</h1>
  <p>{b["lead"]}</p>
  <div class="matrix">{cells}</div>
</section>
<section class="sec wrap reveal">
  <p class="eye">Pick list</p>
  <h2 class="h2">Top SKUs</h2>
  <div class="grid-shop" style="margin-top:12px">{cards(s, b["products"], n=8)}</div>
</section>
<footer class="foot"><div class="wrap"><div>{b["full"]}</div><div>© 2026 · Concept</div></div></footer>
"""
    return css, home


def layout_night(b):
    """Archive market — dark film reel aesthetic."""
    s = b["seed"]
    css = f"""
:root{{--bg:#0a0a0b;--ink:#f0e6d8;--muted:#8a8074;--line:#222;--acc:#e8572a;--font-d:"Special Elite",system-ui;--font-b:"IBM Plex Mono",monospace;--g:clamp(16px,4vw,36px)}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink)}}
img{{display:block;width:100%;height:100%;object-fit:cover;filter:contrast(1.05) saturate(.9)}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),1080px);margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--acc);color:#fff}}
.top{{padding:20px var(--g);display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line)}}
.logo{{font-family:var(--font-d);font-size:22px}}.nav{{display:flex;gap:16px;font-size:11px;text-transform:uppercase}}@media(max-width:700px){{.nav{{display:none}}}}
.bag{{font-size:11px;text-transform:uppercase;color:var(--acc)}}
.hero{{padding:48px var(--g);border-bottom:1px solid var(--line)}}
.hero h1{{font-family:var(--font-d);font-size:clamp(32px,6vw,52px);line-height:1.15;max-width:16ch}}
.hero p{{color:var(--muted);margin:16px 0 24px;max-width:40ch;font-size:13px}}
.btn{{display:inline-flex;padding:10px 16px;border:1px solid var(--acc);color:var(--acc);font-size:11px;text-transform:uppercase}}
.reel{{display:flex;gap:8px;overflow-x:auto;padding:24px var(--g);border-bottom:1px solid var(--line)}}
.reel a{{flex:0 0 200px;border:1px solid var(--line)}}.reel .ph{{aspect-ratio:3/4}}.reel h3{{padding:10px;font-size:12px;font-family:var(--font-d)}}
.sec{{padding:40px var(--g)}}.eye{{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}}
.h2{{font-family:var(--font-d);font-size:28px}}
.grid-shop{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}.card{{border:1px solid var(--line)}}.card .ph{{aspect-ratio:3/4}}.card h3{{padding:8px;font-size:12px;font-family:var(--font-d)}}.card p{{padding:0 8px 10px;color:var(--acc);font-size:12px}}
@media(max-width:900px){{.grid-shop{{grid-template-columns:1fr 1fr}}}}
.col-hero{{padding:40px 0 16px}}.col-hero h1{{font-family:var(--font-d);font-size:36px}}
.tabs{{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}}.tabs button{{padding:6px 10px;background:0;border:1px solid var(--line);color:var(--ink);cursor:pointer;font-size:10px;text-transform:uppercase}}.tabs button.on{{border-color:var(--acc);color:var(--acc)}}
.pdp{{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:40px 0}}@media(max-width:800px){{.pdp{{grid-template-columns:1fr}}}}
.gal .main{{aspect-ratio:3/4;border:1px solid var(--line)}}.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}}.thumbs button{{border:1px solid var(--line);padding:0;aspect-ratio:1;opacity:.5;cursor:pointer;background:0}}.thumbs button.on{{opacity:1;border-color:var(--acc)}}
.info h1{{font-family:var(--font-d);font-size:28px}}.price{{color:var(--acc);margin:10px 0}}.lead{{color:var(--muted);font-size:13px}}
.foot{{padding:28px var(--g);border-top:1px solid var(--line);display:flex;justify-content:space-between;color:var(--muted);font-size:11px;margin-top:32px}}
.reveal{{opacity:0;transition:.8s}}.reveal.in{{opacity:1}}
"""
    # Special Elite may need fallback - use IBM Plex Mono + something available
    # Fix font - Special Elite is on Google Fonts
    reel = "".join(
        f'<a href="product/"><div class="ph"><img src="{img(s+"-r"+str(i),600,800)}" alt="" /></div><h3>{n}</h3></a>'
        for i, (n, _) in enumerate(b["products"][:6])
    )
    home = f"""
<header class="top">
  <a class="logo" href="./">{b["name"]}</a>
  <nav class="nav">{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"][:4])}</nav>
  <span class="bag">Bag 0</span>
</header>
<section class="hero">
  <p class="eye">Archive · {b["locale"]}</p>
  <h1>{b["tagline"]}</h1>
  <p>{b["lead"]}</p>
  <a class="btn" href="collection/">Open the stalls</a>
</section>
<div class="reel reveal">{reel}</div>
<section class="sec reveal">
  <p class="eye">Tonight's picks</p>
  <h2 class="h2">From the racks</h2>
  <div class="grid-shop" style="margin-top:16px">{cards(s, b["products"], n=4)}</div>
</section>
<footer class="foot"><div>{b["full"]}</div><div>© 2026 · Concept</div></footer>
"""
    return css.replace('"Special Elite",system-ui', '"Special Elite",monospace'), home


def layout_sandton(b):
    """Luxury fashion lookbook — full-bleed seasons."""
    s = b["seed"]
    css = f"""
:root{{--bg:#faf8f5;--ink:#1a1512;--muted:#7a7168;--line:#e6e0d8;--acc:#1a1512;--font-d:"Bodoni Moda",serif;--font-b:"Manrope",sans-serif;--g:clamp(18px,4vw,40px)}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:var(--font-b);background:var(--bg);color:var(--ink)}}
img{{display:block;width:100%;height:100%;object-fit:cover}}a{{color:inherit;text-decoration:none}}
.wrap{{width:min(100% - 2*var(--g),1200px);margin-inline:auto}}.demo{{position:fixed;bottom:12px;left:12px;z-index:99;font-size:9px;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;background:var(--ink);color:#fff}}
.top{{position:fixed;inset:0 0 auto;z-index:40;padding:20px var(--g);display:flex;justify-content:space-between;color:#fff;mix-blend-mode:difference}}
.logo{{font-family:var(--font-d);font-size:28px;font-weight:500}}.nav{{display:flex;gap:22px;font-size:12px;letter-spacing:.12em;text-transform:uppercase}}@media(max-width:700px){{.nav{{display:none}}}}
.look{{min-height:100vh;position:relative;display:grid;align-items:end;padding:var(--g);color:#fff;isolation:isolate}}
.look img{{position:absolute;inset:0;z-index:-1;filter:brightness(.62)}}
.look h1{{font-family:var(--font-d);font-size:clamp(48px,10vw,100px);font-weight:500;line-height:.9;max-width:8ch}}
.look p{{max-width:34ch;margin:14px 0 22px;opacity:.85}}
.btn{{display:inline-flex;padding:13px 22px;background:#fff;color:#1a1512;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}}
.seasons{{display:grid;grid-template-columns:1fr 1fr}}.seasons a{{position:relative;min-height:60vh;display:flex;align-items:flex-end;padding:28px;color:#fff;isolation:isolate}}
.seasons a img{{position:absolute;inset:0;z-index:-1;filter:brightness(.5)}}.seasons h3{{font-family:var(--font-d);font-size:40px;font-weight:500}}
@media(max-width:700px){{.seasons{{grid-template-columns:1fr}}}}
.sec{{padding:64px 0}}.eye{{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}}
.h2{{font-family:var(--font-d);font-size:clamp(32px,5vw,48px);font-weight:500}}
.grid-shop{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}.card .ph{{aspect-ratio:3/4;background:#ebe6df;margin-bottom:10px}}.card h3{{font-size:14px}}.card p{{color:var(--muted);margin-top:4px}}
@media(max-width:900px){{.grid-shop{{grid-template-columns:1fr 1fr}}}}
.bag{{font-size:11px;letter-spacing:.1em;text-transform:uppercase}}
.col-hero{{padding:120px 0 20px}}.col-hero h1{{font-family:var(--font-d);font-size:48px;font-weight:500}}
.tabs{{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}}.tabs button{{padding:8px 14px;border:1px solid var(--line);background:#fff;cursor:pointer;font-size:11px;letter-spacing:.1em;text-transform:uppercase}}.tabs button.on{{background:var(--ink);color:#fff}}
.pdp{{display:grid;grid-template-columns:1.1fr .9fr;gap:32px;padding:120px 0 48px}}@media(max-width:800px){{.pdp{{grid-template-columns:1fr;padding-top:100px}}}}
.gal .main{{aspect-ratio:3/4;background:#ebe6df}}.thumbs{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px}}.thumbs button{{border:1px solid var(--line);padding:0;aspect-ratio:1;opacity:.55;cursor:pointer;background:#fff}}.thumbs button.on{{opacity:1}}
.info h1{{font-family:var(--font-d);font-size:36px;font-weight:500}}.price{{font-size:20px;margin:12px 0}}.lead{{color:var(--muted)}}
.foot{{padding:40px var(--g);border-top:1px solid var(--line);display:flex;justify-content:space-between;color:var(--muted);font-size:13px}}
.reveal{{opacity:0;transform:translateY(20px);transition:.8s}}.reveal.in{{opacity:1;transform:none}}
"""
    home = f"""
<header class="top">
  <a class="logo" href="./">{b["name"]}</a>
  <nav class="nav">{"".join(f"<a href='collection/'>{x}</a>" for x in b["links"][:4])}<span class="bag">Bag</span></nav>
</header>
<section class="look">
  <img src="{img(s+'-hero',1800,2200)}" alt="" />
  <div>
    <p class="eye">{b["locale"]}</p>
    <h1>{b["tagline"]}</h1>
    <p>{b["lead"]}</p>
    <a class="btn" href="collection/">Shop the season</a>
  </div>
</section>
<section class="seasons reveal">
  <a href="collection/"><img src="{img(s+'-s1',1200,1600)}" alt="" /><h3>Day</h3></a>
  <a href="collection/"><img src="{img(s+'-s2',1200,1600)}" alt="" /><h3>Evening</h3></a>
</section>
<section class="sec wrap reveal">
  <p class="eye">Edit</p>
  <h2 class="h2">New arrivals</h2>
  <div class="grid-shop" style="margin-top:24px">{cards(s, b["products"], n=4)}</div>
</section>
<footer class="foot"><div>{b["full"]}</div><div>© 2026 · Concept</div></footer>
"""
    return css, home


# ─── Brand registry (12 to rebuild) ───────────────────────────────────────────

BRANDS = [
    {
        "slug": "northline-athletics", "name": "Northline", "full": "Northline Athletics",
        "fonts": "family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700",
        "layout": layout_northline, "locale": "Portland, OR",
        "links": ["Run", "Train", "Outer", "Women", "Men"],
        "tagline": "Move harder. Recover cleaner.",
        "lead": "Performance layers engineered for cold starts, wet miles, and city intervals.",
        "ann": "Drop 07 live · Free shipping over $120",
        "seed": "northline",
        "products": [("NL Apex Jacket", "$248"), ("Stride Short 5\"", "$68"), ("Trail Pack Vest", "$180"), ("Recover Hood", "$120"), ("Pulse Tight", "$88"), ("Grip Sock Pro", "$24")],
    },
    {
        "slug": "atelier-maris", "name": "Atelier Maris", "full": "Atelier Maris",
        "fonts": "family=Cormorant+Garamond:wght@500;600;700&family=Figtree:wght@400;500;600;700",
        "layout": layout_maris, "locale": "Lisbon",
        "links": ["Rings", "Necklaces", "Earrings", "Bridal"],
        "tagline": "Quiet metal. Soft stone.",
        "lead": "Hand-finished jewelry for people who notice the weight of a clasp.",
        "ann": "", "seed": "maris",
        "products": [("Lune Signet", "€420"), ("Tide Collar", "€680"), ("Pearl Drop II", "€290"), ("Sand Band", "€310")],
    },
    {
        "slug": "cedar-and-salt", "name": "Cedar & Salt", "full": "Cedar & Salt",
        "fonts": "family=Fraunces:opsz,wght@9..144,500;600;700&family=Sora:wght@400;500;600;700",
        "layout": layout_cedar, "locale": "Cornwall",
        "links": ["Candles", "Diffusers", "Oils", "Sets"],
        "tagline": "Rooms that smell like places.",
        "lead": "Botanical fragrance for homes that want atmosphere, not perfume fog.",
        "ann": "", "seed": "cedar",
        "products": [("Coastal Fig", "$48"), ("Cedar Smoke", "$48"), ("Salt Air Diffuser", "$64"), ("Morning Resin", "$42")],
    },
    {
        "slug": "volt-kitchen", "name": "Volt", "full": "Volt Kitchen",
        "fonts": "family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700",
        "layout": layout_volt, "locale": "Chicago",
        "links": ["Cookware", "Knives", "Tools", "Bundles"],
        "tagline": "Heat. Speed. Control.",
        "lead": "Industrial-grade cookware scaled for serious home cooks.",
        "ann": "", "seed": "volt",
        "products": [("Skillet 28cm", "$189"), ("Chef Knife 210", "$220"), ("Carbon Wok", "$160"), ("Therm Probe X", "$79"), ("Steel Tong Pro", "$34"), ("Dutch Oven 5L", "$280"), ("Board End-Grain", "$120"), ("Sauce Pan Set", "$310")],
    },
    {
        "slug": "lumen-eyewear", "name": "Lumen", "full": "Lumen Eyewear",
        "fonts": "family=Syne:wght@500;600;700;800&family=Outfit:wght@400;500;600;700",
        "layout": layout_lumen, "locale": "Berlin",
        "links": ["Optical", "Sun", "Blue", "Fit Lab"],
        "tagline": "Frames for faces, not mannequins.",
        "lead": "Precision optical DTC with fit data, blue-light options, and overnight lenses.",
        "ann": "", "seed": "lumen",
        "products": [("Arc 02", "$168"), ("Nova Wire", "$148"), ("Halo Acetate", "$188"), ("Drift Sun", "$158")],
    },
    {
        "slug": "exclusive-living", "name": "Exclusive Living", "full": "Exclusive Living",
        "fonts": "family=Libre+Baskerville:wght@400;700&family=Karla:wght@400;500;600;700",
        "layout": layout_exclusive, "locale": "Germany",
        "links": ["Dining", "Living", "Bedroom", "Oak"],
        "tagline": "Showroom craft. Shopable stock.",
        "lead": "Solid-wood furniture with clear lead times, finishes, and delivery — not just a gallery.",
        "ann": "", "seed": "exclive",
        "products": [("Oak Dining Table 220", "€2,480"), ("Walnut Sideboard", "€1,890"), ("Lounge Chair Linen", "€980"), ("Bed Frame Queen", "€1,640")],
    },
    {
        "slug": "mican-industrial", "name": "MiCan", "full": "MiCan Industrial",
        "fonts": "family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600;700",
        "layout": layout_mican, "locale": "South Africa",
        "links": ["Power", "Hand", "Safety", "Trade"],
        "tagline": "Tools that earn their keep.",
        "lead": "Industrial supply for workshops — fast SKU search, pack sizes, and trade checkout.",
        "ann": "", "seed": "mican",
        "products": [("Impact Driver 18V", "R 2,450"), ("Torque Wrench Set", "R 1,180"), ("Cut-Resist Gloves", "R 89"), ("Angle Grinder", "R 1,650"), ("Drill Bit Pack 50", "R 320"), ("Safety Glasses Pro", "R 145")],
    },
    {
        "slug": "german-industry-parts", "name": "GIP", "full": "German Industry Parts",
        "fonts": "family=Archivo:wght@500;600;700&family=Source+Sans+3:wght@400;500;600;700",
        "layout": layout_gip, "locale": "Germany",
        "links": ["Bearings", "Seals", "Motors", "RFQ"],
        "tagline": "Find the part. Quote the rest.",
        "lead": "B2B spare-parts commerce with cross-reference search and rapid RFQ workflows.",
        "ann": "", "seed": "giparts",
        "products": [("Bearing 6205-2RS", "€12.40"), ("Oil Seal 35×52", "€4.80"), ("Motor Flange IEC", "€186"), ("Hydraulic Hose 2m", "€42"), ("Coupling Elastic", "€68"), ("Filter Cartridge", "€22"), ("V-Belt XPZ", "€9.50"), ("Sensor Proximity", "€54")],
    },
    {
        "slug": "btt-vacuums", "name": "BTT Vacuums", "full": "BTT Vacuums",
        "fonts": "family=Rajdhani:wght@500;600;700&family=Exo+2:wght@400;500;600;700",
        "layout": layout_btt, "locale": "Germany",
        "links": ["Systems", "Filters", "Configure", "Support"],
        "tagline": "Suction engineered for industry.",
        "lead": "Industrial vacuum equipment with configurator-style product pages and clear duty specs.",
        "ann": "", "seed": "bttvac",
        "products": [("IVS-400 Mobile", "€3,200"), ("HEPA Module", "€680"), ("Hose Kit 10m", "€210"), ("Cyclone Presep", "€940")],
    },
    {
        "slug": "jkm-industrial", "name": "JKM", "full": "JKM Industrial Supplies",
        "fonts": "family=Chivo:wght@500;600;700&family=Public+Sans:wght@400;500;600;700",
        "layout": layout_jkm, "locale": "Johannesburg",
        "links": ["Fasteners", "Tools", "Abrasives", "PPE"],
        "tagline": "Density without chaos.",
        "lead": "Industrial fasteners and tools with high-density catalog UX that still feels fast.",
        "ann": "", "seed": "jkmind",
        "products": [("Hex Bolt M10×40", "R 2.40"), ("Socket Cap M8", "R 1.80"), ("Flat Washer M12", "R 0.45"), ("Nylon Nut M10", "R 0.90"), ("Cutting Disc 115", "R 12"), ("Safety Gloves", "R 48"), ("Drill Bit HSS", "R 18"), ("Cable Tie Pack", "R 35")],
    },
    {
        "slug": "night-market-archive", "name": "Night Market", "full": "Night Market Archive",
        "fonts": "family=Special+Elite&family=IBM+Plex+Mono:wght@400;500;600",
        "layout": layout_night, "locale": "Taipei",
        "links": ["Archive", "Stalls", "Vintage", "New"],
        "tagline": "After dark, the good racks open.",
        "lead": "A night-market energy for vintage and limited drops — browse like a reel, buy like a stall.",
        "ann": "", "seed": "nightmkt",
        "products": [("Archive Denim", "$120"), ("Stall Tee", "$48"), ("Night Cap", "$36"), ("Market Tote", "$64"), ("Film Jacket", "$180"), ("Stamp Scarf", "$42")],
    },
    {
        "slug": "sandton-atelier", "name": "Sandton Atelier", "full": "Sandton Atelier",
        "fonts": "family=Bodoni+Moda:opsz,wght@6..96,500;600;700&family=Manrope:wght@400;500;600;700",
        "layout": layout_sandton, "locale": "Johannesburg",
        "links": ["New", "Day", "Evening", "Visit"],
        "tagline": "City polish. Soft light.",
        "lead": "A Sandton boutique rhythm — seasonal looks, clear stock, and a path from lookbook to bag.",
        "ann": "", "seed": "sandton",
        "products": [("Column Dress", "R 2,800"), ("Soft Blazer", "R 3,200"), ("Pleat Skirt", "R 1,650"), ("Silk Cami", "R 980")],
    },
]


def build_brand(b: dict) -> None:
    slug = b["slug"]
    base = ROOT / slug
    css, home = b["layout"](b)
    write(base / "brand.css", css)
    write(base / "brand.js", JS)
    write(base / "index.html", page(f"{b['full']} — Concept", b["fonts"], "brand.css", home, 0))
    write(base / "collection" / "index.html", page(f"{b['full']} — Shop", b["fonts"], "brand.css", simple_collection(b), 1))
    write(base / "product" / "index.html", page(f"{b['full']} — Product", b["fonts"], "brand.css", simple_product(b), 1))
    print(f"built {slug}")


def main() -> None:
    for b in BRANDS:
        build_brand(b)
    # Update SKIP in generate-showcase so regen won't overwrite
    gen = ROOT.parents[1] / "scripts" / "generate-showcase.py"
    text = gen.read_text(encoding="utf-8")
    new_skip = (
        'SKIP_SLUGS = {\n'
        '    "river-quarter", "im-naturkosmetik", "fieldpaw", "ips-germany",\n'
        '    "northline-athletics", "atelier-maris", "cedar-and-salt", "volt-kitchen",\n'
        '    "lumen-eyewear", "exclusive-living", "mican-industrial", "german-industry-parts",\n'
        '    "btt-vacuums", "jkm-industrial", "night-market-archive", "sandton-atelier",\n'
        '}'
    )
    import re
    text2 = re.sub(r"SKIP_SLUGS = \{[^}]+\}", new_skip, text, count=1)
    gen.write_text(text2, encoding="utf-8")
    print("updated SKIP_SLUGS")


if __name__ == "__main__":
    main()
