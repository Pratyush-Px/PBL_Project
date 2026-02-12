"""
Document Comparator
Compares a Purchase Order and an Invoice to find mismatches.
"""

from difflib import SequenceMatcher
from typing import Optional


class DocumentComparator:
    """
    Compares two structured extraction results (order vs invoice).
    Returns a status and a list of differences.
    """

    def __init__(self, amount_tolerance: float = 0.01, name_similarity_threshold: float = 0.70):
        """
        :param amount_tolerance: Absolute tolerance for monetary comparisons.
        :param name_similarity_threshold: Minimum similarity ratio (0-1) to consider
               two item names as the same product.
        """
        self.amount_tolerance = amount_tolerance
        self.name_similarity_threshold = name_similarity_threshold

    def compare(self, order: dict, invoice: dict) -> dict:
        """
        Compare an order and an invoice extraction result.

        :param order: Structured dict from DocumentExtractor (document_type="order").
        :param invoice: Structured dict from DocumentExtractor (document_type="invoice").
        :return: {"status": "Match"|"Mismatch", "differences": [...]}
        """
        differences: list[dict] = []

        # 1. Vendor match
        self._compare_field(
            differences,
            field="vendor",
            order_value=order.get("vendor"),
            invoice_value=invoice.get("vendor"),
            comparator=self._strings_match,
        )

        # 2. Invoice / PO number (informational — often different by design)
        # We skip strict comparison here since order# and invoice# are inherently different.

        # 3. Total amount match
        self._compare_field(
            differences,
            field="total_amount",
            order_value=order.get("total_amount"),
            invoice_value=invoice.get("total_amount"),
            comparator=self._amounts_match,
        )

        # 4. Line-item comparison
        self._compare_items(differences, order.get("items", []), invoice.get("items", []))

        # Calculate match percentage
        total_checks = 2 + len(order.get("items", []))  # Vendor + Total + Lines
        mismatches = len(differences)
        if total_checks > 0:
            score = max(0, 100 - (mismatches / total_checks * 100))
        else:
            score = 100 if mismatches == 0 else 0
        
        status = "Match" if len(differences) == 0 else "Mismatch"

        return {
            "status": status, 
            "match_percentage": round(score, 2),
            "differences": differences
        }

    # ------------------------------------------------------------------
    # Field-level comparison helpers
    # ------------------------------------------------------------------

    def _compare_field(
        self,
        differences: list[dict],
        field: str,
        order_value,
        invoice_value,
        comparator,
    ) -> None:
        """Generic single-field comparison; appends to differences if mismatch."""
        if order_value is None and invoice_value is None:
            return  # both missing → nothing to compare
        if not comparator(order_value, invoice_value):
            differences.append({
                "field": field,
                "order_value": self._serialize(order_value),
                "invoice_value": self._serialize(invoice_value),
            })

    def _strings_match(self, a: Optional[str], b: Optional[str]) -> bool:
        """Case-insensitive string comparison with basic normalization."""
        if a is None or b is None:
            return a == b
        return a.strip().lower() == b.strip().lower()

    def _amounts_match(self, a: Optional[float], b: Optional[float]) -> bool:
        """Numeric comparison within tolerance."""
        if a is None or b is None:
            return a == b
        return abs(a - b) <= self.amount_tolerance

    # ------------------------------------------------------------------
    # Item-level comparison
    # ------------------------------------------------------------------

    def _compare_items(
        self,
        differences: list[dict],
        order_items: list[dict],
        invoice_items: list[dict],
    ) -> None:
        """Compare line items between order and invoice."""
        matched_invoice_indices: set[int] = set()

        for o_item in order_items:
            best_idx, best_ratio = self._find_best_match(o_item["name"], invoice_items, matched_invoice_indices)

            if best_idx is None:
                # Item in order but missing from invoice
                differences.append({
                    "field": f"missing_item",
                    "order_value": o_item["name"],
                    "invoice_value": None,
                })
                continue

            matched_invoice_indices.add(best_idx)
            i_item = invoice_items[best_idx]
            item_name = o_item["name"]

            # Quantity check
            if o_item.get("quantity") != i_item.get("quantity"):
                differences.append({
                    "field": f"quantity ({item_name})",
                    "order_value": str(o_item.get("quantity")),
                    "invoice_value": str(i_item.get("quantity")),
                })

            # Unit price check
            o_price = o_item.get("unit_price")
            i_price = i_item.get("unit_price")
            if o_price is not None and i_price is not None:
                if not self._amounts_match(o_price, i_price):
                    differences.append({
                        "field": f"unit_price ({item_name})",
                        "order_value": str(o_price),
                        "invoice_value": str(i_price),
                    })

            # Line total check
            o_total = o_item.get("total")
            i_total = i_item.get("total")
            if o_total is not None and i_total is not None:
                if not self._amounts_match(o_total, i_total):
                    differences.append({
                        "field": f"line_total ({item_name})",
                        "order_value": str(o_total),
                        "invoice_value": str(i_total),
                    })

        # Extra items in invoice but not in order
        for idx, i_item in enumerate(invoice_items):
            if idx not in matched_invoice_indices:
                differences.append({
                    "field": "extra_item",
                    "order_value": None,
                    "invoice_value": i_item["name"],
                })

    def _find_best_match(
        self,
        name: str,
        candidates: list[dict],
        exclude: set[int],
    ) -> tuple[Optional[int], float]:
        """Find the best fuzzy match for an item name among candidates."""
        best_idx: Optional[int] = None
        best_ratio = 0.0
        name_lower = name.lower()

        for idx, candidate in enumerate(candidates):
            if idx in exclude:
                continue
            ratio = SequenceMatcher(None, name_lower, candidate["name"].lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_idx = idx

        if best_ratio >= self.name_similarity_threshold:
            return best_idx, best_ratio
        return None, 0.0

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _serialize(value) -> str:
        """Convert a value to a JSON-friendly string."""
        if value is None:
            return "N/A"
        return str(value)
