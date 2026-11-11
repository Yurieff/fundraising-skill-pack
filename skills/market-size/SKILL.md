---
name: market-size
description: Sizes a startup's market – builds TAM/SAM/SOM twice (bottom-up from buyers × price, and top-down from a published market figure), triangulates the two, then builds a third number the demand builds cannot give you: the capacity ceiling their own sales and delivery machine can carry. Compares all of it to whatever the deck claims, and reports the distance between what the market could support and what the company's own machine can reach. Produces a sizing note, one csv of every line item, and one chart. Bootstraps the company folder and researches the source material itself when none exists. Invoke when the user says "size the market for X", "what's the TAM for X", or "/market-size X".
version: 0.4
---

# Market Size

## What you're doing

You've been asked how big a startup's market is. **You size the demand twice, independently**,
because a single method is unfalsifiable – bottom-up alone can be built to any number, and
top-down alone inherits someone else's definition of the market.

Then you answer the question the demand builds cannot: **can this company actually reach the
market you just sized?** That is the capacity ceiling, and it is built from their machine – sales
headcount, funnel throughput, delivery capacity – not from the market.

```
   BOTTOM-UP  ──┐
                ├──►  do they agree?  ──►  TAM / SAM / SOM  ──┐
   TOP-DOWN   ──┘        the gap is                           │
                         a finding                            ├──►  the distance
                                                              │     between them
   CAPACITY   ─────────►  what their machine can carry  ──────┘     IS the finding
               never triangulated against the demand builds –
               a gap between them is the finding, not an error
```

Deliverables – exactly three files in `<company-slug>/market-sizing/`, relative to
the current working directory:

1. **`market-sizing.md`** – the note. The primary deliverable.
2. **`market-sizing.csv`** – one row per line item in all three builds, each with its source and flag.
3. **`tam-sam-som.png`** – one chart: the demand builds across the three layers, with the capacity
   ceiling drawn across them (plus any revenue bar the caller names – see Step 8, the chart).

Plus `raw/` holding every page fetched, verbatim, so the run is auditable.

> **Why the third build exists.** Two demand builds can converge beautifully on a multi-billion
> market and still tell a reader nothing, because any revenue target worth naming then needs a
> fraction of a percent of it and every company clears it. The capacity ceiling is what makes the
> sizing discriminating: it asks whether *this* team, with *this* motion, can get there at all.

## Inputs

From `$ARGUMENTS` or the conversation: **a company**. That can be a folder, a loose deck, or just
a name or URL. All three work – see Step 0. If the company is ambiguous (two firms share the
name), ask which one before spending a single fetch.

---

## Step 0 – Build what isn't there

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

Use the card instead of re-researching what it already holds: take the company's job, buyer,
market, stage and geography from it, and research only the fields that are empty or that sizing
needs in more depth. Anything new you learn goes back into the card.

```
  folder + deck   →  read it, go
  loose deck      →  build the folder, deck into <company-slug>/deck/
  name only       →  build the folder, then RESEARCH the inputs yourself
```

When researching from zero, in this order:

1. **The company's own site** – what it sells, to whom, where, and at what price. Pricing pages
   are the highest-value single fetch in this skill: they give you the `price` term directly.
2. **Registry** – Companies House (UK) or SEC EDGAR (US) for accounts, filings, incorporation.
3. **Press** – funding, headcount, market claims, customer counts.

Save every fetch to `raw/` verbatim. Create the company folder `<company-slug>/`: the deck,
if any, goes to `deck/`, your output to `market-sizing/`. Create only the sub-folders you actually
use.

> **Research replaces missing documents. It never replaces missing evidence.** Anything found this
> way carries the same flag and URL as anything else.

---

## Step 1 – Find the claim

What does the company say its market is, and where did that number come from?

Record: the figure, the geography and segment it covers, the year, and the cited source. If the
deck cites an analyst report, note whether the report is being quoted or paraphrased.

**No deck, or no claim in it?** Say so explicitly in the note and continue. An absent claim is a
finding – it is not a blocker.

### Then set the boundary yourself

**A market is bounded by a problem, not by a category.** Before building anything, write down the
specific problem whose sufferers you are about to count. "The online education market" and "the
virtual reality market" are categories, not markets – nobody has the problem "online education".

