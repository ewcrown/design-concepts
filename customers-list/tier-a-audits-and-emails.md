# Tier A Deep Audits + Cold Email Drafts

**Status:** Ready for your review / approve / edit  
**Date:** 2026-08-04  
**Note:** Replace `[YOUR NAME]`, `[AGENCY]`, `[CONCEPT LINK]`, `[LOOM LINK]` before sending.

**Send order (strongest first):**
1. Katie and May
2. Suzy Loves Milo
3. Phases Africa
4. Animal Kingdom
5. Furniture Liquidation Warehouse

---

# 1. Katie and May

| Field | Detail |
|---|---|
| Website | https://www.katieandmay.co.uk |
| Country | UK (Leeds) |
| Industry | Fashion / lifestyle boutique |
| CMS | WordPress + WooCommerce (Divi) |
| Contact | Catherine@katieandmay.co.uk |
| Phone | 07540 264151 |
| Instagram | @katie_and_may |
| Decision maker | Catherine (owner contact on site) |
| Priority | **#1 — strongest problem → solution story** |

## Liked about the business
Independent Leeds boutique with a clear local voice (Yorkshire Style), physical shops, styling services, and a community angle (10% first-order offer). Real brand, not a dropshipper.

## Issues found (specific)

1. **Shop is broken.** `/shop/` and homepage “SHOP PRELOVED” both return **“No Results Found”** — customers literally cannot browse products.
2. **Broken newsletter embed.** Homepage shows raw code: `[yikes-mailchimp form=”3”]` instead of a signup form.
3. **Homepage sells nothing.** Categories exist as links, but the primary commerce paths fail — traffic from Instagram/local search hits a dead end.
4. **Trust/CRO gaps.** No clear featured bestsellers, size guidance, or “new vs preloved” shopping paths that work.
5. **Platform friction.** Woo + Divi setup is fragile; a boutique this size usually converts better on a cleaner Shopify stack.

## Solution (not a service pitch)
Rebuild a simple Shopify storefront where:
- New + Preloved collections actually load
- Homepage shows bestsellers + new drops
- Mobile checkout works in under 3 taps
- Newsletter form works
- Brand feel stays Katie and May (not a generic template)

## Homepage concept brief (for Lovable / v0 / Bolt)
> Create a premium boutique Shopify homepage for Katie and May (Leeds fashion boutique). Keep warm, local, independent branding. Hero: “Live well dressed in Yorkshire.” Nav: New / Preloved / Dresses / Tops / Denim / Accessories / Styling. Featured collections for New Styles + Preloved. Clean product cards with price + “quick add”. Trust strip: free UK returns, local pickup Chapel Allerton, styling available. Working email capture. Mobile-first, fast, minimal.

## Cold email draft

**To:** Catherine@katieandmay.co.uk  
**Subject:** Your online shop is showing “No Results Found”

Hi Catherine,

I was looking at Katie and May and genuinely like how clear the brand feels — local Leeds boutique, Yorkshire style, and a real community around the shop.

One thing stood out though: when I tried to browse the shop (and the Preloved section), the site returns **“No Results Found.”** On the homepage the newsletter form also shows as raw code instead of a signup box. That means people coming from Instagram or Google likely can’t buy.

I put together a quick homepage concept showing how Katie and May could look on a cleaner Shopify setup — same brand feel, but with working collections, better mobile browsing, and a checkout that doesn’t get in the way:

[CONCEPT LINK]

Happy to walk you through it for 15 minutes if useful — no hard sell, just the fixes.

[YOUR NAME]  
[AGENCY]

---

# 2. Suzy Loves Milo Concept Store

| Field | Detail |
|---|---|
| Website | https://suzylovesmiloconcept.com |
| Country | UK (Manchester NQ) |
| Industry | Fashion / vintage / Japanese streetwear |
| CMS | **GoDaddy Website Builder + Online Store** |
| Contact | info@suzylovesmilo.co.uk |
| Instagram | @suzylovesmilo |
| Store | 40 Spear Street, Manchester M1 1AS |
| Priority | **#2 — cult brand, weak tech** |

