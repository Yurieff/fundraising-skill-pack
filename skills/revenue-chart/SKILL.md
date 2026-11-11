---
name: revenue-chart
description: Reads all monthly update files for a startup (investor updates, board updates, monthly reports), builds a revenue dynamics table (revenue-dynamics.md) with month-over-month analysis and a dark-themed matplotlib chart (revenue-dynamics.png), and saves both to the company's revenue-chart/ folder. Invoke when the user asks to "create a revenue chart", "show revenue dynamics" for a company, or "/revenue-chart X".
version: 2.4
---

# Revenue Chart

## What you're doing

You've been asked to produce a revenue dynamics summary for a startup – your own, or one you
advise or track. Your job is to:

```
  READ UPDATES  ──►  EXTRACT REVENUE  ──►  TABLE + OBSERVATIONS  ──►  CHART
  every month        total + product        revenue-dynamics.md       revenue-dynamics.png
                     lines, flagged
```

1. Read all update files in the company's `updates/` folder
2. Extract monthly revenue figures and any product-level breakdown
3. Write a structured `revenue-dynamics.md` table with MoM (month-over-month) analysis and key
   observations
4. Generate a dark-themed `revenue-dynamics.png` chart using Python + matplotlib
5. Save both files to `revenue-chart/`

## Inputs

From `$ARGUMENTS` or the conversation: **a company**, and optionally a folder. The default layout,
relative to the current working directory, is:

```
  <company-slug>/
  ├── updates/                                input – one file per update
  │   ├── 2026-01-31-<company>-monthly.md
  │   ├── 2026-02-28-<company>-monthly.md
  │   └── …
  └── revenue-chart/                          output – this skill writes here
      ├── revenue-dynamics.md
      └── revenue-dynamics.png
```

If the user points at a different folder, or pastes the updates into the conversation, work from
that instead and still save the outputs to `<company-slug>/revenue-chart/`. Updates in PDF or another format: convert
or read them first, and say which files you could not read.

---

## Step 1 – Identify the company and find update files

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

Use the card instead of re-researching what it already holds: take the company name, business model and geography
from it (they set the currency to expect), and fill "Metrics available" with the update files
you find.

Confirm the company folder. List all update files in its `updates/` folder. If
`revenue-chart/revenue-dynamics.md` already exists, you will overwrite it.

---

## Step 2 – Extract revenue data

Read each update file. For each month, extract:

- **Date** – from the filename (`YYYY-MM-DD-<company>-monthly.md` → use that date to determine
  which month is covered), or from the update's own heading if the filename has no date
- **Total revenue** – look for a table row or line matching any of: `Revenue`, `MRR`,
  `Total revenue`, `Revenue (MRR)`, `Revenue (net)` (MRR = monthly recurring revenue)
- **Revenue breakdown** – if the update shows multiple revenue lines per product, capture each
  separately

Rules:

- Keep the company's own currency. Strip currency symbols and convert to a plain number in
  thousands (e.g. `€37,154.66` → `37.2`, `$51k` → `51`)
- If a figure is approximate (e.g. `~€22k`), mark it as estimated in the notes column
- If an update covers multiple months in one file (e.g. a summer recap "Jun–Sep"), extract each
  month separately
- If a month's revenue is not stated directly but can be inferred from a later update's MoM
  percentage (e.g. "Nov was €24k at +7% MoM"), note it as inferred and calculate the implied prior
  month value
- If no revenue figure is available for a month, skip that month rather than guessing
- Net vs gross, MRR vs recognised revenue: if the updates switch definitions, say so in a
  footnote – never chain two definitions into one line silently

Build a list of `(month_label, total_revenue, [breakdown_dict_or_None], notes)` tuples ordered
chronologically.

---

## Step 3 – Write revenue-dynamics.md

Save to `<company-slug>/revenue-chart/revenue-dynamics.md`.

### Format

```markdown
# [Company] – Revenue Dynamics

**Period:** [first month] – [last month] ([N] months)
**Last updated:** [today's date, ISO]
**Currency:** [currency], thousands

## Monthly Revenue Table

| Month | Total (k) | [Product A (k)] | [Product B (k)] | MoM (k) | MoM (%) | Notes |
|-------|-----------|-----------------|-----------------|---------|---------|-------|
| ...   | ...       | ...             | ...             | ...     | ...     | ...   |

*[Any data quality footnotes – inferred values, net vs gross, etc.]*

## Key Observations

**Overall trend:** [Revenue grew from X to Y – +Z% over N months.]

**[Pattern 1]:** [e.g. product mix shift, seasonality, breakout month]

**[Pattern 2]:** [another notable dynamic]

**[Anomaly, if any]:** [e.g. one-off burn spike, stock-out effect]

**Diagram:** [see revenue-dynamics.png]

## Sources

| Month | Update file |
|-------|-------------|
| ...   | ...         |
```

Rules:

- Include product breakdown columns only if the data exists for at least the most recent 3 months
- Omit the breakdown columns if revenue is single-line throughout
- MoM for the first row is always `–`
- Mark inferred/estimated values with `~` prefix and a footnote
- Every number traces to an update file in the Sources table

---

## Step 4 – Generate revenue-dynamics.png

Use any Python 3 that has matplotlib and numpy (`python3 -c "import matplotlib, numpy"` to check).
If none does, ask the user before installing anything; the clean route is a throwaway virtual
environment (`python3 -m venv` + `pip install matplotlib numpy`), never a system-wide
`pip install`.

Use the following Python template. Fill in the `# CONFIGURE` section for the specific company.

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# CONFIGURE ---------------------------------------------------------------
months   = [...]          # x-axis labels, e.g. ["Jan\n2025", "Feb", ...]
total    = [...]          # total revenue in thousands, one value per month
currency = "€"            # the company's own currency symbol; use r"\$" for dollars

