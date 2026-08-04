# Shopify store concepts

Static HTML demos: **Home · Collection · Product** per brand.

## Live site

https://ewcrown.github.io/design-concepts/

## Cache / “I don’t see my changes”

GitHub Pages + browsers cache CSS/JS. We bust that automatically:

```bash
python3 scripts/bust-cache.py
git add docs && git commit -m "chore: cache-bust static assets" && git push
```

Or:

```bash
bash scripts/deploy-docs.sh
```

A **pre-push hook** also runs the bust script — if HTML still has old `?v=` hashes, push is blocked until you commit the update.

**One-time hard refresh in the browser:** `Cmd + Shift + R` (Mac) / `Ctrl + Shift + R` (Windows).

## Local preview

```bash
cd docs
python3 -m http.server 8080
```

Open http://localhost:8080

## Brands

| Brand | Folder |
|-------|--------|
| Katie and May | `docs/katie-and-may/` |
| Suzy Loves Milo | `docs/suzy-loves-milo/` |
| Phases Africa | `docs/phases-africa/` |
| Animal Kingdom | `docs/animal-kingdom/` |
| Furniture Liquidation | `docs/furniture-liquidation/` |