```
   CATEGORY  ✕   "the online education market"
   MARKET    ✓   "people already paying a tutor to pass a specific exam"
```

If you cannot state the problem in one sentence, you cannot size the market, and every number
downstream inherits the vagueness. Record the boundary in the note; a wrong boundary is the most
common way both demand builds come out confidently wrong *together*, which triangulation cannot
catch.

---

## Step 2 – Build the demand twice

### Bottom-up – from the customer up

Pick the formula by business model:

```
 CONSUMER APP        reachable users × paid conversion × ARPU
 B2B SAAS            target accounts × annual contract value
 LOCAL / PHYSICAL    households or sites × penetration × annual spend
 MARKETPLACE         transactions × average value × take rate
```

**Two-sided products: size the demand side first.** For a marketplace, build buyers × spend
before you look at supply, then verify the other side exists at that volume. A marketplace fails
from either side – plenty of eager suppliers with no buyers, or verified demand with nobody to
fulfil it – and sizing from the side that happens to be easy to count hides the failure.

Every term is a number you can point at. Population counts come from statistics offices, trade
bodies or registries – **never from the deck**. Price comes from published pricing pages, the
company's own or a competitor's.

### Top-down – from the published market down

```
   $40B   "global market for X"        ← published figure, cited
     ↓ × 35%   geography they sell in
   $14B
     ↓ × 20%   the segment they sell to
   $2.8B
     ↓ × 15%   the part of the job they actually bill for
   $420M  ← TAM
```

**Show every cut with its rationale.** The third cut is the one everyone skips: a published
"market" usually bundles labour, hardware and adjacent services the company never touches.

Treat published market sizes as **directional, not bankable** – aggregator figures disagree wildly
and are frequently recycled between reports. Name the publisher and the year for each.

---

## Step 3 – Triangulate

```
   within ~2×   →  CONVERGED. Report the range, not a point estimate.

   further apart →  THE GAP IS THE FINDING. Diagnose it:
                    · different market definitions?
                    · top-down includes non-buyers?
                    · bottom-up missed a buyer segment?
                    · one of them is simply wrong?
                    Then say which you trust, and why.
```

**Bottom-up is the load-bearing number. Top-down is the sanity check.** If you can only defend one
in a partner meeting, it is the one built from primitives.

> This step reconciles **the two demand builds only**. The capacity ceiling from Step 6 is never
> triangulated against them – it measures a different thing, and forcing agreement destroys the
> finding.

---

## Step 4 – Compare to the claim

Three numbers side by side: the deck's, your bottom-up, your top-down. Where the deck differs by
more than ~2×, explain the mechanism – not "they were optimistic", but *which step* differs:
geography, segment, buyer definition, price assumption, or the billed slice.

Common mechanisms, worth checking by name: counting all users rather than buyers · global figure
against a regional plan · whole-category spend against the company's own line item · a stale
report used as if current.

---

## Step 5 – Narrow, once

On the number you chose in Step 3:

```
   TAM   everyone who could buy
    │    ↓  keep only markets in the plan
   SAM   who they can actually reach
    │    ↓  × realistic share
   SOM   what they can win – WITHIN 5 YEARS, AT THE CURRENT BUSINESS MODEL
```

State the SOM share assumption as an assumption, flagged `A`. A SOM built on an unstated share
number is the single most common failure in this exercise.

**SOM carries a horizon and a business model, and the note states both.** A share of SAM with no
time attached is not a forecast, it is a wish. Use **5 years**, and if the company's own plan
changes the monetization model inside that window, size the model it will actually be running –
and say that you did.

> **Deliberate departure from the source lecture.** The IIDF (Internet Initiatives Development
> Fund, Russia) market-sizing lecture this skill's capacity build comes from defines SOM over
> **2–3 years**. This skill uses **5**, a decision taken on 2026-08-06: three years is too short a
> window to become big. Any revenue bar applied at a 3-year horizon rejects companies for being
> *early* rather than for being *small*, which is the opposite of what sizing is for.

---

## Step 6 – The capacity ceiling: what their machine can carry

Steps 2–5 sized the demand. This step sizes **the company**, and it is the one that makes the
sizing discriminating.

The question: *over the same 5 years, with the sales and delivery motion this company actually
has, what is the most revenue it can physically produce?* Not what the market will bear – what
they can carry.

