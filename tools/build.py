#!/usr/bin/env python3
"""Build the portfolio site.

Each file in tools/pages/ is the body of one page. This script wraps every
body in the shared header, navigation and footer and writes the finished
.html files to the repository root, which is what GitHub Pages serves.

Usage:  python3 tools/build.py
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = Path(__file__).resolve().parent / "pages"

SITE = {
    "name": "Sam Quentzel",
    "tagline": "Business + Computer Science · AI",
    "email": "q.sam@wustl.edu",
    "linkedin": "https://www.linkedin.com/in/squentzel724/",
    "resume": "assets/docs/Samuel-Quentzel-Resume.pdf",
    "url": "https://sammyq724.github.io/SamQuentzel/",
}

# (file, label in the navigation bar)
NAV = [
    ("index.html", "Welcome"),
    ("resume.html", "Resume"),
    ("purpose.html", "Purpose"),
    ("stories.html", "Stories"),
    ("thought-piece.html", "Thought Piece"),
    ("podcast.html", "Podcast"),
    ("interviews.html", "Interviews"),
    ("brand.html", "Brand Guide"),
]

# Word-count limits from the assignment, checked on every build.
LIMITS = {
    "purpose": (190, 210),
    "story1": (100, 150),
    "story2": (100, 150),
    "story3": (100, 150),
    "story4": (100, 150),
    "thought": (200, 300),
}

ICON_DOWNLOAD = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M12 4v11"/><path d="m7 11 5 5 5-5"/><path d="M5 20h14"/></svg>'
)


class WordCounter(HTMLParser):
    """Counts the words inside every element carrying data-wc="key"."""

    VOID = {"br", "img", "hr", "input", "meta", "link", "source"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str | None] = []
        self.text: dict[str, list[str]] = {}

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        key = dict(attrs).get("data-wc")
        self.stack.append(key)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        for key in self.stack:
            if key:
                self.text.setdefault(key, []).append(data)

    def counts(self) -> dict[str, int]:
        return {k: len(re.findall(r"\S+", " ".join(v))) for k, v in self.text.items()}


def version_assets(page: str) -> str:
    """Add ?v=<content hash> to every local asset link.

    The link changes whenever the file changes, so a browser can never show
    an old stylesheet, image, or resume PDF alongside a new page.
    """
    def stamp(match: re.Match) -> str:
        path = match.group(0)
        file = ROOT / path
        if not file.is_file():
            return path
        return f"{path}?v={hashlib.sha1(file.read_bytes()).hexdigest()[:10]}"

    return re.sub(r"assets/[A-Za-z0-9_./-]+\.(?:css|png|jpg|webp|svg|pdf|woff2)(?![?\w])", stamp, page)


def curl_apostrophes(markup: str) -> str:
    """Turn straight apostrophes in visible text into typographic ones."""
    parts = re.split(r"(<!--.*?-->|<[^>]+>)", markup, flags=re.S)
    for i in range(0, len(parts), 2):  # even items are text between tags
        parts[i] = re.sub(r"(?<=\w)'", "\u2019", parts[i])
    return "".join(parts)


def layout(file: str, meta: dict, body: str) -> str:
    title = meta["title"]
    full_title = f"{title} | {SITE['name']}" if file != "index.html" else f"{SITE['name']} | Digital Career Portfolio"
    desc = html.escape(meta["description"], quote=True)
    current = ' aria-current="page"'
    nav_items = "\n".join(
        f'          <li><a href="{href}"{current if href == file else ""}>{label}</a></li>'
        for href, label in NAV
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(full_title)}</title>
  <meta name="description" content="{desc}">
  <meta name="author" content="{SITE['name']}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(full_title, quote=True)}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{SITE['url']}assets/img/linkedin-cover.png">
  <meta name="theme-color" content="#14202b">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="assets/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/source-serif-4-var.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap bar">
      <a class="brand" href="index.html" aria-label="{SITE['name']}, home">
        <span class="plate" aria-hidden="true">SQ</span>
        <span class="brand-text"><strong>{SITE['name']}</strong><small>{SITE['tagline']}</small></span>
      </a>
      <a class="btn btn-outline" href="{SITE['resume']}" download aria-label="Download resume">{ICON_DOWNLOAD}<span>Download<span class="hide-xs"> resume</span></span></a>
    </div>
    <nav class="site-nav" aria-label="Primary">
      <div class="wrap">
        <ul>
{nav_items}
        </ul>
      </div>
    </nav>
  </header>

  <main id="main">
{body.strip()}
  </main>

  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <a class="brand" href="index.html">
          <span class="plate" aria-hidden="true">SQ</span>
          <span class="brand-text"><strong>{SITE['name']}</strong><small>{SITE['tagline']}</small></span>
        </a>
        <p>Business and Computer Science at WashU. I want to help established businesses modernize with AI.</p>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
          <li><a href="{SITE['linkedin']}" target="_blank" rel="noopener">LinkedIn</a></li>
          <li><a href="{SITE['resume']}" download>Download resume (PDF)</a></li>
        </ul>
      </div>
    </div>
    <div class="wrap">
      <div class="colophon">
        <span>&copy; 2026 {SITE['name']}</span>
        <span>Digital Career Portfolio</span>
      </div>
    </div>
  </footer>
  <script>
    (function () {{
      var here = document.querySelector('.site-nav [aria-current="page"]');
      var list = document.querySelector('.site-nav ul');
      if (here && list && list.scrollWidth > list.clientWidth) {{
        list.scrollLeft = here.offsetLeft - (list.clientWidth - here.offsetWidth) / 2;
      }}
    }})();
  </script>
</body>
</html>
"""


def main() -> int:
    ok = True
    for src in sorted(PAGES.glob("*.html")):
        raw = src.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->", raw, re.S)
        if not m:
            print(f"!! {src.name}: missing metadata comment on the first line")
            ok = False
            continue
        meta = json.loads(m.group(1))
        body = raw[m.end():]

        counter = WordCounter()
        counter.feed(body)
        counts = counter.counts()
        for key, n in counts.items():
            body = body.replace("{{wc:%s}}" % key, str(n))
            lo, hi = LIMITS.get(key, (0, 10**6))
            flag = "" if lo <= n <= hi else f"   <-- OUTSIDE {lo}-{hi}"
            if flag:
                ok = False
            print(f"   {src.name:<22} {key:<8} {n:>4} words{flag}")
        for token, value in (("{{email}}", SITE["email"]), ("{{linkedin}}", SITE["linkedin"]),
                             ("{{resume}}", SITE["resume"]), ("{{download_icon}}", ICON_DOWNLOAD)):
            body = body.replace(token, value)
        body = curl_apostrophes(body)
        left = re.findall(r"\{\{[^}]+\}\}", body)
        if left:
            print(f"!! {src.name}: unresolved tokens {left}")
            ok = False

        (ROOT / src.name).write_text(version_assets(layout(src.name, meta, body)), encoding="utf-8")
        print(f"built {src.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
