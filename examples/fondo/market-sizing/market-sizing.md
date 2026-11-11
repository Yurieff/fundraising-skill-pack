---
title: Fondo – market sizing
company: Fondo
created: 2026-11-11
author: market-size skill (fundraise plugin), v0.4
status: worked example – public sources only
tags: [market-size, fondo, bookkeeping, tax, startups, worked-example]
---

# Fondo – market sizing

## 1. Answer up front

**Fondo's market – outsourced bookkeeping and business tax for early-stage US startups that are
Delaware C-corporations – is worth about USD 129–337 million a year bottom-up, and the published
top-down cross-check lands at USD 92–214 million, 1.4–1.6× apart: converged.** The serviceable
market is USD 100–313 million, and a 5-year obtainable share of 6–12% gives a SOM of USD 6.0–37.6
million a year in 2031. The capacity build – what Fondo's delivery team and customer-acquisition
rate can carry by 2031 – comes out at USD 11.4–55.6 million a year on the funded plan (USD 6.9
million with today's team). **The capacity ceiling sits above the SOM at both ends (1.5–1.9×): the
market binds, not the company.** No market-size claim by Fondo was found to compare against.

```
   USD a year, 2031 horizon (log-ish, not to scale)

   TAM  bottom-up   ███████████████████  129m – 337m      ┐ converged
   TAM  top-down    ██████████████        92m – 214m      ┘ 1.4–1.6×
   SAM  bottom-up   █████████████████    100m – 313m
   ─────────────────────────────────────────────────────  capacity, funded plan  11.4m – 55.6m
   SOM  bottom-up   ████                   6.0m – 37.6m   ← below the ceiling at both ends
   - - - - - - - - - - - - - - - - - - - - - - - - - - -   capacity, current team  6.9m
```

## 2. How to read this note

- **Currency:** US dollars (USD), nominal. "m" = million, "bn" = billion. No conversion was needed.
- **Horizon:** SOM (serviceable obtainable market) and the capacity ceiling are both annual revenue
  in year 5, 2031, at Fondo's current business model (subscription bookkeeping and tax filing).
- **The three builds:** *bottom-up* (accounts × price – the load-bearing number), *top-down* (a
  published US industry revenue figure cut down to Fondo's slice – the sanity check), and
  *capacity* (what Fondo's own team and sales funnel can carry – never averaged with the other two).
- **Line references** like `BU8L` point to rows of `market-sizing.csv` in this folder; `L`/`H` are
  the low and high ends of a range.
- **Flags** on every number:

| Flag | Meaning |
|---|---|
| D | Disclosed – stated by the company or a primary document |
| PM | Public market – a published market or industry figure |
| OB | Operating benchmark – an industry metric standing in for undisclosed company data, named, with URL (web address) |
| E | Estimated – inferred from evidence that does not state it directly |
| A | Assumption – a judgement call with no evidence behind it |
| C | Computed – arithmetic over other rows, no evidence of its own |
| N/A | Not disclosed |

- **Abbreviations:** TAM – total addressable market; SAM – serviceable available market; SOM –
  serviceable obtainable market; ARR – annual recurring revenue; ACV – annual contract value; VC –
  venture capital; CPA – certified public accountant; R&D – research and development; SAFE – simple
  agreement for future equity; C-corporation – a US corporation taxed under Subchapter C of the
  Internal Revenue Code, the standard form for venture-backed startups; US – United States; IPO –
  initial public offering; FTE – full-time equivalent employee; SDR – sales development
  representative; SMB – small and medium-sized business; YC – Y Combinator; NVCA – National Venture
  Capital Association; NAICS – North American Industry Classification System; SAS – Service Annual
  Survey; QSS – Quarterly Services Survey; BDS – Business Dynamics Statistics; FRED – Federal Reserve
  Economic Data; NBER – National Bureau of Economic Research; IPA – INSIDE Public Accounting; Q1–Q4 –
  calendar quarters; B2B – business to business; LLC – limited liability company; SEC – Securities
  and Exchange Commission; EDGAR – Electronic Data Gathering, Analysis and Retrieval (the SEC's filing
  system); HTTP – Hypertext Transfer Protocol (403 = access refused).
- **Chart:** `tam-sam-som.png` in this folder – the same chart twice, light panel above, dark below;
  bars are low–high ranges, the aqua band is the funded-plan capacity ceiling, the dashed aqua line
  the current-team floor.

## 3. The claim

**There is no deck, and no market-size claim by Fondo was found.** Searched: fondo.com (home,
pricing, about, tax credits, bookkeeping, careers), the seed-round press release (2024-11-22), the
TechCrunch seed article (2024-11-22), the FF News pre-seed article (2023-02-24) and Fondo's YC
company page. Axios's 2023-02-13 piece is paywalled and was not read.

The closest thing to a claim is framing, not a size: TechCrunch opens with "an average of 430,000
new business applications were submitted every month" in 2024 and an expected wave of CPA
retirements. Neither is a market for Fondo's product, so there is nothing to put beside the builds
in Step 4. **An absent claim is itself the finding** – a seed company that disclosed USD 6m ARR in 2024-11 and has not
published a market size leaves investors to build it, which is what this note does.

## 4. Market boundary

**The problem:** an early-stage US startup incorporated as a Delaware C-corporation must keep
investor-grade books and file a federal corporate return (Form 1120), state returns and the
Delaware franchise tax every year, and can claim an R&D tax credit – but has no in-house finance
team to do it.

```
   CATEGORY  ✕   "the accounting services market" (USD 220bn, mostly audit, payroll, big companies)
   MARKET    ✓   "pre-seed to Series B Delaware C-corporations with no finance team,
                  buying books + corporate tax filing + R&D credit from outside"
```

Fondo's own words fix the edges: "Fondo is built specifically for Delaware C-Corp startups,
including: Pre-seed to Series B · VC-backed or bootstrapped · US and International founders"
(fondo.com/pricing). Series C+ companies (in-house controllers), LLCs, sole traders and general
SMBs are outside the boundary. TechCrunch describes Fondo as aimed at "startups and small- and
medium-sized businesses" – a wider buyer, recorded as a conflict on the company card, not used here.

## 5. Bottom-up – accounts × annual contract value

Formula (B2B subscription): **target accounts × ACV**, built for two buyer segments that Fondo's
price list itself separates ("Best for seed+ startups" vs "Best for pre-seed startups").

```
  SEGMENT 1 – VC-backed, pre-seed to Series B
    14,757 US companies raised VC in 2025 (BU1, PM)
      × 66.7%  of 2025 deals were pre-seed/seed or early VC (BU6, C)
      × 2–3    years between rounds (BU7, OB)                 → 19,680 – 29,520 companies
      × USD 5,000 – 7,938 ACV (BU9, C from D)                 → USD 98.4m – 234.3m

  SEGMENT 2 – pre-institutional Delaware C-corporations (angel, accelerator, bootstrapped)
    74,716 corporations formed in Delaware in 2025 (BU15, PM)
      × 15–30% founder-led startups (BU16, A)
      − 4,778 that raised a first VC round in 2025 (BU17, PM – already in segment 1)
      × 2 years in this state (BU18, A)                       → 12,859 – 35,274 companies
      × USD 2,400 – 2,900 ACV (BU22, C from D)                → USD 30.9m – 102.3m

  TAM, bottom-up                                              → USD 129.3m – 336.6m (BU24)
```

**Every term:**

| Term | Value | Flag | Source |
|---|---|---|---|
| US companies receiving VC, 2025 | 14,757 | PM | NVCA 2026 Yearbook (PitchBook data), "US VC Deal Flow" table |
| 2025 deals by stage: pre-seed/seed, early, later, growth | 5,049 · 5,165 · 4,167 · 937 | PM | Same yearbook, "US VC Deal Flow by Stage" |
| Years between rounds | 2.0 – 3.0 | OB | Carta data via SaaStr, 2025-11-04: in Q3 2025 23% of companies raised a Series A within 1.5–2 years and 39% took 3+ years |
| Active VC-backed accounts | 19,680 – 29,520 | C | companies financed a year × years between rounds (a steady-state stock) |
| ACV low: Fondo's realised average | USD 5,000 | C | USD 6m ARR ÷ ~1,200 customers (TechCrunch and Fondo press release, 2024-11-22, both D) |
| ACV high: monthly books + TaxPass at list | USD 7,938 | C | USD 499 × 12 + USD 1,950 (fondo.com/pricing, list prices struck through beside offer prices of USD 399 and USD 1,450, D) |
| Delaware corporations formed, 2025 | 74,716 | PM | Delaware Division of Corporations 2025 Annual Report (2024: 58,313) |
| Founder-led startup share of those | 15% – 30% | A | no public split exists; the largest single assumption in this build |
| First VC rounds, 2025 | 4,778 | PM | NVCA 2026 Yearbook, "US First VC & Follow on VC Deal Flow" |
| Years as a pre-institutional C-corporation | 2 | A | judgement call |
| ACV, pre-seed plan | USD 2,400 – 2,900 | C | annual books USD 950 + TaxPass USD 1,450 (offer) or USD 1,950 (list), fondo.com/pricing |

**A count is not a list.** Neither population is enumerated anywhere public: segment 1 is a
steady-state estimate from annual deal counts, segment 2 is an assumption-weighted share of
Delaware formations. Carta's pre-seed reports, which count SAFE rounds directly, returned
HTTP 403 to every fetch and are not used. The ACV excludes the R&D credit study and add-ons, whose
prices Fondo does not publish ("Pricing varies").

## 6. Top-down – from the published US figure down

```
  USD 198.9bn  US revenue, NAICS 5412 accounting, tax preparation, bookkeeping
               and payroll services, 2022 (TD1, PM – Census SAS)
      ↓ brought to 2025 with the Census QSS: sum of 2025 quarters        (TD10, C)
  USD 219.9bn
      ↓ × 23.9%  the part of the job Fondo bills for                      (TD5, C)
               bookkeeping 9.2bn + business tax prep 30.6bn + tax planning 7.8bn
               of 198.9bn; drops audit 42.4bn, payroll 29.0bn, individual tax, other
  USD 52.6bn   (TD11)
      ↓ × 100%   geography – the Census figure is US-only, Fondo files US returns (TD12, E)
      ↓ × 1.16%  young (0–5 year) firms in Information (51) and Professional,
               scientific and technical services (54): their share of US employer-firm
               employment, 1,595,259 of 137,462,444 jobs, 2023 (TD19, C from BDS, PM)
      ↓ × 1.0    spend assumed proportional to employment (TD20, A)
  USD 610m
      ↓ × 15–35% venture-track share of that young-firm employment        (TD21, A)
  USD 91.6m – 213.7m  ← TAM, top-down (TD22)
```

**Rationale for each cut.** The billed-slice cut is the one that matters most and is fully
sourced: three-quarters of the industry's revenue is audit, payroll processing, individual returns
and consulting that Fondo never sells. The segment cut is the weak one. No public data splits
accounting spend by client type, so the note uses employment at young firms in the two sectors
where software and tech startups sit as the proxy, then assumes a venture-track share. Context for
that share: VC-financed firms were only 0.1–0.2% of new US firms in 1981–2001 but grew far larger
than average (Puri and Zarutskie, NBER working paper 14250), so their share of young-firm
*employment* is much higher than their share of young-firm *count*.

Treat this figure as **directional**: it is a government survey, not an aggregator report, but two
of its five cuts are assumptions. The bottom-up shares no input with it except, loosely, the
definition of "startup".

## 7. Triangulation

| | Low | High | Midpoint |
|---|---|---|---|
| Bottom-up TAM | USD 129.3m | USD 336.6m | USD 232.9m |
| Top-down TAM | USD 91.6m | USD 213.7m | USD 152.6m |
| Bottom-up ÷ top-down | 1.41× (TR1) | 1.58× (TR2) | 1.53× (TR3) |

**Converged – within 2× at every point of the range.** Bottom-up runs higher, for a reason worth
naming: the top-down allocates spend by employment, and accounting fees have a fixed floor – a
two-person C-corporation still files a full Form 1120 and a Delaware franchise return – so the
youngest, smallest firms spend more per head than the proportional assumption allows (TD20 = 1.0
is conservative). **Bottom-up is the load-bearing number**; TAM is reported as **USD 129–337m**,
with the top-down as the check that it is not an order of magnitude off.

## 8. TAM → SAM → SOM

```
   TAM   USD 129.3m – 336.6m   pre-seed to Series B US startups, all states
    │    ↓ keep Delaware C-corporations only (Fondo's stated plan):
    │      VC-backed segment × 70–90% (BU25: 70% E from "Nearly 70% U.S. IPOs" choosing
    │      Delaware; 90% A); pre-institutional segment is Delaware by construction
   SAM   USD 99.7m – 313.2m    26,635 – 61,841 accounts (BU30)
    │    ↓ × 6–12% share of SAM, won within 5 years (BU27, A)
   SOM   USD 6.0m – 37.6m      annual revenue in 2031, subscription bookkeeping + tax filing
```

- **Share assumption (A):** 6–12% of SAM. For scale: Fondo's site and YC page say "2,000+
  startups" (D, possibly cumulative rather than active), which is 3.2–7.5% of SAM accounts today
  (BU31, C) – but a count share, at a blended price below the high-end ACV. 6% is roughly holding
  today's top-end share; 12% is roughly doubling it against Pilot, Puzzle, Kruze, Digits, Haven and
  local CPA firms.
- **Horizon:** 5 years, to 2031.
- **Business model:** the one Fondo runs today – subscription bookkeeping (monthly, quarterly or
  annual close) plus annual tax filing and an R&D credit study. Nothing public says the model
  changes inside the window, so it is sized as is.

## 9. Capacity ceiling – what Fondo's machine can carry by 2031

**Motion.** Fondo is **OPS-DELIVERED** (operations-delivered: revenue gated by the throughput of
its accounting team) – "a CPA-led team who takes full ownership of your
bookkeeping, corporate taxes, and R&D tax credits" (fondo.com) – fed by a self-serve sign-up and a
small sales team (Account Executive and SDR roles open on the YC page). The two are gates in series,
not parallel motions: a customer must be won, then served. The ceiling is the **lower** of the two.

```
  DELIVERY GATE   heads × ARR per head
                  80 heads today (CP1, D)
                    × (1 + 10.7%)^5 observed ramp  → 133 heads   (CP10L, C)
                    × (1 + 30%)^5  accelerated     → 297 heads   (CP10H, C/A)
                  × USD 85,714 per head today (CP4, C) … USD 256,000 benchmark (CP11H, OB)
                  → USD 11.4m (CP12L)  …  USD 76.0m (CP12H)

  ACQUISITION GATE  customers in 2031 × ACV
                  2,000 today + 5 × 406 a year observed   → 4,032  (CP16L, C)
                  2,000 today + 5 × 1,000 a year assumed  → 7,000  (CP16H, A)
                  × USD 5,000 … 7,938
                  → USD 20.2m (CP17L)  …  USD 55.6m (CP17H)

  CEILING = lower gate     low: delivery binds   USD 11.4m
                           high: acquisition binds USD 55.6m
```

| Input | Value | Flag | Source |
|---|---|---|---|
| Headcount 2026 | 80 | D | YC company page, "Team Size: 80" (company-maintained; last update date unknown); about page "70+ professionals" |
| Headcount 2024-11 | ~70 | D | TechCrunch 2024-11-22 |
| Headcount end of 2022, ARR end of 2022 | 54; USD 3m | D | FF News 2023-02-24: "doubling its team to 54 people and nearly tripling its annual recurring revenue to $3MM" |
| ARR per head 2022 → 2024 | USD 55,556 → 85,714 | C | ARR ÷ headcount, both years disclosed |
| Observed headcount growth | 10.7% a year | C | 54 → 80 over 3.86 years |
| Accelerated headcount growth | 30% a year | A | no round is publicly being raised; a judgement call for a funded hiring push |
| Benchmark revenue per FTE | USD 256,000 | OB | IPA "Top 500 Firms" deck, 2025: tax-specialist firms; Fondo's own 2022–2024 productivity trend, run five more years, lands near this |
| Net customer additions | 406 a year | C | 1,200 (2024-11-22, D) → 2,000+ (2026-11-11, D) |
| Accelerated additions | 1,000 a year | A | judgement call, ~2.5× observed |

**Funded plan vs current team – reported separately, never blended:**

| | 2031 annual revenue capacity | Role |
|---|---|---|
| **Funded-plan ceiling** | **USD 11.4m – 55.6m** (CP18) | the load-bearing number |
| Current-team ceiling | USD 6.9m (CP8): 80 heads × USD 85,714, no hiring, no productivity gain | the floor |

"Funded plan" needs a caveat: **no round being raised is stated** (company card), the last round
was the USD 7 million seed of 2024-11-22 – "$4.6 million in equity and a $2.4 million debt facility secured from Capchase" (seed release, source 4) – and Fondo reported being profitable at the seed round (TechCrunch and the seed release, 2024-11-22). So the plan
is built from Fondo's own observed ramp (low) and an assumed accelerated ramp (high), not from a
disclosed use of proceeds.

**Which constraint binds.**

```
   SOM 2031           USD 6.0m ────────────────── 37.6m
   Capacity 2031           USD 11.4m ───────────────────── 55.6m
   Capacity ÷ SOM          1.91× at the low ends (CP19L) · 1.48× at the high ends (CP19H)
```

**The capacity ceiling is above the SOM at both ends: THE MARKET BINDS.** Fondo's machine – even
at its observed hiring pace – can carry more revenue than a 6–12% share of its serviceable market
supplies. The finding is not that the market is large; it is that **the market Fondo has chosen is
narrow** – roughly 27,000–62,000 Delaware C-corporation startups at USD 2,400–7,938 a year – and the
company would outgrow its 5-year share of it before it ran out of people. The break-even share at
which the company would bind instead is 11.4–17.7% of SAM (CP20); below that, sizing was the right
question and Section 8 answered it. The gap is a strategy finding (widen the boundary – SMBs, Series
B+, higher-price services – or raise the price per account), not a hiring finding.

## 10. Limits

**What would move the number most:**

1. **The founder-led share of Delaware formations (BU16, A, 15–30%).** It alone swings the
   pre-institutional segment from USD 30.9m to USD 102.3m – the widest single range in the TAM.
   A published split of Delaware incorporations by purpose, or Carta's SAFE company counts (403 to
   every fetch in this run), would replace it with evidence.
2. **The SOM share (BU27, A).** The market-binds conclusion holds only while the 5-year share stays
   below 11.4–17.7% of SAM (CP20). A share above that flips the binding constraint to the company.
3. **The boundary.** TechCrunch describes Fondo as also serving SMBs. If the plan includes general
   SMBs, the TAM is a different, much larger market and this note sizes only its core.
4. **Price per account.** The ACV excludes the R&D credit study and add-on filings, whose prices are
   not published. If they lift the average well above USD 7,938, every demand number rises
   proportionally – and so does the acquisition gate.

**What could not be verified:**

- Whether "2,000+ startups" counts active customers or every startup ever served.
- When the YC page's "Team Size: 80" was last updated, and how the 80 split between delivery,
  sales and engineering.
- Any revenue figure after 2024-11 – none has been published, and none is estimated here.
- The 30% accelerated hiring ramp and the 1,000-a-year acquisition rate – both are assumptions.
- The top-down's employment proxy and venture-track share (TD20, TD21) – both are assumptions.
- Registry: no SEC EDGAR Form D filing was found under Fondo's
  legal name, BloomJoy, Inc. (site footer), so no filing confirms the round amounts.

## 11. Sources

| # | Source | Used for | URL |
|---|---|---|---|
| 1 | Fondo pricing page, retrieved 2026-11-11 | prices, buyer definition | https://fondo.com/pricing |
| 2 | Fondo home page and footer, retrieved 2026-11-11 | job statement, "2,000+ startups" | https://fondo.com/ |
| 3 | Fondo about page, retrieved 2026-11-11 | "70+ professionals", milestones | https://fondo.com/about |
| 4 | Fondo seed press release, dated 2024-11-22 | ARR, customers, round terms | https://fondo.com/blog/fondo-announces-7m-oversubscribed |
| 5 | TechCrunch, 2024-11-22 | ARR, customers, ~70 employees, SMB framing | https://techcrunch.com/2024/11/22/yc-backed-fondo-raises-funding-for-its-ai-powered-bookkeeping-and-taxes-platform/ |
| 6 | FF News, 2023-02-24 | 2022 headcount and ARR | https://ffnews.com/newsarticle/fondo-receives-3mm-in-pre-seed-funding-to-assist-startups-with-taxes/ |
| 7 | YC company page, retrieved 2026-11-11 | team size 80, open sales roles | https://www.ycombinator.com/companies/fondo |
| 8 | NVCA 2026 Yearbook (PitchBook data) | VC company and deal counts, 2025 | https://nvca.org/wp-content/uploads/2026/04/2026-YB-Public-PDF.pdf |
| 9 | SaaStr, 2025-11-04, citing Carta | years between rounds | https://www.saastr.com/your-seed-round-now-needs-to-last-3-years-what-3365-startups-tell-us-about-the-new-series-a-timeline/ |
| 10 | Delaware Division of Corporations, 2025 Annual Report | corporations formed; IPO share | https://corpfiles.delaware.gov/Annual-Reports/Division-of-Corporations-2025-Annual-Report.pdf |
| 11 | U.S. Census Bureau SAS 2022, NAICS 5412 total, via FRED | top-down base | https://fred.stlouisfed.org/data/ATPBAPSRAEE45412 |
| 12 | Same, bookkeeping product line | billed slice | https://fred.stlouisfed.org/data/REVBCCEF5412ALLEST |
| 13 | Same, business tax preparation product line | billed slice | https://fred.stlouisfed.org/data/REVTPOEF5412ALLEST |
| 14 | Same, tax planning product line | billed slice | https://fred.stlouisfed.org/data/REVTPCEF5412ALLEST |
| 15 | U.S. Census Bureau QSS, NAICS 5412, via FRED | 2025 level | https://fred.stlouisfed.org/data/REV5412TAXABL144QNSA |
| 16 | U.S. Census Bureau BDS 2023, economy-wide | total employment | https://www2.census.gov/programs-surveys/bds/tables/time-series/2023/bds2023.csv |
| 17 | U.S. Census Bureau BDS 2023, sector by firm age | young-firm employment | https://www2.census.gov/programs-surveys/bds/tables/time-series/2023/bds2023_sec_fac.csv |
| 18 | Puri and Zarutskie, NBER working paper 14250 | context for the venture-track share | https://www.nber.org/papers/w14250.pdf |
| 19 | INSIDE Public Accounting, "The Top 500 Firms" deck, 2025-10 | revenue per FTE benchmark | https://cpatrendlines.com/wp-content/uploads/2025/10/The-Top-500-Firms-INSIDE-Public-Accounting-Webinar-with-Chelsea-Summers-for-CPA-Trendlines.pdf |
| 20 | SEC EDGAR company search | registry check (no Form D found) | https://www.sec.gov/cgi-bin/browse-edgar?company=BloomJoy&type=D |

Not used, with reason: Carta data pages (HTTP 403 to curl and to the fetch tool); Axios 2023-02-13
(paywall, HTTP 403); Census API (application programming interface; now requires a key – the same series were read through FRED);
Stripe's 2025 annual letter (the Atlas share of Delaware incorporations reported in search results
was not in the fetched text). Every fetched page was saved verbatim in the run's `raw/` folder, indexed in
`raw/fetch-log.md`; the fetched pages are not published with this example.

*This note is a research artifact, not an investment recommendation.*