### Pick the formula by go-to-market motion

```
 DIRECT SALES     reps × capacity per rep × win rate × annual contract value
 SELF-SERVE       traffic × signup conversion × paid conversion × ARPU
 OPS-DELIVERED    delivery units × throughput per unit × price
 MARKETPLACE      supply liquidity × transactions per unit × take rate
 ACQUISITION-LED  targets acquired per year × revenue per target
                  – then check it against ACQUISITION CAPITAL AVAILABLE
```

`OPS-DELIVERED` covers anything gated by human or physical throughput – an ops team, a fleet, a
clinic, a review queue. If the company runs two motions, build both, then combine them by how they
relate:

```
  PARALLEL motions     each brings in its own revenue on its own     →  ADD them
                       (self-serve sign-ups AND a direct-sales team
                       closing other accounts)
  SEQUENTIAL gates     every unit of revenue passes through both     →  take the LOWER
                       (acquisition, then delivery: a customer won      of the two – the
                       by sales still has to be served by ops)          tighter gate binds
```

Never add two gates the same revenue passes through: that counts each customer twice. Name the
binding gate in the note. If one motion is a plan rather than a fact, that is the funded-plan
ceiling below.

> **`ACQUISITION-LED` is gated by capital, not by headcount**, and that makes it the one motion
> where the ceiling can be limited by something the other four never surface. Always compute the
> capital the ramp implies (targets × price per target) and set it beside the round being raised.
> A roll-up plan needing 20× the capital it is raising has a **financing** constraint – which is
> fundable, unlike a small market, and is invisible to both demand builds. Say so plainly.
>
> Do not force a roll-up into `OPS-DELIVERED`: it yields a throughput ceiling that is real but is
> not the binding one.

### Never abstain – assume, and flag it

This step has the same posture as Step 0: **a missing metric is never a reason to skip the
build.** A pre-seed company will disclose almost none of these. Take the metric from an industry
or comparable-company benchmark, flag it `OB`, and name the benchmark with its URL.

> A capacity build made of flagged benchmarks is worth far more than no capacity build. What is
> not acceptable is an unflagged one.

| Input | Where it comes from when undisclosed | Flag |
|---|---|---|
| Headcount in sales / delivery | LinkedIn, the deck's team slide, careers page | `E` |
| Throughput per head | Industry operating benchmark | `OB` |
| Conversion rates | Benchmark, or their own funnel if disclosed | `OB` / `D` |
| Price / contract value | Published pricing page – already Step 2's highest-value fetch | `D` / `PM` |
| Ramp time, churn | Benchmark | `OB` |

### Current team vs funded plan

Compute the ceiling over **the same 5-year horizon as SOM** – two numbers measured over different
windows cannot be compared, and comparing them is the entire point of this step. Over five years
that forces a distinction you must make explicitly:

```
  CURRENT-TEAM CEILING     today's headcount, today's funnel      →  a FLOOR
       │                   over 5 years this is nearly always
       │                   an understatement – they will hire
       ▼
  FUNDED-PLAN CEILING      the hiring and throughput ramp the     →  the LOAD-BEARING
                           round is being raised to fund              number
```

Report the funded-plan ceiling as the headline, with the ramp itself flagged (`OB` from a
benchmark, `A` where it is a judgement call), and the current-team ceiling beside it as the floor.
**Never blend the two into one unlabelled number.**

### What the answer means

Give the ceiling as a range, then state which constraint binds:

```
  capacity ceiling ≥ demand SOM   →  THE MARKET BINDS.
                                     Sizing was the right question; Step 5 answered it.

  capacity ceiling ≪ demand SOM   →  THE COMPANY BINDS. Say so, with the multiple.
                                     A hiring / throughput / business-model finding,
                                     not a market finding. No amount of extra TAM
                                     fixes it.
```

Do **not** average the ceiling against SOM, and do not treat a gap as an error to reconcile. The
two answer different questions; the distance between them is the deliverable.

---

## Step 7 – Write the CSV

`market-sizing.csv`, columns exactly:

`line_id, method, layer, label, value, unit, currency, formula, source, url, flag, note`

- `method` – `bottom-up` · `top-down` · `capacity` · `triangulation` · `claim` · `reference`
  _(`reference` = a bar the caller named, e.g. "does this clear $10M ARR?" – never one this skill
  invented. Older runs used `screen` for the same thing.)_
