---
title: Readiness check – Fondo (worked example, public sources only)
company: Fondo
created: 2026-11-11
author: readiness-check v0.1 (Claude Code)
status: draft
tags: [readiness-check, fondo, worked-example, no-deck]
---

# Readiness check – Fondo

> **Worked example.** Fondo did not take part and has not reviewed this note. There is no deck
> and no covering email: the claims come from Fondo's own website. The three funds are the ones
> this example ran `thesis-fit` against; Fondo named no funds and states no round. Research, not
> investment advice.

## In plain English

This is the first read a fund's analyst gives a startup's materials – done here before any fund
does it. It lists the points a fund may stop on, what the evidence says about each, and how to
fix it. It is not advice on whether to invest, and it gives no verdict on the company. Fondo has
no public deck, so the check read Fondo's website instead; two of the six checks could not run
because they need a deck or the company's own revenue data, and the note names what would fill
each.

## Answer up front

Four points are **high** (funds chosen for this example), all of the same kind – a fund in the list already backs a company that
`/fundraise:competitors` ruled a direct competitor:

- **D02** – General Catalyst backs **Puzzle** (direct).
- **D03** – Index Ventures backs **Pilot** (direct), the rival Fondo's own pricing page compares
  itself to.
- **D04** – Alumni Ventures backs **Haven** (direct), the closest look-alike.
- **D05** – Alumni Ventures also backs **Puzzle** (direct).

One point is **medium**: the website's comparison table names one rival (Pilot) where the
competitor set holds 22 direct competitors (D01). Seven are **low**: six fund-portfolio companies
ruled indirect (D06–D11) and one card conflict on who pays (D12). On two fund axes `thesis-fit`
could not tell whether Fondo fits (General Catalyst on stage, Index Ventures on geography) – a gap
in the funds' own data, listed under Limits, not raised as a doubt.

| Check | Status | High | Medium | Low | What fills it |
|---|---|---|---|---|---|
| C1 Consistency | **skipped** – needs a deck or a covering email to compare with the site | – | – | – | a deck or covering email, then `/fundraise:readiness-check` again |
| C2 Revenue story | **skipped** – no `metrics-pack/` output (card: "Metrics available: none") | – | – | – | `/fundraise:metrics-pack` |
| C3 Market claim | run – no claim to test (no market-size figure on the site or in press) | 0 | 0 | 0 | – |
| C4 Competitors | run – the website's comparison table against `competitors.csv` | 0 | 1 | 0 | – |
| C5 Fund list | run – fit (two axes "thesis-fit could not tell", no point) and portfolio conflicts against `competitors.csv` | 4 | 0 | 6 | – |
| C6 Card conflicts | run – one row in `## Conflicts` at start | 0 | 0 | 1 | – |

## How to read this

- **A point** = a claim the company makes, the evidence that bears on it, why a fund may doubt
  it, how to fix it, and a severity. Every point gives the claim's source (here a web page, a
  card field, or the fund list) and the evidence's source (page, file and row).
- **Severity** says how likely a fund's analyst is to stop on the point, not how good the company
  is. If two rules apply, the higher one wins.

```
  HIGH    the evidence contradicts the claim: the same number, for the same thing and
          period, differs by more than 10% between two places; an absolute claim that a
          source the fund can read refutes, or that an earlier skill says cannot be
          computed – including "no (direct) competitors" against a same-job, same-buyer
          candidate in a target fund's own portfolio; a contracted (not yet billed) month
          stated as current revenue; a target fund read as "no match" on an axis; a
          confirmed direct competitor in a target fund's portfolio
  MEDIUM  the claim cannot be checked, or the evidence against it is unconfirmed: a market
          figure with no source; a claim contradicted only by unconfirmed candidates (except
          the "no competitors" case above); a target fund whose fit is "partial" on
          classified evidence; billed and contracted months blended without labels; a
          "why it is interesting" line with no revenue mechanism; a card conflict on a
          field funds screen on; a competitor list that omits direct competitors
  LOW     presentation: rounding within 10%; a missing date, unit or caveat that does not
          change the number; a card conflict on a descriptive field; a target fund that
          backs an indirect competitor
  NOT A POINT  a fund axis thesis-fit could not tell (too much of the fund's directory
          unclassified) – listed under Limits
```

