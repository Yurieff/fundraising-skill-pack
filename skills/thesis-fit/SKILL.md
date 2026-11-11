---
name: thesis-fit
description: Checks, for one fund or a chosen list of funds, whether a startup matches what the fund says it backs (its stated thesis, quoted from its own site) and what it actually backed (its real portfolio, read from its own directory and classified company by company). Reports a match per fund on four axes – stage, geography, market, business model – and flags portfolio companies that look like competitors into the shared candidates file. Produces a note, one funds CSV, one portfolio CSV per fund. Bootstraps the company card when none exists. Invoke when the user says "does X fit fund Y", "which of these funds fit X", "thesis fit for X", or "/thesis-fit X".
version: 0.1
---

# Thesis Fit

## What you're doing

You've been asked whether a startup fits one fund or a list of funds the founder has chosen.
**You read each fund twice**: what it says it backs, and what it actually backed. A fund's website
is a marketing page; its portfolio is the record. Where the two disagree, the portfolio wins and
the note says so.

```
  STATED THESIS  ───┐
  fund's own site:  │
  stage, geography, │
  markets, model,   ├──►  FIT PER AXIS  ──►  MATCH PER FUND  ──►  COMPETITOR CANDIDATES
  check size        │     stage ·            match / partial /    portfolio companies in the
                    │     geography ·        no match / unknown   startup's market doing a
  REVEALED THESIS ──┘     market ·                                similar job → candidates.csv
  the portfolio it        business model     revealed outweighs
  actually backed,                           stated
  last 3 years
  (never an aggregator)
```

"Fit" here is a match statement – the startup resembles what this fund says and does. It is not a
prediction that the fund will invest and not an investment recommendation.

Deliverables, relative to the current working directory:

1. **`<company-slug>/thesis-fit/thesis-fit.md`** – the note. The primary deliverable.
2. **`<company-slug>/thesis-fit/funds.csv`** – one row per fund: stated and revealed thesis, fit
   per axis.
3. **`<company-slug>/thesis-fit/portfolio-<fund-slug>.csv`** – one per fund: every portfolio
   company in the slice, classified.
4. Rows appended to **`<company-slug>/competitor-candidates/candidates.csv`** – at least one per
   fund.

Plus `<company-slug>/thesis-fit/raw/` holding every page and payload fetched, verbatim, so the run
is auditable.

Abbreviations used in this file: B2B / B2C / B2G = business to business / to consumer / to
government · CSV = comma-separated values · JSON = JavaScript Object Notation · API = application
programming interface · CMS = content management system · URL = web address · HTML = the page's
markup · HTTP = the web's request protocol · AI = artificial intelligence · ML = machine
learning · VC = venture capital · US = United States · ISO = the international date format
(`YYYY-MM-DD`).

## Inputs

From `$ARGUMENTS` or the conversation:

- **a company** – a folder, a loose deck, or just a name or website (Step 0);
- **the funds** – one fund, a list, or a file with one fund per line (Step 1);
- **optionally, a slice** – which investments count. Default: **investments of the last 3 years**,
  counted back from today (for example 2023-11 → 2026-11). The user may name another slice
  ("last 5 years", "only fintech", "seed deals only").

If the company is ambiguous (two firms share the name), ask which one before spending a fetch.

---

## Step 0 – Company card

**Never report "no data".** Take whatever you are given and build the rest.

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

This skill needs five fields before Step 4: **job done for the customer, business model, market,
stage, geography**. Take them from the card if filled. Otherwise research them from the company's
own site (home page, pricing, about), save the fetches to `raw/`, and write them into the card
with their sources. Never compare a fund to a guess: if a field cannot be found, it stays empty in
the card and that axis is `unknown` for every fund.

```
  folder + card   →  read it, go
  loose deck      →  build the folder, deck into <company-slug>/deck/, then the card
  name only       →  build the folder, research the five fields, create the card
```

---

## Step 1 – Funds

Accept one fund, a list, or a file. For each, fix **the fund's own website** before anything
else – it is the only source for Steps 2 and 3.

