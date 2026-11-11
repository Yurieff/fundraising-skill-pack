---
name: metrics-pack
description: Turns a startup's revenue data into MRR (monthly recurring revenue), cohorts, NRR (net revenue retention) and one investor slide. Reads monthly update files, a per-customer revenue export, or a contracts register (client, contract value, start month, term). All arithmetic is done by a tested Python helper, never in prose. Separates billed months from contracted-but-not-yet-billed months, reports contracts shorter than three months as non-recurring, and says "cannot compute yet" for a 12-month NRR when no customer has run twelve months. Produces a plain-English note, four CSVs and one 16:9 slide. Invoke when the user says "build the metrics pack for X", "MRR, cohorts and NRR for X", "what is X's net revenue retention", or "/metrics-pack X".
version: 0.1
---

# Metrics Pack

## What you're doing

You've been asked to turn a startup's revenue data into the numbers a fund analyst reads first:
MRR, cohorts, NRR – on one slide. **The numbers come from `metrics.py`, never from your head.**
You choose the input, run the helper, read its CSVs, and write the words around them.

```
  INPUT                    HELPER (metrics.py)            YOU
  ─────                    ───────────────────            ───
  updates/  (a)  ──┐
  customer export (b) ─┼──►  mrr.csv  cohorts.csv  ──►  metrics.md   (plain English)
  contracts register (c) ┘    nrr.csv  excluded.csv      metrics-slide.png (one slide)
```

Deliverables in `<company-slug>/metrics-pack/`, relative to the current working directory:

1. **`metrics.md`** – the note. Opens with "In plain English."
2. **`mrr.csv`, `cohorts.csv`, `nrr.csv`** (and **`excluded.csv`** for a contracts register) –
   written by the helper, untouched by you.
3. **`metrics-slide.png`** – one 16:9 slide.

Abbreviations used in this file: MRR = monthly recurring revenue; NRR = net revenue retention;
CSV = comma-separated values file; PNG = image file; ISO = the international date format
(`YYYY-MM-DD`, or `YYYY-MM` for a month); EUR = euro; USD = United States dollar; `--as-of` = the
helper option that names the last billed month.

## Inputs

From `$ARGUMENTS` or the conversation: **a company**, and optionally a file. Three kinds of input,
in this order of preference:

| Input | What it is | How it enters the helper |
|---|---|---|
| (b) per-customer export | CSV `customer_id,month,revenue`, month as `YYYY-MM` | `--revenue <csv>` |
| (c) contracts register | CSV with a header row `Client, Contract value, Start month, Term (months)`; lines above the header are skipped; months like `May-26`; values like `"1,550,000"` | `--contracts <csv>` |
| (a) `<company-slug>/updates/` | monthly update files with a revenue line, no customer detail | read as `revenue-chart` does (Step 2 there), write `customer_id,month,revenue` with one customer `total`, then `--revenue` |

With input (a) there are no customers. The helper then writes `cohorts.csv` and `nrr.csv` with
only a header and leaves the `new`, `expansion`, `contraction` and `churned` cells of `mrr.csv`
empty, because with one customer they would only restate total growth. Ignore those columns,
show no heatmap, and print "12-month NRR: cannot compute yet" (reason: no customer detail).
The same holds for any `--revenue` file with a single customer id.

If the company is ambiguous (two firms share the name), ask which one before reading anything.

---

## Step 1 – Company card and input

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

Take the company name, business model, revenue model and geography from the card; geography
suggests the currency to expect. Fill "Metrics available" with the file you use. If the revenue
model is not subscription, say in the note that MRR assumes recurring revenue.

Find the input (table above) and copy it into `<company-slug>/metrics-pack/input/` so the run is
auditable. Never commit or publish a customer-level file unless the owner has said it may be
public. **Currency:** take it from the file; a contracts register often states none. If none is
stated, write "currency not stated" everywhere and never pick one.

**Today and `--as-of`.** `--as-of` is the last month that has actually been billed – normally
the current month, from today's date (ISO). Months after it are *contracted*: signed, not yet
billed.

---

