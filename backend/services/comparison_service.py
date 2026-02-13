from typing import List, Optional

from schemas import (
    LineItemAnalysis,
    ComparisonSummary,
)


def compare_documents(
    invoice_data: dict,
    po_data: dict,
) -> dict:
    """
    Compare extracted invoice data against purchase order data.

    Returns:
        {
            "summary": ComparisonSummary,
            "line_item_analysis": List[LineItemAnalysis],
            "confidence_score": float | None,
        }
    """
    # --- Total comparison ---
    inv_total = invoice_data.get("total_amount")
    po_total = po_data.get("total_amount")

    difference: Optional[float] = None
    if inv_total is not None and po_total is not None:
        difference = round(inv_total - po_total, 2)

    total_status = "match" if difference is not None and difference == 0 else "mismatch"

    summary = ComparisonSummary(
        invoice_total=inv_total,
        po_total=po_total,
        difference=difference,
        status=total_status,
    )

    # --- Line item comparison ---
    inv_items: List[dict] = invoice_data.get("line_items", [])
    po_items: List[dict] = po_data.get("line_items", [])

    analysis: List[LineItemAnalysis] = []
    matched_po_indices: set = set()

    for inv_item in inv_items:
        inv_desc = (inv_item.get("description") or "").strip().lower()
        best_match_idx: Optional[int] = None
        best_match_score: float = 0.0

        for idx, po_item in enumerate(po_items):
            if idx in matched_po_indices:
                continue
            po_desc = (po_item.get("description") or "").strip().lower()

            # Simple substring / exact match scoring
            if inv_desc == po_desc:
                best_match_idx = idx
                best_match_score = 1.0
                break
            elif inv_desc in po_desc or po_desc in inv_desc:
                score = len(min(inv_desc, po_desc, key=len)) / max(
                    len(inv_desc), len(po_desc), 1
                )
                if score > best_match_score and score > 0.5:
                    best_match_idx = idx
                    best_match_score = score

        if best_match_idx is not None:
            matched_po_indices.add(best_match_idx)
            po_match = po_items[best_match_idx]

            # Determine status
            qty_match = inv_item.get("quantity") == po_match.get("quantity")
            price_match = inv_item.get("unit_price") == po_match.get("unit_price")

            if qty_match and price_match:
                status = "match"
            elif not qty_match:
                status = "quantity_mismatch"
            else:
                status = "price_mismatch"

            analysis.append(
                LineItemAnalysis(
                    description=inv_item.get("description", ""),
                    invoice_qty=inv_item.get("quantity"),
                    po_qty=po_match.get("quantity"),
                    invoice_price=inv_item.get("unit_price"),
                    po_price=po_match.get("unit_price"),
                    status=status,
                )
            )
        else:
            # Invoice item not found in PO
            analysis.append(
                LineItemAnalysis(
                    description=inv_item.get("description", ""),
                    invoice_qty=inv_item.get("quantity"),
                    po_qty=None,
                    invoice_price=inv_item.get("unit_price"),
                    po_price=None,
                    status="missing_in_po",
                )
            )

    # Check for extra PO items not matched to any invoice item
    for idx, po_item in enumerate(po_items):
        if idx not in matched_po_indices:
            analysis.append(
                LineItemAnalysis(
                    description=po_item.get("description", ""),
                    invoice_qty=None,
                    po_qty=po_item.get("quantity"),
                    invoice_price=None,
                    po_price=po_item.get("unit_price"),
                    status="extra_in_po",
                )
            )

    # --- Confidence score (average of both documents) ---
    inv_conf = invoice_data.get("confidence_score")
    po_conf = po_data.get("confidence_score")
    scores = [s for s in [inv_conf, po_conf] if s is not None]
    confidence = round(sum(scores) / len(scores), 1) if scores else None

    return {
        "summary": summary,
        "line_item_analysis": analysis,
        "confidence_score": confidence,
    }
