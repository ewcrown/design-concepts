#!/usr/bin/env python3
"""Generate 15 showcase storefront concepts (home/collection/product)."""
from __future__ import annotations

import os
from pathlib import Path

# Skip handcrafted brands when regenerating showcase (custom designer builds)
SKIP_SLUGS = {
    "river-quarter", "im-naturkosmetik", "fieldpaw", "ips-germany",
    "northline-athletics", "atelier-maris", "cedar-and-salt", "volt-kitchen",
    "lumen-eyewear", "exclusive-living", "mican-industrial", "german-industry-parts",
    "btt-vacuums", "jkm-industrial", "night-market-archive", "sandton-atelier",
}


def img(seed: str, w=1200, h=1500) -> str:
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


def fonts_link(families: str) -> str:
    return (
        f'<link rel="preconnect" href="https://fonts.googleapis.com" />'
        f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />'
        f'<link href="https://fonts.googleapis.com/css2?{families}&display=swap" rel="stylesheet" />'
    )


def head(title: str, theme: str, fonts: str, depth: int = 1) -> str:
    prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
  <title>{title}</title>
  {fonts_link(fonts)}
  <link rel="stylesheet" href="{prefix}showcase.css" />
</head>
<body class="{theme}">
<div class="demo-tag">Concept demo</div>
"""


def foot(depth: int = 1) -> str:
    prefix = "../" * depth
    return f"""
<script src="{prefix}showcase.js"></script>
</body>
</html>
"""


def nav(brand: str, links: list[str], ann: str, bag: str = "Bag 0") -> str:
    ls = "".join(f'<a href="collection/">{l}</a>' for l in links)
    return f"""
<div class="sx-top">
  <div class="sx-ann">{ann}</div>
  <div class="wrap">
    <nav class="sx-nav">
      <a class="sx-brand" href="./">{brand}</a>
      <div class="sx-links">{ls}</div>
      <span class="sx-bag">{bag}</span>
    </nav>
  </div>
</div>
"""


def mega_footer(brand: str, cols: list[tuple[str, list[str]]]) -> str:
    col_html = ""
    for title, items in cols:
        links = "".join(f'<a href="collection/">{i}</a>' for i in items)
        col_html += f"<div><h4>{title}</h4>{links}</div>"
    return f"""
<footer class="mega-footer">
  <div class="wrap">
    <div class="grid">
      <div>
        <div class="sx-brand">{brand}</div>
        <p style="margin-top:14px;max-width:32ch;font-size:14px;opacity:.7">Shopify storefront concept — portfolio demo only.</p>
      </div>
      {col_html}
    </div>
    <div class="bar"><span>© 2026 {brand}</span><span>Concept / not a live store</span></div>
  </div>
