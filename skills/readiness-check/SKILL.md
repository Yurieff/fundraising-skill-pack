---
name: readiness-check
description: Reads a startup's pitch deck (if any), its covering email (if given), the shared company card and whatever the earlier fundraise skills produced (thesis fit, market sizing, competitors, metrics pack), and lists the points that may raise doubts with funds – each with the claim and the slide it is on, what the evidence says and where, why a fund may doubt it, how to fix it, and a severity (high, medium, low). Six checks – consistency, revenue story, market claim, competitors, fund list, card conflicts – each skipped, and named with the skill that would fill it, when its input is missing. Never a verdict, a score or an investment recommendation. Produces a note and one doubts CSV. Invoke when the user says "check my deck before I send it to funds", "readiness check for X", "what will investors doubt in X's deck", or "/readiness-check X".
version: 0.1
---

# Readiness Check

## What you're doing

You've been asked to read a startup's materials the way a fund's analyst reads them on the first
pass – and to list, before any fund does, **the points that may raise doubts**. You compare what
the company says (deck, covering email, website) with what the earlier skills found. You do not
redo their research: where an earlier output is missing, the check it feeds is skipped and the
note names the skill that would fill it.

```
  WHAT THE COMPANY SAYS        WHAT THE EVIDENCE SAYS
  ─────────────────────        ──────────────────────────────────────
  deck, slide by slide  ──┐    company-profile.md
  covering email        ──┤    thesis-fit/funds.csv
  website – the claims  ──┤    market-sizing/market-sizing.csv
  when there is no deck   │    competitor-research/competitors.csv
                          │    competitor-candidates/candidates.csv
                          │    metrics-pack/mrr.csv, nrr.csv
                          │                  │
                          └────────┬─────────┘
                                   ▼
     C1 consistency · C2 revenue story · C3 market claim · C4 competitors ·
     C5 fund list · C6 card conflicts        (missing input → check skipped, skill named)
                                   │
                                   ▼
     POINTS THAT MAY RAISE DOUBTS WITH FUNDS
     each: claim + its slide · evidence + its source · why a fund may doubt it ·
           how to fix it · severity high / medium / low
```

**A list of doubts, never a verdict.** The output says which points a fund may stop on and how to
fix each. It gives no verdict on the company and no view on whether to raise or to invest.
There is no score and no overall label.

Deliverables, relative to the current working directory:

1. **`<company-slug>/readiness-check/readiness-check.md`** – the note. The primary deliverable.
   Opens with "In plain English."
2. **`<company-slug>/readiness-check/doubts.csv`** – one row per point.

Plus `<company-slug>/readiness-check/raw/` holding every page fetched and the covering email's
text, verbatim, so the run is auditable.

Abbreviations used in this file: B2B / B2C / B2G = business to business / to consumer / to
government · CSV = comma-separated values · PDF = portable document format · URL = web address ·
TAM / SAM / SOM = total addressable / serviceable addressable / serviceable obtainable market ·
MRR = monthly recurring revenue · ARR = annual recurring revenue · NRR = net revenue retention ·
USD = United States dollar · ISO = the international date format (`YYYY-MM-DD`).

## Inputs

From `$ARGUMENTS` or the conversation: **a company** – a folder, a loose deck, or a name or
website – and optionally a covering email (pasted or as a file) and a list of target funds.

| Input | Where it is | Feeds |
|---|---|---|
| Deck | `<company-slug>/deck/` (PDF, slides or Markdown), or a loose file the user names | C1–C5: the claims |
| Covering email | pasted text or a file; save it to `raw/covering-email.txt` | C1, C5 (funds it names) |
| Website | the card's `website`: home, pricing, about | C1; the claims when there is no deck |
| Company card | `<company-slug>/company-profile.md` | every check; C6 |
| Thesis fit | `<company-slug>/thesis-fit/funds.csv` | C5 |
| Market sizing | `<company-slug>/market-sizing/market-sizing.csv` (and `market-sizing.md`) | C3 |
| Competitors | `<company-slug>/competitor-research/competitors.csv` | C4, C5 |
| Competitor note | `<company-slug>/competitor-research/competitor-report.md` – its Method section lists the candidates ruled "excluded – <leg>" (no CSV row) | C5 |
| Candidates | `<company-slug>/competitor-candidates/candidates.csv` | C4 (partial), C5 |
| Metrics | `<company-slug>/metrics-pack/mrr.csv`, `nrr.csv` (and `metrics.md`, `excluded.csv`) | C2 |