- **Name collisions: ask.** Several firms share names ("Index", "Accel", "Lightspeed" vary by
  region and entity). If a name maps to more than one firm, or the website is not given and two
  candidates exist, ask the user which one. Never pick silently.
- **Fund slug** – lowercase, hyphens (`general-catalyst`), used in the portfolio file name.
- **More than 3 funds → one parallel agent per fund.** Each agent runs Steps 2–5 for its own fund
  and writes only its own files: `portfolio-<fund-slug>.csv`, one fund row in
  `raw/<fund-slug>/fund-row.csv`, its candidate rows in `raw/<fund-slug>/candidates-rows.csv`,
  and its raw fetches under `raw/<fund-slug>/`. You then merge the fund rows into `funds.csv` and
  append the candidate rows yourself, so no two agents write the same file. Three funds or fewer:
  do them in turn yourself.

---

## Step 2 – Stated thesis

What the fund says it invests in, **from the fund's own site only** – the home page, "about",
"approach", "focus", "stages", "sectors" or "how we invest" pages. Not press interviews, not
aggregator profiles, not a partner's social posts: those are a person talking, not the fund
publishing.

Record five things, each as a **verbatim quote with its URL**, or the words **"not published"**:

```
  stage         "seed to growth", "we lead Series A"            → stated_stage
  geography     "Europe and the US", "global"                   → stated_geography
  markets       "fintech, health, climate"                      → stated_markets
  model         "B2B software", "consumer"                      → into the note's stated table
  check size    "first checks of $1–5M"                         → stated_check_size
```

**"Not published" is an answer.** Many funds publish a mission sentence and nothing else. Do not
infer a stated stage from a portfolio, or a stated market from a blog post – that is the revealed
side's job. A fund with nothing stated has every `stated_*` cell "not published", and its match
rests on the portfolio alone; the note says so in those words.

Keep the quote short (the phrase that carries the claim) and put it in the note's stated-thesis
table and its source table. Quote it exactly; where the fund's sentence carries an em dash,
quote the phrase on one side of it rather than changing the fund's punctuation.

---

## Step 3 – Revealed thesis

What the fund actually backed. This is the load-bearing half of the skill.

### 3a – Get the population from the fund's own directory

The list of portfolio companies must come from **the fund's own site** – never from an
aggregator (Crunchbase, Dealroom, PitchBook and the like) and never from web search. Search is
for enrichment only (3c). In order:

```
  1  OWN PAGE        /portfolio · /companies · /investments · /founders
                     curl -sL with a browser User-Agent; save the HTML to raw/
        │ list not in the HTML (JavaScript-rendered, "load more", infinite scroll)?
        ▼
  2  EMBEDDED JSON   grep the HTML for __NEXT_DATA__ · self.__next_f · buildId ·
     OR API          window.__NUXT__ · application/ld+json · CMS hints (strapi,
                     contentful, sanity, algolia, webflow, wp-json)
                     download the page's JavaScript bundles and grep them for
                     "/api/", fetch(, graphql, and foreign hosts
                     try the obvious ones: /wp-json/wp/v2/<type>?per_page=100,
                     /sitemap.xml (portfolio detail pages are often listed there)
                     paginate or lift the page-size parameter until the list ends
        │ still blocked (Cloudflare, 403, empty shell)?
        ▼
  3  BROWSER         the fetch tool first; then a real browser session (page text,
                     scroll, "load more" until the list ends)
```

If an API takes filters (region, sector, fund vehicle), check that the unfiltered call is the
superset before trusting it. Check the list for duplicates by name **and** domain – two
different companies can share a name. Save every payload to `raw/`.

**Fetching hundreds of pages: throttle, and check bytes, not only status.** A site can start
answering a fast crawler with HTTP 202 and an empty body (an `x-amzn-waf-action: challenge`
header is the tell). Fetch at most 2 pages at a time with a pause, check that every saved file
is non-empty, and refetch the empty ones.

**Then say which kind of list you have**, in the note and in the fund's `note` cell:

```
  COMPLETE   the directory was read to its end, its count matches any count the
             fund itself publishes ("300+ companies"), and every company in it
             could be dated for the slice
  FLOOR      anything less: paginated beyond reach, blocked, market-filtered,
             a gap between the list and the fund's own published count, or
             undated companies left out of the slice
```