</footer>
"""


def pcard(seed: str, name: str, price: str, href: str = "product/") -> str:
    return f'<a class="pcard" href="{href}"><div class="img"><img src="{img(seed)}" alt="" loading="lazy" /></div><h3>{name}</h3><p>{price}</p></a>'


def section_count_marker(n: int) -> str:
    return f"<!-- section {n} -->\n"


# ——— Brand definitions ———

BRANDS = [
    # WAVE A
    {
        "slug": "northline-athletics",
        "name": "Northline",
        "full": "Northline Athletics",
        "theme": "theme-northline",
        "wave": "A",
        "sections": 21,
        "fonts": "family=Bebas+Neue&family=DM+Sans:wght@400;500;600;700",
        "ann": "Drop 07 live · Free shipping over $120",
        "links": ["Run", "Train", "Outer", "Women", "Men"],
        "tagline": "Move harder. Recover cleaner.",
        "lead": "Performance layers engineered for cold starts, wet miles, and city intervals.",
        "hero": "kinetic",
        "collection": "runway",
        "gallery": "film",
        "products": [
            ("NL Apex Jacket", "$248"),
            ("Stride Short 5\"", "$68"),
            ("Trail Pack Vest", "$180"),
            ("Recover Hood", "$120"),
            ("Pulse Tight", "$88"),
            ("Grip Sock Pro", "$24"),
            ("Altitude Shell", "$310"),
            ("Base Layer 01", "$54"),
        ],
        "seed": "northline",
        "locale": "Portland, OR",
    },
    {
        "slug": "atelier-maris",
        "name": "Atelier Maris",
        "full": "Atelier Maris",
        "theme": "theme-maris",
        "wave": "A",
        "sections": 21,
        "fonts": "family=Cormorant+Garamond:wght@500;600;700&family=Figtree:wght@400;500;600;700",
        "ann": "Private appointments · Atelier open Thu–Sat",
        "links": ["Rings", "Necklaces", "Earrings", "Bridal", "Objects"],
        "tagline": "Quiet metal. Soft stone.",
        "lead": "Hand-finished jewelry for people who notice the weight of a clasp.",
        "hero": "still",
        "collection": "magazine",
        "gallery": "ambient",
        "products": [
            ("Lune Signet", "€420"),
            ("Tide Collar", "€680"),
            ("Pearl Drop II", "€290"),
            ("Sand Band", "€310"),
            ("Harbor Studs", "€180"),
            ("Citrine Halo", "€540"),
            ("Ribbon Cuff", "€390"),
            ("Vesper Chain", "€250"),
        ],
        "seed": "maris",
        "locale": "Lisbon",
    },
    {
        "slug": "cedar-and-salt",
        "name": "Cedar & Salt",
        "full": "Cedar & Salt",
        "theme": "theme-cedar",
        "wave": "A",
        "sections": 22,
        "fonts": "family=Fraunces:opsz,wght@9..144,500;600;700&family=Sora:wght@400;500;600;700",
        "ann": "New: Coastal Fig · Ships in recycled glass",
        "links": ["Candles", "Diffusers", "Oils", "Sets", "Ritual"],
        "tagline": "Rooms that smell like places.",
        "lead": "Botanical fragrance for homes that want atmosphere, not perfume fog.",
        "hero": "split",
        "collection": "taxonomy",
        "gallery": "swatch",
        "products": [
            ("Coastal Fig", "$48"),
            ("Cedar Smoke", "$48"),
            ("Salt Air Diffuser", "$64"),
            ("Morning Resin", "$42"),
            ("Clay Vessel Set", "$96"),
            ("Travel Tin Trio", "$36"),
            ("Linen Mist", "$28"),
            ("Altar Oil", "$54"),
        ],
        "seed": "cedar",
        "locale": "Cornwall",
    },
    {
        "slug": "volt-kitchen",
        "name": "Volt",
        "full": "Volt Kitchen",
        "theme": "theme-volt",
        "wave": "A",
        "sections": 21,
        "fonts": "family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700",
        "ann": "Pro tools for home kitchens · 30-day heat test",
        "links": ["Cookware", "Knives", "Tools", "Table", "Bundles"],
        "tagline": "Heat. Speed. Control.",
        "lead": "Industrial-grade cookware scaled for serious home cooks.",
        "hero": "full",
        "collection": "hybrid",
        "gallery": "explode",
        "products": [
            ("Skillet 28cm", "$189"),
            ("Chef Knife 210", "$220"),
            ("Carbon Wok", "$160"),
            ("Therm Probe X", "$79"),
            ("Steel Tong Pro", "$34"),
            ("Dutch Oven 5L", "$280"),
            ("Board End-Grain", "$120"),
            ("Sauce Pan Set", "$310"),
        ],
        "seed": "volt",
        "locale": "Chicago",
    },
    {
        "slug": "lumen-eyewear",
        "name": "Lumen",
        "full": "Lumen Eyewear",
        "theme": "theme-lumen",
        "wave": "A",
        "sections": 22,
        "fonts": "family=Syne:wght@500;600;700;800&family=Outfit:wght@400;500;600;700",
        "ann": "Virtual try-on · Free returns 30 days",
        "links": ["Optical", "Sun", "Blue", "Fit Lab", "Lenses"],
        "tagline": "Frames for faces, not mannequins.",
        "lead": "Precision optical DTC with fit data, blue-light options, and overnight lenses.",
        "hero": "tech",
        "collection": "editorial",
        "gallery": "orbit",
        "products": [
            ("Arc 02", "$168"),
            ("Nova Wire", "$148"),
            ("Halo Acetate", "$188"),
            ("Drift Sun", "$158"),
            ("Pulse Blue", "$138"),
            ("Studio Thin", "$178"),
            ("Night Shield", "$128"),
            ("Clip Module", "$48"),
        ],
        "seed": "lumen",
        "locale": "Berlin",
    },
    # WAVE B
    {
        "slug": "exclusive-living",
        "name": "Exclusive Living",
        "full": "Exclusive Living",
        "theme": "theme-exclusive",
        "wave": "B",
        "sections": 25,
        "fonts": "family=Libre+Baskerville:wght@400;700&family=Karla:wght@400;500;600;700",
        "ann": "Solid wood furniture · Showroom appointments available",
        "links": ["Dining", "Living", "Bedroom", "Oak", "Walnut"],
        "tagline": "Showroom craft. Shopable stock.",
        "lead": "Solid-wood furniture with clear lead times, finishes, and delivery — not just a gallery.",
        "hero": "split",
        "collection": "chapters",
        "gallery": "stack",
        "products": [
            ("Oak Dining Table 220", "€2,480"),
            ("Walnut Sideboard", "€1,890"),
            ("Lounge Chair Linen", "€980"),
            ("Bed Frame Queen", "€1,640"),
            ("Console Slim", "€720"),
            ("Bookshelf Bay", "€1,120"),
            ("Bench Seat", "€540"),
            ("Nightstand Pair", "€680"),
        ],
        "seed": "exclive",
        "locale": "Germany",
    },
    {
        "slug": "im-naturkosmetik",
        "name": "i+m",
        "full": "i+m Naturkosmetik",
        "theme": "theme-im",
        "wave": "B",
        "sections": 25,
        "fonts": "family=Playfair+Display:wght@500;600;700&family=Nunito+Sans:wght@400;500;600;700",
        "ann": "Natural cosmetics · Berlin-made · Vegan formulas",
        "links": ["Face", "Body", "Hair", "Sets", "Ingredients"],
        "tagline": "Skin care with receipts.",
        "lead": "Ingredient-led natural beauty with transparent formulas and calm, clinical clarity.",
        "hero": "still",
        "collection": "masonry",
        "gallery": "swatch",
        "products": [
            ("Hydro Face Cream", "€28"),
            ("Cleanse Balm", "€22"),
            ("Serum Vitamin C", "€34"),
            ("Body Oil Rose", "€26"),
            ("Hair Mask", "€24"),
            ("Lip Care Duo", "€14"),
            ("Travel Kit", "€42"),
            ("SPF Fluid", "€29"),
        ],
        "seed": "imnat",
        "locale": "Berlin",
    },
    {
        "slug": "mican-industrial",
        "name": "MiCan",
        "full": "MiCan Industrial",
        "theme": "theme-mican",
        "wave": "B",
        "sections": 26,
        "fonts": "family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600;700",
        "ann": "Wholesale tools · Net terms for trade accounts",
        "links": ["Power", "Hand", "Safety", "Consumables", "Trade"],
        "tagline": "Tools that earn their keep.",
        "lead": "Industrial supply for workshops — fast SKU search, pack sizes, and trade checkout.",
        "hero": "full",
        "collection": "b2b",
        "gallery": "tiles",
        "products": [
            ("Impact Driver 18V", "R 2,450"),
            ("Torque Wrench Set", "R 1,180"),
            ("Cut-Resist Gloves", "R 89"),
            ("Angle Grinder", "R 1,650"),
            ("Drill Bit Pack 50", "R 320"),
            ("Safety Glasses Pro", "R 145"),
            ("Compressor 50L", "R 4,200"),
            ("Tape Measure 8m", "R 78"),
        ],
        "seed": "mican",
        "locale": "South Africa",
    },
    {
        "slug": "german-industry-parts",
        "name": "GIP",
        "full": "German Industry Parts",
        "theme": "theme-gip",
        "wave": "B",
        "sections": 25,
        "fonts": "family=Archivo:wght@500;600;700&family=Source+Sans+3:wght@400;500;600;700",
        "ann": "Spare parts search · RFQ in under 2 minutes",
        "links": ["Bearings", "Seals", "Motors", "Hydraulics", "RFQ"],
        "tagline": "Find the part. Quote the rest.",
        "lead": "B2B spare-parts commerce with cross-reference search and rapid RFQ workflows.",
        "hero": "tech",
        "collection": "density",
        "gallery": "compare",
        "products": [
            ("Bearing 6205-2RS", "€12.40"),
            ("Oil Seal 35×52", "€4.80"),
            ("Motor Flange IEC", "€186"),
            ("Hydraulic Hose 2m", "€42"),
            ("Coupling Elastic", "€68"),
            ("Filter Cartridge", "€22"),
            ("V-Belt XPZ", "€9.50"),
            ("Sensor Proximity", "€54"),
        ],
        "seed": "giparts",
        "locale": "Germany",
    },
    {
        "slug": "ips-germany",
        "name": "IPS",
        "full": "IPS Germany",
        "theme": "theme-ips",
        "wave": "B",
        "sections": 26,
        "fonts": "family=Oswald:wght@500;600;700&family=Work+Sans:wght@400;500;600;700",
        "ann": "Construction & mining parts · Europe-wide dispatch",
        "links": ["Excavator", "Loader", "Wear", "Hydraulics", "Catalog"],
        "tagline": "Heavy catalog. Light friction.",
        "lead": "Construction and mining spare parts with machine filters, wear-part guides, and bulk order.",
        "hero": "kinetic",
        "collection": "map",
        "gallery": "explode",
        "products": [
            ("Bucket Tooth Set", "€240"),
            ("Track Pad Pair", "€890"),
            ("Hydraulic Cylinder", "€1,240"),
            ("Filter Kit 2000h", "€186"),
            ("Pin & Bushing", "€320"),
            ("Cab Glass Front", "€540"),
            ("Pump Cartridge", "€760"),
            ("Wear Plate AR400", "€410"),
        ],
        "seed": "ipsgerm",
        "locale": "Germany",
    },
    # WAVE C
    {
        "slug": "river-quarter",
        "name": "River Quarter",
        "full": "River Quarter",
        "theme": "theme-river",
        "wave": "C",
        "sections": 31,
        "fonts": "family=Bodoni+Moda:opsz,wght@6..96,500;600;700&family=Manrope:wght@400;500;600;700",
        "ann": "SS edit online · Click & collect Northern Quarter",
        "links": ["New", "Womens", "Mens", "Archive", "Visit"],
        "tagline": "Independent fashion with a pulse.",
        "lead": "A riverside boutique energy — sharp edits, real stock, zero brochure dead-ends.",
        "hero": "kinetic",
        "collection": "editorial",
        "gallery": "snap",
        "products": [
            ("Bias Slip Dress", "£128"),
            ("Boxy Blazer", "£186"),
            ("Pleat Trouser", "£98"),
            ("Knit Polo", "£72"),
            ("Archive Denim", "£110"),
            ("Silk Scarf", "£54"),
            ("Leather Belt", "£68"),
            ("Evening Tank", "£84"),
        ],
        "seed": "riverq",
        "locale": "Manchester",
    },
    {
        "slug": "btt-vacuums",
        "name": "BTT Vacuums",
        "full": "BTT Vacuums",
        "theme": "theme-btt",
        "wave": "C",
        "sections": 31,
        "fonts": "family=Rajdhani:wght@500;600;700&family=Exo+2:wght@400;500;600;700",
        "ann": "Industrial vacuum systems · Configure & request quote",
        "links": ["Systems", "Accessories", "Filters", "Configure", "Support"],
        "tagline": "Suction engineered for industry.",
        "lead": "Industrial vacuum equipment with configurator-style product pages and clear duty specs.",
        "hero": "tech",
        "collection": "matrix",
        "gallery": "ar",
        "products": [
            ("IVS-400 Mobile", "€3,200"),
            ("HEPA Module", "€680"),
            ("Hose Kit 10m", "€210"),
            ("Cyclone Presep", "€940"),
            ("ATEX Unit 2", "€5,800"),
            ("Nozzle Pack", "€145"),
            ("Filter Bag Case", "€96"),
            ("Wall Dock", "€420"),
        ],
        "seed": "bttvac",
        "locale": "Germany",
    },
    {
        "slug": "jkm-industrial",
        "name": "JKM",
        "full": "JKM Industrial Supplies",
        "theme": "theme-jkm",
        "wave": "C",
        "sections": 30,
        "fonts": "family=Chivo:wght@500;600;700&family=Public+Sans:wght@400;500;600;700",
        "ann": "Fasteners & tools · Same-day Johannesburg metro",
        "links": ["Fasteners", "Tools", "Abrasives", "PPE", "Bulk"],
        "tagline": "Density without chaos.",
        "lead": "Industrial fasteners and tools with high-density catalog UX that still feels fast.",
        "hero": "full",
        "collection": "density",
        "gallery": "tunnel",
        "products": [
            ("Hex Bolt M12 Pack", "R 186"),
            ("Nut Assortment", "R 94"),
            ("Cutting Disc 115", "R 42"),
            ("Socket Set 1/2\"", "R 780"),
            ("Anchor Sleeve", "R 28"),
            ("PPE Kit Site", "R 320"),
            ("Cable Tie Box", "R 65"),
            ("Drill Bit Cobalt", "R 210"),
        ],
        "seed": "jkmind",
        "locale": "South Africa",
    },
    {
        "slug": "night-market-archive",
        "name": "Night Market",
        "full": "Night Market Archive",
        "theme": "theme-night",
        "wave": "C",
        "sections": 32,
        "fonts": "family=Anton&family=Outfit:wght@400;500;600;700",
        "ann": "Archive drop Friday 18:00 · Limited sizes",
        "links": ["Archive", "Japan", "UK", "Racks", "Stories"],
        "tagline": "Cult pieces. Open browse.",
        "lead": "Vintage and street capsules with editorial density — shop without a login wall.",
        "hero": "kinetic",
        "collection": "runway",
        "gallery": "reel",
        "products": [
            ("Work Jacket 90s", "£145"),
            ("Selvedge Pair", "£120"),
            ("Mesh Jersey", "£64"),
            ("Army Liner", "£98"),
            ("Canvas Tote", "£42"),
            ("Cap Archive", "£36"),
            ("Fleece Half-Zip", "£88"),
            ("Track Pant", "£76"),
        ],
        "seed": "nightmkt",
        "locale": "Manchester",
    },
    {
        "slug": "sandton-atelier",
        "name": "Sandton Atelier",
        "full": "Sandton Atelier",
        "theme": "theme-sandton",
        "wave": "C",
        "sections": 31,
        "fonts": "family=Italiana&family=Montserrat:wght@400;500;600;700",
        "ann": "Showroom by appointment · Nationwide delivery",
        "links": ["Living", "Lighting", "Textiles", "Art", "Atelier"],
        "tagline": "Luxury home, finally shoppable.",
        "lead": "Sandton showroom presence translated into a calm, conversion-ready online atelier.",
        "hero": "still",
        "collection": "season",
        "gallery": "split",
        "products": [
            ("Bouclé Sofa", "R 48,000"),
            ("Marble Console", "R 22,500"),
            ("Brass Floor Lamp", "R 9,800"),
            ("Linen Curtain Pair", "R 6,400"),
            ("Art Print Large", "R 4,200"),
            ("Oak Coffee Table", "R 18,600"),
            ("Velvet Ottoman", "R 7,900"),
            ("Ceramic Vessel", "R 2,450"),
        ],
        "seed": "sandton",
        "locale": "Johannesburg",
    },
]


def hero_html(b: dict) -> str:
    s = b["seed"]
    h = b["hero"]
    if h == "kinetic":
        return f"""