- `layer` – `input` · `TAM` · `SAM` · `SOM` · `capacity`
- `formula` – how this line was computed from other lines, by `line_id` (e.g. `L3 × L4`)
- `url` – a working link, or blank plus a `note` saying why there isn't one

### Flags

| Flag | Means |
|---|---|
| `D` | **Disclosed** – stated by the company or a primary document |
| `PM` | **Public market** – a published market or industry figure |
| `OB` | **Operating benchmark** – an industry or comparable-company operating metric standing in for company data the company did not disclose |
| `E` | **Estimated** – inferred from evidence that does not state it directly; the `note` says inferred from what |
| `A` | **Assumption** – a judgement call with no evidence behind it |
| `C` | **Computed** – arithmetic from other rows, carrying no independent evidence of its own |
| `N/A` | **Not disclosed** |

**The rule that keeps these apart, and it is mechanically checkable:**

```
   formula column non-empty   ⇒   flag is C
   everything else            ⇒   carries a source, or it is A
```

`C` exists because arithmetic is not evidence. A row that multiplies two other rows inherits their
weakness and adds none of its own – flagging it `E` alongside a genuinely estimated input hides
which numbers in the build were actually guessed.

`OB` exists because "we assumed 4 deals per rep per month, which is the published SaaS median" and
"we assumed 20% market share" are not the same claim, and a reader must be able to tell them apart
at a glance. An `OB` row without a named benchmark and a URL is an `A` row wearing a better label.

Every row is a sourced number, a labelled assumption, or arithmetic over the other two. **There is
no fourth category.**

---

## Step 8 – The chart

Use any Python 3 that has matplotlib (`python3 -c "import matplotlib"` to check). If none does,
ask the user before installing anything; the clean route is a throwaway virtual environment
(`python3 -m venv` + `pip install matplotlib`), never a system-wide `pip install`.

One PNG: the demand builds side by side across the three layers, plus the deck's claim if there is
one, **with the capacity ceiling drawn across them as a horizontal reference line**.

```
   $B │ ███ ███          bottom-up │ top-down │ claim
      │ ███ ███ ▒▒▒
      │ ███ ███ ▒▒▒
      ├─────────────────────────────── capacity ceiling  ◄─ the gap IS the chart
      │ ███ ███ ▒▒▒
      ├─────────────────────────────── revenue bar, only if the caller named one
      └──TAM───SAM───SOM──
```

**Draw a second, revenue-bar rule only if the user named a number** ("does this clear $10M ARR?").
This skill carries no revenue bar of its own and invents none – see House rules.

The vertical distance between the SOM bars and the capacity line is the finding from Step 6, and
this is where a reader sees it without doing arithmetic. Label every rule directly with its
value.

Palette: categorical slots 1 and 2 for the demand builds (`#2a78d6`
blue, `#eb6834` orange in light; `#3987e5` / `#d95926` in dark) and **slot 3 aqua for capacity**
(`#1baf7a` light, `#199e70` dark). A reference rule is a threshold, not a series: draw it in
secondary text colour, dashed. Light **and** dark variants, values direct-labelled. Read the PNG
afterwards and eyeball it for label collisions before calling it done.

---

## Step 9 – Write the note

`market-sizing.md`. Self-contained: a reader must decode it without opening another file.

```
 1  Frontmatter      title, company, created, author, status, tags
 2  Answer up front  the range in one sentence, all three builds named, and
                     which constraint binds – market or company
 3  How to read      flags (incl. OB and C), currency, the three builds,
                     the 5-year horizon, every abbreviation
 4  The claim        what the deck said, and its source
 5  Market boundary  the specific problem the market is bounded by
 6  Bottom-up        the formula, every term, every source
 7  Top-down         every cut, with rationale
 8  Triangulation    converged or not – and the diagnosis if not
 9  TAM / SAM / SOM  the narrowing, share assumption + horizon + model stated
10  Capacity ceiling motion, formula, every input with its flag; funded-plan
                     headline and current-team floor; the gap vs SOM, and which
                     of the two is the lower ceiling – the market or the machine
11  Limits           what would move the number most; what you could not verify
12  Sources          full table, every row with a working URL or a stated reason
```

