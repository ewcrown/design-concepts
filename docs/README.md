# Shopify store concepts (GitHub Pages)

Static HTML concepts for Tier A cold outreach: **Home · Collection · Product** per brand.

## Local preview

```bash
cd docs
python3 -m http.server 8080
```

Open http://localhost:8080

## Publish on GitHub Pages

1. Create a GitHub repo (e.g. `customer-finder` or `shopify-concepts`)
2. Push this project
3. Repo **Settings → Pages**
4. Source: **Deploy from a branch**
5. Branch: `main` · Folder: **/docs**
6. Save — wait ~1 minute

Your live URLs will look like:

```
https://YOUR_USERNAME.github.io/REPO_NAME/
https://YOUR_USERNAME.github.io/REPO_NAME/katie-and-may/
https://YOUR_USERNAME.github.io/REPO_NAME/katie-and-may/collection.html
https://YOUR_USERNAME.github.io/REPO_NAME/katie-and-may/product.html
```

Use the **Home** URL as `[CONCEPT LINK]` in each email.

## Brands

| Brand | Folder |
|-------|--------|
| Katie and May | `docs/katie-and-may/` |
| Suzy Loves Milo | `docs/suzy-loves-milo/` |
| Phases Africa | `docs/phases-africa/` |
| Animal Kingdom | `docs/animal-kingdom/` |
| Furniture Liquidation | `docs/furniture-liquidation/` |