## Liked about the business
Cult Northern Quarter store with real editorial reputation (Japanese imports, designer vintage, A-list visitors). Offline brand is strong enough that the online store should be a destination, not a brochure.

## Issues found (specific)

1. **Catalog gatekept.** `/products` **redirects to login** (`/m/login?r=%2Fproducts`) — guest shoppers can’t browse the full shop freely.
2. **GoDaddy stack.** Generator meta: “Go Daddy Website Builder” — limited ecommerce UX vs modern fashion stores.
3. **Homepage is thin.** Little product merchandising; feels like a contact/landing page more than a store.
4. **Admin leak.** Signed-in state shows `filler@godaddy.com` in the public HTML — looks unfinished.
5. **Brand mismatch.** In-store experience is curated and editorial; online doesn’t match that quality bar.

## Solution
Migrate to Shopify with:
- Open browsing (no login wall for products)
- Editorial homepage (New from Japan / Archive / Lifestyle)
- Strong product cards + storytelling
- Instagram → PDP path that converts
- Keep raw, cult aesthetic — not polished corporate fashion

## Homepage concept brief
> Premium Shopify homepage for Suzy Loves Milo Concept (Manchester vintage/Japanese streetwear). Keep the cult, slightly raw aesthetic. Hero photography of store/rails. Nav: Shop / New / Archive / Lifestyle / Visit Store. Featured: New arrivals + WHP x SLM. Product cards with mood, not generic grids. Store hours + Spear Street visit CTA. Trust: curated in Japan, Northern Quarter since Hatch days. Mobile-first.

## Cold email draft

**To:** info@suzylovesmilo.co.uk  
**Subject:** Your online shop asks people to log in before browsing

Hi Suzy / Bobbie,

I’ve followed what you’ve built with Suzy Loves Milo in the Northern Quarter — the Japanese sourcing and curation is genuinely special.

Looking at the site, one conversion issue jumped out: the **Products page sends visitors to a login screen** before they can browse. For a brand with your cult following, that likely loses a lot of Instagram traffic before anyone sees a piece.

I mocked a homepage concept that keeps your aesthetic but opens the catalog properly and makes the online store feel closer to the in-person experience:

[CONCEPT LINK]

If you want, I can show you the before/after in a 15-minute call.

[YOUR NAME]  
[AGENCY]

---

# 3. Phases Africa Furniture & Decor

| Field | Detail |
|---|---|
| Website | https://www.phasesafrica.com |
| Country | ZA (Cape Town / Somerset West) + ships internationally |
| Industry | African furniture / decor / art |
| CMS | WordPress (portfolio-style, not full cart ecommerce) |
| Contact | info@phasesafrica.com |
| Founder | Noleen Kutash |
| Priority | **#3 — made-to-order UX rebuild** |

## Liked about the business
24 years, sustainably sourced African craftsmanship, international shipping history (started in LA), strong story. Made-to-order model (80% custom, 4–6 week lead time, 60% deposit) is a real business — the website just doesn’t sell it well.

## Issues found (specific)

1. **Not a real shop.** Products live as “portfolio items”; buying is “email us / contact form,” not add-to-cart.
2. **Broken/odd contact URL.** Contact lives at a mangled path: `/https-www-phasesafrica-com-contact/`.
3. **Category pages are blog posts.** e.g. African Home Decor page is mostly text, not a browsable collection.
4. **High-intent buyers get friction.** International customers need clear pricing signals, deposit flow, lead times, shipping expectations on every product.
5. **Story buried.** Sustainability + craftsmanship should lead the homepage; currently feels dated and content-heavy.

## Solution
Shopify (or Shopify + custom draft order / deposit app) homepage + product templates that:
- Show collections with starting prices / “from”
- Clear “Made to order · 4–6 weeks · 60% deposit”
- Strong photography grids
- Simple inquiry → deposit path
- Mobile-first for US/EU buyers

