---
name: competitors
description: Maps a startup's competitors – writes an explicit membership test, sweeps for operators through several independent routes, classifies each as direct / former direct / indirect, compares pricing like-for-like from published pages, researches total funding per competitor with an entity check, and sweeps M&A comparables with deal values and multiples. Produces a competitor note, one csv, one price chart, and a two-sheet shareable market-analysis workbook (competitors + M&A comparables). Bootstraps the company folder and researches the source material itself when none exists. Invoke when the user says "who competes with X", "competitor research on X", or "/competitors X".
version: 0.3
---

# Competitors

## What you're doing

You've been asked who else is in a startup's market, at what price, on whose money – and what
companies like it have sold for.

```
  WRITE THE TEST  ──►  SWEEP  ──►  CLASSIFY  ──►  PRICE  ──►  FUND  ──►  M&A COMPS
   what counts?        several      direct /      like-for-   who backs   who bought
                       routes       indirect      like        them        whom, at what
```

Deliverables – exactly four files in `<company-slug>/competitor-research/`,
relative to the current working directory:

1. **`competitor-report.md`** – the note. The primary deliverable.
2. **`competitors.csv`** – one row per competitor, with classification, pricing, funding, evidence.
3. **`price-ladder.png`** – one chart of the price comparison.
4. **`<company-slug>_market_analysis.xlsx`** – the shareable two-sheet workbook:
   competitors + M&A comparables (Step 9).

Plus `raw/` holding every page fetched, verbatim, and `workbook-data.json` – the workbook's
structured input.

## Inputs

From `$ARGUMENTS` or the conversation: **a company**. A folder, a loose deck, or just a name or
URL – all three work (Step 0). If two firms share the name, ask which before spending a fetch.

---

## Step 0 – Build what isn't there

**Never report "no data".**

<!-- profile:start -->
## The company card

`<company-slug>/company-profile.md` – read it first. If it is missing, create it. If a field is
empty and you learn it, fill it and update `updated` / `updated_by`. Never overwrite a filled
field: if you find a different value, add a row to `## Conflicts` with both values and sources.
The card ends with a `## Conflicts` section (create it if missing) whose table header is exactly
`| Field | Card value | Card source | New value | New source | Found by | Date |`.

| Field | Allowed values |
|---|---|
| Job done for the customer | one sentence, in the company's own words, quoted, with URL |
| Who pays | free text |
| Business model | B2B · B2C · B2G |
| Revenue model | subscription · transaction · ads · one-off · n.a. |
| Market | exactly one: Fintech & insurance · Health & bio · Commerce & retail · Logistics & supply chain · AI & data infrastructure · Enterprise software · Cybersecurity · Legal, compliance & governance · Sales & marketing · HR & talent · Education · Media, gaming & entertainment · Real estate & construction · Energy, climate & agriculture · Industrial & robotics · Consumer lifestyle & services · Other |
| Vertical | free text |
| Stage | pre-seed · seed · Series A · Series B+ · n.a. |
| Geography | headquarters country; countries it sells in |
| Round being raised | amount + currency + instrument, or "not stated" |
| Metrics available | where (`updates/`, exports), or "none" |

Frontmatter: `company`, `slug`, `website`, `updated` (ISO date), `updated_by` (skill name).
The card's table has a third column, `Source`, filled for every field.
<!-- profile:end -->

Use the card instead of re-researching what it already holds: its "Job done for the customer"
row is the job you need below. Research the company's offer again only for fields that are empty.

```
  folder + deck   →  read it, go
  loose deck      →  build the folder, deck into <company-slug>/deck/
  name only       →  build the folder, then RESEARCH what the company sells
```

You need one thing before Step 1: **what job does this company do for its customer?** Take it
from the card if filled; otherwise get it from the company's own site, in its own words, not from
a category label, and write it into the card. Save every fetch to `raw/`.
Create the company folder `<company-slug>/`: the deck, if any, goes to `deck/`, your output to
`competitor-research/`.

---

## Step 1 – Write the test

Before naming a single competitor, write down what a company must *do* to count as one. Decompose
the job into observable legs.

```
  a physical service might need three legs:
      collects from the customer · stores off-site · redelivers on request

  a B2B tool might need two:
      serves the same buyer · replaces the same budget line
```

Then the three classes:

```
 DIRECT          does the whole job, evidenced on its own site
 FORMER DIRECT   did once – no longer trades independently
 INDIRECT        fails at least one leg, but contests the same
                 customer / price point / capital
```

**The test goes in the report**, printed, so a reader can classify a company the sweep missed. It
is also the only defence against the two failure modes here: counting adjacent companies as rivals,
and missing rivals who describe themselves differently.