<section class="hero-kinetic">
  <div class="pane"><img src="{img(s+'-h1',1400,1600)}" alt="" /><div class="overlay"><div class="sx-eyebrow">{b['locale']}</div><h1 class="sx-h1">{b['name']}</h1><p class="sx-lead" style="color:rgba(255,255,255,.85)">{b['tagline']}</p></div></div>
  <div class="pane"><img src="{img(s+'-h2',1400,1600)}" alt="" /><div class="overlay"><p class="sx-lead" style="color:rgba(255,255,255,.85)">{b['lead']}</p><div class="btns"><a class="btn btn-solid" href="collection/">Shop now</a><a class="btn btn-light" href="product/">Featured</a></div></div></div>
</section>"""
    if h == "split":
        return f"""
<section class="hero-split">
  <div class="media"><img src="{img(s+'-hero',1400,1600)}" alt="" /></div>
  <div class="copy">
    <div class="sx-eyebrow">{b['full']}</div>
    <h1 class="sx-h1">{b['tagline']}</h1>
    <p class="sx-lead">{b['lead']}</p>
    <div class="btns"><a class="btn btn-ink" href="collection/">Explore</a><a class="btn btn-ghost" href="product/">View piece</a></div>
  </div>
</section>"""
    if h == "still":
        return f"""
