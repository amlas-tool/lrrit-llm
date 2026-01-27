from __future__ import annotations

from typing import List, Dict, Any
import fitz  # PyMuPDF


def extract_text_pages(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Returns: [{"page": 1, "text": "..."} ...]
    """
    doc = fitz.open(pdf_path)
    pages = []
    for i in range(len(doc)):
        text = doc[i].get_text("text") or ""
        pages.append({"page": i + 1, "text": text})
    return pages

