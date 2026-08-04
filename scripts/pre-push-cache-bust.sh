#!/bin/sh
# Auto cache-bust CSS/JS URLs before each push to GitHub Pages
ROOT="$(git rev-parse --show-toplevel)"
python3 "$ROOT/scripts/bust-cache.py"
git add "$ROOT/docs" >/dev/null 2>&1 || true
# If the stamp changed tracked files, amend isn't allowed in hooks easily —
# instead stage changes so the push commit includes them when user commits again.
# For push-only: create a tiny stamp commit if dirty.
if ! git diff --cached --quiet -- "$ROOT/docs"; then
  git commit -m "chore: cache-bust static assets for GitHub Pages" >/dev/null 2>&1 || true
fi