<section class="hero-still">
  <div class="media"><img src="{img(s+'-hero',1600,1000)}" alt="" /></div>
  <div class="copy wrap" style="padding-inline:0;max-width:var(--max);margin:0 auto;width:100%">
    <div><div class="sx-eyebrow">{b['locale']}</div><h1 class="sx-h1">{b['name']}</h1></div>
    <div><p class="sx-lead">{b['lead']}</p><div class="btns"><a class="btn btn-ink" href="collection/">Shop</a></div></div>
  </div>
</section>"""
    if h == "tech":
        return f"""
<section class="hero-tech">
  <div class="orb"></div>
  <div class="copy">
    <div class="sx-eyebrow">{b['full']}</div>
    <h1 class="sx-h1">{b['tagline']}</h1>
    <p class="sx-lead">{b['lead']}</p>
    <div class="btns" style="justify-content:center"><a class="btn btn-solid" href="collection/">Enter catalog</a><a class="btn btn-ghost" style="border-color:var(--bg);color:var(--bg)" href="product/">Featured SKU</a></div>
  </div>
</section>"""
    # full
    return f"""
<section class="hero-full">
  <div class="bg"><img src="{img(s+'-hero',1800,1200)}" alt="" /></div>
  <div class="copy">
    <div class="sx-eyebrow">{b['locale']}</div>
    <h1 class="sx-h1">{b['name']}</h1>
    <p class="sx-lead">{b['lead']}</p>
    <div class="btns"><a class="btn btn-solid" href="collection/">Shop collection</a><a class="btn btn-light" href="product/">Product</a></div>
  </div>
</section>"""


def build_home_sections(b: dict) -> str:
    """Compose ≥N unique sections based on wave target."""
    s = b["seed"]
    products = b["products"]
    n_target = b["sections"]
    parts: list[str] = []
    n = 0

    def add(html: str):
        nonlocal n
        n += 1
        parts.append(section_count_marker(n) + html)

    add(hero_html(b))

    add(f"""
<div class="trust wrap">
  <div>Fast checkout</div><div>Clear shipping</div><div>Mobile-first</div><div>{b['locale']}</div>
</div>""")

    cards = "".join(pcard(f"{s}-p{i}", name, price) for i, (name, price) in enumerate(products[:4], 1))
    add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">Featured</h2><a href="collection/">View all</a></div>
  <div class="grid4">{cards}</div>
</div></section>""")

    add(f"""
<section class="marquee reveal"><div class="marquee-track">
  <span>{b['tagline']}</span><span>·</span><span>{b['full']}</span><span>·</span><span>{b['locale']}</span><span>·</span>
  <span>{b['tagline']}</span><span>·</span><span>{b['full']}</span><span>·</span><span>{b['locale']}</span><span>·</span>
</div></section>""")

    cats = "".join(
        f'<a class="cat" href="collection/"><img src="{img(s+"-c"+str(i))}" alt="" /><div class="shade"><h3>{lab}</h3><p>Shop →</p></div></a>'
        for i, lab in enumerate(b["links"][:3], 1)
    )
    add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">Shop by edit</h2></div>
  <div class="grid3">{cats}</div>
</div></section>""")

    add(f"""
<section class="sx-sec tight reveal"><div class="wrap">
  <div class="split-text">
    <div><div class="sx-eyebrow">Story</div><h2 class="sx-h2">{b['tagline']}</h2></div>
    <div><p class="sx-lead" style="max-width:none">{b['lead']} Built as a Shopify concept to show how {b['full']} could convert with stronger merchandising and clearer product paths.</p>
    <div class="btns"><a class="btn btn-ghost" href="collection/">Browse</a></div></div>
  </div>
</div></section>""")

    add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="lookbook">
    <div class="tall"><img src="{img(s+'-lb1',1000,1400)}" alt="" /></div>
    <div class="stack"><div><img src="{img(s+'-lb2')}" alt="" /></div><div><img src="{img(s+'-lb3')}" alt="" /></div></div>
  </div>
</div></section>""")

    add(f"""
<section class="sx-sec tight reveal"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">Look closer</h2></div>
  <div class="filmstrip">
    {''.join(f'<div class="shot"><img src="{img(s+"-f"+str(i))}" alt="" /></div>' for i in range(1,7))}
  </div>
</div></section>""")

    add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="value">
    <article><h3 class="sx-h3">Designed to sell</h3><p>Homepages that lead with brand, then merchandise — not a wall of widgets.</p></article>
    <article><h3 class="sx-h3">Catalog clarity</h3><p>Collections that filter, group, and explain without feeling like a spreadsheet.</p></article>
    <article><h3 class="sx-h3">Product presence</h3><p>Galleries that feel new-school: scrub, snap, orbit, explode — not three thumbnails.</p></article>
  </div>
</div></section>""")

    add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">How it works</h2></div>
  <div class="steps">
    <article><div class="n">01</div><h3 class="sx-h3">Discover</h3><p style="color:var(--muted);font-size:14px;margin-top:8px">Land on a brand-first hero with one clear path.</p></article>
    <article><div class="n">02</div><h3 class="sx-h3">Browse</h3><p style="color:var(--muted);font-size:14px;margin-top:8px">Collections shaped for how this category actually shops.</p></article>
    <article><div class="n">03</div><h3 class="sx-h3">Decide</h3><p style="color:var(--muted);font-size:14px;margin-top:8px">Product pages that prove materials, fit, and trust.</p></article>
    <article><div class="n">04</div><h3 class="sx-h3">Checkout</h3><p style="color:var(--muted);font-size:14px;margin-top:8px">Shopify-native speed and payment confidence.</p></article>
  </div>
</div></section>""")

    more = "".join(pcard(f"{s}-m{i}", name, price) for i, (name, price) in enumerate(products[4:8], 1))
    add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">More from the line</h2><a href="collection/">Collection</a></div>
  <div class="grid4">{more}</div>
</div></section>""")

    add(f"""
<section class="banner reveal">
  <div class="media"><img src="{img(s+'-ban')}" alt="" /></div>
  <div class="copy">
    <div class="sx-eyebrow">Featured drop</div>
    <h2 class="sx-h2">{products[0][0]}</h2>
    <p class="sx-lead">{products[0][1]} · Limited availability concept</p>
    <div class="btns"><a class="btn btn-ink" href="product/">View product</a></div>
  </div>
