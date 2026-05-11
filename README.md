# Aetas in the Workplace

**Live site:** https://itw.aetaspartners.com  
**Repo:** https://github.com/AetasAi/AetasInTheWorkplace  
**Deployed via:** GitHub Pages (automatic on push to `main`)  
**Contact:** matthew.steiner@aetas-partners.com

---

## Overview

Aetas in the Workplace is a consultancy-led business performance service for SMEs, LLPs, and professional practices. It operates under the Aetas Wealth brand (a trading style of Insight Financial Associates Limited, FCA registration 458421).

The site presents the service to two primary audiences — limited companies and LLPs — and includes client tools (forms, calculator, diagnostic), content (insights articles, case studies), and post-booking support.

---

## Site Structure

### Main audience pages

| File | Description |
|------|-------------|
| `index.html` | Homepage — performance positioning, stats, proof section with case study links, audience split |
| `limited-companies.html` | Audience page for SMEs and limited companies |
| `llps.html` | Audience page for LLPs and professional practices |

### Tools and conversion pages

| File | Description |
|------|-------------|
| `calculator.html` | ROEI Calculator — interactive sliders calculate the cost of financial pressure; personalised inline CTA connected to calculated figure |
| `investment.html` | Pricing — per-employee fee structure (£115–165/employee/year by headcount band), transparent |
| `diagnostic.html` | 8-minute self-assessment diagnostic tool |

### Content

| File | Description |
|------|-------------|
| `insights.html` | Insights index — links to all five hosted articles (all internal, no off-site links) |
| `insights/why-financial-wellbeing-is-a-business-issue.html` | Article |
| `insights/when-everyday-life-stops-talking-back.html` | Article |
| `insights/introducing-the-aetas-collective.html` | Article |
| `insights/financial-wellbeing-in-the-workplace.html` | Article |
| `insights/strengthening-your-team-through-financial-wellbeing.html` | Article |
| `insights/article-template.html` | Template for future articles (see below) |
| `case-studies/bristol-organisation.html` | Case study: Bristol-based organisation — workshop, pension review, Collective services |
| `case-studies/uk-retail-group.html` | Case study: Large UK retail group — diagnostic, pension review (no change recommended), Shop St |

### Client forms (noindex — private)

| File | Description |
|------|-------------|
| `benefits-review.html` | Employee Benefits Data Capture — 7 sections, jsPDF output, EmailJS delivery to both parties |
| `data-processing-agreement.html` | UK GDPR DPA — 15 clauses, electronic signature, jsPDF output, EmailJS delivery |
| `form-thankyou.html` | Post-submission thank you — reads URL params (`?form=benefits|dpa&org=NAME&ref=REF`), per-form content, PDF re-download from sessionStorage |

### Post-booking page (noindex — private)

| File | Description |
|------|-------------|
| `whats-next.html` | Shown after booking a Workplace Performance Review. Two conversation structure, preparation guide, practicalities, links to both client forms |

### Support pages

| File | Description |
|------|-------------|
| `faqs.html` | FAQs — current positioning (Clarity/Confidence/Stability), per-employee pricing |
| `privacy.html` | Privacy policy |
| `404.html` | Custom 404 |
| `charities.html` | Meta-refresh redirect → `charitywellbeing.aetaspartners.com` |

### Infrastructure

| File | Description |
|------|-------------|
| `CNAME` | Custom domain: `itw.aetaspartners.com` |
| `sitemap.xml` | Sitemap for search engines |
| `robots.txt` | Permits ClaudeBot, GPTBot, PerplexityBot, Google-Extended |
| `llms.txt` | AI crawler guidance — service description, pages, contact |
| `manifest.webmanifest` | PWA manifest |
| `og-image.png` | Open Graph image (1200×630) |

---

## Design System

Pure static HTML, CSS, and vanilla JavaScript. No build tools, frameworks, or dependencies.

### Colours

```css
--navy:       #1a2b4a   /* Primary — headers, nav, footer, CTAs */
--navy-mid:   #2d4270   /* Hover states */
--navy-light: #e8ecf3   /* Subtle section backgrounds */
--gold:       #b8934a   /* Accent — bullets, borders, CTA buttons */
--gold-light: #d4b07a   /* Text on dark backgrounds */
--gold-pale:  #f5ede0   /* Callout box backgrounds */
--cream:      #faf8f5   /* Page background */
--white:      #ffffff
```

### Typography

| Role | Font | Weights |
|------|------|---------|
| Display, headings | Cormorant Garamond | 300, 400, 500, 600 (+ italic variants) |
| Body, UI, labels | Jost | 300, 400, 500 |
| Signatures (forms only) | Great Vibes | 400 |

All loaded via Google Fonts.

### Responsive breakpoint

Navigation collapses to hamburger menu at 700–800px (varies by page). Grids collapse to single column at similar breakpoints.

---

## Navigation

All main public pages share this nav order:

```
Limited companies | LLPs | Pricing | Calculator | Diagnostic | Insights | FAQs | Book a Review
```

Nav CTA booking link:
```
https://links.aetas-partners.com/widget/booking/IacdM2cW2bnLm0pK7Jty
```

> **Important:** The nav block is duplicated in every `.html` file. If any nav label or link changes, update all pages. The `class="active"` (or `class="nav-cta"`) attribute marks the CTA button.

---

## Integrations

