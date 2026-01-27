from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
import hashlib
import json


def stable_hash(obj: Any) -> str:
    """
    Create a stable short hash for audit/provenance using canonical JSON.
    """
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


@dataclass(frozen=True)
class Provenance:
    report_id: str
    source_path: str
    page: int
    extractor: str                       # "pymupdf" | "pdfplumber" | "camelot" | "ocr"
    bbox: Optional[List[float]] = None   # [x0, y0, x1, y1] in PDF coords if available
    confidence: Optional[float] = None   # heuristic 0..1, if available
    notes: Optional[str] = None


@dataclass(frozen=True)
class TextChunk:
    chunk_id: str                        # e.g., "p02_c05"
    provenance: Provenance
    text: str
    text_hash: str                       # stable hash of text content for audit


@dataclass(frozen=True)
class TableEvidence:
    table_id: str                        # e.g., "p03_t01"
    provenance: Provenance
    title_hint: Optional[str]
    n_rows: int
    n_cols: int
    header: Optional[List[str]]          # best-effort header row
    rows: List[List[str]]                # rectangularised grid
    csv_path: str
    md_path: str
    json_path: str
    table_hash: str                      # stable hash of table content for audit
    text_fallback: str                   # short markdown rendering for prompt inclusion


@dataclass(frozen=True)
class EvidencePack:
    report_id: str
    source_path: str
    text_chunks: List[TextChunk]
    tables: List[TableEvidence]
    pack_hash: str                       # stable hash of full pack for versioning/audit
    metadata: Dict[str, Any]             # reserved for doc-level fields (e.g., type=PSII/AAR)


def to_jsonable(obj: Any) -> Any:
    """
    Convert dataclasses to JSON-serialisable dicts.
    """
    if hasattr(obj, "__dataclass_fields__"):
        d = asdict(obj)
        return d
    if isinstance(obj, list):
        return [to_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items()}
    return obj