- **Run / partial / skipped.** A check runs when its inputs exist; it is partial when only part
  of them exist, and says what it used; it is skipped when they are missing, and names what
  would fill it. Skipped is not "no problem found".
- **Direct / indirect** are `/fundraise:competitors`' rulings: direct = passes all three legs of
  its test – L1 keeps the books, L2 files the US federal corporate return (Form 1120), L3 files the
  research and development credit (Form 6765) – each quoted from the operator's own site; indirect = fails one or more of those but
  contests the same customer. **Candidate** = a fund's portfolio company that `thesis-fit` flagged
  as possibly competing with Fondo; every candidate here has been ruled on.
- **No score.** The table above counts points per severity; there is no total, no grade, and no
  overall label.
- **Abbreviations.** AI = artificial intelligence · ARR = annual recurring revenue · CFO = chief
  financial officer · CPA = certified public accountant · CSV = comma-separated values · ISO = the
  international date format (YYYY-MM-DD) · MRR = monthly recurring revenue · NRR = net revenue
  retention · R&D = research and development · SAM = serviceable available market · SMB = small
  and medium-sized business · SOM = serviceable obtainable market · TAM = total addressable
  market · URL = web address · US = United States · USD = United States dollar · YC = Y
  Combinator. Dates are ISO.

## Materials read

- **Deck:** none – no deck is public. The claims come from the website, as the skill directs.
- **Covering email:** not given.
- **Website:** https://fondo.com/, https://fondo.com/pricing and https://fondo.com/about, fetched
  2026-11-11 (each page served in full), saved to the run's `readiness-check/raw/` folder (not
  published with this example). Fondo's own words below are quoted
  as fetched.

| Page | Claim (verbatim) | Tested by |
|---|---|---|
| https://fondo.com/ | "Set up in minutes and put accounting on autopilot with a CPA-led team who takes full ownership of your bookkeeping, corporate taxes, and R&D tax credits." | card, Job done for the customer – same words, no point |
| https://fondo.com/ (footer of every page) | "Built for Delaware C-Corps. Trusted by 2,000+ startups." | C1 – skipped |
| https://fondo.com/ | "We've helped thousands of startups save $100M+"; "Since 2019"; "$8B + Transactions Categorized" | C1 – skipped |
| https://fondo.com/pricing | "Fondo compared to the alternatives" – "A modern accounting platform vs. legacy approaches."; columns "Pilot" and "CPA/Accounting Firm" | C4 – D01 |
| https://fondo.com/pricing | "Monthly Plan $499 $399 /month"; "Quarterly Plan $1,198 /quarter"; "Annual Plan $950 /year"; "TaxPass" "Limited time offer" "$1,950 $1,450 /year" | card, Who pays and Revenue model – consistent, no point |
| https://fondo.com/pricing | "Fondo is built specifically for Delaware C-Corp startups, including:" "Pre-seed to Series B" | card, Who pays – consistent; used in the fix to D12 |
| https://fondo.com/about | "Fondo is a group of growing group of 70+ professionals supporting founders every day." | C1 – skipped |
| https://fondo.com/about | "2023" "1,000+ startups trust Fondo" | C1 – skipped |
| https://fondo.com/about | "We started Fondo as a small team in San Francisco" | card, Geography – consistent, no point |
| all three pages | no market-size figure, no revenue figure, no round being raised, no fund named | C3 – no claim to test; C2 – skipped; C5 – fund list from `funds.csv` |

## Inputs