If the company is ambiguous (two firms share the name), ask which one before reading anything.

---

## Step 0 – Company card and inventory

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

Read the card first: its values are the baseline every deck claim is compared against. **Count
the rows in `## Conflicts` now** – C6 reports the rows that were there before this run; rows this
run adds are reported under C1.

If a deck or email states a value for an **empty** card field (for example "Round being
raised"), fill it with the slide as its source. If it states a **different** value for a filled
field, add a Conflicts row (`Found by` = `readiness-check`) and raise the point under C1.

Then take the inventory – one line per input, present or not, with its path. It goes into the
note (section 5) and decides which checks run:

```
  C1 Consistency    runs with a deck or a covering email (between slides, deck against
                    email, both against the website); website alone → skipped ("needs a
                    deck or a covering email to compare with the site")
  C2 Revenue story  needs metrics-pack/mrr.csv          missing → skipped, /fundraise:metrics-pack
  C3 Market claim   needs market-sizing/market-sizing.csv  missing → skipped, /fundraise:market-size
  C4 Competitors    needs competitor-research/competitors.csv
                    only candidates.csv → PARTIAL, /fundraise:competitors named
                    neither → skipped, /fundraise:competitors (and /fundraise:thesis-fit)
  C5 Fund list      needs thesis-fit/funds.csv           missing → skipped, /fundraise:thesis-fit
                    conflicts read on competitors.csv; on candidates.csv only → PARTIAL
  C6 Card conflicts needs company-profile.md             always runs once the card exists
```

A check whose inputs exist but whose claim does not ("the deck states no TAM") **runs** and says
"no claim to test" – an absent claim is recorded in the checks table, not raised as a doubt.

**Never fill a gap yourself.** Do not size the market, classify competitors, compute NRR or rate
a fund's fit in place of the skill that does it. Skipped is an answer; the note says which skill
fills it.

---

## Step 1 – Read the claims

**With a deck:** read it slide by slide (a PDF page by page; a slide file exported to PDF or
read as text; a Markdown deck by its slide headings). Number slides as the deck numbers them, or
by page. For each slide, note every claim a fund would test:

```
  numbers       customers, revenue, MRR / ARR, growth, NRR, round size, valuation, team size
  market        TAM / SAM / SOM, its source, geography, year
  competition   "no direct competitors", the competitor list or matrix
  why now / why it is interesting   the line that says why the company will grow
  funds         a target-fund slide or the funds the email names
  card fields   stage, geography, business model, revenue model, round being raised
```

Quote each claim verbatim with its slide number. A claim's source is always written as
`deck <file>, slide <n>` (or `covering email, paragraph <n>`, or the page URL).

**Without a deck:** read the company's own site – home, pricing, about – with `curl -sL` and a
browser User-Agent, save each page to `raw/`, and take the claims from there. Each claim's source
is the page URL. Say in the note that there is no deck and the claims come from the website.

**The covering email**, if given: save its text to `raw/covering-email.txt` and read its claims
the same way.

---

## Step 2 – Run the checks

Run C1 to C6 in order. Each produces zero or more points. A point always has all five parts –
**claim (with its source), evidence (with its source), why a fund may doubt it, how to fix it,
severity** – or it is not a point.

### Severity – what makes a doubt high, medium or low

Severity says how likely a fund's analyst is to stop on the point. It says nothing about the
company's quality. If two rules apply, the higher one wins.

```
  HIGH    the evidence contradicts the claim:
          · the same number, for the same thing and period, differs by more than 10%
            between two places (slides, email, website, an earlier skill's output) – a
            lower-bound claim ("2,000+", "100+ customers") counts as differing only when
            the other figure is LOWER than the bound; a higher figure agrees with it
          · an absolute claim ("no direct competitors", "NRR 130%") that a source the
            fund can read itself refutes, or that the earlier skill says cannot be computed
            – this includes "no (direct) competitors" against a candidate in a target
            fund's own portfolio whose own words describe the same job for the same buyer
            (C4): that fund refutes it from its own portfolio page, confirmed or not
          · a figure stated as current revenue that equals a month metrics-pack marks
            `contracted` (signed, not yet billed) – the deck presents future revenue as
            today's (C2)
          · a target fund that thesis-fit reads as "no match" on an axis
          · a confirmed direct competitor in a target fund's portfolio
  MEDIUM  the claim cannot be checked, or the evidence against it is unconfirmed:
          · a market figure with no source on the slide
          · a claim contradicted only by unconfirmed candidates – except the absolute
            "no (direct) competitors" case above, which is high
          · a target fund whose fit is "partial" on classified evidence – few or none of
            the fund's classified companies share the startup's value (C5); a gap in the
            fund's own data ("thesis-fit could not tell") is not a doubt
          · a revenue total, series or chart that blends billed and contracted months
            without labelling them, where no single stated figure is a contracted month;
            revenue that counts non-recurring contracts as recurring
          · a "why it is interesting" line that shows no revenue mechanism
          · a card conflict on a field funds screen on: stage, geography, market,
            business model, revenue model, round being raised
  LOW     presentation:
          · the same number rounded differently, within 10%
          · a missing date, unit or caveat that does not change the number
          · a card conflict on a descriptive field: job done, who pays, vertical,
            metrics available
```

Each check below says how its own findings map onto these rules.

### C1 – Consistency

The deck against itself, against the covering email, and against the company's own site.

- **Between slides:** the same metric stated twice (customers on the traction slide and on the
  summary slide, revenue in two places). Different values → high above 10%, low within it.
- **Deck against email:** every number and every fund the email names, against the deck.
- **Deck against site:** fetch the site pages that state the same metric (home page counters,
  the funding announcement, pricing) and save them to `raw/`. Quote the site's words exactly.
- **Deck against card:** a deck value that differs from a filled card field (Step 0).
- **A lower bound is contradicted only from below.** "2,000+ startups" or "100+ customers"
  against a LOWER figure for the same thing and period → high more than 10% below the bound,
  low within it; against a higher figure → no point, the two agree.
- Different definitions are not a contradiction: "USD 5 million, of which 1 million debt"
  against "USD 4 million equity" is the same round. Say so and raise it at low, as a wording
  point, only if a reader could take the two for different rounds.
- A site counter can be newer than the deck: still a point, because the fund reads both. The fix
  is to align the two and date the number.

### C2 – Revenue story

Does the line that says why the company is interesting show **how revenue grows** – for example
an NRR above 100%, or billed MRR rising month on month – or only that the market is big? Then
cross-check every revenue number in the deck with `metrics-pack`.

**Read NRR only as `metrics-pack` reports it.** Never compute, estimate or extrapolate NRR, and
never take it from a shorter window. In order:

```
  1  metrics.md says "cannot compute yet" (no customer detail, a single-customer
     export, or a register with no renewal recorded) → NRR cannot be computed yet,
     whatever nrr.csv holds
  2  nrr.csv has only its header                    → NRR cannot be computed yet
  3  nrr.csv has data rows                          → quote them; for a contracts
     register add "counts only renewals recorded in the register"
```

Then:

| Deck says | metrics-pack says | Severity |
|---|---|---|
| an NRR figure | cannot compute yet | high – quote metrics.md's reason |
| an NRR figure | a figure more than 10 percentage points away | high |
| an NRR figure from a contracts register, no caveat | a figure, register caveat | low |
| an MRR or revenue figure | last billed `mrr` more than 10% away | high |
| an MRR or revenue figure, stated as current, equal to a `contracted` month | that month is contracted, not billed | high – future revenue shown as today's |
| a revenue series or total that blends billed and contracted months, unlabelled | the months after `--as-of` are `contracted` | medium – the figure exists, its label is wrong |
| revenue that includes short contracts | `excluded.csv` lists them as non-recurring | medium |
| "why it is interesting" = market size only | any | medium – the fix shows the measurable mechanism from mrr.csv, and NRR or "cannot compute yet" with the reason |

A growth rate the deck states is checked against `mrr.csv` with a command over the billed rows;
quote the command's output. A number the pack does not contain is not derived here: say the pack
lacks it.

### C3 – Market claim

The deck's TAM (and SAM, SOM or revenue target, if stated) against the two demand builds and the
capacity ceiling in `market-sizing.csv`. Read it with the `csv` module and `skipinitialspace=True`
(its header has a space after each comma). Rows: `layer` = `TAM` / `SAM` / `SOM` with `method` =
`bottom-up`, `top-down` or `triangulation`; `layer` = `capacity` for the ceiling (funded-plan
headline and current-team floor); `method` = `claim` for what market-size read from the deck.
Quote `market-sizing.md`'s Step 4 mechanism where it explains a gap – do not re-size anything.

```
  deck TAM more than 2× the higher demand-build TAM             high – name the mechanism
                                                                 market-size gives (geography,
                                                                 segment, buyer, price, billed slice)
  deck TAM within 2× of the builds, no source on the slide      medium
  deck TAM within 2× of the builds, sourced                     no point
  deck SOM or revenue target above the funded-plan ceiling      high – the company binds
  deck SOM or revenue target between the current-team floor
  and the funded-plan ceiling                                   low – the hiring plan carries it
```

Compare in one currency, converted only at a rate `market-sizing.md` states.

### C4 – Competitors

The deck's competitor slide (or "no direct competitors" line) against `competitors.csv`
(`classification` = `direct` · `former direct` · `indirect` · `unverified`; read with
`skipinitialspace=True`).

```
  "no (direct) competitors"   ≥ 1 `direct` row in competitors.csv          high
  the competitor slide        omits one or more `direct` rows               medium – name them
  the competitor slide        calls an `indirect` row direct, or the
                              reverse                                       low
```

**Partial – no `competitors.csv`, only `candidates.csv`.** Candidates are portfolio companies
`thesis-fit` flagged; nobody has ruled on them yet. Use what they offer and say the check is
partial, naming `/fundraise:competitors`:

```
  "no (direct) competitors"   a candidate in a TARGET fund's portfolio whose own
                              words (why_flagged) describe the same job for the
                              same buyer                                   high – that fund's
                                                                           analyst knows the company
  "no (direct) competitors"   candidates only elsewhere, or a similar job
                              for another buyer                            medium – unconfirmed
```

Quote the candidate's own words from `why_flagged`, cite the row (`candidates.csv`, name and
fund) and the fund's `portfolio_url`. Write "candidate, not yet ruled on by
`/fundraise:competitors`" in the point. Neither file → C4 skipped.

