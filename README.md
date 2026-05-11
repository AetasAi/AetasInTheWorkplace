# Brand refresh — applying the patch

This bundle contains the brand refresh as a single git patch.
The commit is on a clean local branch in my sandbox but I can't push it for you
(no GitHub credentials inside the sandbox), so you apply it locally.

## What changed

24 files, 427 inserts / 142 deletes. Every change is one of:

- **Palette:** navy unified to brand `#0d2c6c` (was three variants);
  gold unified to `#b8934a` (was two variants); navy-mid hover shade
  harmonised to `#1d4291`; meta theme-color and `manifest.webmanifest` updated.
- **Header:** `<img class="nav-mark">` inserted at the start of every
  `.nav-logo` (10 pages) and `.nav-brand` (8 pages) anchor. Light-bg pages
  use `aetas-mark.svg`; dark-bg pages use `aetas-mark-reverse.svg`. Markup
  is minimal — no wrapper spans — so the existing CSS rule
  `.nav-logo span { color: gold }` is untouched: "Aetas" stays navy,
  "in the Workplace" stays gold.
- **Footer:** same mark insertion for `.footer-logo` (6) and
  `.footer-brand` (8) using the reverse mark on dark backgrounds.
- **Footer lockup:** `<img src="/aetas-horizontal-reverse.svg">` linked to
  `aetas-partners.com`, injected before every `</footer>` (all 24 pages),
  centred, with subtle hover-to-100% opacity. Marked with the comment
  `<!-- brand-refresh: aetas partners lockup -->` for idempotency.
- **Typography:** Cormorant Garamond + Jost left untouched (per your
  decision to keep the existing type system).

## Applying it

```bash
cd /path/to/AetasInTheWorkplace
git fetch
git checkout main
git checkout -b brand-refresh
git am /path/to/0001-Brand-refresh-logo-palette-footer-lockup.patch
git push -u origin brand-refresh
```

Then open a PR from `brand-refresh` → `main` on GitHub to review the
exact diff before merging.

## Previews

- `preview-header-homepage.png` — header before/after on homepage
- `preview-footer-homepage.png` — full homepage footer (after) showing the
  Aetas Partners lockup at the bottom
- `preview-header-article.png` — header on an Insights article (navy nav,
  reverse mark)
- `preview-footer-article-compare.png` — Insights article footer before/after
- `preview-footer-diagnostic-compare.png` — Diagnostic page footer before/after
