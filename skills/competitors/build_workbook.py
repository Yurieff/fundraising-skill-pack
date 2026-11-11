#!/usr/bin/env python3
"""Build the /competitors market-analysis workbook (xlsx) from workbook-data.json.

Usage:
    python3 build_workbook.py workbook-data.json <company>_market_analysis.xlsx

Emits a two-sheet workbook:

    sheet "competitors"      9 columns, one row per material competitor
    sheet "M&A comparables"  12 columns, one row per comparable deal

Each sheet ends with a blank row, then a synthesis paragraph merged across
columns A–E on a light-gray fill.

JSON schema (all keys required; a sheet may have an empty rows list):

    {
      "company": "Acme",                # subject company, interpolated into headers
      "competitors": {
        "rows": [ [cell x 9], ... ],
        "synthesis": "one paragraph"
      },
      "ma_comparables": {
        "rows": [ [cell x 12], ... ],
        "synthesis": "one paragraph"
      }
    }

    cell = "plain text"
         | 2013                              # numbers pass through as numbers
         | null                              # renders empty – avoid; write "Not disclosed"
         | {"text": "...", "url": "https://..."}   # cell text with a hyperlink

One hyperlink per cell (xlsx limit as written by openpyxl). Convention: company name links to the company site, year founded to LinkedIn,
round/deal cells to the announcement; a cell citing a source inline carries the
word "Source" in its text and the cell itself is hyperlinked.
"""

import json
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

SHEETS = [
    {
        "title": "competitors",
        "key": "competitors",
        "headers": [
            "Company",
            "Year founded",
            "Last round / status",
            "Investors",
            "ICP (ideal customer profile)",
            "Short description",
            "Business model",
            "Similarity to {company}",
            "Difference from {company}",
        ],
        # widths measured from the gold example (A/B were unset there; set for legibility)
        "widths": [22, 14, 28.2, 28.4, 29.6, 25.8, 37.5, 32.6, 37.8],
    },
    {
        "title": "M&A comparables",
        "key": "ma_comparables",
        "headers": [
            "Company",
            "Year founded",
            "Short description",
            "Acquirer",
            "Deal year",
            "Deal value / EV",
            "Revenue at deal",
            "EV / Revenue",
            "EBITDA",
            "EV / EBITDA",
            "Other metrics at deal time",
            "Deal rationale",
        ],
        "widths": [22, 14, 44.4, 18, 20.2, 29.5, 21.4, 25.5, 25.2, 23.6, 38.9, 38.8],
    },
]

FONT_BASE = Font(name="Arial")
FONT_HEADER = Font(name="Arial", bold=True)
FONT_LINK = Font(name="Arial", color="0000FF", underline="single")
ALIGN_WRAP_TOP = Alignment(wrap_text=True, vertical="top")
FILL_SYNTHESIS = PatternFill(fill_type="solid", fgColor="F3F3F3")
SYNTHESIS_MERGE_COLS = 5  # merged A..E, as in the example


def write_cell(ws, row, col, cell):
    c = ws.cell(row=row, column=col)
    c.alignment = ALIGN_WRAP_TOP
    if isinstance(cell, dict):
        c.value = cell["text"]
        c.hyperlink = cell["url"]
        c.font = FONT_LINK
    else:
        c.value = cell
        c.font = FONT_BASE
    return c


def build_sheet(ws, spec, data, company):
    for i, w in enumerate(spec["widths"], start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    n_cols = len(spec["headers"])
    for i, header in enumerate(spec["headers"], start=1):
        c = ws.cell(row=1, column=i, value=header.format(company=company))
        c.font = FONT_HEADER
        c.alignment = ALIGN_WRAP_TOP

    for r, row in enumerate(data["rows"], start=2):
        if len(row) != n_cols:
            sys.exit(
                f"sheet '{spec['title']}' row {r - 1}: {len(row)} cells, expected {n_cols}"
            )
        for i, cell in enumerate(row, start=1):
            write_cell(ws, r, i, cell)

    # blank row, then the synthesis paragraph merged A..E on gray
    synth_row = len(data["rows"]) + 3
    c = ws.cell(row=synth_row, column=1, value=data["synthesis"])
    c.font = FONT_BASE
    c.alignment = ALIGN_WRAP_TOP
    ws.merge_cells(
        start_row=synth_row, start_column=1, end_row=synth_row, end_column=SYNTHESIS_MERGE_COLS
    )
    for i in range(1, SYNTHESIS_MERGE_COLS + 1):
        ws.cell(row=synth_row, column=i).fill = FILL_SYNTHESIS
    ws.row_dimensions[synth_row].height = 150


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    with open(sys.argv[1]) as f:
        data = json.load(f)

    company = data["company"]
    wb = Workbook()
    wb.remove(wb.active)
    for spec in SHEETS:
        build_sheet(wb.create_sheet(spec["title"]), spec, data[spec["key"]], company)
    wb.save(sys.argv[2])
    print(f"wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()
