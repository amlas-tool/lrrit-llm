from typing import List, Optional


def normalise_cell(cell: Optional[str]) -> str:
    """
    Normalise table cell text without 'improving' it.
    """
    if cell is None:
        return ""
    return (
        str(cell)
        .replace("\n", " ")
        .replace("\r", " ")
        .strip()
    )


def render_markdown_table(
    header: Optional[List[str]],
    rows: List[List[str]],
    max_rows: int = 12
) -> str:
    """
    Render a simple, robust markdown table.
    Truncates rows to keep prompt size bounded.
    """
    if not rows and not header:
        return "(Empty table)"

    if header:
        header_norm = [normalise_cell(h) for h in header]
    else:
        # fallback header
        n_cols = len(rows[0]) if rows else 0
        header_norm = [f"col{i+1}" for i in range(n_cols)]

    body = rows[:max_rows]

    lines = []
    lines.append("| " + " | ".join(header_norm) + " |")
    lines.append("| " + " | ".join(["---"] * len(header_norm)) + " |")

    for r in body:
        r = (r + [""] * (len(header_norm) - len(r)))[:len(header_norm)]
        r_norm = [normalise_cell(c) for c in r]
        lines.append("| " + " | ".join(r_norm) + " |")

    if len(rows) > max_rows:
        lines.append("")
        lines.append(f"(Truncated: showing {max_rows} of {len(rows)} rows.)")

    return "\n".join(lines)


def render_table_text_fallback(
    table_id: str,
    page: int,
    markdown_table: str
) -> str:
    """
    Short, prompt-safe representation for LLM consumption.
    """
    return (
        f"[Table {table_id} | page {page}]\n"
        f"{markdown_table}"
    )
