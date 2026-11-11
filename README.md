# Fundraising skill pack

Claude Code skills that check a startup the way a fund analyst would – before it raises.

**In plain English.** Founders often go to investors with a market size copied from someone
else's report, a "we have no direct competitors" slide and a revenue chart nobody has checked.
An analyst at a fund takes these apart in an hour. This pack lets Claude Code do the same work
first, on your own startup, from public sources: it sizes the market two ways and checks whether
your team can actually reach it, maps your competitors with their prices, funding and exits, and
turns your monthly updates into a revenue table and chart. Every number in the output carries a
source you can open.

> **Status: v0.6 – early release.** The skills have been run on real companies, but they are
> still being refined. Expect changes. Feedback and issues are welcome.

## The five steps

Run the skills in this order. Each one reads what the earlier ones wrote, through one shared
company card.

```
                       <company-slug>/company-profile.md   ← created by the first skill run,
                                      │                      read and filled by all others
                                      ▼
 1 thesis-fit ──► 2 market-size ──► 3 competitors ──► 4 metrics-pack ──► 5 readiness-check
   chosen funds:    two demand        full competitor   MRR, cohorts,      deck + everything
   thesis, real     builds +          set, prices,      NRR, one slide     above → "these points
   portfolio, fit   capacity          funding, M&A                         may raise doubts with
       │                                  ▲                                funds"
       └─► competitor-candidates/ ────────┘  (portfolio companies that look like competitors)
```

MRR = monthly recurring revenue. NRR = net revenue retention. TAM / SAM / SOM = total,
serviceable and obtainable market. M&A = mergers and acquisitions.

## What's inside

| # | Skill | What it answers | Status |
|---|---|---|---|
| 1 | `thesis-fit` | For each fund you choose: does your startup match its stated thesis and the companies it actually backed? Which portfolio companies look like your competitors? | v0 |
| 2 | `market-size` | How big is the market – and can this company's sales and delivery machine actually reach it? TAM / SAM / SOM built bottom-up and top-down, plus a capacity ceiling | working |
| 3 | `competitors` | Who else does this job, at what price, on whose money – and what have companies like this sold for? Note, CSV (comma-separated values) file, price chart, two-sheet Excel workbook | working |
| 4 | `metrics-pack` | What do the revenue data say – MRR, cohorts and NRR? Separates billed from contracted months, reports short contracts as non-recurring, says "cannot compute yet" when NRR needs history the data lacks. Note, four CSVs, one investor slide | v0 |
| 5 | `readiness-check` | Which points in your deck and numbers may raise doubts with funds – each with the slide, the evidence, why a fund may doubt it, how to fix it and a severity. Checks that need an earlier skill's output are skipped and name that skill. It lists doubts and gives no investment recommendation | v0 |
| – | `revenue-chart` | What do the monthly updates say about revenue, month by month? Table with month-over-month analysis, chart. Stays until replaced by `metrics-pack` | working |

## Install