## Homepage concept brief
> Premium Shopify homepage for Phases Africa. Hero: handcrafted African furniture, warm wood tones, lifestyle interiors. Headline about sustainably sourced African craftsmanship since 2001. Nav: Furniture / Lighting / Rugs / Art / Kids / About. Featured collections. Trust: made to order, international shipping, 60% deposit, 4–6 week lead time. Product cards with “Inquire / Order” CTA. Elegant, gallery-like, not warehouse furniture aesthetic.

## Cold email draft

**To:** info@phasesafrica.com  
**Subject:** Made-to-order furniture is hard to buy on your site

Hi Noleen,

Phases Africa’s story is excellent — 20+ years of handcrafted African furniture and decor, with real international shipping experience. That kind of craftsmanship deserves a storefront that matches it.

Right now the site works more like a portfolio than a shop: products are hard to browse as collections, and buying still routes through a contact form (the contact URL itself looks broken). For made-to-order pieces, buyers need lead times, deposit terms, and starting prices visible before they inquire — otherwise many leave.

I drafted a homepage concept that keeps your brand, but structures the store around how high-ticket furniture buyers actually decide:

[CONCEPT LINK]

Would a short 15-minute walkthrough be useful?

[YOUR NAME]  
[AGENCY]

---

# 4. Animal Kingdom (Pretoria)

| Field | Detail |
|---|---|
| Website | https://animalkingdom.co.za |
| Country | ZA |
| Industry | Pet supplies |
| CMS | WooCommerce |
| Catalog size | ~1,100+ products (Dogs 449, Cats 156, Fish 185, etc.) |
| Contact | info@animal-kingdom.co.za / pretoria@animal-kingdom.co.za |
| Phone | 012 991-4872 |
| Priority | **#4 — mid-market Woo → Shopify CRO** |

## Liked about the business
35+ years, wide pet categories (not just dogs/cats), physical stores + online, real inventory depth. Strong local trust potential.

## Issues found (specific)

1. **Homepage is generic.** Repeated “competitively priced pet food and supplies” — no brand differentiation vs Petworld / Takealot.
2. **Typos hurt trust.** e.g. Fish nav says **“Canopes”** instead of Canopies.
3. **“Available In Store Only” on homepage deals.** Hot deals show as store-only with raw product URLs in places — kills online conversion.
4. **Thin product pages.** Example PDP has short copy, weight field, little trust content, sparse imagery vs modern pet ecommerce.
5. **Merchandising weak.** Category counts exist, but filtering/search/cross-sell feel dated; “You Might Like” is thin.
6. **Competing against Shopify-native chains** (Petworld already on Shopify).

## Solution
Shopify migration focused on:
- Pet-type mega menu + filters (brand, life stage, diet)
- Online-first deals (not store-only dead ends)
- Richer PDPs (ingredients, feeding guide, reviews)
- Trust: 35 years, store pickup, delivery ETA
- Cleaner mobile category browsing

## Homepage concept brief
> Modern Shopify homepage for Animal Kingdom SA. Hero: “Trusted pet care for 35+ years.” Shop by pet tiles (Dog/Cat/Fish/Bird/Reptile/Small Pet). Bestsellers + New arrivals. Trust: free delivery threshold, store pickup Pretoria, vet-informed advice. Clean product cards with ratings. Fix store-only confusion with clear “Ship / Pickup” badges. Bright, friendly, professional — not cartoonish.

## Cold email draft

**To:** info@animal-kingdom.co.za  
**Subject:** One thing on Animal Kingdom’s site that’s likely costing online sales

Hi there,

Animal Kingdom’s range is impressive — 35+ years and a real multi-pet catalog is rare compared with smaller pet shops.

Looking at the online store, a few conversion issues stood out: homepage deals marked **“Available In Store Only,”** thin product pages, and small trust/UX issues (even a typo like “Canopes” in the fish menu). Against national players with cleaner Shopify stores, that friction adds up.

I put together a homepage concept showing how Animal Kingdom could present the same catalog with clearer browsing, better product pages, and an online-first deals section:

[CONCEPT LINK]

