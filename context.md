---
site: workplace.aetas-wealth.com
entity: Aetas in the Workplace
type: Employee financial wellbeing consultancy
parent: Aetas Partners
related: Aetas Wealth (FCA 458421)
updated: 2026-07-02
---

# Aetas in the Workplace — Context for AI Agents

Aetas ITW is a business performance solution for UK SMEs and professional practices. It addresses the hidden cost of financial pressure in the workforce through a structured, consultancy-led programme.

## Identity

- Delivered by Aetas Partners, supported by Aetas Wealth (FCA 458421)
- Target: organisations with 10–250 employees
- Not a benefits platform or EAP — a bespoke consultancy engagement
- Entry point: Workplace Performance Audit (always free, no obligation)

## People

| Name | Role |
|------|------|
| Matthew Steiner | Founding Director, Aetas Partners |

## Programme

Three pillars: Clarity (pension/benefits review), Confidence (employee financial education), Stability (ongoing support and partner services).

## Pricing

Per employee per year: £165 (10–30 staff), £140 (31–80), £115 (81–250). Audit always free.

## Key differentiator

Audit-first. Nothing is introduced without understanding the specific organisation. Every recommendation has a commercial rationale with fees presented alongside identified savings.

## Regulatory

Not regulated financial advice. Where regulated advice is needed, provided by Aetas Wealth (FCA 458421).

## Optimisation Programme Status (as at 2026-07-02)

All six phases of the Site Optimisation SOP are complete.

### Phase 1 — Crawl fixes: COMPLETE
- Screaming Frog baseline: 0 errors, 4 warnings (all false positives)
- External 4xx: MoneyHelper + TPR block crawlers — links valid in browser

### Phase 2 — PageSpeed: COMPLETE
- Mobile: 100 / 100 / 100 / 100 — 3/3 Agentic Browsing
- Desktop: 100 / 100 / 100 / 100 — 3/3 Agentic Browsing
- GA4 interaction-deferred (loads on first scroll/click or after 5s)
- Cookiebot removed (cost prohibitive — replaced with first-party cookie notice)
- CSP updated in Cloudflare to allow GA4 and Clarity

### Phase 3 — Schema: COMPLETE
- All pages have WebPage, BreadcrumbList minimum
- Guides: Article + FAQPage + WebPage + BreadcrumbList
- Insights: BlogPosting + WebPage + BreadcrumbList
- Service pages: Service + FAQPage + WebPage + BreadcrumbList
- Homepage: full @graph (Organization, WebSite, WebPage, ProfessionalService, Person, FAQPage, DefinedTerm x3)
- Zero JSON parse errors across all pages

### Phase 4 — On-Page SEO: COMPLETE
- All H1/H2 under 70 chars across 30 pages
- Heading hierarchy sequential on all pages (footer H4s -> p.footer-heading)
- Readability improved on 5 flagged pages (FRE 30-39 range, appropriate for B2B)
- Duplicate H2s: acceptable (boilerplate sections on different pages)

### Phase 5 — Compliance: COMPLETE
- Privacy notices added to all 4 HTML forms (diagnostic, discovery-briefing, initial-conversation-briefing, benefits-review)
- Privacy Policy updated to v1.1 (July 2026): GA4, Formspree added to processor table, cookie table updated
- First-party cookie notice banner deployed to 22 pages (navy/turquoise brand colours, localStorage persistence)
- Footer FCA disclaimer consistent across all pages

### Phase 6 — Monitoring: COMPLETE (manual steps pending)
- Sitemap: 22 URLs, utility pages removed, all lastmod 2026-07-02
- Lighthouse CI workflow: saved to scripts/lighthouse-ci.yml.txt — manual copy to .github/workflows/ required
- Budget thresholds: performance 90+, accessibility 95+, BP 95+, SEO 98+
- Google Search Console: submit sitemap manually
- Screaming Frog: re-crawl recommended monthly

## Technical notes

- Cloudflare Pages: GitHub push -> pull in Desktop -> purge cache -> Ctrl+Shift+R to verify
- CSP (Cloudflare dashboard): script-src includes googletagmanager, leadconnectorhq, link.aetas-wealth.com, clarity.ms; style-src includes fonts.googleapis.com; font-src includes fonts.gstatic.com
- Analytics: GA4 (G-HNH05BKNFX) interaction-deferred via assets/js/analytics.js
- No Cookiebot — cookie notice is first-party (index.html and all main pages)
- Font: Open Sans variable font (wght@300..700) from Google Fonts