You need [Claude Code](https://claude.com/claude-code). In Claude Code, run:

```
/plugin marketplace add Yurieff/fundraising-skill-pack
/plugin install fundraise@yurieff
```

Restart Claude Code if it asks you to. To get new versions later:

```
/plugin marketplace update yurieff
```

**Used an early version?** The plugin was called `fundraising-skill-pack` and is now `fundraise`.
Remove the old one, then install the new one:

```
/plugin uninstall fundraising-skill-pack@yurieff
/plugin install fundraise@yurieff
```

Commands change from `/fundraising-skill-pack:<skill>` to `/fundraise:<skill>`.

**Without the plugin system:** copy any folder from `skills/` into `~/.claude/skills/` (for all
projects) or into `.claude/skills/` inside one project.

## Use

Ask in plain words, or call a skill directly:

```
/fundraise:thesis-fit acme.com "General Catalyst, Index Ventures"
/fundraise:market-size acme.com
/fundraise:competitors "Acme, London, AI bookkeeping for small firms"
/fundraise:metrics-pack acme
/fundraise:readiness-check acme
/fundraise:revenue-chart acme
```

Natural requests work too: *"size the market for acme.com"*, *"who competes with Acme?"*.

The input can be a company name, a website, a pitch deck, or a folder. If there is no folder,
the skill creates one in your current directory and researches the rest itself:

```
<company-slug>/
├── company-profile.md       the shared company card (see "Shared files")
├── competitor-candidates/   candidates.csv, written by thesis-fit, read by competitors
├── deck/                    the pitch deck, if you have one
├── updates/                 monthly updates – input for revenue-chart and metrics-pack
├── thesis-fit/              output of thesis-fit
├── market-sizing/           output of market-size
├── competitor-research/     output of competitors
├── metrics-pack/            output of metrics-pack
├── revenue-chart/           output of revenue-chart
└── readiness-check/         output of readiness-check
```

## Shared files

- **`company-profile.md`** – one card per company: the job it does for customers, who pays,
  business model, market, stage, geography, round being raised, and where its metrics are. The
  first skill you run creates it; every later skill reads it first and fills empty fields. A skill
  never overwrites a filled field: if it finds a different value, it records both values and
  their sources in a `Conflicts` section. Every field has a source.
- **`competitor-candidates/candidates.csv`** – portfolio companies of the funds you chose that
  look like competitors. `thesis-fit` writes it; `competitors` reads it as one of its search
  routes and rules on each candidate.

A full `market-size` or `competitors` run does a lot of web research and can take a long time.
Run it in a folder you are happy to fill with files.

## Worked example – Fondo

[`examples/fondo/`](examples/fondo/) is one full run of the pack on
[Fondo](https://fondo.com) – bookkeeping, corporate tax and research and development tax credits
for US (United States) startups, backed by Y Combinator, seed stage – checked against three funds
chosen for the example: General Catalyst, Index Ventures and Alumni Ventures. All runs were made
on 2026-11-11 with public sources only. There is no deck: `readiness-check` took Fondo's claims
from its website.

| Step | Headline (from the outputs) | Wall clock | Note |
|---|---|---|---|
| 1 `thesis-fit` | Alumni Ventures matches on all four axes; General Catalyst and Index Ventures are partial – on one axis each the fund's own directory is too thin to read (General Catalyst: stage unknown for 148 of 199 companies; Index Ventures: region tagged for 16 of 66). 13 candidate rows (12 companies) flagged as possible competitors. Every portfolio list is a floor | about 18 min (from file timestamps; not timed) | [thesis-fit.md](examples/fondo/thesis-fit/thesis-fit.md) |
| 2 `market-size` | TAM USD 129–337 million a year bottom-up, USD 92–214 million top-down – converged (1.4–1.6× apart); SOM USD 6.0–37.6 million a year in 2031; capacity ceiling USD 11.4–55.6 million on the funded plan, USD 6.9 million with today's team – the market binds, not the company. No market-size claim by Fondo was found | about 26 min | [market-sizing.md](examples/fondo/market-sizing/market-sizing.md) |
| 3 `competitors` | 22 direct competitors (13 material), 26 indirect, 13 unverified – a floor; Pilot, Haven and Zeni matter most; Fondo's USD 499 a month list price for monthly bookkeeping is mid-range (USD 200–549 across five like-for-like offers); no disclosed-price sale of a company doing the same job, so no supportable M&A multiple | about 32 min | [competitor-report.md](examples/fondo/competitor-research/competitor-report.md) |
| 4 `metrics-pack` | Not run on Fondo: Fondo publishes no revenue data. See the separate anonymised example below | – | – |
| 5 `readiness-check` | 12 points that may raise doubts with funds: 4 high (each fund in the example's list backs a company ruled a direct competitor – Puzzle at General Catalyst and at Alumni Ventures, Pilot at Index Ventures, Haven at Alumni Ventures), 1 medium (the website's comparison names one rival), 7 low. Consistency and revenue-story checks skipped: no deck, no metrics | about 6 min | [readiness-check.md](examples/fondo/readiness-check/readiness-check.md) |

The shared company card is [`company-profile.md`](examples/fondo/company-profile.md); each folder
also holds the CSV files, and `competitors` its chart and Excel workbook. Fetched pages are not
published. USD = United States dollar.

> **Disclaimer.** Built from public sources only. Fondo did not take part in this example and has
> not reviewed it; the fund list is the example's, not Fondo's. It is research, not investment
> advice, and says nothing about whether anyone should invest in, or raise from, anyone.

## Worked example – Example Co (metrics)

[`examples/example-co/`](examples/example-co/) runs `metrics-pack` on an anonymised contracts
register – 109 contracts, all starting in 2026, currency not stated. It is **not** Fondo's data and
belongs to no named company. Billed MRR (monthly recurring revenue) in 2026-11 is 3.33 million;
three one-month contracts (369,800 in total) are left out as one-off work; 12-month NRR (net revenue
retention) cannot be computed yet, because no contract has run twelve months and renewed. Note:
[metrics.md](examples/example-co/metrics-pack/metrics.md); slide:
[metrics-slide.png](examples/example-co/metrics-pack/metrics-slide.png); input:
[register.csv](examples/example-co/metrics-pack/input/register.csv).

## Requirements

- Claude Code with web access (web search and page fetch).
- Python 3 with `matplotlib` (all skills that draw), `numpy` (`revenue-chart`, `metrics-pack`
  slide) and `openpyxl` (`competitors`). Check with
  `python3 -c "import matplotlib, numpy, openpyxl"`. The `metrics-pack` calculation helper
  (`metrics.py`) needs no extra libraries; only its slide needs matplotlib and numpy. The skills
  will not install anything without asking you.

## What the skills run, and what they connect to

- **No API (application programming interface) keys, no accounts, no tokens.** Nothing in this repository asks for a credential.
- **Runs locally:** three small Python pieces – chart templates inside the skill text,
  [`skills/competitors/build_workbook.py`](skills/competitors/build_workbook.py), which turns a
  JSON (JavaScript Object Notation) file into an Excel workbook, and [`skills/metrics-pack/metrics.py`](skills/metrics-pack/metrics.py),
  which computes MRR, cohorts and NRR (tested in `tests/`). None makes network calls.
- **Reads from the public web**, through Claude Code's own search and fetch tools (and `curl` for
  public pages): the company's own site, company registries (UK Companies House, US SEC EDGAR – the Securities and Exchange Commission's filing system),
  pricing pages, funding and acquisition press, and the portfolio pages of the funds you
  name.
- **Sends nothing anywhere else.** All output is written to files in your current directory.
- **Your confidential material stays yours.** If you give a skill a data room, it marks those
  figures `confidential` and keeps them out of the shareable workbook.

## Principles the skills follow

- **Every number carries a source** – a link, a named document, or a flag saying it is an
  assumption. Each note ends with a source table.
- **"Not disclosed" is not zero**, and **"cannot compute" is an answer** – the skills never
  invent a multiple or borrow another company's funding round.
- **Research artifacts, not investment advice.** The skills report what the evidence supports and
  stop. They give no recommendation to invest or not.

## Author

Nikita Yuriev – venture investor and startup mentor. For contacts – [fundraising.skill@gmail.com](mailto:fundraising.skill@gmail.com)

## License

[MIT](LICENSE) – free to use, change and share, including commercially, with the copyright
notice kept.