⚠️ **Categories rarely share a vocabulary.** The same product gets sold as different words by
different sellers. If you sweep only the words the company uses about itself, you will
systematically miss the larger, older, better-distributed operators who use incumbent language.
Write the test on **function**, never on self-description.

---

## Step 2 – Sweep, through several independent routes

One search is not a sweep. Run at least four routes that could each surface a competitor the
others miss:

```
 1  vocabulary        every word the category uses, not just the company's
 2  the customer      what would a buyer actually search for?
 3  registries        Companies House SIC codes · SEC EDGAR · trade bodies
 4  supply side       who sells software/services TO these operators?
                      their customer lists are a census
 5  reverse traces    competitor comparison pages, "alternatives to X" pages,
                      review-site categories
 6  capital           funding press, accelerator and investor portfolios, and
                      `<company-slug>/competitor-candidates/candidates.csv`, if it exists
```

**Route 6 reads the candidates file.** `<company-slug>/competitor-candidates/candidates.csv`
(written by `thesis-fit`) has the columns `name,domain,fund,portfolio_url,why_flagged,found_by,date_found`.
Each row is a candidate: it gets the Step 1 test like any other name, and is ruled on in Step 3.
A row whose `name` is `none found` means that fund's portfolio was swept – do not sweep it again.
A candidate that fails the Step 1 test and does not contest the same buyer is **excluded** (Step
3): it gets no CSV row and is listed in the Method section as "excluded – <which leg it failed>",
never silently dropped.
The note's Method section says how many candidates came from fund portfolios and how each was
ruled.

**Stopping rule:** stop when two consecutive routes add no new material competitor. The sweep
has converged only if no route left an unchecked named list (a directory, a customer list, an
"alternatives to X" page whose names were not all tested); otherwise the count is a floor. If
you stop before that – budget, blocks, time – **say so in the note and call the count a floor.**
A census that did not converge is a floor, not a ceiling, and the reader must be told which they
have.

⚠️ **Paid firmographic databases are NOT a seventh route.** Apollo.io was measured against a
hand-built 34-operator census on 2026-08-06: it recovered **56%
blind**, ran **50% false positives**, and **8 of 34 operators were absent from its index entirely**.
It is an enrichment layer, not a discovery route. Two rules survive from that test and apply to any
such source:

```
  a database row is a CANDIDATE, never a competitor
      → it still needs the Step 1 test, evidenced on the company's own site.
        The database's own description text is third-party and does not count.

  an unmatched row means UNKNOWN, never SMALL
      → coverage failure is silent: a company the database lacks
        returns empty, not flagged.
```

Grade each operator as you go:

```
 MATERIAL   multi-city, funded, franchised, or evidently scaled
 MINOR      trading, but single-market or sub-scale
 MICRO      one-person, pre-launch, or an unverifiable trading entity
```

---

## Step 3 – Classify

Apply the Step 1 test to each. Evidence for every classification is a quote from the company's
**own site**, recorded in the CSV.

Boundary calls to make explicitly, because they recur:

```
  looks similar, fails a leg    →  INDIRECT, and say which leg
  same job, different labour    →  usually INDIRECT – name the difference
  dead or absorbed              →  FORMER DIRECT, with what happened to it
  fails a leg AND does not      →  EXCLUDED – not a competitor: no CSV row; listed in the
  contest the same buyer           Method section as "excluded – <leg it failed>"
```

**Former direct competitors are worth real effort.** What happened to the companies that already
tried this is often the most decision-relevant section in the report: who bought them, for how
much, against how much raised.

---

## Step 4 – Price

```
  LIKE-FOR-LIKE      same unit, same market, tier by tier   ← the real comparison
  ENTRY PRICE ONLY   "from $X" – basis differs              ← labelled as such
```

Rules:

- **Only prices published on the operator's own page.** Not the deck's version of a competitor's
  price. Re-pull them yourself.
- Compare headline to headline, and matching tier to matching tier. Applying one company's
  discounts while quoting others at list price is the standard way this table lies.
- Where units genuinely differ, say so rather than forcing a comparison.
- Record what is **excluded** – setup fees, delivery, onboarding, minimums.

---

## Step 5 – Funding, per competitor

For every company found:

```
  total raised      currency + amount
  last round        stage + date
  investors         who led
  source            where it came from
  flag              D / E / N/A     ← N/A = not disclosed, NOT zero
```

Where to look, in order of trust:

```
  SEC EDGAR / Form D  ─┐
  Companies House      ├─  filings   → flag D
  company's own page  ─┘
  funding press        ──  reported  → flag E
  aggregators          ──  noisy     → flag E, and name which one
```