Look for the fund's own count on its home, "about" and founder pages before calling a list
complete – a directory can hold two-thirds of the portfolio the fund claims.

A floor is never evidence of absence. If a floor holds no company in the startup's market, the
answer is "none found in the part read", never "the fund has no companies like you".

### 3b – Fix the slice

Default: **investments of the last 3 years**, counted back from today by month. Use the
investment date the directory publishes. If the fund gives only a year, use whole years (for
today 2026-11-11: 2024–2026) and say which you used. If the directory gives no date at all, in
this order:

```
  1  the fund's own announcement of the deal    "we're leading X's seed round" – its date
  2  the company's own announcement of the round
  3  a proxy the fund's own site carries        e.g. the upload month in the company's logo
                                                URL (…/2024/04/…) = when the site added it;
                                                say "proxy"; the earliest year present is
                                                usually a site migration – read it as
                                                "that year or earlier"
```

**A fund's first post about a company is not always the deal.** Retrospectives, interviews and
follow-on rounds ("catching up with…", "since leading its seed in 2021") are dated by the post,
not the investment. Keep only posts that announce the fund's own entry; list the rest in the note
as excluded, with the entry year where the post states it. A company with no date found stays
out of the slice and is counted in the note as "undated".

Record for the note: total directory size, retrieval date, slice definition, slice size
(`portfolio_n`), undated count.

**Very large portfolios: filter to the startup's market first, and say so.** When the slice holds
more than about 300 companies, or the directory cannot be read to its end, use the directory's
own sector or keyword filter (or a keyword pass over the full list) to keep only companies in or
next to the startup's market, and classify those. The portfolio CSV then holds the filtered set,
the slice cell says so ("2024–2026, fintech filter"), the revealed-markets cell describes the
filter rather than the fund's whole mix, and the list is a **floor**. A market-filtered set
cannot show a market mismatch: back the market axis with the fund's own sector counts over the
whole directory, and say so.

### 3c – Enrich

You need a one-line description and a website for every company in the slice:

1. the directory's own blurb, if it has one;
2. the company's own site – `<title>`, meta description, the first heading (bulk `curl` with a
   time limit; then the fetch tool for the ones `curl` cannot read);