## Step 2 – Run the helper

Use `/usr/bin/python3` or any Python 3.9+; `metrics.py` needs only the standard library and makes
no network calls. It sits next to this file (`skills/metrics-pack/metrics.py`; in an installed
plugin, `${CLAUDE_PLUGIN_ROOT}/skills/metrics-pack/metrics.py`).

```bash
python3 <path>/metrics.py --contracts <register.csv> --out-dir <company-slug>/metrics-pack \
        --as-of 2026-11 --min-term 3
python3 <path>/metrics.py --revenue <export.csv>     --out-dir <company-slug>/metrics-pack \
        --as-of 2026-11
```

What it writes:

| File | Columns | Meaning |
|---|---|---|
| `mrr.csv` | `month, mrr, new, expansion, contraction, churned, status` | one row per calendar month; `status` is `billed` up to `--as-of`, `contracted` after |
| `cohorts.csv` | `cohort, month_offset, revenue` | cohort = a customer's first month with revenue; offset = months since then |
| `nrr.csv` | `start_month, months, nrr` | 12-month NRR for every start month where it can be computed from **billed** months only (a month after `--as-of` never counts); header only if none can. Also header only for a single-customer export, and for a contracts register with no recorded renewal; for a register, only start months in which some client has a recorded renewal (rule in Step 2) are listed |
| `excluded.csv` | `client, value, start, term` | contracts shorter than `--min-term` months (default 3) |

If the helper stops with `error:`, it names the bad column or value. Fix the input at the source
(or ask the owner) – never edit around it.

**What the helper assumes (state each in the note):**

- Contract value is the **total over the term**, spread evenly: value ÷ term per month, from the
  start month. If the owner says it is per month or per year, stop and ask – the answer changes
  every number.
- A contract is recurring only if its term is at least `--min-term` months. Shorter ones are
  *non-recurring*: reported in `excluded.csv`, not in MRR.
- Nothing renews unless a new row says so. When a contract's term ends, the helper shows the
  revenue leaving as `churned`. In a contracts register that is **contract end, not proven
  churn** – say so for every such month.
- **A contracts register records contracts, not renewals.** Contract end reads as lost revenue,
  so the helper computes `nrr.csv` from a register only for start months in which some client has
  a **recorded renewal**. Rule: a renewal is a later recurring contract (term at least
  `--min-term`) of the same client whose start month is at least one month after the end month
  of an earlier recurring contract (end month = start month + term - 1; so a back-to-back
  contract starting the month after the end counts, and a gap is allowed). A second contract
  that overlaps the first (an upsell or add-on) is **not** a renewal. If no client has a
  renewal, `nrr.csv` is header only and the answer is "cannot compute yet". If some do, the
  figure reflects **only the renewals the register records** and the note and the slide must
  say so.
- A customer who stops and later returns counts as `new` again.

---

## Step 3 – Read the outputs

Read the CSVs with the `csv` module. Every number you write comes from them. Compute nothing in
prose; if you need a number the CSVs lack (for example a share), compute it with a command and
quote the command's output.

1. **MRR.** The last billed month's `mrr`; the peak month and its `status`; the
   billed-to-contracted split. Name the first and last month in the data.
2. **Run-off.** Months after the last contract start only lose revenue, because nothing in the
   data renews. Mark them as run-off of contracts without renewal, never as churn.
3. **Cohorts.** Count cohorts with at least two months of **billed** revenue. The heatmap on the
   slide needs at least two such cohorts; otherwise skip it and say why.
