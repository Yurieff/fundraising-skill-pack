"""Revenue arithmetic for the metrics-pack skill: MRR, cohorts, NRR.

MRR = monthly recurring revenue. NRR = net revenue retention.
Standard library only, no network. Rows are (customer_id, "YYYY-MM", revenue).

Usage:
  python3 metrics.py (--revenue <csv> | --contracts <csv>) --out-dir <dir>
                     [--as-of YYYY-MM] [--min-term 3]
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

Row = Tuple[str, str, float]

_MONTH_RE = re.compile(r"^(\d{4})-(0[1-9]|1[0-2])$")
_MON = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


def _check_month(value: str, where: str) -> str:
    if not _MONTH_RE.match(value or ""):
        raise ValueError("bad month '%s' in %s: expected YYYY-MM" % (value, where))
    return value


def _index(month: str) -> int:
    y, m = month.split("-")
    return int(y) * 12 + int(m) - 1


def _month(index: int) -> str:
    return "%04d-%02d" % (index // 12, index % 12 + 1)


def load_revenue(path: str) -> List[Row]:
    """Read CSV customer_id,month,revenue. ValueError names the column or bad value."""
    rows: List[Row] = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for col in ("customer_id", "month", "revenue"):
            if col not in (reader.fieldnames or []):
                raise ValueError("missing column '%s' in %s" % (col, path))
        for n, rec in enumerate(reader, start=2):
            month = _check_month((rec["month"] or "").strip(), "%s line %d" % (path, n))
            raw = (rec["revenue"] or "").strip().replace(",", "")
            try:
                rev = float(raw)
            except ValueError:
                raise ValueError("bad revenue '%s' in %s line %d" % (rec["revenue"], path, n))
            rows.append(((rec["customer_id"] or "").strip(), month, rev))
    return rows


def _parse_start(text: str, where: str) -> str:
    m = re.match(r"^([A-Za-z]{3})-(\d{2})$", (text or "").strip())
    if not m or m.group(1).lower() not in _MON:
        raise ValueError("bad start month '%s' in %s: expected Mon-YY, e.g. May-26" % (text, where))
    return "%04d-%02d" % (2000 + int(m.group(2)), _MON[m.group(1).lower()])


def contracts_to_monthly(path: str, min_term: int = 3) -> Tuple[List[Row], List[dict]]:
    """Spread each contract's value evenly over its term, starting at the start month.

    Contracts with term < min_term are returned in the second list instead.
    """
    rows: List[Row] = []
    excluded: List[dict] = []
    for client, value, start, term in _read_register(path):
        if term < min_term:
            excluded.append({"client": client, "value": value, "start": start, "term": term})
            continue
        s = _index(start)
        for off in range(term):
            rows.append((client, _month(s + off), value / term))
    return rows, excluded


def _renewal_months(path: str, min_term: int) -> set:
    """Months in which some client has a recorded renewal.

    A renewal is a later recurring contract (term >= min_term) of the same client whose start
    month is at least one month after the end month of an earlier recurring contract, where
    end month = start + term - 1 (so renewal start >= earlier start + term). Overlapping
    contracts (upsells, add-ons) are not renewals. A month counts if the client was billed
    under the earlier contract in that month.
    """
    by_client: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
    for client, _value, start, term in _read_register(path):
        if term >= min_term:
            by_client[client].append((_index(start), term))
    out = set()
    for contracts in by_client.values():
        for s, term in contracts:
            if any(s2 >= s + term for s2, _t in contracts):
                out.update(_month(s + k) for k in range(term))
    return out


def _read_register(path: str) -> List[Tuple[str, float, str, int]]:
    """Parsed contracts register: (client, value, start "YYYY-MM", term)."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        table = list(csv.reader(fh))
    header_at = None
    for i, cells in enumerate(table):
        joined = ",".join(cells)
        if all(k in joined for k in ("Client", "Contract value", "Start month", "Term")):
            header_at = i
            break
    if header_at is None:
        raise ValueError("no header with Client, Contract value, Start month, Term in %s" % path)
    head = [c.strip() for c in table[header_at]]

    def col(name: str) -> int:
        for j, c in enumerate(head):
            if c.startswith(name):
                return j
        raise ValueError("missing column '%s' in %s" % (name, path))

    ci, vi, si, ti = col("Client"), col("Contract value"), col("Start month"), col("Term")
    out: List[Tuple[str, float, str, int]] = []
    for k, cells in enumerate(table[header_at + 1:], start=header_at + 2):
        if not any(c.strip() for c in cells):
            continue
        where = "%s line %d" % (path, k)
        client = cells[ci].strip()
        try:
            value = float(cells[vi].strip().replace(",", ""))
        except ValueError:
            raise ValueError("bad contract value '%s' in %s" % (cells[vi], where))
        start = _parse_start(cells[si], where)
        try:
            term = int(cells[ti].strip())
        except ValueError:
            raise ValueError("bad term '%s' in %s" % (cells[ti], where))
        if term < 1:
            raise ValueError("bad term '%s' in %s" % (cells[ti], where))
        out.append((client, value, start, term))
    return out


def _by_customer(rows: List[Row]) -> Dict[str, Dict[str, float]]:
    out: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for cust, month, rev in rows:
        out[cust][month] += rev
    return out