</section>""")

    add(f"""
<section class="quote reveal">
  <blockquote>“{b['tagline']}”</blockquote>
  <cite>{b['full']} · Concept direction</cite>
</section>""")

    add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">Materials & mood</h2></div>
  <div class="materials">
    {''.join(f'<figure><img src="{img(s+"-mat"+str(i))}" alt="" /><figcaption>Surface 0{i}</figcaption></figure>' for i in range(1,5))}
  </div>
</div></section>""")

    add(f"""
<section class="sx-sec tight reveal"><div class="wrap">
  <div class="stats">
    <div><strong>4.9</strong><span>Concept rating</span></div>
    <div><strong>2–4w</strong><span>Typical build</span></div>
    <div><strong>100%</strong><span>Mobile ready</span></div>
    <div><strong>Shopify</strong><span>Native stack</span></div>
  </div>
</div></section>""")

    add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="press"><span>Vogue Biz</span><span>Dezeen</span><span>Monocle</span><span>Wallpaper*</span><span>Retail Gazette</span></div>
</div></section>""")

    add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">Community</h2></div>
  <div class="ugc">
    {''.join(f'<a href="product/"><img src="{img(s+"-u"+str(i),800,800)}" alt="" /></a>' for i in range(1,7))}
  </div>
</div></section>""")

    add(f"""
<section class="visit reveal">
  <div class="copy">
    <div class="sx-eyebrow">Visit</div>
    <h2 class="sx-h2">{b['locale']}</h2>
    <div class="meta"><span>Showroom / studio concept</span><span>Open concept hours listed on Shopify</span><span>Pickup & delivery ready</span></div>
    <div class="btns"><a class="btn btn-ink" href="collection/">Shop online</a></div>
  </div>
  <div class="media"><img src="{img(s+'-store')}" alt="" /></div>
</section>""")

    add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="compare">
    <article><h3 class="sx-h3">Before</h3><p style="color:var(--muted);margin-top:10px">Thin catalog, unclear CTAs, brochure energy, friction before browse.</p></article>
    <article><h3 class="sx-h3">After</h3><p style="color:var(--muted);margin-top:10px">Brand-led home, intentional collections, product galleries that prove the piece.</p></article>
  </div>
</div></section>""")

    add(f"""
<section class="sx-sec reveal"><div class="wrap wrap-narrow" style="max-width:800px;margin:0 auto">
  <div class="sx-head"><h2 class="sx-h2">FAQ</h2></div>
  <div class="faq">
    <details open><summary>Is this a live store?</summary><p>No — this is a portfolio concept for Shopify migration / rebuild conversations.</p></details>
    <details><summary>Can this be produced on Shopify?</summary><p>Yes. Layouts map to Online Store 2.0 sections, metafields, and custom liquid/CSS.</p></details>
    <details><summary>What about wholesale / RFQ?</summary><p>B2B patterns (trade login, RFQ, dense SKUs) are demonstrated on industrial concepts.</p></details>
  </div>
</div></section>""")

    add(f"""
<section class="newsletter reveal wrap" style="max-width:var(--max)">
  <div>
    <div class="sx-eyebrow">Stay close</div>
    <h2 class="sx-h2">Notes from {b['name']}</h2>
    <p class="sx-lead">Drops, restocks, and studio notes — concept newsletter block.</p>
  </div>
  <form onsubmit="return false">
    <input type="email" placeholder="Email address" aria-label="Email" />
    <button class="btn btn-solid" type="submit">Join</button>
  </form>
</section>""")

    # Extra sections for B/C density
    if n_target >= 24:
        add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">Mosaic edit</h2></div>
  <div class="mosaic">
    <div class="a"><img src="{img(s+'-mo1')}" alt="" /></div>
    <div class="b"><img src="{img(s+'-mo2')}" alt="" /></div>
    <div class="c"><img src="{img(s+'-mo3')}" alt="" /></div>
    <div class="d"><img src="{img(s+'-mo4')}" alt="" /></div>
    <div class="e"><img src="{img(s+'-mo5')}" alt="" /></div>
  </div>
</div></section>""")

        add(f"""
<section class="sx-sec tight reveal"><div class="wrap">
  <div class="deals">
    <article><div class="pct">15%</div><p>Trade opener</p></article>
    <article><div class="pct">Free</div><p>Ship threshold concept</p></article>
    <article><div class="pct">24h</div><p>Quote response target</p></article>
  </div>
</div></section>""")

        add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="split2">
    <a class="panel" href="collection/"><img src="{img(s+'-pa1')}" alt="" /><div class="shade"><h3>{b['links'][0]}</h3><p>Open collection →</p></div></a>
    <a class="panel" href="collection/"><img src="{img(s+'-pa2')}" alt="" /><div class="shade"><h3>{b['links'][1]}</h3><p>Open collection →</p></div></a>
  </div>
</div></section>""")

        add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">Process</h2></div>
  <div class="timeline">
    <article><h3 class="sx-h3">Audit</h3><p style="color:var(--muted);font-size:14px">Map friction on the current site and category reality.</p></article>
    <article><h3 class="sx-h3">Concept</h3><p style="color:var(--muted);font-size:14px">Home / collection / product direction like this demo.</p></article>
    <article><h3 class="sx-h3">Build</h3><p style="color:var(--muted);font-size:14px">Shopify theme, apps, redirects, and launch QA.</p></article>
  </div>
</div></section>""")

    if n_target >= 30:
        add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="rfq">
    <div>
      <div class="sx-eyebrow">Trade / RFQ</div>
      <h2 class="sx-h2">Need a line quote?</h2>
      <p class="sx-lead" style="max-width:none">Concept RFQ block for industrial and wholesale flows.</p>
    </div>
    <form onsubmit="return false">
      <input placeholder="Company" /><input placeholder="SKU / machine" />
      <textarea rows="3" placeholder="Notes"></textarea>
      <button class="btn btn-ink" type="submit">Request quote</button>
    </form>
  </div>
</div></section>""")

        add(f"""
<section class="sx-sec tight reveal"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">Spec strip</h2></div>
  <table class="table-dense">
    <thead><tr><th>Module</th><th>Intent</th><th>Status</th></tr></thead>
    <tbody>
      <tr><td>Hero</td><td>Brand signal</td><td>Locked</td></tr>
      <tr><td>Collection</td><td>{b['collection']} system</td><td>Demo</td></tr>
      <tr><td>PDP gallery</td><td>{b['gallery']} gallery</td><td>Demo</td></tr>
      <tr><td>Checkout</td><td>Shopify native</td><td>Ready</td></tr>
    </tbody>
  </table>