| Input | Path | Present | Used by |
|---|---|---|---|
| Deck | `fondo/deck/` | **missing** – no public deck | C1 skipped |
| Covering email | – | not given | C1 skipped |
| Website | https://fondo.com/ (home, pricing, about) | yes, 3 pages fetched | the claims; C4 |
| Company card | `fondo/company-profile.md` | yes; `## Conflicts` has 1 row at start | all; C6 |
| Thesis fit | `fondo/thesis-fit/funds.csv` | yes, 3 funds | C5 |
| Market sizing | `fondo/market-sizing/market-sizing.csv` | yes, 101 rows | C3 |
| Competitors | `fondo/competitor-research/competitors.csv` | yes, 61 rows (22 direct, 26 indirect, 13 unverified) | C4, C5 |
| Candidates | `fondo/competitor-candidates/candidates.csv` | yes, 13 rows | C5 |
| Metrics | `fondo/metrics-pack/mrr.csv`, `nrr.csv` | **missing** (card: "Metrics available: none"; no public Fondo metrics) | C2 skipped |

The card was read first. The website states no value for an empty card field ("Round being
raised" stays "not stated", "Metrics available" stays "none") and no value that differs from a
filled one, so this run added no Conflicts row and left the card unchanged.

## Points

### C1 – Consistency

Skipped – see "Skipped and partial checks".

### C2 – Revenue story

Skipped – see "Skipped and partial checks".

### C3 – Market claim

Runs, **no claim to test.** `market-sizing.csv` row CL1 records that no market-size figure was
found on fondo.com (home, pricing, about, tax-credits, bookkeeping), in the seed press release,
TechCrunch 2024-11-22 or the YC page; the three pages read in this run state none either. Had a
deck stated a TAM, it would be compared with the two demand builds – bottom-up USD 129.3m–336.6m,
top-down USD 91.6m–213.7m a year (rows BU24L/H, TD22L/H) – and a stated SOM or revenue target
with the 2031 ceilings: current-team floor USD 6.9m (CP8), funded-plan ceiling USD 11.4m–55.6m
(CP18L/H).

### C4 – Competitors

**D01 – medium.** Claim: "Fondo compared to the alternatives" – "A modern accounting platform vs.
legacy approaches." The table's columns name two alternatives: "Pilot" and "CPA/Accounting Firm"
(https://fondo.com/pricing, retrieved 2026-11-11). Evidence: `competitors.csv` holds **22 direct
competitors** (13 material, 7 minor, 2 micro; a floor), each passing the same three-job test on its
own site. Material direct rows besides Pilot: Zeni, Haven, Every, Puzzle, Kruze Consulting, Burkland
Associates, inDinero, Bookkeeper360, Graphite Financial, Aprio, Escalon, Rivet. The generic
"CPA/Accounting Firm" column can stand for the firm-type rows; the startup-specialist platforms
**Haven, Zeni, Every and Puzzle** are not named. *Why a fund may doubt it:* a fund's analyst builds
the competitor map from the same public pages; a comparison that names one rival reads as a
narrower map than the one the analyst finds, and Haven's own blog ranks Haven as a Fondo
alternative (https://www.usehaven.com/blog-posts/the-4-best-fondo-alternatives-for-startups).
*Fix:* on any competitor slide, name the material direct competitors – at least Pilot, Haven,
Zeni, Puzzle and Every – and say how Fondo differs (the competitor note's public-evidence
differences: quarterly and annual close options, a tax package priced below Pilot and Zeni at
list, Delaware franchise tax included). Re-run `/fundraise:competitors` if the set changes.

The website calls no `indirect` row direct, or the reverse.

### C5 – Fund list

**Target funds:** Fondo named no funds and states no round, so the list is the three funds in
`thesis-fit/funds.csv` – General Catalyst, Index Ventures, Alumni Ventures – chosen for this worked
example, as the skill directs when no list is given. Fit: General Catalyst partial, Index Ventures
partial, Alumni Ventures match.

| Fund | Axis not "match" | Counts and reading (quoted from `funds.csv`'s `note`) | Result |
|---|---|---|---|
| General Catalyst | stage – partial | "stage: 26 of 51 classified (148 unclassified) → unknown → partial" | thesis-fit could not tell – no point (Limits) |
| Index Ventures | geography – unknown | "geography: 4 of 16 classified (50 unclassified) → unknown → unknown" | thesis-fit could not tell – no point (Limits) |
| Alumni Ventures | none | all four axes "match" | no fit point |

No fit point: no axis is "no match", and no "partial" rests on classified evidence.

**Portfolio conflicts**, each fund's candidates looked up in `competitors.csv`:

| Candidate | Fund | `competitors.csv` ruling | Point |
|---|---|---|---|
| Puzzle | General Catalyst | direct, material | D02 – high |
| Pilot | Index Ventures | direct, material | D03 – high |
| Haven | Alumni Ventures | direct, material | D04 – high |
| Puzzle | Alumni Ventures | direct, material | D05 – high |
| Kick | General Catalyst | indirect, material | D06 – low |
| Collective | General Catalyst | indirect, material | D07 – low |
| Cynch AI | Alumni Ventures | indirect, minor | D08 – low |
| MainStreet | Alumni Ventures | indirect, material; absorbed (acquired by Employer.com, 2025-05-05) | D09 – low |
| Ardius | Alumni Ventures | indirect, material; absorbed (acquired by Gusto, 2021-06-17) | D10 – low |
| Bridger Group | Alumni Ventures | indirect, minor | D11 – low |
| Stacks | General Catalyst | not in `competitors.csv`: ruled **excluded** in the competitor note's Method – "fails L1, L2, L3 (close software for enterprise accounting teams; different buyer)" | no point (Limits) |
| Numos | General Catalyst | excluded – "fails L1, L2, L3 (agent software for finance departments; different buyer)" | no point (Limits) |
| Apron | Index Ventures | excluded – "fails L1, L2, L3 (payments and bill-pay platform)" | no point (Limits) |

**D02 – high.** Claim: General Catalyst as a target fund (`thesis-fit/funds.csv`). Evidence:
General Catalyst backs Puzzle – "Run your books with Puzzle's AI suite or add a Puzzle bookkeeper
for expert review or a fully managed close." (`candidates.csv`, Puzzle / General Catalyst;
https://www.generalcatalyst.com/companies/puzzle). `competitors.csv` rules Puzzle direct, material
(bookkeeping; business tax return through a partner accounting firm; research and development
credit study). Its accounting-firm technology and business is being sold to Accrual (announced
2026-09-02, terms not disclosed). *Why:* the fund already backs a confirmed direct competitor; its
partners know that company's numbers and may ask how Fondo differs, or hold back for the conflict.
*Fix:* name Puzzle on the competitor slide and state how Fondo differs; be ready for the
portfolio-conflict question. If the sale to Accrual changes Puzzle's offer, re-run
`/fundraise:competitors`.

**D03 – high.** Claim: Index Ventures as a target fund (`thesis-fit/funds.csv`). Evidence: Index
Ventures backs Pilot – "Get expert bookkeeping, CFO, and tax services tailored for startups and
small businesses." (`candidates.csv`, Pilot / Index Ventures;
https://www.indexventures.com/companies/pilot/). `competitors.csv` rules Pilot direct, material:
same three jobs, same buyer, more than USD 158 million raised (reported 2021-03-27). Separately,
press coverage of Fondo's seed round lists an "Index Ventures Scout Fund" among its investors
(TechCrunch, 2024-11-22, recorded in `thesis-fit.md`); a scout fund is a separate vehicle, and
Fondo does not appear in Index Ventures' directory. *Why:* the fund already backs the
best-capitalised direct competitor, the one Fondo's own pricing page compares itself to; its
partners may ask how Fondo differs, or hold back for the conflict. *Fix:* state how Fondo differs
from Pilot on the competitor slide, with prices from the competitor note; be ready for the
portfolio-conflict question, and say plainly how the scout-fund investment relates to the main
fund if asked.

**D04 – high.** Claim: Alumni Ventures as a target fund (`thesis-fit/funds.csv`). Evidence: Alumni
Ventures backs Haven – "AI-powered financial platform replacing legacy accounting tools for
startups and SMBs, automating over 70% of core functions like bookkeeping, taxes, and R&D
credits" (fund's directory blurb; `candidates.csv`, Haven / Alumni Ventures;
https://www.av.vc/portfolio). `competitors.csv` rules Haven direct, material: same three jobs, same
buyer; its funding beyond an undisclosed pre-seed could not be tied to the entity. *Why:* the fund
already backs the closest look-alike to Fondo; it may ask how Fondo differs, or hold back for the
conflict. *Fix:* name Haven on the competitor slide and state how Fondo differs; be ready for the
portfolio-conflict question.

**D05 – high.** Claim: Alumni Ventures as a target fund (`thesis-fit/funds.csv`). Evidence: Alumni
Ventures also backs Puzzle – "Puzzle is an accounting platform that uses automation and AI to give
its customers easy access to accurate, current financial data" (fund's directory blurb;
`candidates.csv`, Puzzle / Alumni Ventures; https://www.av.vc/portfolio). `competitors.csv` rules
Puzzle direct, material. *Why:* a second confirmed direct competitor in the same fund's portfolio,
next to Haven. *Fix:* as for D02 and D04 – name Puzzle, state how Fondo differs, be ready for the
portfolio-conflict question.

**D06 – low.** General Catalyst backs Kick – "Kick is the agentic ledger that does your books with
you." (`candidates.csv`; https://www.generalcatalyst.com/companies/kick); ruled indirect, material
(accounting software; none of the three legs on its own site). *Why:* the fund backs software in an
adjacent part of Fondo's job and may ask where the two overlap. *Fix:* be ready to say where Fondo
and Kick overlap and where they do not; no change to the materials unless a deck names Kick.

**D07 – low.** General Catalyst backs Collective – "company formation, tax, accounting &
bookkeeping" for self-employed businesses (`candidates.csv`;
https://www.generalcatalyst.com/companies/collective); ruled indirect, material (bookkeeping only;
its tax work is for S corporation solo owners). *Why:* a bookkeeping and tax service for a
different buyer; the fund may ask where the two overlap. *Fix:* be ready to say why a Delaware
C-corporation startup and a solo S corporation owner are different buyers.

**D08 – low.** Alumni Ventures backs Cynch AI – "Cynch is transforming small-business tax prep with
an AI-native platform" (fund's directory blurb; `candidates.csv`; https://www.av.vc/portfolio);
ruled indirect, minor (bookkeeping on its own site; a C-corporation return not evidenced; no
research and development credit). *Why:* the fund backs a small-business tax and bookkeeping
company and may ask where the two overlap. *Fix:* be ready to say where Fondo and Cynch AI overlap.

**D09 – low.** Alumni Ventures backs MainStreet – "helps small businesses and startups discover,
apply for, and receive government stimulus funds, hiring incentives, and tax credits" (fund's
directory blurb; `candidates.csv`; https://www.av.vc/portfolio); ruled indirect, material (tax
credits only), absorbed: acquired by Employer.com, 2025-05-05. *Why:* the fund's portfolio held a
startup tax-credit company, now part of an acquirer; the fund may ask about the tax-credit line.
*Fix:* be ready to say how Fondo's tax-credit service compares.

**D10 – low.** Alumni Ventures backs Ardius – "a research and development tax credit management
platform" (fund's directory blurb; `candidates.csv`; https://www.av.vc/portfolio); ruled indirect,
material (research and development credit only), absorbed: acquired by Gusto, 2021-06-17. *Why:*
the credit product now sits inside Gusto's payroll offer; the fund may ask about the tax-credit
line. *Fix:* be ready to say how Fondo's credit service compares with a payroll provider's.

**D11 – low.** Alumni Ventures backs Bridger Group – "uses AI to transform small- and medium-sized
accounting firms by automating repetitive tasks like data entry and transaction reconciliation"
(fund's directory blurb; `candidates.csv`; https://www.av.vc/portfolio); ruled indirect, minor
(bookkeeping through owned accounting firms; no business return or credit on the pages read).
*Why:* the fund backs a group of accounting firms that keeps small businesses' books; it may ask
where the two overlap. *Fix:* be ready to say where Fondo and Bridger Group overlap.

### C6 – Card conflicts

`## Conflicts` held one row when this run started (added by `market-size`, 2026-11-11).

**D12 – low.** Claim: card field Who pays – "Startups and scaling tech companies – mainly US
Delaware C-corporations – paying for bookkeeping, corporate tax filing and tax-credit studies"
(`company-profile.md`; card source https://fondo.com/pricing, retrieved 2026-11-11). Evidence: "a
bookkeeping platform aimed at startups and small- and medium-sized businesses" – a wider buyer
(https://techcrunch.com/2024/11/22/yc-backed-fondo-raises-funding-for-its-ai-powered-bookkeeping-and-taxes-platform/,
2024-11-22). Who pays is a descriptive field, so low. *Why:* a fund that reads the press piece next
to the site sees two buyers – Delaware C-corporation startups, or small businesses in general – and
the buyer definition sets the market size a fund will test. *Fix:* state the buyer in one sentence
in every material – the pricing page's own words are "built specifically for Delaware C-Corp
startups", "Pre-seed to Series B" – and keep the card's value, which comes from the company's own
page. If the buyer is wider, re-run `/fundraise:market-size`.

## Skipped and partial checks

| Check | What is missing | What was done with what exists | Fills it | The claim it would test |
|---|---|---|---|---|
| C1 Consistency | a deck or a covering email – the skill compares them with the site; the site alone has nothing to be compared with | the site's claims were read and listed under Materials read; nothing was compared. For a deck, the earlier outputs already record public figures it would be read against: the site's "Trusted by 2,000+ startups" next to "about 1,200 customers" and USD 6 million ARR in TechCrunch, 2024-11-22 (`market-sizing.md`); the about page's "Served our first startup" in 2019 next to a founding year of 2020 in a 2023 company release (`competitor-report.md`) | a deck or covering email, then `/fundraise:readiness-check` again | any customer count, team size, founding year or round a deck states, against the site and the company's announcements |
| C2 Revenue story | `metrics-pack/mrr.csv`, `nrr.csv` – card: "Metrics available: none"; Fondo publishes no revenue series | nothing – no revenue growth or NRR is inferred here | `/fundraise:metrics-pack`, run on the company's own revenue export or contracts register | the deck's revenue figures and its "why it is interesting" line – whether it shows how revenue grows |

No check is partial.

## Limits

- Each point is a doubt a fund may raise, not a finding that a claim is false.
- **Public sources only.** Fondo did not take part and has not reviewed this note. Every page was
  retrieved on 2026-11-11; the site can change after that date.
- **The fund list is the example's, not Fondo's.** Fondo states no round and names no funds. The
  C5 points say which funds in this list back which competitors; they say nothing about whether
  Fondo should approach any fund, or whether any fund would invest.
- **The website was read as static pages.** Which column of the pricing page's comparison table is
  ticked for each feature is not readable as static text, so D01 rests on the alternatives the
  table names, not on its ticks.
- **Excluded candidates.** Stacks, Numos (General Catalyst) and Apron (Index Ventures) are not
  rows in `competitors.csv` because `/fundraise:competitors` ruled them excluded – they fail all
  three legs and serve a different buyer. A candidate the competitor note's Method lists as
  excluded has been ruled on, so, as the skill directs, it raises no point and is listed here.
- Candidates come only from the three funds' portfolios; the full competitor set is
  `/fundraise:competitors`' and is itself a floor (22 direct, with the long tail of accounting
  firms sampled, not counted).
- **Thesis-fit could not tell** on two fund axes, because the funds' own directories leave too
  many companies unclassified: General Catalyst on stage ("26 of 51 classified (148
  unclassified)"; the fund states "Seed and early stage is our core") and Index Ventures on
  geography ("4 of 16 classified (50 unclassified)"; geography "not published"). These are gaps
  in the evidence, not doubts a fund would raise; each fund knows its own portfolio. Each fund's
  portfolio list in `funds.csv` is a floor, not a complete portfolio.
- Prices on the pricing page are partly promotional ("Limited time offer"); the comparisons in
  D01 and D03 use the competitor note's list prices.
- Research, not investment advice.

## Sources

| Source | What it gave | Retrieved |
|---|---|---|
| https://fondo.com/ (`readiness-check/raw/fondo.com.html`) | job sentence; "Built for Delaware C-Corps. Trusted by 2,000+ startups."; "We've helped thousands of startups save $100M+"; "Since 2019"; "$8B + Transactions Categorized" | 2026-11-11 |
| https://fondo.com/pricing (`readiness-check/raw/fondo.com_pricing.html`) | "Fondo compared to the alternatives" table (Pilot, "CPA/Accounting Firm"); plan prices; "built specifically for Delaware C-Corp startups", "Pre-seed to Series B" | 2026-11-11 |
| https://fondo.com/about (`readiness-check/raw/fondo.com_about.html`) | "70+ professionals"; "1,000+ startups trust Fondo" (2023); "We started Fondo as a small team in San Francisco" | 2026-11-11 |
| `fondo/company-profile.md` | card fields; `## Conflicts` (1 row: Who pays) | 2026-11-11 |
| `fondo/thesis-fit/funds.csv`, rows General Catalyst, Index Ventures, Alumni Ventures | fit labels and counts | 2026-11-11 |
| `fondo/thesis-fit/thesis-fit.md` | "Index Ventures Scout Fund" in Fondo's seed round, citing https://techcrunch.com/2024/11/22/yc-backed-fondo-raises-funding-for-its-ai-powered-bookkeeping-and-taxes-platform/ | 2026-11-11 |
| `fondo/competitor-candidates/candidates.csv`, 13 rows | candidates, their own words, fund pages | 2026-11-11 |
| https://www.generalcatalyst.com/companies/puzzle, /kick, /collective | Puzzle, Kick, Collective in General Catalyst's portfolio (via `candidates.csv`) | 2026-11-11 |
| https://www.indexventures.com/companies/pilot/ | Pilot in Index Ventures' portfolio (via `candidates.csv`) | 2026-11-11 |
| https://www.av.vc/portfolio | Haven, Puzzle, Cynch AI, MainStreet, Ardius, Bridger Group in Alumni Ventures' portfolio (via `candidates.csv`) | 2026-11-11 |
| `fondo/competitor-research/competitors.csv`, 61 rows | classifications and grades; Pilot's funding; Puzzle's sale to Accrual; MainStreet and Ardius acquisitions | 2026-11-11 |
| `fondo/competitor-research/competitor-report.md`, Method | Stacks, Numos, Apron excluded; Fondo's differences on public evidence; founding-year note | 2026-11-11 |
| https://www.usehaven.com/blog-posts/the-4-best-fondo-alternatives-for-startups (via `competitor-report.md`) | Haven ranks itself a Fondo alternative | 2026-11-11 |
| `fondo/market-sizing/market-sizing.csv`, rows CL1, BU24L/H, TD22L/H, CP8, CP18L/H; `market-sizing.md` | no market claim found; demand builds and ceilings; press customer count and ARR | 2026-11-11 |
| https://techcrunch.com/2024/11/22/yc-backed-fondo-raises-funding-for-its-ai-powered-bookkeeping-and-taxes-platform/ | "a bookkeeping platform aimed at startups and small- and medium-sized businesses" (via `company-profile.md` Conflicts) | 2026-11-11 |

Next step: fix the points above, then re-run the skill each fix names (`/fundraise:<skill>`),
then `/fundraise:readiness-check` again.