### C5 – Fund list

The target funds – from the deck's fund slide, the email, or the user's list; if none is given,
the funds in `funds.csv`, and the note says so – against `thesis-fit/funds.csv`.

Read each axis that is not `match` on its own. `funds.csv`'s `note` cell gives, after "Fit
counts –", per axis, the counts, the portfolio-side reading and the fit: "<axis>: <k> of
<classified> classified (<unclassified> unclassified) → <revealed reading> → <fit>". The revealed
reading says whether the fit rests on evidence or on a gap in the fund's data:

```
  axis fit "no match"                                   high – name the axis, quote the counts
                                                        (the fund's own words or its classified
                                                        portfolio say no)
  axis fit "partial", revealed reading "thin" or "none" medium – classified evidence: few or none
                                                        of the fund's classified companies share
                                                        the startup's value; quote the counts
  axis fit "partial" or "unknown", revealed "unknown"   NO POINT – "thesis-fit could not tell":
                                                        the fund's directory leaves most
                                                        companies unclassified, or the list
                                                        read is a floor with none found. List
                                                        it in the checks table and in Limits
                                                        with the counts
  every axis "match"                                    no fit point
  a target fund not in funds.csv                        not checked – listed in the checks table:
                                                        run /fundraise:thesis-fit with it
```