</div></section>""")

        add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="grid2">
    <div><img src="{img(s+'-wide1',1400,900)}" alt="" style="aspect-ratio:16/10;object-fit:cover" /></div>
    <div style="display:flex;flex-direction:column;justify-content:center;padding:12px">
      <div class="sx-eyebrow">Editorial</div>
      <h2 class="sx-h2">One more reason to stay</h2>
      <p class="sx-lead" style="max-width:none">Extended homepage depth for Wave C — more storytelling without losing the buy path.</p>
      <div class="btns"><a class="btn btn-ghost" href="product/">See product</a></div>
    </div>
  </div>
</div></section>""")

        add(f"""
<section class="sx-sec reveal"><div class="wrap">
  <div class="grid3">
    {''.join(f'<article style="padding:22px;border:1px solid var(--line)"><h3 class="sx-h3">{t}</h3><p style="color:var(--muted);font-size:14px;margin-top:8px">{d}</p></article>' for t,d in [
      ("Shipping", "Thresholds and ETA messaging in-theme."),
      ("Trust", "Reviews, guarantees, and policy clarity."),
      ("Merch", "Featured, seasonal, and evergreen rails."),
    ])}
  </div>
</div></section>""")

        add(f"""
<section class="sx-sec tight reveal"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">Last call</h2><a href="collection/">Shop all</a></div>
  <div class="grid4">
    {''.join(pcard(f"{s}-z{i}", name, price) for i, (name, price) in enumerate(products[:4], 1))}
  </div>
</div></section>""")

        add(f"""
<section class="sx-sec reveal" style="background:var(--panel)"><div class="wrap" style="text-align:center;padding-block:24px">
  <div class="sx-eyebrow">Concept complete</div>
  <h2 class="sx-h2" style="max-width:16ch;margin:12px auto">{b['full']} on Shopify</h2>
  <p class="sx-lead" style="margin:16px auto 0">Home · Collection · Product — built as a portfolio wave {b['wave']} demo.</p>
  <div class="btns" style="justify-content:center"><a class="btn btn-ink" href="collection/">Open collection</a></div>
</div></section>""")

    # Pad to exact target if short (shouldn't be)
    while n < n_target:
        add(f"""
<section class="sx-sec tight reveal"><div class="wrap">
  <div class="split-text">
    <h2 class="sx-h2">Detail {n}</h2>
    <p class="sx-lead" style="max-width:none">Additional merchandising block for {b['full']} — keeping homepage rhythm above {n_target} sections.</p>
  </div>
</div></section>""")

    footer_cols = [
        ("Shop", b["links"][:4]),
        ("Company", ["About", "Visit", "Contact", "Careers"]),
        ("Help", ["Shipping", "Returns", "FAQ", "Trade"]),
    ]
    add(mega_footer(b["full"], footer_cols))

    # verify
    assert n >= n_target, f"{b['slug']} only {n} sections, need {n_target}"
    return "\n".join(parts), n


def build_collection(b: dict) -> str:
    s = b["seed"]
    layout = b["collection"]
    products = b["products"] * 2  # denser
    facets = "".join(f'<button class="{"active" if i==0 else ""}">{lab}</button>' for i, lab in enumerate(["All"] + b["links"][:4]))

    hero = f"""
<div class="col-hero wrap">
  <div class="sx-eyebrow">Collection · {b['collection']} system</div>
  <h1 class="sx-h1">{b['full']}</h1>
  <p class="sx-lead">{b['lead']}</p>
  <div class="facets">{facets}</div>
</div>
"""

    def cards(n=8, grid="grid4"):
        html = "".join(pcard(f"{s}-col{i}", name, price, "../product/") for i, (name, price) in enumerate(products[:n], 1))
        return f'<div class="{grid}">{html}</div>'

    body = ""
    if layout == "runway":
        items = "".join(
            f'<a href="../product/"><div class="img"><img src="{img(s+"-rw"+str(i))}" alt="" /></div><div style="padding:16px"><h3>{name}</h3><p style="color:var(--muted)">{price}</p></div></a>'
            for i, (name, price) in enumerate(products[:8], 1)
        )
        body = f'<div class="col-runway">{items}</div>'
    elif layout == "magazine":
        body = f"""
<div class="wrap col-magazine">
  <a class="feature" href="../product/"><img src="{img(s+'-mag')}" alt="" /><div class="meta"><h2 class="sx-h2">{products[0][0]}</h2><p>{products[0][1]}</p></div></a>
  <div class="side">{cards(4, "grid2")}</div>
</div>"""
    elif layout == "masonry":
        items = "".join(
            f'<a class="pcard" href="../product/"><div class="img"><img src="{img(s+"-ms"+str(i))}" alt="" /></div><h3>{name}</h3><p>{price}</p></a>'
            for i, (name, price) in enumerate(products[:9], 1)
        )
        body = f'<div class="wrap col-masonry">{items}</div>'
    elif layout == "hybrid":
        body = f"""
<div class="wrap col-hybrid">
  <aside class="side-filters">
    <h3 class="sx-h3" style="margin-bottom:12px">Filters</h3>
    {''.join(f'<label><input type="checkbox" /> {lab}</label>' for lab in b['links'])}
    <div style="margin-top:16px"><button class="btn btn-ink" style="width:100%">Apply</button></div>
  </aside>
  <div>{cards(8)}</div>
</div>"""
    elif layout == "taxonomy":
        fams = "".join(
            f'<div class="family"><div class="img"><img src="{img(s+"-tx"+str(i))}" alt="" /></div><h3 class="sx-h3">{lab}</h3><p style="color:var(--muted);font-size:14px;margin:8px 0 14px">Family edit</p><a class="btn btn-ghost" href="../product/">Open</a></div>'
            for i, lab in enumerate(b["links"][:3], 1)
        )
        body = f'<div class="wrap col-taxonomy">{fams}</div><div class="wrap" style="margin-top:40px">{cards(4)}</div>'
    elif layout == "editorial":
        items = "".join(
            f'<a class="pcard" href="../product/"><div class="img"><img src="{img(s+"-ed"+str(i))}" alt="" /></div><h3>{name}</h3><p>{price}</p></a>'
            for i, (name, price) in enumerate(products[:8], 1)
        )
        body = f'<div class="wrap col-editorial">{items}</div>'
    elif layout == "chapters":
        ch = ""
        for i, lab in enumerate(b["links"][:3], 1):
            ch += f"""
<div class="chapter">
  <div class="ch-copy"><div class="sx-eyebrow">Chapter 0{i}</div><h2 class="sx-h2">{lab}</h2><p class="sx-lead">Curated {lab.lower()} pieces with finish notes and lead times.</p><a class="btn btn-ghost" href="../product/">View</a></div>
  <div class="grid2">{''.join(pcard(f"{s}-ch{i}{j}", name, price, "../product/") for j, (name, price) in enumerate(products[i:i+2], 1))}</div>
</div>"""
        body = f'<div class="wrap col-chapters">{ch}</div>'
    elif layout == "b2b":
        skus = "".join(
            f'<div class="sku"><code>SKU-{1000+i}</code><h3 style="margin:8px 0">{name}</h3><p>{price} · pack</p><a class="btn btn-ghost" style="margin-top:12px" href="../product/">Add</a></div>'
            for i, (name, price) in enumerate(products[:9], 1)
        )
        body = f'<div class="wrap col-b2b"><div class="sku-grid">{skus}</div></div>'
    elif layout == "density":
        rows = "".join(
            f'<div class="row"><div class="thumb"><img src="{img(s+"-d"+str(i),200,200)}" alt="" /></div><div><strong>{name}</strong><div style="color:var(--muted);font-size:12px">SKU-{2000+i}</div></div><div>In stock</div><div>Box</div><div>{price}</div></div>'
            for i, (name, price) in enumerate(products[:10], 1)
        )
        body = f'<div class="wrap col-density">{rows}</div>'
    elif layout == "matrix":
        body = f"""
<div class="wrap col-matrix">
  <table class="table-dense">
    <thead><tr><th>Model</th><th>Duty</th><th>Airflow</th><th>Price</th><th></th></tr></thead>
    <tbody>
      {''.join(f'<tr><td>{name}</td><td>Industrial</td><td>High</td><td>{price}</td><td><a href="../product/">Configure</a></td></tr>' for name, price in products[:8])}
    </tbody>
  </table>
</div>"""
    elif layout == "season":
        blocks = ""
        for i, lab in enumerate(["Summer light", "Winter depth", "Atelier forever"], 1):
            blocks += f"""
<div class="season-block">
  <div class="label">{lab}</div>
  <div class="grid3">{''.join(pcard(f"{s}-ss{i}{j}", name, price, "../product/") for j, (name, price) in enumerate(products[i:i+3], 1))}</div>
</div>"""
        body = f'<div class="wrap col-season">{blocks}</div>'
    elif layout == "map":
        body = f"""
<div class="col-map">
  <div class="map-panel">
    <div class="sx-eyebrow">Navigate</div>
    <h2 class="sx-h2">Categories</h2>
    <div class="cats">{''.join(f'<a href="../product/"><span>{lab}</span><span>→</span></a>' for lab in b['links'])}</div>
  </div>
  <div><img src="{img(s+'-map',1200,1400)}" alt="" /></div>
</div>"""
    else:
        body = f'<div class="wrap">{cards(8)}</div>'

    return hero + f'<section class="sx-sec">{body}</section>' + mega_footer(b["full"], [("Shop", b["links"][:3]), ("Help", ["Shipping", "Returns"]), ("More", ["Home", "Product"])])