### Analytics — GA4
**Measurement ID:** `G-HNH05BKNFX`  
All pages include the GA4 tag. Shared property with `aetas-partners.com` — filter by hostname `itw.aetaspartners.com` in GA4 for ITW-only data.

### Booking — GoHighLevel
All booking CTAs link to the GHL widget. The `whats-next.html` page should be set as the confirmation redirect URL in GHL calendar settings.

### Forms — EmailJS + jsPDF

Both client forms generate a formatted A4 PDF client-side (jsPDF) and deliver it to both parties via EmailJS on submission.

**EmailJS credentials:**
```
Public Key:           T-OvAY8-q_r_P4tAA
Service ID:           service_dztbuyl
Internal template:    template_283g3pp   → matthew.steiner@aetas-partners.com
Confirm template:     template_2hfklis   → client email address
```

**Template variables used:**
- Internal: `{{ref}}` `{{org}}` `{{contact}}` `{{email}}` `{{form_type}}` `{{form_data}}` `{{submitted}}`
- Confirm: `{{ref}}` `{{org}}` `{{contact}}` `{{to_email}}` `{{form_type}}`

**CDN libraries (loaded in both form pages):**
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.31/jspdf.plugin.autotable.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
```

**Auto-generated reference formats:**
- Benefits form: `AEB-YYYYMM-XXXX`
- DPA: `APL-DPA-YYYYMM-XXXX`

---

## Adding New Insights Articles

Use `insights/article-template.html` as the base. Replace these placeholders:

| Placeholder | Replace with |
|-------------|--------------|
| `ARTICLE_TITLE` | Full article title |
| `ARTICLE_META_DESCRIPTION` | ~155-char SEO description |
| `ARTICLE_SLUG` | URL slug (no `.html`) matching the filename |
| `ARTICLE_CATEGORY` | e.g. `Business performance` |
| `ARTICLE_STANDFIRST` | Opening paragraph |
| `ARTICLE_DATE` | e.g. `May 2026` |
| `ARTICLE_READ_TIME` | e.g. `3 min` |
| `ARTICLE_BODY_HTML` | Full article body (h2, h3, p, ul/li) |

Then:
1. Save as `insights/[your-slug].html`
2. Add an entry to the `ALL_ARTICLES` array in the page's `<script>` block
3. Add a card to `insights.html`
4. Update `sitemap.xml`

---

## Adding New Case Studies

Use either existing case study as a template. Save to `case-studies/[slug].html`.

Checklist:
- [ ] Anonymise all client details (type, location, size)
- [ ] Add `Details in this case study have been anonymised.` to the footer legal text
- [ ] Cross-link from the other case study's "More case studies" section
- [ ] Add to case study strips on `limited-companies.html` and `llps.html`
- [ ] Add link to proof section on `index.html`
- [ ] Add to `sitemap.xml`

---

## Deployment

GitHub Pages deploys automatically on every push to `main`. Takes 1–2 minutes.

**Domain:** `itw.aetaspartners.com` (configured via `CNAME`)  
**Branch:** `main` only

### Push workflow

```bash
git add -A
git commit -m "Description of changes"
git push https://AetasAi:[TOKEN]@github.com/AetasAi/AetasInTheWorkplace.git main
```

A short-lived GitHub Personal Access Token (Classic, `repo` scope) is generated per session and deleted immediately after each push to avoid long-lived credentials in the environment.

---

## CTA Language Reference

Use these consistently across all pages:

| Context | Text |
|---------|------|
| Nav button | `Book a Review` |
| Hero and primary page CTAs | `Book a Workplace Performance Review` |
| Article / form in-page CTAs | `Book a Workplace Performance Review` |

Primary booking link: `https://links.aetas-partners.com/widget/booking/IacdM2cW2bnLm0pK7Jty`

---

## Employee Ceiling

The service targets organisations with **10–250 employees**. This figure appears in:
- `calculator.html` — slider max and hint text
- `investment.html` — pricing band (81–250)
- `limited-companies.html`, `llps.html`, `faqs.html` — copy and schema
- `llms.txt` — AI crawler guidance

If this figure changes, update all instances.

---

## Head Tag Requirements (all pages)

```html
<!-- GA4 — always first in <head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HNH05BKNFX"></script>
<script>
  window.dataLayer=window.dataLayer||[];
  function gtag(){dataLayer.push(arguments);}
  gtag('js',new Date());
  gtag('config','G-HNH05BKNFX');
</script>

<!-- Favicon + PWA -->
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="#1a2b4a">

<!-- Canonical + OG (adjust per page) -->
<link rel="canonical" href="https://itw.aetaspartners.com/[page-url]">
<meta property="og:title" content="[Page title]">
<meta property="og:description" content="[Page description]">
<meta property="og:url" content="https://itw.aetaspartners.com/[page-url]">
<meta property="og:type" content="website">
<meta property="og:image" content="https://itw.aetaspartners.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
```

Private pages (forms, whats-next, form-thankyou) also include:
```html
<meta name="robots" content="noindex, nofollow">
```

---

## Regulatory Footer

All public pages include (adapted per page):

> Aetas in the Workplace provides workplace financial wellbeing, education, and consultancy services to employers. These services do not constitute regulated financial advice. Where regulated advice is required, this is provided separately by Aetas Wealth, a trading style of Insight Financial Associates Limited, authorised and regulated by the Financial Conduct Authority (registration number 458421).

---

*Aetas in the Workplace · A trading style of Aetas Wealth, Insight Financial Associates Limited · FCA reg 458421*