⚠️ **Entity check – skipping it has already produced two false figures in real runs.**

```
  "Boombox raised $7M from Forerunner + Ulu"
        │
        └─►  that round belongs to boombox.io – a generative-AI MUSIC company.
             The storage company of the same name has no funding record at all.

  Same source: "BOXIE24, $5.5M Series A"  →  no such round exists.
```

> **The round must name THIS company** – this domain, this market, this country. Same name is not
> same company. If you cannot tie it, mark `N/A`. **Never borrow a round.**

Both false figures above came from company-supplied comparables. Treat company-supplied
competitor funding as a lead to verify, never as a source.

---

## Step 6 – M&A comparables

Who has bought companies like this one, and at what price? Sweep for acquisitions in the
category – acquisition press, acquirer announcements, SEC filings, Companies House, the
former-direct trail from Step 3 (those exits belong here too).

Three tiers of comparable, and **every row says which tier it is inside its own description
cell** – a reader of the sheet alone must know what kind of comparable they are looking at:

```
 1  DIRECT PRODUCT ANALOG     same product, acquired
 2  CLIENT / ICP ANALOG       same buyer and budget line, different product
                              (ICP = ideal customer profile)
 3  FINANCIAL BENCHMARK       bigger horizontal player whose deal anchors the
                              multiple range – labelled "financial benchmark,
                              not a product analog"
```

Per deal, pursue: acquirer · deal year · deal value / EV (with structure caveats) · revenue at
deal · EV/Revenue · EBITDA · EV/EBITDA · other metrics at deal time · deal rationale (what the
acquirer said it was buying).

Discipline – this table is where multiples get invented, so:

```
  "CANNOT COMPUTE" IS AN ANSWER.  Never derive a multiple from:
      · a partial stake            (80% of the equity is not EV)
      · an earn-out formula        (4.25× EBITDA as a payout formula is not a multiple)
      · mismatched periods         (2018 revenue under a 2021 deal price)
      · group-level figures        (the parent's revenue is not the subsidiary's)
    Write "Cannot compute" and say why, in the cell.

  "NOT DISCLOSED" IS SPELLED OUT.  Never a bare N/A, never a blank –
    not disclosed ≠ zero, and a blank cell reads as "nothing there".

  THE ENTITY CHECK APPLIES TO DEALS.  The deal must name THIS company –
    same domain, same market. Never borrow an acquisition any more than a round.
```

Every figure carries its source as a hyperlink in the workbook (Step 9) and a row in the
report's source table. Where a press-reported price is unconfirmed by either party, say so
next to the number.

Close the step with a synthesis paragraph – it becomes the bottom row of the workbook's
M&A sheet: is the deal market proven, who are the likely acquirers of **this** company, and
what multiple range do the disclosed deals actually support – **naming which companies form
the bounds** (a range bounded by a horizontal SaaS and a services firm is not a range of
direct analogs, and the reader must be told).

---

## Step 7 – Write the CSV

`competitors.csv`, columns exactly:

`name, domain, country, classification, grade, legs_matched, evidence, status, price_entry, price_basis, price_like_for_like, total_raised, last_round, investors, funding_flag, funding_source, confidential, note, url`

- `classification` – `direct` · `former direct` · `indirect` · `unverified`
- `grade` – `material` · `minor` · `micro`
- `evidence` – the verbatim quote that placed it in its class
- `confidential` – `no` (default, publicly evidenced) · `yes` (came from the data room)

**One CSV, not two.** If a shareable copy is needed later, blank the fields on `confidential = yes`
rows and **keep the rows** – filtering rows out deletes competitors the report profiles, which has
already had to be undone once.

---

## Step 8 – The chart

Use any Python 3 that has matplotlib and openpyxl (`python3 -c "import matplotlib, openpyxl"` to
check). If none does, ask the user before installing anything; the clean route is a throwaway
virtual environment (`python3 -m venv` + `pip install matplotlib openpyxl`), never a system-wide
`pip install`.

One PNG: the price comparison, sorted, subject company marked. Only include operators whose prices
are genuinely like-for-like; put the rest in a table instead. Palette: blue `#2a78d6` for the
field, orange `#eb6834` for the subject company (dark variant `#3987e5` / `#d95926`), light **and**
dark variants. matplotlib reads a pair of `$` signs as math – escape them as `\$`. Read the PNG
afterwards and check for label collisions.

---

## Step 9 – Build the workbook

