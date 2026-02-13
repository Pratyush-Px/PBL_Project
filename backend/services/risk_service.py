from typing import List

from schemas import LineItemAnalysis, ComparisonSummary, RiskResult


def calculate_risk(
    summary: ComparisonSummary,
    line_item_analysis: List[LineItemAnalysis],
    invoice_currency: str | None,
    po_currency: str | None,
) -> RiskResult:
    """
    Calculate risk score based on comparison results.

    Rules:
        - Totals differ       → +40
        - Missing items        → +30
        - Quantity mismatch    → +20
        - Currency mismatch    → +10

    Score is capped at 100.
    """
    score = 0
    reasons: list[str] = []

    # Rule 1: Totals differ
    if summary.status == "mismatch":
        score += 40
        reasons.append("Total amounts differ")

    # Rule 2: Missing items (missing_in_po or extra_in_po)
    has_missing = any(
        item.status in ("missing_in_po", "extra_in_po")
        for item in line_item_analysis
    )
    if has_missing:
        score += 30
        reasons.append("Missing or extra line items detected")

    # Rule 3: Quantity mismatch
    has_qty_mismatch = any(
        item.status == "quantity_mismatch" for item in line_item_analysis
    )
    if has_qty_mismatch:
        score += 20
        reasons.append("Quantity mismatch in line items")

    # Rule 4: Currency mismatch
    if (
        invoice_currency
        and po_currency
        and invoice_currency.upper() != po_currency.upper()
    ):
        score += 10
        reasons.append("Currency mismatch")

    # Cap at 100
    score = min(score, 100)

    risk_reason = "; ".join(reasons) if reasons else "No issues detected"

    return RiskResult(risk_score=score, risk_reason=risk_reason)