3. web search by name plus context, for the rest – and check it is the same company (domain,
   country, the fund's own mention). Same name is not same company.

Every description that did not come from the directory carries its source and date in the row's
`note`. A company you cannot describe stays in the CSV with `market` blank and a note; report how
many – it makes every share a floor.

### 3d – Classify every company

Per company, in the same vocabulary as the company card, so the startup and the portfolio can be
compared cell for cell:

```
  stage            pre-seed · seed · Series A · Series B+ · unknown
                   the stage of the round the fund joined, if the directory or an
                   announcement states it; otherwise the stage the directory shows,
                   labelled as such in note; never researched on an aggregator
  business_model   B2B · B2C · B2G – by who pays (own call; prosumer → B2C)
  market           exactly one from the card's fixed list
  vertical         free text, finer than market
```

**Stage is the costliest axis** – few directories publish it. Look on the fund's own site
first: announcement and story pages ("Seeding the future with X", "Our investment in X's Series
A") state the round. Resolve as many as you can: an axis where more than half of the slice is
unclassified reads `unknown` (Step 4), so a handful of stories is not enough. Leave the rest
`unknown` and report the count.
Map a fund's own stage labels only where they are unambiguous ("Seed" → seed, "Growth" →
Series B+); keep a label like "Early" in `note` and record `unknown`.

Geography is the company's headquarters country, as the directory publishes it or as the
company's own site states it; record it in `note` when the directory has none. If the directory
publishes only regions ("North America"), compare at region level and say so in the fit reason.

**The website wins over the directory blurb** when they disagree, and the disagreement goes in
`note`.

Then summarise the slice per axis, from the written CSV:

```
  revealed_stage       counts per stage, unknowns included:  "seed 4 · Series A 6 · Series B+ 9 · unknown 12"
  revealed_geography   top headquarters countries with counts
  revealed_markets     top markets with counts – and the startup's market with its count
  revealed_models      B2B / B2C / B2G counts
```

---

## Step 4 – Fit

Per fund, per axis, compare the startup's card value with the stated thesis and with the revealed
portfolio. First count, per axis, over the slice:

```
  N            rows in the slice (portfolio_n)
  classified   rows whose value on THIS axis is known (stage not "unknown", a
               geography published or found, market and model filled)
  unclassified N − classified
  k            classified rows that share the startup's value
  share        k ÷ classified
```

Then read each side, **in this order** – the first line that applies wins:

```
  REVEALED (from the slice)                                STATED (from Step 2)
  unknown    unclassified > 50% of N, or k = 0 in a FLOOR   says yes      the value is named or covered
  backs it   k ≥ 2 AND share ≥ 10%                          says no       other values named, this one not
  thin       k ≥ 1 but below either threshold               not published
  none       k = 0, and the list is COMPLETE
```

Both thresholds are fixed so that labels compare across funds of any size: 2 companies out of
300 is "thin" (0.7%), not "backs it". The share is measured over classified rows only, and the
majority-unclassified rule stops a few known rows from speaking for the whole slice.

Then the fit:

| Revealed | Stated says yes | Stated says no | Not published |
|---|---|---|---|
| backs it | match | match – note the disagreement | match |
| thin | partial | partial | partial |
| none | partial – note the disagreement | no match | no match |
| unknown | partial – rests on the stated side | no match | unknown |

**Every fit reason gives its counts**: "<k> of <classified> classified (<unclassified> unclassified)",
for example "4 of 16 classified (50 unclassified)", in the note's fit table and in `funds.csv`'s
`note`.

**Revealed outweighs stated.** A fund that says "seed" but led only growth rounds in the slice is
read on what it did, and the note says where the two sides disagree.

```
  fit_overall   any axis "no match"     →  no match
                all four axes "match"    →  match
                all four axes "unknown"  →  unknown
                otherwise                →  partial
```

`fit_overall` is `match` only if no axis is `no match`. **No invented score**: no points, no
weights, no percentages of fit – four labelled axes and one rule.

---

## Step 5 – Candidates

Portfolio companies that may compete with the startup. A candidate must be **in the same market
and doing a similar job** – compare its one-liner with the card's "Job done for the customer".
Same market alone is not enough: a payments company is not a bookkeeping firm's competitor.

- Sweep the **full directory** when you obtained it (a competitor backed six years ago still sits
  in the portfolio), otherwise the slice or the filtered set; say which in `why_flagged`.
- **Sweep by keyword over every description, never only by the fund's sector filter.** The
  job's own words (for a bookkeeping firm: bookkeeping, accounting, tax, close, back office)
  over all one-liners – the fund's sector tags misfile companies, and the closest candidate can
  sit under another tag.
- Companies that share the market but sell a different job (a tool sold to accounting firms,
  against a startup that does the accounting) are **not** flagged; list them in the note as
  "adjacent, not flagged" with the reason, so the reader can disagree.
- Quote why: `why_flagged` holds the candidate's own words (directory blurb or its site), plus
  the shared job in a few words.
- **A fund with none gets a `none found` row**: `name` = `none found`, `domain` blank,
  `why_flagged` = what was swept ("full directory, 412 companies" or "floor: fintech filter, 60
  companies"). A `none found` row on a floor says "floor" in `why_flagged`.

Append to `<company-slug>/competitor-candidates/candidates.csv`. Create it with the header if it
is missing. **Never delete or rewrite other rows** – other runs and other skills own them; skip a
row only if the same `name` and `fund` already appear. Columns exactly:

`name,domain,fund,portfolio_url,why_flagged,found_by,date_found`

- `domain` – the candidate's bare domain (`example.com`)
- `portfolio_url` – the fund's page that lists it
- `found_by` – `thesis-fit`
- `date_found` – today, ISO

`/fundraise:competitors` reads this file as its sweep route 6 and rules on each candidate. This
skill only flags; it does not classify direct versus indirect.

---

## Step 6 – Note and CSVs

### The CSVs

Write every CSV with Python's `csv` module (quoting on), never by hand – one-liners contain
commas.

`funds.csv`, columns exactly:

`fund,website,stated_stage,stated_geography,stated_markets,stated_check_size,revealed_stage,revealed_geography,revealed_markets,revealed_models,portfolio_n,slice,fit_stage,fit_geography,fit_market,fit_model,fit_overall,candidates_n,note`

- every `stated_*` cell – the short quote, or `not published`
- every `fit_*` cell – exactly one of `match`, `partial`, `no match`, `unknown`
- `portfolio_n` – the number of data rows in that fund's portfolio CSV, nothing else
- `slice` – the definition, for example `2024–2026 by investment year`
- `candidates_n` – the number of real candidate rows written for this fund (0 when the only row
  is `none found`)
- `note` – how the list was obtained, COMPLETE or FLOOR, and where stated and revealed disagree;
  then, always, the Step 4 counts for all four axes in exactly this form, which
  `readiness-check` parses: `Fit counts – stage: <k> of <classified> classified (<unclassified>
  unclassified) → <revealed> → <fit>; geography: …; market: …; model: ….` – `<revealed>` is
  `backs it`, `thin`, `none` or `unknown`, `<fit>` the axis's `fit_*` label

`portfolio-<fund-slug>.csv`, columns exactly:

`name,website,year,stage,business_model,market,vertical,one_liner,source_url,note`

- `year` – the investment year (the slice key)
- `source_url` – the fund's page or payload that lists this company
- `note` – enrichment source and date, stage basis, headquarters country if not in the directory,
  blurb-versus-site disagreements

### The note

`thesis-fit.md`. Self-contained: a reader must follow it without opening another file.

```
 1  Frontmatter       title, company, created, author, status, tags
 2  Answer up front   which funds match and on what, in two or three sentences;
                      the per-fund table: fund · stage · geography · market · model ·
                      overall · candidates – labels only, no score
 3  How to read       the four axes, the fit labels and the rule, COMPLETE vs FLOOR,
                      the slice, "fit is not a recommendation", every abbreviation
 4  The company       the five card fields used, with sources
 5  Per fund          one section each:
                        · stated thesis – table: axis · quote · URL (or "not published")
                        · how the portfolio was obtained – route, payload or page, total
                          size, the fund's own count, slice and its date basis, N,
                          COMPLETE or FLOOR, undated and excluded counts
                        · revealed thesis – the four summaries
                        · fit per axis – the label, the counts ("<k> of <classified>
                          classified (<unclassified> unclassified)"), the one-line reason,
                          and where stated and revealed disagree
                        · candidates – names, quotes, or "none found" and what was swept;
                          then "adjacent, not flagged" with the reason
 6  Limits            floors, unclassified tails, stage basis, what was not read
 7  Sources           full table: every stated quote, every directory page or payload,
                      every enrichment source – URL and retrieval date
```

**Diagram-first** for structure, prose for findings. Name the fund's words when you quote them;
never paraphrase a stated thesis into something stronger.

---

## Step 7 – Verify, then wrap up

Run these as commands, not by eye:

- `head -1` of `funds.csv`, of each `portfolio-<fund-slug>.csv` and of `candidates.csv` equals
  the column lists above, exactly.
- For each fund, `portfolio_n` equals the data-row count of its portfolio CSV (read with the `csv`
  module – one-liners can hold line breaks).
- Every `fit_*` cell is one of the four labels and recomputes from the portfolio CSV with the
  Step 4 thresholds (k ≥ 2 and share ≥ 10% of classified; unknown above 50% unclassified);
  `fit_overall` follows the rule from the four axes; every fit reason in the note carries its counts.
- Every `stated_*` cell is either "not published" or appears, quoted, with a URL in the source
  table.
- For each fund the note says how the list was obtained and whether it is COMPLETE or a FLOOR.
- A fund with no published thesis has every `stated_*` = "not published" and its section says the
  match rests on the portfolio.
- `candidates.csv` has at least one row per fund, and no row from an earlier run was lost (count
  rows before and after).
- Numbers in the note recomputed **from the CSVs**, not from working notes. Every abbreviation
  expanded in the note.
- Chat summary, short: per fund the overall fit and the axis that decided it, whether each list is
  complete or a floor, and the candidates found.
- Last line of the chat summary: "Next step: `/fundraise:market-size`".

## House rules

- **The population comes from the fund's own site, never an aggregator.** Search enriches
  descriptions; it never adds or removes a portfolio company.
- **A count is not a list.** "The fund backed 40 fintech companies" needs the 40 rows in the CSV,
  or the note says the count is the fund's own claim and was not enumerated.
- **A floor is never absence.** A partial list that shows no company like the startup says "none
  found in the part read".
- **"Unknown" is an answer.** An axis that cannot be read is `unknown`, never guessed into a
  match.
- **"Not published" is an answer.** Never infer the stated thesis from the portfolio.
- **No invented score.** Four labelled axes and one rule, nothing weighted.
- Dates absolute ISO. Every abbreviation expanded in the file that uses it.
- **No investment recommendation.** "Fit" says the startup matches what the fund says and does;
  it never says the fund will, or should, invest, or that the founder should pitch it.

## Field notes from validation runs

Lessons from runs on real funds, kept here until they are folded into the steps above. Most
of the first run's lessons are already folded into Step 3 and Step 5; these bullets say why.

- **Step 3a – a crawler can be blocked silently.** In the first run a fund's site returned HTTP
  202 with an empty body to every page after about 330 fast requests; only the byte count showed
  it. Two at a time with a pause cleared it.
- **Step 3a – read the fund's own count before calling a list complete.** One directory listed
  620 companies on a site that claims "900+"; another embedded 1,773 records against "1,800+".
- **Step 3b – the fund's first post about a company is often a retrospective.** 23 of 89
  first posts inside one window were interviews, profiles or follow-ons for companies backed
  years earlier; dating by them would have put long-held companies into a 3-year slice.
- **Step 3b – a fund's own site can carry a usable date where its directory has none.** One
  fund's embedded JSON held no investment date, but every logo URL held its upload month. Used
  as a labelled proxy, with "2021" (the earliest year present) read as "2021 or earlier".
- **Step 3d – stage at entry sits in the fund's own stories, not its directory.** One fund's
  "Seeding the future with …" and "Our investment in …" pages gave the round for 51 of 199
  companies; the rest stayed `unknown` and the axis still resolved.
- **Step 5 – the closest candidate was outside the sector filter.** At one fund the company
  doing the same job for the same buyer was tagged "AI & ML", not "FinTech"; only a keyword pass
  over all descriptions found it. The two closest candidates at another fund were backed five
  and more years before the slice – hence the full-directory sweep.
- **The startup's own round may name a fund's affiliate.** The subject's seed round listed a
  fund's scout vehicle, though the company is not in that fund's directory. Record it in the
  note as a fact about the relationship; it is not a fit signal.
- **Step 4 – a bare count made every fund match.** The first version read "backs it" at 2
  companies, so all three funds matched on all four axes – one on 4 North America rows out of 66,
  50 of them untagged. The share threshold and the majority-unclassified rule turned that axis
  `unknown`, and a fund's stage axis with 148 of 199 rows unclassified `partial`. Keep the counts
  in every reason so a reader can see why.

## Changelog

- **v0.1 (2026-11-11):** built. Stated thesis from the fund's own site, revealed thesis from its
  own portfolio directory (own page → embedded JSON or API → browser), fit per axis with revealed
  outweighing stated, competitor candidates written to the shared candidates file. First
  acceptance run (one startup, three funds) folded in: throttled fetching, date rules for
  directories without dates, stage from the fund's own stories, keyword sweep for candidates.
  Review fix the same day: "backs it" needs k ≥ 2 and a share ≥ 10% of classified rows; an axis
  more than half unclassified reads `unknown`; "rarely" renamed "thin"; counts in every reason.
  Release fix the same day: `funds.csv`'s `note` always ends with the "Fit counts – …" string
  that `readiness-check` parses.