# Set has_breakdown = True if you have per-product revenue for >= 3 months.
# Fill product_a / product_b only for the months where data exists;
# use None for months where breakdown is unavailable.
has_breakdown = False
product_a_label = "Product A"
product_b_label = "Product B"
product_a = [None, None, 14, 15, ...]   # None = no data for that month
product_b = [None, None, 10, 22, ...]

# Shade zones: list of (x_start, x_end, hex_color, alpha, legend_label)
# Use 0-based float index positions (e.g. 5.5 to 8.5). Set to [] if none.
shade_zones = [
    (start_idx - 0.5, end_idx + 0.5, '#888888', 0.13, 'Label for this zone'),
]

# Key annotations: {x_index: (label_text, y_offset, color)}
# Positive y_offset = label above the point; negative = below
annotations = {
    5: (f"First {currency}50k", 5, '#e0e0e0'),
}

company_name = "Company"
out_path     = "<company-slug>/revenue-chart/revenue-dynamics.png"
# -------------------------------------------------------------------------

x = np.arange(len(months))

fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#0f1117')

for (x0, x1, col, alpha, lbl) in shade_zones:
    ax.axvspan(x0, x1, alpha=alpha, color=col)

if has_breakdown:
    split_x = [i for i, v in enumerate(product_a) if v is not None]
    pa = [product_a[i] for i in split_x]
    pb = [product_b[i] for i in split_x]
    ax.bar(split_x, pa, color='#5b8dee', alpha=0.75, label=product_a_label, width=0.55, zorder=2)
    ax.bar(split_x, pb, bottom=pa, color='#f06292', alpha=0.80, label=product_b_label, width=0.55, zorder=2)

line_color = '#4fc3f7' if not has_breakdown else '#ffffff'
ax.plot(x, total, color=line_color, linewidth=2.5, zorder=4, label='Total revenue')
ax.scatter(x, total, color=line_color, s=55, zorder=5)
if not has_breakdown:
    ax.fill_between(x, total, alpha=0.12, color='#4fc3f7')

for idx, (label, yoff, col) in annotations.items():
    va = 'bottom' if yoff > 0 else 'top'
    ax.annotate(label, xy=(x[idx], total[idx]),
                xytext=(x[idx], total[idx] + yoff),
                ha='center', va=va, fontsize=7.5, color=col,
                arrowprops=dict(arrowstyle='->', color='#666677', lw=0.9),
                bbox=dict(boxstyle='round,pad=0.25', fc='#1a1d2e', ec='none', alpha=0.85))

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{currency}{v:.0f}k'))
ax.set_ylim(0, max(total) * 1.30)
ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=9, color='#cccccc')
ax.tick_params(axis='y', labelcolor='#cccccc', labelsize=9)
ax.set_xlabel('Month', color='#aaaaaa', fontsize=10, labelpad=8)
ax.set_ylabel('Monthly Revenue', color='#aaaaaa', fontsize=10, labelpad=8)
ax.set_title(
    f'{company_name} – Revenue Dynamics  '
    f'({months[0].replace(chr(10)," ")} – {months[-1].replace(chr(10)," ")})',
    color='#ffffff', fontsize=14, pad=16, fontweight='bold')

for spine in ax.spines.values():
    spine.set_edgecolor('#2a2a3a')
ax.grid(axis='y', color='#1e2030', linestyle='--', linewidth=0.8)
ax.grid(axis='x', color='#171720', linestyle=':', linewidth=0.5)

handles = [plt.Line2D([0],[0], color=line_color, linewidth=2, label='Total revenue')]
if has_breakdown:
    handles += [mpatches.Patch(color='#f06292', alpha=0.85, label=product_b_label),
                mpatches.Patch(color='#5b8dee', alpha=0.8,  label=product_a_label)]
for (_, _, col, alpha, lbl) in shade_zones:
    handles.append(mpatches.Patch(color=col, alpha=min(alpha*3, 1), label=lbl))
ax.legend(handles=handles, loc='upper left',
          facecolor='#1a1d2e', edgecolor='#2a2a3a',
          labelcolor='#cccccc', fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.savefig(out_path, dpi=150, facecolor=fig.get_facecolor())
print("Saved:", out_path)
```

After running the script, confirm the file was created at the expected path, then open the PNG
and check it for label collisions.

---

## Step 5 – Confirm output

Report back:

- How many months of data were found
- Date range covered
- Whether a product breakdown was included
- Any months where data was missing or inferred
- Paths of both saved files
- Last line: "Next step: `/fundraise:metrics-pack`"

## House rules

- **No guessed months.** A month without a stated or inferable figure is skipped, and the note
  says so.
- Dates absolute ISO. Currency native, stated in the table header.
- Every abbreviation expanded in the file that uses it.
- The table is a reading of the company's own updates, not an audit: say so if the updates
  contradict each other.

## Changelog

- **v2.4 (2026-11-11):** reads and fills the shared company card; the report ends with the next
  step, `/fundraise:metrics-pack`.
- **v2.3 (2026-11-11):** output moves to `<company-slug>/revenue-chart/`; updates are read from
  `<company-slug>/updates/`.
- **v2.2 (2026-11-10): first public release** in the fundraising skill pack. Generic folder
  layout, currency as a parameter, a sources table, machine-specific instructions removed.
- v2 (2026-08-04): reads and writes `10_company-materials/updates/`.
- v1 (2026-05-06): initial version – tested on two companies' monthly updates (17 months
  single-line; 10 months with a two-product breakdown).