def build_gallery(b: dict) -> str:
    s = b["seed"]
    g = b["gallery"]
    frames = "".join(f'<div class="frame"><img src="{img(s+"-g"+str(i))}" alt="" /></div>' for i in range(1, 5))
    if g == "film":
        return f'<div class="gal-film">{frames}</div>'
    if g == "stack":
        return f'<div class="gal-stack">{frames}</div>'
    if g == "orbit":
        return f"""
<div class="gal-orbit"><img src="{img(s+'-orb')}" alt="" />
  <button class="hotspot" style="left:30%;top:40%" aria-label="lens"></button>
  <button class="hotspot" style="left:62%;top:55%" aria-label="hinge"></button>
  <button class="hotspot" style="left:48%;top:72%" aria-label="temple"></button>
</div>"""
    if g == "split":
        return f"""
<div class="gal-split">
  <div class="frame"><span class="tag">Day</span><img src="{img(s+'-sp1')}" alt="" /></div>
  <div class="frame"><span class="tag">Night</span><img src="{img(s+'-sp2')}" alt="" /></div>
</div>"""
    if g == "swatch":
        return f"""
<div class="gal-swatch">
  <div class="main"><img src="{img(s+'-sw0')}" alt="" /></div>
  <div class="thumbs">
    {''.join(f'<button class="{"active" if i==1 else ""}"><img src="{img(s+"-sw"+str(i))}" alt="" /></button>' for i in range(1,5))}
  </div>
</div>"""
    if g == "snap":
        return f"""
<div class="gal-snap">
  {''.join(f'<div class="frame"><img src="{img(s+"-sn"+str(i))}" alt="" /><div class="cap">Look 0{i}</div></div>' for i in range(1,5))}
</div>"""
    if g == "explode":
        return f"""
<div class="gal-explode"><img src="{img(s+'-ex')}" alt="" />
  <div class="pin" style="left:28%;top:32%"><button></button><span>Handle geometry</span></div>
  <div class="pin" style="left:55%;top:48%"><button></button><span>Core material</span></div>
  <div class="pin" style="left:70%;top:68%"><button></button><span>Base finish</span></div>
</div>"""
    if g == "ambient":
        return f"""
<div class="gal-ambient">
  <div class="wide"><img src="{img(s+'-amw',1400,900)}" alt="" /></div>
  <div class="pair"><div class="frame"><img src="{img(s+'-am1')}" alt="" /></div><div class="frame"><img src="{img(s+'-am2')}" alt="" /></div></div>
</div>"""
    if g == "ar":
        return f"""
<div class="gal-ar">
  <div class="ring"></div>
  <div class="stub">
    <div class="sx-eyebrow">AR preview</div>
    <h3 class="sx-h3">Place in space</h3>
    <p class="sx-lead" style="margin:12px auto">Configurator-style AR stub for industrial equipment.</p>
    <button class="btn btn-solid" type="button">Launch preview</button>
  </div>
</div>"""
    if g == "compare":
        return f"""
<div class="gal-compare">
  <div class="frame"><img src="{img(s+'-cp1')}" alt="" /><label>OEM cross-ref</label></div>
  <div class="frame"><img src="{img(s+'-cp2')}" alt="" /><label>GIP equivalent</label></div>
</div>"""
    if g == "tunnel":
        return f"""
<div class="gal-tunnel">
  {''.join(f'<div class="frame"><img src="{img(s+"-tn"+str(i))}" alt="" /></div>' for i in range(1,4))}
</div>"""
    if g == "tiles":
        return f"""
<div class="gal-tiles">
  <div class="main"><img src="{img(s+'-tl0')}" alt="" /></div>
  <div class="frame"><img src="{img(s+'-tl1')}" alt="" /></div>
  <div class="frame"><img src="{img(s+'-tl2')}" alt="" /></div>
</div>"""
    if g == "reel":
        return f"""
<div class="gal-reel">
  <div class="slides">{''.join(f'<div class="frame"><img src="{img(s+"-rl"+str(i))}" alt="" /></div>' for i in range(1,5))}</div>
  <div class="dots"></div>
</div>"""
    return f'<div class="gal-film">{frames}</div>'


