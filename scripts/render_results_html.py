from __future__ import annotations

import json
import html
from pathlib import Path
from datetime import datetime

# NHS-ish palette (approx)
NHS_BLUE = "#005EB8"
NHS_LIGHT_BLUE = "#E8F1FB"
NHS_DARK = "#0B0C0C"
NHS_GREY = "#F3F2F1"
NHS_RED = "#D5281B"
NHS_AMBER = "#FFB81C"
NHS_GREEN = "#007F3B"


def _badge_colour(value: str) -> str:
    v = (value or "").upper().strip()
    if v in ("GOOD", "YES", "TRUE"):
        return NHS_GREEN
    if v in ("SOME",):
        return NHS_AMBER
    if v in ("LITTLE", "NO", "FALSE"):
        return NHS_RED
    return NHS_BLUE


def _esc(s: str) -> str:
    return html.escape(s or "")


def render_html(report_dir: Path) -> Path:
    results_path = report_dir / "agent_results.json"
    pack_path = report_dir / "evidence_pack.json"

    if not results_path.exists():
        raise FileNotFoundError(f"Missing: {results_path}")

    results = json.loads(results_path.read_text(encoding="utf-8"))

    pack = None
    if pack_path.exists():
        try:
            pack = json.loads(pack_path.read_text(encoding="utf-8"))
        except Exception:
            pack = None

    # Extract a few header fields if available
    report_id = report_dir.name
    source_path = (pack or {}).get("source_path", "")
    pack_hash = (pack or {}).get("pack_hash", "")
    chunk_count = len((pack or {}).get("text_chunks", []) or [])
    table_count = len((pack or {}).get("tables", []) or [])

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Order agents by id if possible
    def sort_key(item):
        k = item[0]
        return k

    agent_items = sorted(results.items(), key=sort_key)

    cards_html = []
    for key, obj in agent_items:
        agent_id = obj.get("agent_id", key)
        dim = obj.get("dimension", "")
        rating = obj.get("rating", "")
        uncertainty = obj.get("uncertainty", False)
        rationale = obj.get("rationale", "")
        evidence = obj.get("evidence", []) or []

        rating_col = _badge_colour(rating)
        uncert_col = _badge_colour("YES" if uncertainty else "NO")

        # Evidence list
        ev_rows = []
        if evidence:
            for e in evidence:
                eid = e.get("id", "")
                quote = e.get("quote", "")
                etype = e.get("evidence_type", "")
                et_col = _badge_colour("GOOD" if etype == "positive" else "LITTLE" if etype == "negative" else "SOME")
                ev_rows.append(f"""
                <div class="ev-row">
                  <div class="ev-meta">
                    <span class="pill" style="background:{et_col}">{_esc(etype or "evidence")}</span>
                    <span class="ev-id">{_esc(eid)}</span>
                  </div>
                  <div class="ev-quote">“{_esc(quote)}”</div>
                </div>
                """)
        else:
            ev_rows.append('<div class="muted">No evidence quotes returned.</div>')

        cards_html.append(f"""
        <section class="card">
          <div class="card-head">
            <div>
              <div class="agent-title">{_esc(agent_id)} — {_esc(dim)}</div>
              <div class="muted">Key: positive = supports dimension, negative = contrary/weakening evidence</div>
            </div>
            <div class="badges">
              <div class="badge">
                <div class="badge-label">Rating</div>
                <div class="pill" style="background:{rating_col}">{_esc(rating)}</div>
              </div>
              <div class="badge">
                <div class="badge-label">Uncertainty</div>
                <div class="pill" style="background:{uncert_col}">{'YES' if uncertainty else 'NO'}</div>
              </div>
            </div>
          </div>

          <div class="card-body">
            <h3>Rationale</h3>
            <p>{_esc(rationale)}</p>

            <h3>Evidence</h3>
            {''.join(ev_rows)}

            <details class="raw">
              <summary>Raw model output</summary>
              <pre>{_esc(obj.get("raw_output",""))}</pre>
            </details>
          </div>
        </section>
        """)

    html_out = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>LRRIT Agent Results — {html.escape(report_id)}</title>
  <style>
    :root {{
      --nhs-blue: {NHS_BLUE};
      --nhs-light: {NHS_LIGHT_BLUE};
      --nhs-dark: {NHS_DARK};
      --nhs-grey: {NHS_GREY};
    }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: var(--nhs-dark);
      background: var(--nhs-grey);
    }}
    header {{
      background: var(--nhs-blue);
      color: white;
      padding: 20px 24px;
    }}
    .wrap {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 18px 18px 40px 18px;
    }}
    .meta {{
      background: white;
      border-radius: 12px;
      padding: 14px 16px;
      margin-top: -18px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.08);
      border-left: 6px solid var(--nhs-blue);
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px 18px;
      margin-top: 8px;
    }}
    .meta .k {{ font-weight: 700; }}
    .meta .v {{ word-break: break-all; }}
    .card {{
      background: white;
      border-radius: 12px;
      margin-top: 16px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.06);
      overflow: hidden;
      border: 1px solid #e6e6e6;
    }}
    .card-head {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      padding: 14px 16px;
      background: var(--nhs-light);
      border-bottom: 1px solid #e6e6e6;
    }}
    .agent-title {{
      font-size: 18px;
      font-weight: 800;
      margin-bottom: 4px;
    }}
    .badges {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    .badge-label {{
      font-size: 12px;
      opacity: 0.85;
      margin-bottom: 4px;
    }}
    .pill {{
      display: inline-block;
      color: white;
      font-weight: 800;
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 12px;
      letter-spacing: 0.2px;
    }}
    .card-body {{
      padding: 14px 16px 18px 16px;
    }}
    h3 {{
      margin: 14px 0 6px 0;
      font-size: 14px;
      letter-spacing: 0.2px;
      text-transform: uppercase;
      opacity: 0.8;
    }}
    p {{
      margin: 0;
      line-height: 1.45;
    }}
    .muted {{
      opacity: 0.75;
      font-size: 12px;
    }}
    .ev-row {{
      border-left: 4px solid var(--nhs-blue);
      padding: 10px 10px;
      margin: 10px 0;
      background: #fafafa;
      border-radius: 8px;
    }}
    .ev-meta {{
      display: flex;
      gap: 10px;
      align-items: center;
      margin-bottom: 6px;
    }}
    .ev-id {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      font-size: 12px;
      opacity: 0.8;
    }}
    .ev-quote {{
      font-size: 14px;
    }}
    details.raw {{
      margin-top: 12px;
    }}
    pre {{
      background: #0b0c0c;
      color: #f5f5f5;
      padding: 12px;
      border-radius: 10px;
      overflow-x: auto;
      font-size: 12px;
    }}
    footer {{
      margin-top: 18px;
      font-size: 12px;
      opacity: 0.75;
    }}
    @media (max-width: 760px) {{
      .meta-grid {{ grid-template-columns: 1fr; }}
      .card-head {{ flex-direction: column; }}
      .badges {{ justify-content: flex-start; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <div style="font-size:22px;font-weight:900;">LRRIT Agent Results</div>
      <div style="opacity:0.9;margin-top:4px;">Report: {html.escape(report_id)} • Generated: {html.escape(now)}</div>
    </div>
  </header>

  <div class="wrap">
    <div class="meta">
      <div style="font-weight:900;font-size:14px;">EvidencePack summary</div>
      <div class="meta-grid">
        <div><span class="k">Source:</span> <span class="v">{html.escape(source_path)}</span></div>
        <div><span class="k">Pack hash:</span> <span class="v">{html.escape(pack_hash)}</span></div>
        <div><span class="k">Text chunks:</span> <span class="v">{chunk_count}</span></div>
        <div><span class="k">Tables:</span> <span class="v">{table_count}</span></div>
      </div>
      <footer>Open this file locally in any browser. No data is uploaded anywhere.</footer>
    </div>

    {''.join(cards_html)}
  </div>
</body>
</html>
"""

    out_path = report_dir / "agent_results.html"
    out_path.write_text(html_out, encoding="utf-8")
    return out_path


def main():
    # Default to your 'test' report directory
    report_dir = Path("data") / "processed" / "reports" / "test"

    # Allow override via env var or first CLI arg
    import os, sys
    if len(sys.argv) > 1:
        report_dir = Path(sys.argv[1])
    elif os.environ.get("LRRIT_REPORT_DIR"):
        report_dir = Path(os.environ["LRRIT_REPORT_DIR"])

    out = render_html(report_dir)
    print(f"Wrote: {out.resolve()}")


if __name__ == "__main__":
    main()
