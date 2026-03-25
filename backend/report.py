"""
report.py — HTML report generator for invoice vs purchase order comparison.

Generates styled HTML reports that display the exact same fields and
comparison structure as the React ResultsSection component.
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def _get_confidence_color(score) -> str:
    if score is None:
        return "#888"
    if score > 85:
        return "#22c55e"
    if score >= 70:
        return "#eab308"
    return "#ef4444"


def _get_risk_color(score) -> str:
    if score <= 30:
        return "#22c55e"
    if score <= 70:
        return "#f97316"
    return "#ef4444"


def _get_status_color(status: str) -> str:
    status_lower = (status or "").lower()
    colors = {
        "match": "#22c55e",
        "quantity_mismatch": "#f97316",
        "price_mismatch": "#f97316",
        "missing_in_po": "#ef4444",
        "extra_in_invoice": "#ef4444",
        "extra_in_po": "#3b82f6",
        "mismatch": "#ef4444",
    }
    return colors.get(status_lower, "#888")


def _get_status_bg(status: str) -> str:
    status_lower = (status or "").lower()
    colors = {
        "match": "#dcfce7",
        "quantity_mismatch": "#fff7ed",
        "price_mismatch": "#fff7ed",
        "missing_in_po": "#fef2f2",
        "extra_in_invoice": "#fef2f2",
        "extra_in_po": "#eff6ff",
        "mismatch": "#fef2f2",
    }
    return colors.get(status_lower, "#f3f4f6")


def _format_value(value, decimals=2) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, (int, float)):
        return f"{value:.{decimals}f}"
    return str(value)


def _format_qty(value) -> str:
    if value is None:
        return "-"
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    return str(value)


def _format_price(value) -> str:
    if value is None:
        return "-"
    if isinstance(value, (int, float)):
        return f"{value:.2f}"
    return str(value)


def generate_report(order_id: str, result: dict, reports_dir: str) -> str:
    """
    Generate an HTML report for a comparison result.

    Args:
        order_id: The order identifier
        result: The comparison result dict (same structure as /compare response)
        reports_dir: Directory to save the report

    Returns:
        Absolute path to the generated report file.
    """
    os.makedirs(reports_dir, exist_ok=True)

    summary = result.get("summary", {})
    line_items = result.get("line_item_analysis", [])
    confidence = result.get("confidence_score")
    risk_score = result.get("risk_score", 0)
    risk_reason = result.get("risk_reason", "")
    processing_time = result.get("processing_time_ms", 0)

    # Build line item rows
    line_item_rows = ""
    for item in line_items:
        status = item.get("status", "")
        status_color = _get_status_color(status)
        status_bg = _get_status_bg(status)
        row_bg = status_bg

        line_item_rows += f"""
            <tr style="background-color: {row_bg};">
                <td>{item.get('description', '')}</td>
                <td style="text-align:center;">{_format_qty(item.get('invoice_qty'))}</td>
                <td style="text-align:center;">{_format_qty(item.get('po_qty'))}</td>
                <td style="text-align:right;">{_format_price(item.get('invoice_price'))}</td>
                <td style="text-align:right;">{_format_price(item.get('po_price'))}</td>
                <td style="text-align:center;">
                    <span style="
                        background-color: {status_color};
                        color: white;
                        padding: 3px 10px;
                        border-radius: 12px;
                        font-size: 0.8em;
                        font-weight: 600;
                        text-transform: uppercase;
                    ">{status.replace('_', ' ')}</span>
                </td>
            </tr>"""

    if not line_items:
        line_item_rows = """
            <tr>
                <td colspan="6" style="text-align:center; color:#888; padding:20px;">
                    No line items to compare
                </td>
            </tr>"""

    # Summary status badge
    summary_status = summary.get("status", "")
    summary_badge_color = "#22c55e" if summary_status == "match" else "#ef4444"

    # Difference color
    diff_value = summary.get("difference")
    diff_color = "#22c55e" if diff_value is not None and diff_value == 0 else "#ef4444"

    # Confidence badge
    conf_color = _get_confidence_color(confidence)
    conf_text = f"{confidence}%" if confidence is not None else "N/A"

    # Risk badge
    r_color = _get_risk_color(risk_score)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparison Report — Order {order_id}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            padding: 30px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #1e293b;
        }}
        .header h1 {{
            font-size: 1.8em;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            color: #94a3b8;
            font-size: 0.9em;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }}
        .card {{
            background: #1e293b;
            border-radius: 12px;
            padding: 24px;
            border: 1px solid #334155;
        }}
        .card h3 {{
            font-size: 1.1em;
            margin-bottom: 16px;
            color: #c4b5fd;
        }}
        .summary-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #334155;
        }}
        .summary-row:last-of-type {{
            border-bottom: none;
        }}
        .summary-row span {{
            color: #94a3b8;
        }}
        .summary-row strong {{
            color: #f1f5f9;
        }}
        .status-badge {{
            display: inline-block;
            margin-top: 12px;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: white;
        }}
        .score-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #334155;
        }}
        .score-item:last-of-type {{
            border-bottom: none;
        }}
        .score-item span {{
            color: #94a3b8;
        }}
        .badge {{
            padding: 4px 14px;
            border-radius: 16px;
            font-weight: 700;
            font-size: 0.9em;
            color: white;
        }}
        .risk-reason {{
            margin-top: 12px;
            padding: 10px;
            background: #0f172a;
            border-radius: 8px;
            font-size: 0.88em;
            color: #fbbf24;
        }}
        .processing-time {{
            margin-top: 12px;
            color: #64748b;
            font-size: 0.85em;
        }}
        .table-card {{
            margin-top: 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.92em;
        }}
        th {{
            background: #0f172a;
            color: #94a3b8;
            padding: 12px 10px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.8em;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #334155;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #1e293b;
            color: #e2e8f0;
        }}
        tr:hover {{
            filter: brightness(1.05);
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #1e293b;
            color: #475569;
            font-size: 0.8em;
        }}
        @media print {{
            body {{
                background: white;
                color: #1e293b;
            }}
            .card {{
                background: #f8fafc;
                border-color: #e2e8f0;
            }}
            th {{
                background: #f1f5f9;
                color: #475569;
            }}
            td {{
                color: #1e293b;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Invoice vs Purchase Order — Report</h1>
            <div class="subtitle">Order ID: {order_id} &nbsp;|&nbsp; Generated: {timestamp}</div>
        </div>

        <div class="metrics-grid">
            <!-- Comparison Summary -->
            <div class="card">
                <h3>Comparison Summary</h3>
                <div class="summary-row">
                    <span>Invoice Total:</span>
                    <strong>{_format_value(summary.get('invoice_total'))}</strong>
                </div>
                <div class="summary-row">
                    <span>PO Total:</span>
                    <strong>{_format_value(summary.get('po_total'))}</strong>
                </div>
                <div class="summary-row">
                    <span>Difference:</span>
                    <strong style="color: {diff_color};">{_format_value(diff_value)}</strong>
                </div>
                <span class="status-badge" style="background-color: {summary_badge_color};">
                    {summary_status.upper()}
                </span>
            </div>

            <!-- AI Analysis -->
            <div class="card">
                <h3>AI Analysis</h3>
                <div class="score-item">
                    <span>Confidence Score</span>
                    <span class="badge" style="background-color: {conf_color};">{conf_text}</span>
                </div>
                <div class="score-item">
                    <span>Risk Score</span>
                    <span class="badge" style="background-color: {r_color};">{risk_score}/100</span>
                </div>
                {f'<div class="risk-reason"><strong>Risk Factor:</strong> {risk_reason}</div>' if risk_reason else ''}
                <div class="processing-time">⏱ Processed in {processing_time:.0f} ms</div>
            </div>
        </div>

        <!-- Line Item Analysis -->
        <div class="card table-card">
            <h3>Line Item Analysis</h3>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Description</th>
                            <th style="text-align:center;">Inv Qty</th>
                            <th style="text-align:center;">PO Qty</th>
                            <th style="text-align:right;">Inv Price</th>
                            <th style="text-align:right;">PO Price</th>
                            <th style="text-align:center;">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {line_item_rows}
                    </tbody>
                </table>
            </div>
        </div>

        <div class="footer">
            Invoice &amp; PO Validator &mdash; Auto-generated report
        </div>
    </div>
</body>
</html>"""

    report_filename = f"report_{order_id}.html"
    report_path = os.path.join(reports_dir, report_filename)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    return report_path