A gap in thesis-fit's data is not a doubt a fund would raise: the fund knows its own portfolio.
Never turn it into a fix that asks the founder to do thesis-fit's research.

**Portfolio conflicts – re-checked against confirmed competitors, not only candidates.** For each
target fund, take its rows in `candidates.csv` and look each up by name and domain in
`competitors.csv`:

```
  candidate classified `direct`                  high – the fund already backs a direct competitor
  candidate classified `unverified`               medium
  candidate classified `indirect` or `former direct`  low
  candidate listed as "excluded – <leg>" in       no point – list it in Limits with the leg
  competitor-report.md's Method                   it failed (competitors ruled on it)
  candidate absent from competitors.csv and       medium – say competitors did not rule on it
  from the Method's excluded list
  no competitors.csv at all                       PARTIAL: one medium point per fund with a
                                                  same-job candidate, "unconfirmed", naming
                                                  /fundraise:competitors
  only a `none found` row for the fund            no conflict point; say what thesis-fit swept
```

The point states the fact (the fund backs company X; X's own words) and what a fund may ask. It
never says to drop or to pitch a fund.

### C6 – Card conflicts

Every row in `company-profile.md` `## Conflicts` that existed before this run is one point. Claim
= the card value and its source; evidence = the new value and its source; severity by field, as
in the rules above (screening field → medium; descriptive field → low; high when the deck states
one of the two values and the other comes from a primary document such as a filing or the
company's own announcement). The fix names which source to correct. An empty Conflicts table →
C6 runs, no points, and the note says so.

---

## Step 3 – Write doubts.csv

Write it with Python's `csv` module (quoting on), never by hand – quotes contain commas. Columns
exactly:

`id,check,severity,claim,claim_source,evidence,evidence_source,why_doubt,fix`

- `id` – `D01`, `D02`, … in note order (by check, then high before medium before low)
- `check` – `C1` … `C6`
- `severity` – exactly one of `high`, `medium`, `low`
- `claim` – the verbatim quote
- `claim_source` – `deck <file>, slide <n>`, `covering email, paragraph <n>`, a URL, or
  `company-profile.md, <field>` (C6)
- `evidence` – what the evidence says, quoted where it is words
- `evidence_source` – a URL, or a file with its row (`competitor-candidates/candidates.csv, Pilot
  / Index Ventures`), never blank
- `why_doubt` – one or two sentences, from the fund's side of the table
- `fix` – what to change in the materials, and the skill to re-run if a number moves

Skipped checks are not rows: they live in the note's checks table.

---

## Step 4 – readiness-check.md

Self-contained: a reader must follow it without opening another file. Frontmatter: `title`,
`company`, `created` (ISO date), `author`, `status: draft`, `tags`.

```
 1  In plain English.  one short paragraph, no jargon: this is a fund analyst's first read
                       of the materials, done before any fund does it – the points a fund
                       may stop on, and how to fix each. It is not advice on whether to
                       invest, and it gives no verdict on the company.
 2  Answer up front    the high points, one line each; then the checks table:
                       check · status (run / partial / skipped) · points (high / medium /
                       low) · what fills it, if skipped or partial
 3  How to read        the severity rules (Step 2, printed), claim source, evidence source,
                       partial, skipped, every abbreviation
 4  Materials read     deck (file, slide count) or "no deck – claims from the website";
                       covering email or "not given"; the claims table: slide · claim
 5  Inputs             one line per input from Step 0: path, present or missing, used by
 6  Points             grouped by check C1–C6; each point: id · severity · the claim
                       (quote, source) · the evidence (source) · why a fund may doubt it ·
                       how to fix it
 7  Skipped and partial  per check: what is missing, what was done with what exists, the
                       skill that fills it, and the deck claim it would test
 8  Limits             what was not read; fund axes thesis-fit could not tell (C5), with
                       their counts; that each point is a doubt a fund may raise, not a
                       finding that the claim is false
 9  Sources            full table: every slide, page, file and row cited, with retrieval date
```

**Counts are allowed, a score is not.** The checks table counts points per severity; there is no
total, no grade, no "ready" or "not ready".

Last line of the note, and of the chat summary: "Next step: fix the points above, then re-run the
skill each fix names (`/fundraise:<skill>`), then `/fundraise:readiness-check` again."

---

## Step 5 – Verify, then wrap up

Run these as commands, not by eye:

- `head -1 doubts.csv | tr -d '\r'` equals the column list in Step 3, exactly (the `csv` module
  ends lines with `\r\n`).
- Every row (read with the `csv` module): `check` in C1–C6, `severity` in high / medium / low,
  `claim_source` and `evidence_source` non-empty.
- Every `id` in `doubts.csv` appears in the note, and the note's counts per check and severity
  recompute from the CSV.
- Every check C1–C6 appears in the checks table; each skipped or partial one names the
  `/fundraise:<skill>` that fills it.
- C2: if `metrics-pack` says "cannot compute yet", no NRR figure appears in the note except the
  deck's own, quoted.
- No verdict and no recommendation – this finds nothing (`<company>` = the company's name):

  ```bash
  grep -iE "should invest|recommend (investing|an investment)|invest in <company>|ready to raise|not ready" \
       <company-slug>/readiness-check/readiness-check.md <company-slug>/readiness-check/doubts.csv
  ```
- No em dash in any file; every abbreviation expanded in the note.
- Chat summary, short: the high points, one line each; the checks skipped or partial and the
  skills that fill them; the paths of the two files.
- Last line of the chat summary: the next-step line from Step 4.

## House rules

- **Doubts, never a verdict.** No score, no grade, no "ready"; the note lists points and fixes.
- **No investment recommendation.** Nothing here says a fund will, or should, invest, or that the
  founder should pitch or drop a fund.
- **Every point has both sources.** A claim without its slide or page, or a doubt without its
  evidence source, is not a point.
- **Skipped is an answer.** A missing earlier output skips its check and names the skill; it is
  never filled in by guessing.
- **Never redo an earlier skill's work.** No market sizing, no competitor classification, no NRR
  here – only the comparison.
- **"Cannot compute" stays "cannot compute".** An NRR that `metrics-pack` could not compute is
  never estimated, and a deck figure against it is a high point.
- **A candidate is not a confirmed competitor.** Say "candidate, not yet ruled on" until
  `/fundraise:competitors` has ruled.
- Quote the company's and the funds' words exactly. Dates absolute ISO. Every abbreviation
  expanded in the file that uses it.

## Changelog

- **v0.1 (2026-11-11):** built. Six checks (consistency, revenue story, market claim,
  competitors, fund list, card conflicts), explicit severity rules, `doubts.csv`, skipped and
  partial checks named with the skill that fills them; NRR read only as `metrics-pack` reports
  it; reads the shared company card. Replaces the placeholder.
  Review fix the same day: the general severity rules now carry the C4 case (an absolute "no
  competitors" claim met by a same-job, same-buyer candidate in a target fund's portfolio is
  high) and the billed-versus-contracted split (a contracted month stated as current revenue is
  high; an unlabelled blend is medium); C5 raises a fit point only for "no match" or a
  "partial" on classified evidence – a gap in the fund's own data is reported as "thesis-fit
  could not tell", not as a doubt.
  Release fix the same day: a candidate the competitor note lists as excluded raises no point
  (Limits only); a lower-bound claim ("2,000+") is contradicted only by a lower figure.