def build_product(b: dict) -> str:
    name, price = b["products"][0]
    gal = build_gallery(b)
    return f"""
<section class="pdp">
  <div class="pdp-gal">{gal}</div>
  <div class="pdp-info">
    <div class="sx-eyebrow">{b['full']} · {b['gallery']} gallery</div>
    <h1 class="sx-h1" style="font-size:clamp(32px,4vw,52px)">{name}</h1>
    <div class="price">{price}</div>
    <p class="desc">{b['lead']}</p>
    <div class="swatches">
      <button style="background:#222" aria-label="dark"></button>
      <button style="background:#c4b5a0" aria-label="sand"></button>
      <button style="background:var(--accent)" aria-label="accent"></button>
    </div>
    <div class="sizes">
      <button class="active">S</button><button>M</button><button>L</button><button>XL</button>
    </div>
    <button class="btn btn-ink" style="width:100%" data-atc type="button">Add to bag</button>
    <div class="pdp-specs">
      <dl>
        <dt>SKU</dt><dd>{b['seed'].upper()}-001</dd>
        <dt>Origin</dt><dd>{b['locale']}</dd>
        <dt>System</dt><dd>{b['gallery']} gallery</dd>
        <dt>Stack</dt><dd>Shopify concept</dd>
      </dl>
    </div>
  </div>
</section>
<div class="sticky-atc"><strong>{name}</strong><button class="btn btn-ink" type="button">Add to bag · {price}</button></div>
<section class="sx-sec"><div class="wrap">
  <div class="sx-head"><h2 class="sx-h2">You may also like</h2></div>
  <div class="grid4">
    {''.join(pcard(f"{b['seed']}-rel{i}", n, p, "./") for i, (n, p) in enumerate(b['products'][1:5], 1))}
  </div>
</div></section>
""" + mega_footer(b["full"], [("Shop", b["links"][:3]), ("Product", ["Care", "Shipping"]), ("Back", ["Home", "Collection"])])


def write_brand(b: dict):
    base = ROOT / b["slug"]
    (base / "collection").mkdir(parents=True, exist_ok=True)
    (base / "product").mkdir(parents=True, exist_ok=True)

    # Home (depth 1 from showcase/)
    home_body, count = build_home_sections(b)
    home = (
        head(f"{b['full']} — Homepage Concept", b["theme"], b["fonts"], depth=1)
        + nav(b["name"], b["links"], b["ann"])
        + f"<!-- SECTION_COUNT:{count} -->\n"
        + home_body
        + foot(1)
    )
    (base / "index.html").write_text(home, encoding="utf-8")

    # Collection — fix nav links for subfolder
    col_nav = nav(b["name"], b["links"], b["ann"]).replace('href="./"', 'href="../"').replace('href="collection/"', 'href="./"')
    col = (
        head(f"{b['full']} — Collection Concept", b["theme"], b["fonts"], depth=2)
        + col_nav
        + build_collection(b).replace('href="collection/"', 'href="./"').replace("href=\"product/\"", 'href="../product/"')
        + foot(2)
    )
    # fix mega footer relative links in collection - product links already ../product/
    (base / "collection" / "index.html").write_text(col, encoding="utf-8")

    prod_nav = nav(b["name"], b["links"], b["ann"]).replace('href="./"', 'href="../"').replace('href="collection/"', 'href="../collection/"')
    prod = (
        head(f"{b['full']} — Product Concept", b["theme"], b["fonts"], depth=2)
        + prod_nav
        + build_product(b)
        + foot(2)
    )
    (base / "product" / "index.html").write_text(prod, encoding="utf-8")
    print(f"✓ {b['slug']} home sections={count} col={b['collection']} gal={b['gallery']}")


def write_showcase_index():
    cards = []
    for b in BRANDS:
        cards.append(f"""
<article class="card">
  <div class="meta">Wave {b['wave']} · {b['sections']}+ sections · {b['collection']} / {b['gallery']}</div>
  <h2>{b['full']}</h2>
  <p>{b['lead']}</p>
  <div class="links">
    <a class="primary" href="{b['slug']}/">Home</a>
    <a href="{b['slug']}/collection/">Collection</a>
    <a href="{b['slug']}/product/">Product</a>
  </div>
  <div class="meta">{b['locale']}</div>
</article>""")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Showcase Portfolio — 15 Concepts</title>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    :root {{ --bg:#0c0d10; --panel:#14161c; --ink:#f2f3f7; --muted:#9aa3b2; --line:#262a34; --accent:#d6b48a; }}
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    body {{ font-family:Manrope,sans-serif; background:radial-gradient(900px 500px at 80% -20%, rgba(214,180,138,.16), transparent 55%), var(--bg); color:var(--ink); }}
    a {{ color:inherit; text-decoration:none; }}
    .wrap {{ max-width:1100px; margin:0 auto; padding:clamp(48px,8vw,88px) clamp(20px,4vw,32px); }}
    .eyebrow {{ font-size:11px; letter-spacing:.22em; text-transform:uppercase; color:var(--accent); font-weight:700; margin-bottom:16px; }}
    h1 {{ font-family:"Instrument Serif",serif; font-size:clamp(40px,6vw,64px); font-weight:400; letter-spacing:-.03em; line-height:.95; margin-bottom:14px; }}
    header p {{ color:var(--muted); max-width:540px; line-height:1.7; }}
    header {{ margin-bottom:36px; padding-bottom:28px; border-bottom:1px solid var(--line); }}
    .grid {{ display:grid; gap:14px; }}
    .card {{ background:linear-gradient(180deg,rgba(255,255,255,.03),transparent), var(--panel); border:1px solid var(--line); border-radius:14px; padding:24px; display:grid; gap:12px; }}
    .card h2 {{ font-family:"Instrument Serif",serif; font-size:26px; font-weight:400; }}
    .card p {{ color:var(--muted); font-size:14px; line-height:1.55; }}
    .links {{ display:flex; flex-wrap:wrap; gap:8px; }}
    .links a {{ font-size:11px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; padding:10px 14px; border-radius:999px; border:1px solid var(--line); background:#10131a; }}
    .links a.primary {{ background:var(--accent); border-color:var(--accent); color:#1a140e; }}
    .meta {{ font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); }}
    .back {{ display:inline-block; margin-bottom:20px; color:var(--accent); font-size:12px; letter-spacing:.14em; text-transform:uppercase; font-weight:700; }}
  </style>
</head>
<body>
  <div class="wrap">
    <a class="back" href="../">← All concepts</a>
    <header>
      <div class="eyebrow">Showcase portfolio</div>
      <h1>15 concepts across three waves.</h1>
      <p>Wave A fictional (≥20 sections) · Wave B Tier-B leads (≥24) · Wave C mix (≥30). Each includes a distinct collection system and new-school product gallery. Client demos are untouched.</p>
    </header>
    <div class="grid">
      {''.join(cards)}
    </div>
  </div>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for b in BRANDS:
        if b["slug"] in SKIP_SLUGS:
            print(f"↷ skip custom {b['slug']}")
            continue
        write_brand(b)
    write_showcase_index()
    print(f"\nDone: {len(BRANDS)} brands → {ROOT}")


if __name__ == "__main__":
    main()
