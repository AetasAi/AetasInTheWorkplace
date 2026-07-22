#!/usr/bin/env python3
"""
Aetas in the Workplace, Insights index auto-builder.

Scans insights/*.html, extracts metadata, and rebuilds the article
grid in insights.html between markers:

    <!-- AUTO-INSIGHTS-START -->
    ...replaced automatically...
    <!-- AUTO-INSIGHTS-END -->

Articles with a datePublished in the FUTURE are excluded.
Upload future-dated articles and they appear automatically on their
scheduled date via the daily GitHub Action.

Run locally from repo root:
    py scripts\\build-insights-index.py

Per-article controls (optional, add to <head>):
    <meta name="itw-listed"     content="false">          hide from index
    <meta name="itw-tag"        content="Business case">  card tag label
    <meta name="itw-author"     content="Matthew Steiner"> author line
"""

import re
import sys
from datetime import date
from pathlib import Path

INSIGHTS_DIR = Path("insights")
INDEX_FILE   = Path("insights.html")

START_MARKER = "<!-- AUTO-INSIGHTS-START -->"
END_MARKER   = "<!-- AUTO-INSIGHTS-END -->"


def extract_meta(html, name):
    m = re.search(rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"', html)
    return m.group(1).strip() if m else None

def extract_og(html, prop):
    m = re.search(rf'<meta\s+property="{re.escape(prop)}"\s+content="([^"]*)"', html)
    return m.group(1).strip() if m else None

def extract_json_ld_date(html):
    m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
    return m.group(1)[:10] if m else None

def extract_h1(html):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else None

def format_display_date(iso_str):
    d = date.fromisoformat(iso_str)
    return f"{d.strftime('%B')} {d.year}"

def parse_articles(insights_dir):
    articles = []
    today = date.today()

    for path in sorted(insights_dir.glob("*.html")):
        if path.name == "index.html":
            continue
        html = path.read_text(encoding="utf-8")

        listed = extract_meta(html, "itw-listed")
        if listed and listed.lower() == "false":
            continue

        pub_iso = extract_json_ld_date(html)
        if pub_iso:
            pub_date = date.fromisoformat(pub_iso)
            if pub_date > today:
                print(f"  Skipping (future): {path.name}, scheduled {pub_iso}")
                continue
        else:
            pub_iso  = today.isoformat()
            pub_date = today

        title  = extract_h1(html) or extract_og(html, "og:title") or path.stem
        desc   = extract_meta(html, "description") or extract_og(html, "og:description") or ""
        tag    = extract_meta(html, "itw-tag") or "Insights"
        author = extract_meta(html, "itw-author") or "Matthew Steiner"

        articles.append({
            "slug":        path.stem,
            "title":       title,
            "desc":        desc,
            "tag":         tag,
            "author":      author,
            "pub_date":    pub_date,
            "pub_display": format_display_date(pub_iso),
        })

    articles.sort(key=lambda a: a["pub_date"], reverse=True)
    return articles

def build_cards(articles):
    if not articles:
        return '      <div class="article-card"><p>No articles published yet.</p></div>'

    cards = []
    for a in articles:
        card = f'''      <div class="article-card reveal">
        <span class="article-tag">{a["tag"]}</span>
        <p class="article-meta">{a["author"]} · {a["pub_display"]}</p>
        <h3>{a["title"]}</h3>
        <p>{a["desc"]}</p>
        <a class="card-link" href="/insights/{a["slug"]}">Read article</a>
      </div>'''
        cards.append(card)
    return "\n\n".join(cards)

def main():
    repo_root    = Path(__file__).resolve().parent.parent
    insights_dir = repo_root / INSIGHTS_DIR
    index_path   = repo_root / INDEX_FILE

    if not insights_dir.exists():
        sys.stderr.write(f"Insights directory not found: {insights_dir}\n")
        return 1
    if not index_path.exists():
        sys.stderr.write(f"Index not found: {index_path}\n")
        return 1

    print("Aetas in the Workplace, Insights Index Builder")
    print(f"Scanning: {insights_dir}")
    print()

    articles = parse_articles(insights_dir)
    print(f"Found {len(articles)} published article(s)")
    for a in articles:
        print(f"  + {a['slug']}, {a['pub_display']}")

    cards_html = build_cards(articles)

    index_html = index_path.read_text(encoding="utf-8")
    if START_MARKER not in index_html or END_MARKER not in index_html:
        sys.stderr.write(f"Markers not found in {INDEX_FILE}.\n")
        sys.stderr.write(f"Add inside the grid div:\n  {START_MARKER}\n  {END_MARKER}\n")
        return 1

    before    = index_html[:index_html.index(START_MARKER) + len(START_MARKER)]
    after     = index_html[index_html.index(END_MARKER):]
    new_index = before + "\n" + cards_html + "\n      " + after

    index_path.write_text(new_index, encoding="utf-8")
    print()
    print(f"✓ {INDEX_FILE} updated with {len(articles)} article(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
