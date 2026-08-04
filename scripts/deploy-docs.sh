#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 scripts/bust-cache.py
git add docs
git status -sb
echo ""
echo "Cache-busting applied. Commit + push when ready:"
echo "  git commit -am \"chore: cache-bust assets\" && git push"
