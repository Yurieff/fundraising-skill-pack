---
title: Example Co – revenue metrics (MRR, cohorts, NRR)
company: Example Co (anonymised contracts register)
created: 2026-11-11
author: metrics-pack v0.1
status: draft
---

# Example Co – revenue metrics

**In plain English.** The register lists 109 contracts, all starting in 2026. Of these, 106 are
12-month contracts and 3 last one month. As of 2026-11, the company is billing about 3.33 million
a month from the 12-month contracts; the register does not say in which currency. A further 0.48
million a month starts in 2026-12 – signed, but not yet billed. Every contract starts in 2026, so
no customer has been around for twelve months: it is too early to say whether customers renew or
pay more, and this note does not guess. The three one-month contracts (369,800 in total) are
one-off work, not recurring revenue, and are left out of the monthly figures.

## Answer up front

| Item | Value |
|---|---|
| Last billed month | 2026-11 |
| Billed MRR in 2026-11 | 3,331,560.50 (currency not stated) |
| Peak MRR | 3,812,842 in 2026-12, status: contracted, not yet billed |
| 12-month NRR | cannot compute yet: no contract has run 12 months and renewed |
| Excluded contracts | 3 (one-month terms), 369,800 in total |

## How to read this

- **MRR (monthly recurring revenue):** what the company bills each month from contracts that
  repeat. One-off work is not MRR.
- **Cohort:** the customers who started in the same month, followed over time.
- **NRR (net revenue retention):** take the customers you had in one month and ask how much those
  same customers pay twelve months later, as a share of what they paid then. Above 100% means the
  company grows even with no new customers; below 100% means it leaks. It needs twelve months of
  history, so a young company often cannot show it yet.
- **Billed vs contracted:** billed months have happened (up to 2026-11; this run is dated
  2026-11-11). Contracted months are signed but lie in the future and can still change. On the
  slide they are dashed and shaded.
- **Run-off:** every contract in the register ends 12 months after it starts and the register
  records no renewals. From 2027-01 the revenue therefore falls only because contracts reach their
  end. That is contract end, not proven customer loss: the register cannot tell the two apart.

## MRR

| Month | MRR | New | Expansion | Contraction | Churned | Status |
|---|---|---|---|---|---|---|
| 2026-01 | 170,783 | 170,783 | 0 | 0 | 0 | billed |
| 2026-02 | 171,389 | 606 | 0 | 0 | 0 | billed |
| 2026-03 | 213,953 | 42,565 | 0 | 0 | 0 | billed |
| 2026-04 | 673,725 | 459,771 | 0 | 0 | 0 | billed |
| 2026-05 | 869,016 | 195,291 | 0 | 0 | 0 | billed |
| 2026-06 | 1,140,865 | 271,850 | 0 | 0 | 0 | billed |
| 2026-07 | 1,279,860 | 138,995 | 0 | 0 | 0 | billed |
| 2026-08 | 1,357,269 | 77,409 | 0 | 0 | 0 | billed |
| 2026-09 | 2,405,108 | 1,047,839 | 0 | 0 | 0 | billed |
| 2026-10 | 3,000,463 | 595,355 | 0 | 0 | 0 | billed |
| 2026-11 | 3,331,560 | 331,097 | 0 | 0 | 0 | billed |
| 2026-12 | 3,812,842 | 481,281 | 0 | 0 | 0 | contracted |
| 2027-01 | 3,642,059 | 0 | 0 | 0 | 170,783 (contract end) | contracted |
| 2027-02 | 3,641,453 | 0 | 0 | 0 | 606 (contract end) | contracted |
| 2027-03 | 3,598,888 | 0 | 0 | 0 | 42,565 (contract end) | contracted |
| 2027-04 | 3,139,117 | 0 | 0 | 0 | 459,771 (contract end) | contracted |
| 2027-05 | 2,943,826 | 0 | 0 | 0 | 195,291 (contract end) | contracted |
| 2027-06 | 2,671,976 | 0 | 0 | 0 | 271,850 (contract end) | contracted |
| 2027-07 | 2,532,982 | 0 | 0 | 0 | 138,995 (contract end) | contracted |
| 2027-08 | 2,455,572 | 0 | 0 | 0 | 77,409 (contract end) | contracted |
| 2027-09 | 1,407,733 | 0 | 0 | 0 | 1,047,839 (contract end) | contracted |
| 2027-10 | 812,378 | 0 | 0 | 0 | 595,355 (contract end) | contracted |
| 2027-11 | 481,281 | 0 | 0 | 0 | 331,097 (contract end) | contracted |

Source: `mrr.csv`; table values rounded to whole units (2026-11 is exactly 3,331,560.50). Months from 2027-01 are run-off of contracts without a recorded renewal.

## Cohorts

`cohorts.csv` holds 12 cohorts (2026-01 to 2026-12). Ten of them (2026-01 to 2026-10) have at least
two billed months, so the slide shows a heatmap. It reads 100% everywhere, and that is built in,
not a finding: the helper spreads each contract's value evenly over its term, so a cohort's
revenue cannot change while its contracts run. Real retention shows only when contracts renew, grow or
stop early, and the register has no such events yet.

## NRR

**12-month NRR cannot be computed yet.** `nrr.csv` has no data row. NRR needs a billed month twelve
months after a customer's start month, and the first start month in the register is 2026-01, so
the earliest such month is 2027-01, after today. Nothing is estimated or taken from a shorter
window.

## Excluded contracts

Rule: a contract with a term shorter than 3 months is non-recurring and is not in MRR.

| Client | Contract value | Start month | Term (months) |
|---|---|---|---|
| Client_013 | 112,500 | 2026-02 | 1 |
| Client_014 | 185,300 | 2026-02 | 1 |
| Client_015 | 72,000 | 2026-03 | 1 |

## Assumptions

- **Contract value = total over the term**, spread evenly (value divided by term, per month, from
  the start month). If the register means value per month or per year, every number changes.
- **Currency: the register gives no currency.** All amounts are in the register's own unit.
- The start month is the first billed month; no billing delays, discounts or payment failures are
  modelled.
- Nothing renews, expands or contracts unless a row says so; the register has one row per contract
  and no renewal rows.
- A register records contracts, not renewals, so NRR is computed only for start months with a recorded renewal (a later contract of the same client starting after an earlier one ends); there is none here, so it is not computed. Any future figure would count only renewals recorded in the register.
- The register is the company's own list. It was not audited against invoices or bank data.
- Customer names are anonymised in the source (`Client_001` and so on).

## Limits

The data cannot show retention, expansion, churn or payment behaviour. The figures after 2026-11
are contracted values, not forecasts. Nothing in this note is an investment recommendation.

## Sources

| Item | Detail |
|---|---|
| Input | contracts register (CSV, 109 contracts, 3 preamble lines), retrieved 2026-11-11; copy in `input/register.csv` |
| Helper | `skills/metrics-pack/metrics.py`, run with `--contracts ... --as-of 2026-11 --min-term 3` |
| Outputs | `mrr.csv`, `cohorts.csv`, `nrr.csv`, `excluded.csv` in this folder |