The shareable two-sheet xlsx. **No new research happens here** – sheet 1 re-presents Steps 1–5,
sheet 2 re-presents Step 6. The formatting is fixed by the builder script; workbooks are written
in English.

```
  workbook-data.json  ──►  build_workbook.py  ──►  <slug>_market_analysis.xlsx
   you write this          fixed formatting, don't reimplement        both files in competitor-research/
```

`build_workbook.py` sits in this skill's own base directory, next to this file. Run it with the
same Python as the chart:

`python3 <this-skill-dir>/build_workbook.py workbook-data.json <company-slug>_market_analysis.xlsx`
The json schema is documented in the builder's docstring: per sheet a list of rows plus a
synthesis paragraph; each cell is plain text, a number, or `{"text", "url"}` for a hyperlink.

**Sheet 1 `competitors`** – 9 columns: Company · Year founded · Last round / status · Investors ·
ICP (ideal customer profile) · Short description · Business model · Similarity to \<Company\> ·
Difference from \<Company\>. The Difference cell **ends with the spelled-out verdict** – "Direct
competitor" / "Former direct competitor" / "Adjacent competitor". Row scope: material direct +
former direct that matter + the closest adjacent, roughly the top 6–10; the full census stays in
the csv, and the synthesis row states the cut ("the csv holds N more minor operators").

**Sheet 2 `M&A comparables`** – 12 columns: Company · Year founded · Short description · Acquirer ·
Deal year · Deal value / EV · Revenue at deal · EV / Revenue · EBITDA · EV / EBITDA · Other
metrics at deal time · Deal rationale.

Rules the workbook lives by:

- **Hyperlinks are the sourcing.** One per cell: company name → its site, year founded →
  LinkedIn, round/deal cells → the announcement. A cell citing a source inline carries the word
  "Source" in its text, with the cell hyperlinked. Extra sources go in the report's source table.
- **Built to leave the building.** Publicly evidenced data only – anything the csv marks
  `confidential = yes` stays out of the workbook entirely.
- **No coded shorthand anywhere.** Verdicts spelled out, "Not disclosed" / "Cannot compute"
  written in words, ICP expanded in its own header. The workbook must decode without a legend.
- Each sheet ends with a blank row, then its synthesis paragraph, merged across columns A–E on
  a light-gray fill – the builder does this from the json's `synthesis` field. Sheet 1's
  synthesis is the market verdict (how crowded, who matters most, what actually differentiates
  the subject – the same answer the note leads with); sheet 2's is the Step 6 close.

---

## Step 10 – Write the note

`competitor-report.md`. Self-contained – a reader who does not know the category must follow it.

```
 1  Frontmatter      title, company, created, author, status, tags
 2  Answer up front  how crowded, who matters most, in one paragraph
 3  How to read      THE TEST, printed · flags · grades · every abbreviation
 4  The market       what the product is, before naming anyone
 5  Method           routes run, what converged, what didn't
 6  Direct           table + short profiles of the ones that matter
 7  Former direct    what happened to them, and what it cost
 8  Indirect         grouped by why they're adjacent
 9  Pricing          like-for-like table, then entry prices, with exclusions
10  Funding          who is capitalised, and by whom
11  M&A comparables  the deals, the multiples that survived, likely acquirers
12  Limits           what the sweep missed, routes blocked, counts vs lists
13  Sources          full table, working URL or a stated reason
```

**Define before naming.** No operator appears before the product is explained. **No process
narration** – which route found what belongs in `raw/`, not the report.

---

## Step 11 – Verify, then wrap up

- The test is printed in the note and every row's classification matches it.
- Every competitor has evidence; every funding figure and every deal passed the entity check.
- Every count in the note has a list behind it, **or the note says it doesn't.**
- Prices re-pulled from source, not carried from the deck.
- **Workbook checks:** every multiple recomputes from the two figures in its own row; every
  hyperlink resolves (curl the targets); nothing `confidential = yes` appears anywhere in the
  xlsx; open the built file with openpyxl and re-read both sheets – headers, verdicts, both
  synthesis rows present.
- Chat summary, short: how many found and of what grade, the two or three that matter and why, the
  pricing headline, who is best capitalised, the M&A headline (deal market proven or not, and the
  supportable multiple range with its bounds named), and whether the sweep converged.
- Last line of the chat summary: "Next step: `/fundraise:metrics-pack`".

## House rules

- **A count is not a list.** State a number, and either the enumeration exists or you say it
  doesn't. This has bitten before.
- **Never borrow a funding round – or an acquisition.** Same name ≠ same company.
- **Never invent a multiple.** A multiple exists only when EV and the denominator are disclosed,
  for the same entity, over matching periods. Otherwise the cell says "Cannot compute" and why.