def mrr_by_month(rows: List[Row], as_of: Optional[str] = None) -> List[dict]:
    """One dict per calendar month from first to last: month, mrr, new, expansion,
    contraction, churned, status (billed up to and including as_of, else contracted)."""
    if not rows:
        return []
    if as_of is not None:
        _check_month(as_of, "as_of")
    cust = _by_customer(rows)
    lo = min(_index(r[1]) for r in rows)
    hi = max(_index(r[1]) for r in rows)
    out: List[dict] = []
    for idx in range(lo, hi + 1):
        month, prev = _month(idx), _month(idx - 1)
        mrr = new = exp = con = churn = 0.0
        for months in cust.values():
            cur, before = months.get(month, 0.0), months.get(prev, 0.0)
            mrr += cur
            if before <= 0 < cur:
                new += cur
            elif before > 0 and cur <= 0:
                churn += before
            elif cur > before > 0:
                exp += cur - before
            elif 0 < cur < before:
                con += before - cur
        status = "billed" if as_of is None or month <= as_of else "contracted"
        out.append({"month": month, "mrr": mrr, "new": new, "expansion": exp,
                    "contraction": con, "churned": churn, "status": status})
    return out


def cohort_table(rows: List[Row]) -> Dict[str, Dict[int, float]]:
    """Cohort = month of a customer's first revenue > 0; inner key = months since then."""
    cust = _by_customer(rows)
    table: Dict[str, Dict[int, float]] = {}
    for months in cust.values():
        positive = [m for m, v in months.items() if v > 0]
        if not positive:
            continue
        first = min(positive)
        base = _index(first)
        inner = table.setdefault(first, {})
        for m, v in months.items():
            if v > 0:
                off = _index(m) - base
                inner[off] = inner.get(off, 0.0) + v
    return {k: dict(sorted(v.items())) for k, v in sorted(table.items())}


def nrr(rows: List[Row], start: str, months: int = 12) -> Optional[float]:
    """Revenue in start+months from customers billed in start, divided by their revenue in
    start. None if no such customer or start+months is past the last month in the data."""
    if not rows:
        return None
    target = _month(_index(start) + months)
    if target > max(r[1] for r in rows):
        return None
    cust = _by_customer(rows)
    base = [c for c, m in cust.items() if m.get(start, 0.0) > 0]
    if not base:
        return None
    denom = sum(cust[c][start] for c in base)
    return sum(cust[c].get(target, 0.0) for c in base) / denom


def _write(path: str, header: List[str], lines: List[list]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(lines)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="MRR, cohorts and NRR from revenue data.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--revenue", help="CSV customer_id,month,revenue")
    src.add_argument("--contracts", help="contracts register CSV")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--as-of", help="YYYY-MM; later months are marked contracted")
    ap.add_argument("--min-term", type=int, default=3)
    a = ap.parse_args(argv)

    excluded: List[dict] = []
    try:
        if a.revenue:
            rows = load_revenue(a.revenue)
        else:
            rows, excluded = contracts_to_monthly(a.contracts, a.min_term)
        mrr = mrr_by_month(rows, a.as_of)
    except (ValueError, OSError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 1

    os.makedirs(a.out_dir, exist_ok=True)
    n_customers = len({r[0] for r in rows})
    # One customer id (for example a single "total" line from monthly updates) carries no
    # customer detail: movements, cohorts and NRR would only restate total growth.
    single = a.revenue is not None and n_customers <= 1
    blank = "" if single else None
    _write(os.path.join(a.out_dir, "mrr.csv"),
           ["month", "mrr", "new", "expansion", "contraction", "churned", "status"],
           [[d["month"], "%.2f" % d["mrr"]]
            + [blank if single else "%.2f" % d[k]
               for k in ("new", "expansion", "contraction", "churned")]
            + [d["status"]] for d in mrr])
    cohorts = {} if single else cohort_table(rows)
    _write(os.path.join(a.out_dir, "cohorts.csv"), ["cohort", "month_offset", "revenue"],
           [[c, off, "%.2f" % v] for c, inner in cohorts.items() for off, v in inner.items()])
    # NRR uses billed months only: a contract running out its term is not a measured
    # retention outcome, and months after --as-of have not happened yet.
    billed = [r for r in rows if a.as_of is None or r[1] <= a.as_of]
    months = sorted({r[1] for r in billed})
    # A contracts register has one row per contract: contract end would read as lost
    # revenue. NRR is computed only for start months in which some client has a recorded
    # renewal (see _renewal_months); the figure reflects only the renewals recorded.
    eligible = None
    if a.contracts:
        eligible = _renewal_months(a.contracts, a.min_term)
    nrr_lines = []
    if not single:
        for m in months:
            if eligible is not None and m not in eligible:
                continue
            v = nrr(billed, m, 12)
            if v is not None:
                nrr_lines.append([m, 12, "%.4f" % v])
    _write(os.path.join(a.out_dir, "nrr.csv"), ["start_month", "months", "nrr"], nrr_lines)
    if a.contracts:
        _write(os.path.join(a.out_dir, "excluded.csv"), ["client", "value", "start", "term"],
               [[e["client"], "%.2f" % e["value"], e["start"], e["term"]] for e in excluded])

    print("months: %d  customers: %d  excluded: %d  nrr rows: %d"
          % (len(mrr), len({r[0] for r in rows}), len(excluded), len(nrr_lines)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