Open to a 15-minute review if you’d like me to walk through the fixes.

[YOUR NAME]  
[AGENCY]

---

# 5. Furniture Liquidation Warehouse

| Field | Detail |
|---|---|
| Website | https://www.loungesuiteforsale.co.za |
| Alt domain | furnitureliquidation.co.za (returns Forbidden) |
| Country | ZA (5 Gauteng branches) |
| Industry | Furniture / liquidation |
| CMS | WooCommerce |
| Contact | glen@furnitureliquidation.co.za |
| Phone | 011 616 2026 / +27 82 730 8262 |
| Priority | **#5 — multi-branch + unstable web** |

## Liked about the business
5 showrooms, liquidation price positioning, active social selling, clear local demand for lounge suites/recliners. Real offline footprint.

## Issues found (specific)

1. **Site instability.** Homepage returned **500** during audit; primary brand domain `furnitureliquidation.co.za` returns **Forbidden**.
2. **Thin online catalog.** Shop shows ~21 products while they clearly move much more stock via Facebook/showrooms.
3. **Domain/brand split.** Trading as Furniture Liquidation Warehouse but selling via loungesuiteforsale.co.za — confusing for returning customers.
4. **UX is deal-spammy.** “Unbeatable Deal!” badges everywhere; weak storytelling for higher-ticket lounge suites (dimensions buried, delivery/branch stock unclear).
5. **Multi-location ecommerce gap.** Hard to tell what’s available at Denver vs Midrand vs Centurion online.

## Solution
Stable Shopify storefront with:
- One primary domain
- Branch availability / pickup
- Strong lounge suite PDPs (dimensions, materials, guarantee)
- Cleaner deal merchandising (not badge overload)
- WhatsApp + store locator integration

## Homepage concept brief
> Shopify homepage for Furniture Liquidation Warehouse (Gauteng). Hero: warehouse pricing + showroom confidence. “Brand-new stock. Liquidation prices. 5 locations.” Featured: Lounge Suites / Recliners / Beds. Product cards with clear price + % off + “View in showroom.” Store locator strip. Trust: guarantees, delivery, WhatsApp sales chat. Bold commercial look, not luxury design gallery.

## Cold email draft

**To:** glen@furnitureliquidation.co.za  
**Subject:** Your furniture site was down while I was checking it

Hi Glen,

You’ve built something strong with Furniture Liquidation Warehouse — 5 Gauteng locations and a clear “brand-new stock at liquidation prices” offer.

While reviewing the online shop, the site returned errors (and furnitureliquidation.co.za was blocked), and the live catalog looked much smaller than what you clearly sell in-store and on social. For high-ticket lounge suites, that usually means Facebook traffic arrives and can’t finish the buy online.

I mocked a cleaner homepage concept focused on stable browsing, clearer suite details, and multi-branch pickup/delivery:

[CONCEPT LINK]

If useful, I can show you the issues and fixes in 15 minutes.

[YOUR NAME]  
[AGENCY]

---

# Approval checklist (you)

For each lead, mark:

| Lead | Approve email? | Edit needed? | Concept ready? | Loom ready? | Send? |
|---|---|---|---|---|---|
| Katie and May | ☐ | ☐ | ☐ | ☐ | ☐ |
| Suzy Loves Milo | ☐ | ☐ | ☐ | ☐ | ☐ |
| Phases Africa | ☐ | ☐ | ☐ | ☐ | ☐ |
| Animal Kingdom | ☐ | ☐ | ☐ | ☐ | ☐ |
| Furniture Liquidation | ☐ | ☐ | ☐ | ☐ | ☐ |

---

# Recommended sequence this week

1. You fill in name/agency + approve Katie and May email  
2. Build Katie and May homepage concept (Lovable/v0) — strongest demo  
3. Record 2–3 min Loom  
4. Send Day 1 email  
5. Repeat for Suzy Loves Milo same week  
6. Then ZA leads (Phases → Animal Kingdom → Furniture Liquidation)

**Do not send all 5 the same day.** Keep it personalized and paced (~1–2/day).
