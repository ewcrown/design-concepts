#!/usr/bin/env python3
"""Stamp CSS/JS URLs with a content hash so GitHub Pages/browsers fetch fresh assets."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def short_hash(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(data).hexdigest()[:10]


def main() -> None:
    css_v = short_hash(DOCS / "shared.css")
    js_v = short_hash(DOCS / "premium.js")
    stamp = f"css-{css_v}_js-{js_v}"
    (DOCS / "CACHE_VERSION").write_text(stamp + "\n")

    updated = 0
    for path in DOCS.rglob("*.html"):
        text = path.read_text()
        original = text

        if "http-equiv=\"refresh\"" not in text and "<head>" in text:
            if 'http-equiv="Cache-Control"' not in text:
                text = text.replace(
                    "<head>",
                    "<head>\n"
                    '  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />\n'
                    '  <meta http-equiv="Pragma" content="no-cache" />\n'
                    '  <meta http-equiv="Expires" content="0" />',
                    1,
                )

        text = re.sub(
            r"(shared\.css)(?:\?v=[^\"'\s]*)?",
            rf"\1?v={css_v}",
            text,
        )
        text = re.sub(
            r"(premium\.js)(?:\?v=[^\"'\s]*)?",
            rf"\1?v={js_v}",
            text,
        )

        if text != original:
            path.write_text(text)
            updated += 1

    print(f"cache bust css={css_v} js={js_v} · updated {updated} html files")


if __name__ == "__main__":
    main()