**Diagram-first** for anything structural (the funnel, the cuts, the comparison). Prose for
findings and caveats.

---

## Step 10 – Verify, then wrap up

- **All three builds present** – bottom-up, top-down, capacity. A run without a capacity build is
  incomplete, not "capacity build not applicable".
- Every CSV row has a flag; every `D`/`PM` row has a URL.
- **Every `C` row has a non-empty `formula`, and every row with a non-empty `formula` is `C`.**
- **Every `OB` row names its benchmark and carries a URL.** If it can't, it is an `A` row.
- SOM states its horizon (5 years) and the business model it assumes.
- The capacity ceiling is computed over that same horizon, with funded-plan and current-team
  figures reported separately.
- Numbers in the note recomputed **from the CSV**, not from working notes.
- The chart matches the CSV, including every reference line drawn on it.
- Every abbreviation expanded in the note itself.
- Chat summary, short: the range, whether the two demand builds converged, the deck-vs-yours gap
  and its mechanism, **the gap between SOM and the capacity ceiling and which of the two is the
  lower ceiling**, and the one thing that would most move the number.
- Last line of the chat summary: "Next step: `/fundraise:competitors`".

## House rules

- **No naked numbers.** Sourced, flagged as an assumption, or arithmetic over rows that are.
- **A count is not a list.** If you state a population, the enumeration exists or the note says it
  doesn't.
- **Ranges over point estimates.** Report the band the evidence supports.
- **Never source a market size from the deck** and then compare it to the deck.
- **Never skip the capacity build for lack of data.** Benchmark it and flag it – see Step 6.
- **A market is bounded by a problem, not a category** – see Step 1.
- Dates absolute ISO. Currency native, conversion rate stated inline where used.
- **No revenue bar of its own.** This skill reports what the market could support and what the
  company's machine can reach, and stops. It carries no fund's screen, threshold or pass/fail
  test. If the user names a bar, answer against *that* number and say whose it is.
- Findings are research artifacts, not picks. This skill produces no investment recommendation.

## Field notes from validation runs

Lessons from private runs on real companies, kept here until they are folded into the steps
above. The companies are not named.

- **Step 6 – the capital check applies to any motion whose unit of delivery is a financed
  asset**, not only to roll-ups. Data centres, clinics, fleets and plants are `OPS-DELIVERED` by
  motion, but the binding number can be the capital the ramp implies. In one run the throughput
  ceiling came out at USD 419m a year – real, but not binding; the ramp needed USD 4–6bn against
  a nominal share capital. Compute the capital line beside the throughput line.
- **Step 2 – when a company sells the same physical unit two ways, size the primitive once and
  price it twice.** Sizing the two markets separately and adding them double-counts the asset.
  Sizing in physical units (for example megawatts) and pricing them both ways exposed a 13–18×
  revenue swing on roughly 2× the capital – the largest sensitivity in that run.
- **Step 3 – interrogate a non-converging build line by line before blaming the definitions.**
  Two builds 2.2× apart came down to one row (state-built capacity that appears in no published
  market figure and cannot be sold to the subject). Removing it took the gap to 1.3×, and the
  diagnosis itself was the finding.
- **Step 2 – where announced supply stands in for demand, calibrate it in the one market that
  publishes both sides**, derive the overshoot factor there, apply it elsewhere, and state it as
  the top limit of the note.
- **Where no published price benchmark exists, derive one from a single publisher's own revenue
  and capacity forecasts** – internally consistent, and checkable against any broker band.

## Changelog

- **v0.4 (2026-11-11):** reads and fills the shared company card (`company-profile.md`); the chat
  summary ends with the next step, `/fundraise:competitors`. Release fix the same day: two
  motions are added only when parallel; sequential gates take the lower ceiling.
- **v0.3 (2026-11-10): first public release** in the fundraising skill pack. Output paths made
  generic; machine-specific instructions removed; run history condensed into the field notes.
- **v0.3 (2026-09-01):** the borrowed fund screen and its pass/fail verdict removed. The skill
  reports what the market could support and what the company's machine can reach, and stops.
- **v0.2 (2026-08-06): the capacity build** (Step 6), the 5-year SOM horizon, and the `OB` and
  `C` flags.
- **v0 (2026-08-03):** built. Two independent demand builds, because a single method is
  unfalsifiable.
