---
title: Thesis fit – Fondo against General Catalyst, Index Ventures, Alumni Ventures
company: Fondo
created: 2026-11-11
author: thesis-fit v0.1 (Claude Code)
status: acceptance run
tags: [thesis-fit, fondo, general-catalyst, index-ventures, alumni-ventures]
---

# Thesis fit – Fondo

## Answer up front

**Alumni Ventures matches** Fondo on all four axes. **General Catalyst and Index Ventures are
partial**: each matches on three axes, and on the fourth its own portfolio data is too thin to
read – General Catalyst's stage is unclassified for 148 of 199 companies, and Index Ventures
tags a region for only 16 of 66. Neither shows a mismatch. All three back fintech companies
(at least 10% of each slice) sold mostly to businesses. Every list read is a **floor**, not a
complete portfolio (see each fund's section). Each fund has also backed companies that look like Fondo's
competitors: **Pilot** at Index Ventures, **Kick** and **Puzzle** at General Catalyst, **Haven**
and **Puzzle** at Alumni Ventures, among 13 candidates in total.

| Fund | Stage | Geography | Market | Model | Overall | Candidates | List |
|---|---|---|---|---|---|---|---|
| General Catalyst | partial | match | match | match | **partial** | 5 | floor |
| Index Ventures | match | unknown | match | match | **partial** | 2 | floor |
| Alumni Ventures | match | match | match | match | **match** | 6 | floor |

"Match" means Fondo resembles what the fund says it backs and what it has backed. It does not
predict that a fund will invest, and it is not an investment recommendation.

## How to read this

```
  STATED    the fund's own words on its own site, quoted with URL – or "not published"
  REVEALED  the companies the fund actually backed in the slice, classified one by one
  FIT       per axis, from the two sides; the portfolio outweighs the website
```

- **Axes.** Stage (Fondo: seed), geography (Fondo: headquartered in the United States), market
  (Fondo: Fintech & insurance, one of the company card's fixed list), business model (Fondo: B2B).
- **Reading the portfolio side**, per axis, first rule that applies: "unknown" = more than half
  of the slice unclassified on that axis, or 0 matching companies in a floor; "backs it" = at
  least 2 classified companies share Fondo's value **and** they are at least 10% of the
  classified rows; "thin" = at least 1 but below either threshold; "none" = 0 in a complete list.
  Each fit reason gives "k of classified (unclassified)".
- **Fit labels.** `match`, `partial`, `no match`, `unknown`, from the table in the skill's Step 4.
  `fit_overall` is `no match` if any axis is `no match`, `match` if all four are, `unknown` if all
  four are, otherwise `partial`. There is no score.
- **Complete or floor.** A list is complete only if the directory was read to its end and its
  count matches any count the fund publishes. Otherwise it is a floor: absence in it is not
  evidence of absence.
- **Slice.** Default: investments of the last 3 years. The date basis differs by fund, because no
  fund publishes the same date field – each section says which basis was used.
- **Abbreviations.** B2B / B2C / B2G = business to business / to consumer / to government ·
  CPA = certified public accountant · CFO = chief financial officer · R&D = research and
  development · SMB = small and medium-sized business · FP&A = financial planning and analysis ·
  AP/AR = accounts payable / accounts receivable · CSV = comma-separated values · JSON =
  JavaScript Object Notation · IPO = initial public offering · VC = venture capital · AI =
  artificial intelligence · ML = machine learning · US = United States · HTTP = Hypertext
  Transfer Protocol (202, 200 = status codes the server returns). Em dashes inside quoted
  one-liners in the portfolio CSVs are rendered as en dashes.

## The company

From `fondo/company-profile.md`, created in this run from Fondo's own pages.

| Field | Value | Source |
|---|---|---|
| Job done for the customer | "Set up in minutes and put accounting on autopilot with a CPA-led team who takes full ownership of your bookkeeping, corporate taxes, and R&D tax credits." | https://fondo.com/ |
| Business model | B2B – plans sold to startups | https://fondo.com/pricing |
| Market | Fintech & insurance | own classification of the job above |
| Stage | seed – "closed an oversubscribed $7 million seed funding round" (2024-11-22) | https://fondo.com/blog/fondo-announces-7m-oversubscribed |
| Geography | United States (San Francisco); sells to US Delaware C-corporations | https://fondo.com/about |

One fact the funds' own pages do not show: press coverage of Fondo's seed round lists an
"Index Ventures Scout Fund" among its investors
(https://techcrunch.com/2024/11/22/yc-backed-fondo-raises-funding-for-its-ai-powered-bookkeeping-and-taxes-platform/).
A scout fund is a separate vehicle; Fondo does not appear in Index Ventures' directory. Recorded
as a fact, not used in any fit.

---

## General Catalyst

### Stated thesis

| Axis | Quote | URL |
|---|---|---|
| Stage | "Seed and early stage is our core" … "an entrepreneurial-minded multistage platform" | https://www.generalcatalyst.com/stories/seed-at-general-catalyst |
| Geography | not published | – |
| Markets | not published (the portfolio page has sector filters – a directory taxonomy, not a thesis) | – |
| Business model | not published | – |
| Check size | not published | – |

### How the portfolio was obtained

```
  /portfolio (Webflow page, 100 per page) ──► sitemap.xml lists 620 /companies/ pages
        ──► each page read: industry · "Backed since" year · region · website
        ──► slice = "Backed since" 2024, 2025 or 2026  ──►  199 companies
```

- Directory: 620 company pages (https://www.generalcatalyst.com/sitemap.xml, retrieved
  2026-11-11); 34 have no year (undated).
- The fund's home page states "900+ portfolio companies" (as of 2025-06-30), so the directory
  holds about two-thirds of the claimed portfolio. **FLOOR.**
- Slice: **2024–2026 by investment year** – the directory gives years only, so whole years were
  used, not 2023-11 → 2026-11. N = **199**.
- Descriptions: the directory has none; one-liners taken from each company's own site
  (title and meta description, retrieved 2026-11-11).
- Stage: the directory has none. The fund's own story pages ("Seeding the future with …",
  "Our investment in …") state the round for 51 of the 199; the other 148 are `unknown`.

### Revealed thesis

| Axis | Slice of 199 |
|---|---|
| Stage | seed 26 · pre-seed 1 · Series A 8 · Series B+ 16 · unknown 148 |
| Geography (regions as published) | North America 147 · Europe 26 · Asia 11 · Distributed 9 · Middle East and North Africa 3 · Latin America 1 · none 2 |
| Market (top) | AI & data infrastructure 36 · Health & bio 33 · **Fintech & insurance 23** · Industrial & robotics 20 |
| Business model | B2B 138 · B2C 46 · B2G 15 |

### Fit per axis

| Axis | Revealed | Stated | Fit | Why |
|---|---|---|---|---|
| Stage | unknown – 26 seed of 51 classified (148 unclassified) | yes | partial | more than half the slice has no stage; rests on the stated side |
| Geography | backs it – 147 North America of 197 classified (2 unclassified) | not published | match | region-level only: the directory publishes "North America", not countries |
| Market | backs it – 23 fintech of 199 classified (0 unclassified), 11.6% | not published | match | rests on the portfolio |
| Model | backs it – 138 B2B of 199 classified (0 unclassified) | not published | match | rests on the portfolio |

Stage is `partial`: the fund says seed is its core, and 26 of the 51 companies with a known
stage are seed, but 148 of 199 have no stage, so the portfolio side cannot be read. Geography,
market and model rest on the portfolio alone, because the site publishes no thesis for them.

### Candidates

Full directory (620) swept by keyword (bookkeeping, accounting, tax, close, back office) on each
company's own site text, then read against Fondo's job.

| Candidate | Why flagged (its own words) | Backed |
|---|---|---|
| Kick | "Kick is the agentic ledger that does your books with you." | 2024 |
| Stacks | "Stacks brings accounting teams and AI agents into one workspace for reconciliations, close and reporting." | 2025 |
| Numos | "Numos AI agents automate accounting and FP&A: close, AP/AR, reconciliations" | 2026 |
| Puzzle | "Run your books with Puzzle's AI suite or add a Puzzle bookkeeper for expert review or a fully managed close." | 2019 |
| Collective | "company formation, tax, accounting & bookkeeping" for self-employed businesses | 2019 |

Adjacent, not flagged – they sell to accounting firms, not to startups: Accrual ("AI tax
preparation, audit, and advisory for CPA firms"), Accordance, Nace.AI, Black Ore. Also tax for
individuals, not companies: Prime Meridian, Fifteenth.

---

## Index Ventures

### Stated thesis

| Axis | Quote | URL |
|---|---|---|
| Stage | "From seed to venture to explosive growth, we work with entrepreneurs and their companies at every stage" | https://www.indexventures.com/philosophy/ |
| Stage | "Index backs companies from Seed to IPO." | https://www.indexventures.com/companies/ |
| Geography | not published (offices listed: San Francisco, New York, London) | – |
| Markets | "across every sector" | https://www.indexventures.com/philosophy/ |
| Business model | not published | – |
| Check size | not published | – |

### How the portfolio was obtained

```
  /companies/ – server-rendered list, all 332 cards on one page (sector, region, seed tags)
        ──► 332 company pages: website + links to the fund's own Perspectives posts
        ──► 344 posts fetched, publication date read  ──►  first post per company
        ──► slice = first post dated 2023-11-11 → 2026-11-11, deal announcements only ──► 66
```

- Directory: **332** companies, read to its end (the page's own structured list names the same
  332). No count published by the fund to compare.
- **Dates are the weak point.** The directory gives no investment date. The date used is the
  fund's own first post about the company. 118 companies have no dated post (undated). Of 89
  companies whose first post falls in the window, 23 were removed because the post is a
  retrospective or a follow-on, not the deal: Alan, BIT ODD (seed 2022), ClickHouse (Series A
  2021), Cohere (Series A 2021), Cradle, Dream Games (Series A 2021), Jump (seed 2021), Taktile
  (2021), Wealthfront, and 14 whose posts state no entry date (Anthropic, Chai Discovery, Common
  Room, DataSnipper, Empathy, Fireworks, GetHarley, Mirage, Mistral, Motive, Nexthink, Notion,
  Scale, ServiceTitan). **FLOOR** – the directory is complete, the dated slice is not.
- Slice: **2023-11-11 → 2026-11-11 by post date**. N = **66**.
- Stage: the round Index joined, as its own post states, for 43 of 66; 23 `unknown`.
- Retrieval note: after about 330 fast requests (10 at a time) the site answered HTTP 202 with an empty body
  and the header `x-amzn-waf-action: challenge` (a bot check). Refetched at 2 requests at a time
  with a 1-second pause; every file was then 200 and non-empty.

### Revealed thesis

| Axis | Slice of 66 |
|---|---|
| Stage | seed 20 · Series A 14 · Series B+ 9 · unknown 23 |
| Geography (regions as published) | Europe 11 · North America 4 · Asia 1 · none 50 |
| Market (top) | AI & data infrastructure 15 · **Fintech & insurance 10** · Cybersecurity 8 · Enterprise software 8 · Industrial & robotics 8 |
| Business model | B2B 58 · B2C 6 · B2G 2 |

### Fit per axis

| Axis | Revealed | Stated | Fit | Why |
|---|---|---|---|---|
| Stage | backs it – 20 seed of 43 classified (23 unclassified) | yes | match | seed named and done |
| Geography | unknown – 4 North America of 16 classified (50 unclassified) | not published | unknown | 50 of 66 rows carry no region tag, and the site states no geography |
| Market | backs it – 10 fintech of 66 classified (0 unclassified), 15.2% | yes ("every sector") | match | stated and revealed agree |
| Model | backs it – 58 B2B of 66 classified (0 unclassified) | not published | match | rests on the portfolio |

### Candidates

Full directory (332) swept by keyword on each company's own site text.

| Candidate | Why flagged (its own words) | Backed |
|---|---|---|
| Pilot | "Get expert bookkeeping, CFO, and tax services tailored for startups and small businesses." – same job, same buyer | first Index post 2021 |
| Apron | "Apron brings payments, expenses, and accounting together in one platform. Built for business owners, accountants, and finance teams." | Series B joined 2024 |

Adjacent, not flagged: Fonoa (indirect tax for e-businesses), Loctax (tax intelligence for
in-house tax teams), DataSnipper (audit for accounting firms), Taxfix (personal tax returns),
Adfin (payments and financial admin), Check and Remote (payroll).

---

## Alumni Ventures

### Stated thesis

| Axis | Quote | URL |
|---|---|---|
| Stage | "We invest in companies at all stages" … "from pre-seed to pre-IPO" | https://www.av.vc/entrepreneurs |
| Geography | "across all regions" | https://www.av.vc/entrepreneurs |
| Markets | "in (almost) all sectors" | https://www.av.vc/entrepreneurs |
| Business model | not published | – |
| Check size | "Our check size ranges from $100K to $10M with a sweet spot of $1M – $3M" | https://www.av.vc/entrepreneurs |

The fund also states it is "strictly a co-investor. We don't sit on boards or set terms."
(same page).

### How the portfolio was obtained

```
  /portfolio – Next.js page; the whole directory sits in the embedded __NEXT_DATA__ JSON
        ──► 1,773 records: name · description · website · stage tag · sector tag · geography tag
        ──► VERY LARGE: filtered to the fund's own FinTech sector tag first ──► 185
        ──► slice = logo upload year 2024–2026 ──► 68
```

- Directory: **1,773** records (1,771 distinct names – two different companies are both called
  "Haven"); the fund states "1,800+ portfolio companies" (https://www.av.vc/for-founders). The
  records carry no investment date.
- **Market filter applied first**, because the portfolio is very large: only records tagged
  FinTech were classified (185 of 1,773).
- **Date basis is a proxy.** The only date the fund's own data holds is the upload month in each
  company's logo URL (for example `…imgix.net/2024/04/…`) – when the fund's site added the
  company. 2021 is the earliest year present, so it probably means "2021 or earlier". 54 FinTech
  records have no logo date (undated).
- Slice: **2024–2026 by logo upload year**, FinTech filter. N = **68**. **FLOOR**: filtered,
  date-proxied, and below the fund's own count.
- Stage: the fund's own tag. "Seed" → seed; "Growth" and "Late" → Series B+; "Early" kept in the
  row note and not mapped (it spans Series A and later) → 21 `unknown`.

### Revealed thesis

| Axis | Slice of 68 (FinTech filter) |
|---|---|
| Stage | seed 37 · Series B+ 10 · unknown 21 |
| Geography (tags as published) | United States 52 (California 18 · New York 14 · other US regions 20) · rest 16 |
| Market | **Fintech & insurance 53** · Legal, compliance & governance 4 · Real estate & construction 4 · Consumer lifestyle & services 3 · Commerce & retail 1 · Energy, climate & agriculture 1 · Industrial & robotics 1 · Sales & marketing 1 – on a set filtered to fintech; whole directory: FinTech 185 of 1,773 |
| Business model | B2B 39 · B2C 29 |

### Fit per axis

| Axis | Revealed | Stated | Fit | Why |
|---|---|---|---|---|
| Stage | backs it – 37 seed of 47 classified (21 unclassified) | yes | match | stated and revealed agree |
| Geography | backs it – 52 United States of 68 classified (0 unclassified) | yes | match | stated and revealed agree |
| Market | backs it – 53 fintech of 68 classified (0 unclassified) | yes | match | the filter makes this axis unable to show a mismatch; the fund's own sector counts (FinTech 185 of 1,773, 10.4%) back it independently |
| Model | backs it – 39 B2B of 68 classified (0 unclassified) | not published | match | rests on the portfolio |

### Candidates

Keyword pass over **all 1,773** descriptions, not only the FinTech set – the closest candidate
is tagged AI & ML and the sector filter alone would have missed it.

| Candidate | Why flagged (the fund's directory blurb) | Added |
|---|---|---|
| Haven | "AI-powered financial platform replacing legacy accounting tools for startups and SMBs, automating over 70% of core functions like bookkeeping, taxes, and R&D credits" – same job, same buyer | 2025 |
| Puzzle | "an accounting platform that uses automation and AI to give its customers easy access to accurate, current financial data" | 2023 |
| Cynch AI | "transforming small-business tax prep with an AI-native platform" | 2025 |
| MainStreet | "helps small businesses and startups discover, apply for, and receive … tax credits" | 2021 or earlier |
| Ardius | "a research and development tax credit management platform" | undated |
| Bridger Group | "uses AI to transform small- and medium-sized accounting firms by automating repetitive tasks like data entry and transaction reconciliation" | 2025 |

Adjacent, not flagged: Accordance (copilot for accounting professionals), Central (payroll and
compliance back office for startups – no bookkeeping or tax), Jirav (planning software).

---

## Limits

- **Every list is a floor.** General Catalyst's directory holds 620 of "900+" companies; Index
  Ventures' dated slice misses 118 undated companies; Alumni Ventures was filtered to one sector
  and dated by a proxy. A fund showing no company like Fondo in the part read would still not
  mean the fund has none.
- **Stage is the thinnest axis.** No directory publishes stage at entry except Alumni Ventures'
  own tag. 148 of 199 General Catalyst rows are unclassified, so that axis reads `unknown` on the
  portfolio side; 23 of 66 Index Ventures rows are unclassified, a minority, so it is read.
- **Geography is region-level** for General Catalyst and Index Ventures; Index tags only 16 of 66
  rows, so its geography is `unknown`. More stage stories or headquarters lookups would resolve
  both `partial` results – this run did not do that work.
- **Candidates are flags, not rulings.** `/fundraise:competitors` reads
  `fondo/competitor-candidates/candidates.csv` and applies its own test to each.
- Classifications (business model, market, vertical) are own calls from each company's site or
  the fund's blurb; the row `note` holds the source.

## Sources

| What | URL | Retrieved |
|---|---|---|
| Fondo – job, product | https://fondo.com/ | 2026-11-11 |
| Fondo – pricing, buyer, model | https://fondo.com/pricing | 2026-11-11 |
| Fondo – headquarters | https://fondo.com/about | 2026-11-11 |
| Fondo – seed round | https://fondo.com/blog/fondo-announces-7m-oversubscribed | 2026-11-11 |
| Fondo – seed investors incl. Index Ventures Scout Fund | https://techcrunch.com/2024/11/22/yc-backed-fondo-raises-funding-for-its-ai-powered-bookkeeping-and-taxes-platform/ | 2026-11-11 |
| General Catalyst – stated stage | https://www.generalcatalyst.com/stories/seed-at-general-catalyst | 2026-11-11 |
| General Catalyst – strategies page (no geography, market or check size stated) | https://www.generalcatalyst.com/capital | 2026-11-11 |
| General Catalyst – "900+ portfolio companies" | https://www.generalcatalyst.com/ | 2026-11-11 |
| General Catalyst – directory (620 company pages) | https://www.generalcatalyst.com/sitemap.xml | 2026-11-11 |
| General Catalyst – company pages | https://www.generalcatalyst.com/companies/<slug> (one per row in `portfolio-general-catalyst.csv`) | 2026-11-11 |
| General Catalyst – stage per company | https://www.generalcatalyst.com/stories/<slug> (cited in each row's `note`) | 2026-11-11 |
| Index Ventures – stated stage, markets | https://www.indexventures.com/philosophy/ | 2026-11-11 |
| Index Ventures – stated stage ("Seed to IPO"), directory | https://www.indexventures.com/companies/ | 2026-11-11 |
| Index Ventures – company pages | https://www.indexventures.com/companies/<slug>/ (one per row) | 2026-11-11 |
| Index Ventures – post dates and rounds | https://www.indexventures.com/perspectives/<slug>/ (cited in each row's `note`) | 2026-11-11 |
| Alumni Ventures – stated stage, geography, markets, check size | https://www.av.vc/entrepreneurs | 2026-11-11 |
| Alumni Ventures – "1,800+ portfolio companies" | https://www.av.vc/for-founders | 2026-11-11 |
| Alumni Ventures – directory (embedded JSON, 1,773 records) | https://www.av.vc/portfolio | 2026-11-11 |
| Portfolio company one-liners | each company's own site, URL in the row's `website` | 2026-11-11 |

Raw fetches were kept in the run's `thesis-fit/raw/` folder (one folder per fund, plus `fondo/`); they are not published with this example.

Next step: `/fundraise:market-size`