4. **NRR.** First check the input. For input (a) or a single-customer export, ignore `nrr.csv`,
   `cohorts.csv` and the movement columns: the answer is "cannot compute yet". Otherwise, if
   `nrr.csv` has data rows, quote them; for a contracts register add "counts only renewals
   recorded in the register". If it has only the header, the answer is
   **"12-month NRR cannot be computed yet"**: no customer has a revenue month twelve months
   after its start. Never estimate it, never fill it from a shorter window. Give the reason in
   one line (for example "every contract in the register starts in 2026, so none has run twelve
   months and renewed").
5. **Excluded.** Number of excluded contracts, their total value, and the rule that excluded them.

---

## Step 4 – metrics-slide.png

Needs matplotlib and numpy (`python3 -c "import matplotlib, numpy"`). If missing, ask before
installing anything; the clean route is a throwaway virtual environment. The base is the chart
template in `revenue-chart` (dark theme, label-collision check).

One 16:9 slide, in this layout:

```
 ┌─────────────────────────────────────────────────────────────┐
 │ <Company> – revenue metrics            as of <ISO date>       │
 ├──────────────────────────────┬──────────────────────────────┤
 │ MRR line: solid = billed,    │ cohort heatmap (billed months │
 │ dashed + shaded = contracted │ only, % of month 0) – or the  │
 │                              │ NRR panel if no heatmap       │
 ├──────────────────────────────┴──────────────────────────────┤
 │ NRR: <figure>  or  "12-month NRR: cannot compute yet"         │
 │ three one-line takeaways                                       │
 └─────────────────────────────────────────────────────────────┘
```

Rules for the slide:

- **Contracted is never styled as billed.** Months after `--as-of` use a dashed line, hollow
  markers and a labelled shaded band "contracted, not yet billed".
- For a contracts register, a shown NRR figure carries the caveat "counts only renewals recorded
  in the register" (the script adds it when `source = "register"`).
- The NRR line shows the figure from `nrr.csv`, or the exact words "12-month NRR: cannot compute
  yet".
- Heatmap only if at least two cohorts have at least two billed months.
- Three one-line takeaways, each traceable to a CSV row, none a recommendation or a prediction.
- Currency in the axis title; "currency not stated" if the source gave none.
- All figures on the slide are read from the CSVs by the script, not typed in. The takeaways are
  the only typed text: check each number in them against the CSVs after drawing.

```python
import csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# CONFIGURE ---------------------------------------------------------------
company  = "Company"
folder   = "<company-slug>/metrics-pack"
currency = "currency not stated"      # or "EUR", "USD" ...
as_of    = "2026-11"                  # same value as --as-of
source   = "register"                 # "register" (--contracts) or "export" (--revenue)
takeaways = [                         # three one-liners, each checked against the CSVs
    "Takeaway 1",
    "Takeaway 2",
    "Takeaway 3",
]
# -------------------------------------------------------------------------

def read(name):
    with open(os.path.join(folder, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

mrr, coh, nrr_rows = read("mrr.csv"), read("cohorts.csv"), read("nrr.csv")
months = [r["month"] for r in mrr]
vals = [float(r["mrr"]) for r in mrr]
billed = [r["status"] == "billed" for r in mrr]
x = np.arange(len(months))
nb = sum(billed)                                   # billed months come first

BG, FG, MUTED = '#0f1117', '#e0e0e0', '#9aa0b4'
BILLED, CONTR = '#4fc3f7', '#f2b84b'

fig = plt.figure(figsize=(13.333, 7.5), facecolor=BG)         # 16:9
gs = fig.add_gridspec(3, 2, height_ratios=[0.5, 5.2, 1.9], width_ratios=[1.35, 1],
                      hspace=0.35, wspace=0.18, left=0.06, right=0.97, top=0.97, bottom=0.04)
ax_t = fig.add_subplot(gs[0, :]); ax_t.axis('off')
ax_t.text(0, 0.5, f"{company} – revenue metrics", color='#fff', fontsize=20,
          fontweight='bold', va='center')
ax_t.text(1, 0.5, f"billed through {as_of}", color=MUTED, fontsize=11, ha='right', va='center')

# --- MRR line ---
ax = fig.add_subplot(gs[1, 0]); ax.set_facecolor(BG)
if nb < len(months):
    ax.axvspan(nb - 0.5, len(months) - 0.5, color=CONTR, alpha=0.10, zorder=0)
    ax.text(nb - 0.35, 0.97, "contracted,\nnot yet billed", color=CONTR, fontsize=9,
            transform=ax.get_xaxis_transform(), va='top')
ax.plot(x[:nb], vals[:nb], color=BILLED, lw=2.6, marker='o', ms=5, label='billed MRR', zorder=3)
if nb < len(months):
    j = max(nb - 1, 0)                                         # join the two segments
    ax.plot(x[j:], vals[j:], color=CONTR, lw=2.2, ls='--',
            label='contracted MRR (not billed)', zorder=3)
    ax.scatter(x[nb:], vals[nb:], s=28, facecolors=BG, edgecolors=CONTR, zorder=4)  # hollow
ax.set_ylim(0, max(vals) * 1.18)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v/1e6:.1f}m' if max(vals) >= 2e6 else f'{v/1e3:.0f}k'))
step = max(1, len(months) // 8)
ax.set_xticks(x[::step]); ax.set_xticklabels(months[::step], fontsize=9, color=FG, rotation=45, ha='right')
ax.tick_params(axis='y', labelcolor=FG, labelsize=9)
ax.set_ylabel(f"MRR ({currency})", color=MUTED, fontsize=10)
ax.set_title("Monthly recurring revenue (MRR)", color='#fff', fontsize=12, loc='left')
ax.grid(axis='y', color='#1e2030', ls='--', lw=0.8)
for s in ax.spines.values(): s.set_edgecolor('#2a2a3a')
ax.legend(loc='upper left', bbox_to_anchor=(0, 0.86), facecolor='#1a1d2e', edgecolor='#2a2a3a',
          labelcolor=FG, fontsize=9)

# --- cohort heatmap (billed months only) or NRR panel ---
cohorts = {}
for r in coh:
    c, off = r["cohort"], int(r["month_offset"])
    if months.index(c) + off < nb:                              # billed months only
        cohorts.setdefault(c, {})[off] = float(r["revenue"])
usable = {c: d for c, d in cohorts.items() if len(d) >= 2}
ax2 = fig.add_subplot(gs[1, 1]); ax2.set_facecolor(BG)
if len(usable) >= 2:
    names = sorted(usable); width = max(max(d) for d in usable.values()) + 1
    grid = np.full((len(names), width), np.nan)
    for i, c in enumerate(names):
        for off, v in usable[c].items():
            grid[i, off] = v / usable[c][0] * 100
    im = ax2.imshow(grid, cmap='viridis', vmin=0, vmax=max(120, np.nanmax(grid)), aspect='auto')
    ax2.set_yticks(range(len(names))); ax2.set_yticklabels(names, fontsize=8, color=FG)
    ax2.set_xticks(range(width)); ax2.set_xticklabels(range(width), fontsize=8, color=FG)
    ax2.set_xlabel("months since cohort start", color=MUTED, fontsize=9)
    ax2.set_title("Cohorts: revenue as % of month 0 (billed months)", color='#fff', fontsize=12, loc='left')
    for i in range(len(names)):
        for j in range(width):
            if not np.isnan(grid[i, j]) and len(names) <= 14 and width <= 14:
                ax2.text(j, i, f"{grid[i, j]:.0f}", ha='center', va='center', fontsize=7,
                         color='#fff' if grid[i, j] < 90 else '#111')
else:
    ax2.axis('off')
    ax2.text(0, 0.9, "No cohort heatmap", color='#fff', fontsize=12, fontweight='bold')
    ax2.text(0, 0.78, "fewer than two cohorts have two\nbilled months of history", color=MUTED, fontsize=10, va='top')
for s in ax2.spines.values(): s.set_edgecolor('#2a2a3a')

# --- NRR figure and takeaways ---
ax3 = fig.add_subplot(gs[2, :]); ax3.axis('off')
if nrr_rows:
    last = nrr_rows[-1]
    nrr_text = f"12-month NRR: {float(last['nrr'])*100:.0f}%  (start {last['start_month']})"
    if source == "register":
        nrr_text += " – counts only renewals recorded in the register"
else:
    nrr_text = "12-month NRR: cannot compute yet"
ax3.text(0, 0.95, nrr_text, color=BILLED, fontsize=16, fontweight='bold', va='top')
for i, t in enumerate(takeaways):
    ax3.text(0, 0.62 - i * 0.2, f"{i+1}.  {t}", color=FG, fontsize=11.5, va='top')

out = os.path.join(folder, "metrics-slide.png")
fig.savefig(out, dpi=150, facecolor=BG)
print("Saved:", out)
```

After running the script, confirm the file exists, **open the PNG and check it for label
collisions** (legend over the line, band label over a marker, takeaway text running off the
edge). Fix and redraw until clean.

---

## Step 5 – metrics.md

Self-contained: a reader must follow it without opening another file. Frontmatter: `title`,
`company`, `created` (ISO date), `author`, `status: draft`.

```
 1  In plain English.   one short paragraph, no jargon: what the company bills today, what is
                         signed but not yet billed, whether customers have stayed long enough
                         to measure retention, what was left out and why
 2  Answer up front    last billed MRR · peak MRR and its status · NRR (figure or "cannot
                         compute yet") · number of excluded contracts
 3  How to read        MRR, cohort and NRR explained in plain words (below) and every
                         abbreviation expanded
 4  MRR                table from mrr.csv (month · MRR · new · expansion · contraction ·
                         churned · status); run-off months marked "contract end, renewal not
                         recorded"
 5  Cohorts            what the heatmap shows, or why there is none
 6  NRR                the figure and its start month (for a register: "counts only renewals recorded
                         in the register"), or "cannot compute yet" with the reason
 7  Excluded           table from excluded.csv and the rule that excluded each
 8  Assumptions        each helper assumption from Step 2, plus currency and input quality
 9  Limits             what the data cannot show; nothing here is a forecast or a recommendation
10  Sources            input file (name, retrieval date), helper version, CSVs produced
```

Plain-words definitions to carry into section 3:

- **MRR (monthly recurring revenue):** what the company bills each month from contracts that
  repeat. One-off work is not MRR.
- **Cohort:** the customers who started in the same month, followed over time.
- **NRR (net revenue retention):** take the customers you had in one month; ask how much those
  same customers pay twelve months later, as a share of what they paid then. Above 100% means the
  company grows even with no new customers; below 100% means it leaks. It needs twelve months of
  history, so a young company often cannot show it yet – and that is an answer, not a gap to fill.
- **Billed vs contracted:** billed months have happened; contracted months are signed but lie in
  the future and can still change.

---

## Step 6 – Verify, then wrap up

Run these as commands, not by eye:

- `head -1` of each CSV equals the column list in Step 2, exactly.
- The slide's figures (last billed MRR, peak, NRR text, takeaway numbers) match `mrr.csv` and
  `nrr.csv`: print them from the CSVs and compare.
- Every excluded contract in `excluded.csv` appears in the note.
- If `nrr.csv` has no data row (or the input is (a) or a single-customer export), both the note and the slide say "cannot compute yet".
- Every month after `--as-of` is `contracted` in `mrr.csv` and drawn dashed on the slide.
- The note states the currency, or "currency not stated".
- No em dash in any file; every abbreviation expanded.
- Chat summary, short: last billed MRR, contracted months ahead, NRR status, excluded count, the
  paths of the files.
- Last line of the chat summary: "Next step: `/fundraise:readiness-check`".

## House rules

- **Numbers only from `metrics.py` output.** Prose never computes.
- **Contracted is not billed.** Future months are labelled as such wherever they appear.
- **One-month and other short contracts are non-recurring.** Reported, never in MRR.
- **"Cannot compute" is an answer.** No estimated, extrapolated or short-window NRR.
- **Contract end is not churn.** Without renewal data the helper's `churned` column in run-off
  months means contracts reached their end.
- Dates absolute ISO. Every abbreviation expanded in the file that uses it.
- **No investment recommendation, no forecast.** The pack reports what the data shows and stops.
- A customer-level file stays private unless its owner says otherwise.

## Changelog

- **v0.1 (2026-11-11): first version.** `metrics.py` (MRR, cohorts, NRR from a revenue export or
  a contracts register) with tests; the one-slide template; reads and fills the shared company
  card; the report ends with the next step, `/fundraise:readiness-check`.
