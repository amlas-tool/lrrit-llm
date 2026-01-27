from __future__ import annotations

import os
import json
from typing import List, Dict, Any, Optional

import pdfplumber

from lrrit_llm.evidence.render import (
    render_markdown_table,
    render_table_text_fallback,
)


def extract_tables_from_pdf(
    pdf_path: str,
    report_id: str,
    out_dir: str,
    page_numbers: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    """
    Extract tables using pdfplumber.

    Returns a list of table dicts suitable for build_evidence_pack().
    Also writes CSV / MD / JSON artefacts to disk.
    """
    tables_out: List[Dict[str, Any]] = []

    tables_dir = os.path.join(out_dir, "tables")
    os.makedirs(tables_dir, exist_ok=True)

    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        page_idxs = (
            [p - 1 for p in page_numbers]
            if page_numbers
            else range(len(pages))
        )

        for pi in page_idxs:
            page = pages[pi]
            page_no = pi + 1

            try:
                raw_tables = page.extract_tables()
            except Exception as e:
                # Fail soft: log via notes, continue
                continue

            for ti, grid in enumerate(raw_tables, start=1):
                if not grid or len(grid) < 2:
                    continue

                # Normalise grid
                norm = [
                    [(c or "").strip() for c in row]
                    for row in grid
                    if row
                ]

                if len(norm) < 2:
                    continue

                header = norm[0]
                rows = norm[1:]

                table_id = f"p{page_no:02d}_t{ti:02d}"

                md = render_markdown_table(header, rows, max_rows=12)
                text_fallback = render_table_text_fallback(table_id, page_no, md)

                # Paths
                csv_path = os.path.join(tables_dir, f"{table_id}.csv")
                md_path = os.path.join(tables_dir, f"{table_id}.md")
                json_path = os.path.join(tables_dir, f"{table_id}.json")

                _write_csv(csv_path, header, rows)
                _write_text(md_path, md)

                meta = {
                    "report_id": report_id,
                    "table_id": table_id,
                    "page": page_no,
                    "extractor": "pdfplumber",
                    "n_rows": len(rows),
                    "n_cols": len(header),
                }
                _write_json(json_path, meta)

                tables_out.append({
                    "page": page_no,
                    "extractor": "pdfplumber",
                    "table_id": table_id,
                    "header": header,
                    "rows": rows,
                    "csv_path": csv_path,
                    "md_path": md_path,
                    "json_path": json_path,
                    "text_fallback": text_fallback,
                    "title_hint": None,
                    "bbox": None,
                    "confidence": None,
                })

    return tables_out


def _write_csv(path: str, header: List[str], rows: List[List[str]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(",".join(_csv_escape(h) for h in header) + "\n")
        for r in rows:
            r = (r + [""] * (len(header) - len(r)))[:len(header)]
            f.write(",".join(_csv_escape(c) for c in r) + "\n")


def _write_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _csv_escape(s: str) -> str:
    s = (s or "").replace('"', '""')
    if any(ch in s for ch in [",", "\n", '"']):
        return f'"{s}"'
    return s
