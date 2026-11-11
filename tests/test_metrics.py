"""Tests for skills/metrics-pack/metrics.py (standard library only)."""
from __future__ import annotations

import csv
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "skills", "metrics-pack"))

import metrics  # noqa: E402

ROWS = [
    ("A", "2025-01", 100.0), ("B", "2025-01", 100.0),
    ("A", "2026-01", 150.0), ("C", "2026-01", 200.0),
]


def write(tmp: str, name: str, text: str) -> str:
    path = os.path.join(tmp, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


class MetricsTest(unittest.TestCase):
    def test_cohort_table(self):
        self.assertEqual(
            metrics.cohort_table(ROWS),
            {"2025-01": {0: 200.0, 12: 150.0}, "2026-01": {0: 200.0}},
        )

    def test_nrr_12m(self):
        self.assertEqual(metrics.nrr(ROWS, "2025-01"), 0.75)

    def test_nrr_none_without_customers(self):
        self.assertIsNone(metrics.nrr(ROWS, "2025-06"))

    def test_nrr_none_past_data(self):
        self.assertIsNone(metrics.nrr(ROWS, "2026-01"))

    def test_bad_month_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "r.csv", "customer_id,month,revenue\nA,2025-1,10\n")
            with self.assertRaises(ValueError) as cm:
                metrics.load_revenue(p)
            self.assertIn("2025-1", str(cm.exception))

    def test_contracts_spread(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "c.csv",
                      "Title line,,,\n,,,\n,,,\n"
                      "Client,Contract value,Start month,Term (months)\n"
                      'Client_X,"1,200",Jan-26,12\n')
            rows, excluded = metrics.contracts_to_monthly(p)
            self.assertEqual(excluded, [])
            self.assertEqual(len(rows), 12)
            self.assertEqual([r[1] for r in rows],
                             ["2026-%02d" % m for m in range(1, 13)])
            self.assertTrue(all(r[0] == "Client_X" and r[2] == 100.0 for r in rows))

    def test_min_term_excludes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "c.csv",
                      "Title,,,\n,,,\n,,,\n"
                      "Client,Contract value,Start month,Term (months)\n"
                      'Client_Y,"500",Feb-26,1\n')
            rows, excluded = metrics.contracts_to_monthly(p)
            self.assertEqual([r for r in rows if r[0] == "Client_Y"], [])
            self.assertEqual(len(excluded), 1)
            self.assertEqual(excluded[0]["term"], 1)
            self.assertEqual(excluded[0]["client"], "Client_Y")

    def test_mrr_movements(self):
        rows = [("A", "2026-01", 100.0), ("A", "2026-02", 150.0),
                ("B", "2026-02", 50.0), ("B", "2026-03", 50.0)]
        out = {d["month"]: d for d in metrics.mrr_by_month(rows)}
        self.assertEqual(out["2026-02"]["new"], 50.0)
        self.assertEqual(out["2026-02"]["expansion"], 50.0)
        self.assertEqual(out["2026-03"]["churned"], 150.0)
        self.assertEqual(out["2026-03"]["mrr"], 50.0)

    def test_as_of_marks_contracted(self):
        rows = [("A", "2026-01", 100.0), ("A", "2026-02", 100.0),
                ("A", "2026-03", 100.0)]
        out = {d["month"]: d for d in metrics.mrr_by_month(rows, as_of="2026-02")}
        self.assertEqual(out["2026-03"]["status"], "contracted")
        self.assertEqual(out["2026-02"]["status"], "billed")


class CliTest(unittest.TestCase):
    def _run(self, tmp, name, text, flag, *extra):
        src = write(tmp, name, text)
        out = os.path.join(tmp, "out")
        self.assertEqual(metrics.main([flag, src, "--out-dir", out] + list(extra)), 0)
        def rd(f):
            with open(os.path.join(out, f), newline="", encoding="utf-8") as fh:
                return list(csv.reader(fh))
        return rd

    REG = ("T,,,\n,,,\n,,,\nClient,Contract value,Start month,Term (months)\n"
           'A,"1,200",Jan-25,12\nB,"1,200",Jun-26,12\n')

    def test_register_without_renewals_has_no_nrr(self):
        with tempfile.TemporaryDirectory() as tmp:
            rd = self._run(tmp, "c.csv", self.REG, "--contracts", "--as-of", "2026-12")
            self.assertEqual(rd("nrr.csv"), [["start_month", "months", "nrr"]])

    def test_register_with_overlapping_contract_has_no_nrr(self):
        with tempfile.TemporaryDirectory() as tmp:
            reg = self.REG + 'A,"600",Jun-25,12\n'
            rd = self._run(tmp, "c.csv", reg, "--contracts", "--as-of", "2026-12")
            self.assertEqual(rd("nrr.csv"), [["start_month", "months", "nrr"]])

    def test_register_with_renewal_row_has_nrr(self):
        with tempfile.TemporaryDirectory() as tmp:
            reg = self.REG + 'A,"1,200",Jan-26,12\n'
            rd = self._run(tmp, "c.csv", reg, "--contracts", "--as-of", "2026-12")
            self.assertGreater(len(rd("nrr.csv")), 1)

    def test_single_customer_export_has_no_nrr_cohorts_movements(self):
        with tempfile.TemporaryDirectory() as tmp:
            txt = "customer_id,month,revenue\n" + "".join(
                "total,2025-%02d,%d\n" % (m, 100 + m) for m in range(1, 13)
            ) + "total,2026-01,200\n"
            rd = self._run(tmp, "r.csv", txt, "--revenue")
            self.assertEqual(rd("nrr.csv"), [["start_month", "months", "nrr"]])
            self.assertEqual(len(rd("cohorts.csv")), 1)
            self.assertEqual(rd("mrr.csv")[1][2:6], ["", "", "", ""])


if __name__ == "__main__":
    unittest.main()