- **Prices from the operator's own page**, never from the subject company's materials.
- Where a finding has a counter-reading, print the counter-reading next to it.
- Data-room figures are marked `confidential = yes`, never silently mixed into a shareable claim.
- Dates absolute ISO. Every abbreviation expanded in the note itself.
- Findings are research artifacts. This skill produces no investment recommendation.

## Field notes from validation runs

Lessons from private runs on real companies across B2B SaaS, consumer apps, infrastructure and
early AI products, kept here until they are folded into the steps above. The companies are not
named.

**Writing the test (Steps 0–1)**

- **Read the subject's terms and privacy policy, not just its homepage.** In one run the homepage
  sold team-wide use while the terms capped the beta at one user and three processes; the gap
  became a main finding.
- **Run the subject through its own test.** An unreleased product is a plan. Write down every
  ruling that bends a leg, so a reader can repeat it.
- **Buyer is an axis, not a gate.** Gating on one buyer once excluded the very companies whose
  exits the M&A step relied on. Gate only on function. A test written from the subject's own
  module list is self-description in disguise and guarantees an "uncrowded market" finding.
  Under-counting, not over-counting, is the live risk in a mature category with a new vocabulary.
- **A fourth class, `converging`**: vendors whose shipped launches move them across a leg inside
  the observation window. In a consolidating category this is often the main finding; give it its
  own dated table.

**Sweeping (Step 2)**

- **Run vocabulary routes in the market's own languages, and add the bundle route** – a
  capability shipped free inside an incumbent's licence appears in no startup database and no
  funding press.
- **Keep a route-by-route table of what each route added**, so the stopping rule is auditable.
- **With parallel research agents, log the URL next to every saved file**, and archive each
  agent's final report verbatim in `raw/`. Read any automatically grouped list before it ships:
  substring grouping misfiles names.

**Pricing and funding (Steps 4–5)**

- **Like-for-like prices can cover the wrong layer.** Say which layer the chart prices. "Nobody
  publishes a price" is a finding, and it can hold for one commercial unit and not the other –
  report the asymmetry.
- **Run the entity check on the domain, not only the name.** A same-name domain turned out to be
  a clothing manufacturer; another was a parked domain for sale. Read a guessed domain before
  quoting anything from it.
- **Aggregator page furniture is not data.** Some aggregators show a promotional "raised USD X"
  banner on every company page, and search summaries repeat it as the company's round.

**M&A comparables (Step 6)**

- **Check every direct competitor for a pending sale by name.** A pending deal has no filing yet;
  a plain news search finds it.
- **A listed acquirer's statutory accounts are a purchase-price route** (Australian Securities
  Exchange Appendix 4E, UK annual report, SEC 10-K or 20-F). A headline "up to USD 90m" price was
  USD 50m of purchase consideration; the rest was retention pay.
- **The SEC purchase-price-allocation route** recovers prices the press never carried, and shows
  earn-outs that lapsed.
- **Keep a public comparables table as standard.** In several runs the listed peers carried the
  whole valuation signal while "cannot compute" hit most or all private deals – say so rather than
  quoting a range the deals do not support. Add a small-cap floor tier (sub-USD 100m deals) and
  keep valuation events (funding rounds) apart from transactions.
- **Recompute every public comparable from its own page**, and check redirects when sources
  disagree on a domain.

**Verifying (Step 11)**

- **Read the HTTP status in the fetch logs before citing.** Take links only from fetches that
  returned 200. A 403 or 429 from `curl` is usually a bot block, not a dead link – retry in a
  browser and record the retrieval route in the source table.
- **Scan for confidential data before the workbook ships.** In one run the scan caught a
  data-room funding figure leaking into three cells.

## Changelog

- **v0.3 (2026-11-11):** reads and fills the shared company card; sweep route 6 reads
  `competitor-candidates/candidates.csv` and rules on each row (a candidate that fails the test is
  listed as excluded, with the leg it failed); the chat summary ends with the next step,
  `/fundraise:metrics-pack`. Release fix the same day: "excluded" defined in Step 3 (fails a leg
  and does not contest the same buyer; no CSV row); the sweep converges only when no route left
  an unchecked named list.
- **v0.2 (2026-11-10): first public release** in the fundraising skill pack. Output paths made
  generic; machine-specific instructions removed; run history condensed into the field notes.
- **v0.1 (2026-08-11):** the M&A comparables step and the two-sheet workbook added.
- **v0 (2026-08-03):** built. Guards encoded from earlier failures: the entity check, the
  count-is-not-a-list rule, and the one-CSV rule.
