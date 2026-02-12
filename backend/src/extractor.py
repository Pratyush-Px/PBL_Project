"""
Structured Document Extractor
Extracts structured fields from cleaned OCR text using regex + rule-based parsing.
No ML models or external invoice libraries — pure pattern matching.
"""

import re
from typing import Optional


class DocumentExtractor:
    """
    Extracts structured invoice/order data from cleaned OCR text.
    Each extraction method is independent and can be improved individually.
    """

    def extract(self, text: str, document_type: Optional[str] = None) -> dict:
        """
        Main entry point: extract all fields from OCR text.

        :param text: Cleaned OCR text string.
        :param document_type: Optional hint ("invoice" or "order"). Auto-detected if None.
        :return: Structured dict with all extracted fields.
        """
        doc_type = document_type or self._detect_document_type(text)
        return {
            "document_type": doc_type,
            "vendor": self._extract_vendor(text),
            "invoice_number": self._extract_invoice_number(text),
            "date": self._extract_date(text),
            "items": self._extract_items(text),
            "total_amount": self._extract_total_amount(text),
        }

    # ------------------------------------------------------------------
    # Document type detection
    # ------------------------------------------------------------------

    def _detect_document_type(self, text: str) -> str:
        """Infer whether the document is an invoice or a purchase order."""
        upper = text.upper()
        order_keywords = ["PURCHASE ORDER", "P.O.", "PO NUMBER", "PO NO", "ORDER #", "ORDER NO"]
        invoice_keywords = ["INVOICE", "INV-", "INV NO", "BILL TO", "AMOUNT DUE"]

        order_score = sum(1 for kw in order_keywords if kw in upper)
        invoice_score = sum(1 for kw in invoice_keywords if kw in upper)

        if order_score > invoice_score:
            return "order"
        return "invoice"

    # ------------------------------------------------------------------
    # Vendor extraction
    # ------------------------------------------------------------------

    def _extract_vendor(self, text: str) -> Optional[str]:
        """
        Extract vendor / supplier name.
        Strategy: look for labelled lines first, then fall back to the first
        non-empty line of the document.
        """
        patterns = [
            r"(?:vendor|supplier|from|bill\s*from|sold\s*by|company)\s*[:\-]\s*(.+)",
        ]
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                return m.group(1).strip()

        # Fallback: first non-empty line that isn't a common header keyword
        for line in text.splitlines():
            line = line.strip()
            if line and not re.match(
                r"^(invoice|purchase\s*order|date|bill\s*to|ship\s*to|order|po|#|page)",
                line,
                re.IGNORECASE,
            ):
                return line
        return None

    # ------------------------------------------------------------------
    # Invoice / PO number extraction
    # ------------------------------------------------------------------

    def _extract_invoice_number(self, text: str) -> Optional[str]:
        """Extract invoice or PO number."""
        patterns = [
            r"(?:invoice|inv|bill)\s*(?:#|no\.?|number)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
            r"INV[- ]?(\d+)",
            r"(?:purchase\s*order|po)\s*(?:#|no\.?|number)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
            r"PO[- ]?(\d+)",
            r"(?:order)\s*(?:#|no\.?|number)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
        ]
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                return m.group(1).strip()
        return None

    # ------------------------------------------------------------------
    # Date extraction
    # ------------------------------------------------------------------

    def _extract_date(self, text: str) -> Optional[str]:
        """Extract the first recognisable date from the text."""
        # Try labelled dates first
        labelled = re.search(
            r"(?:date|dated|invoice\s*date|order\s*date|due\s*date)\s*[:\-]?\s*(.+)",
            text,
            re.IGNORECASE,
        )
        if labelled:
            date_str = self._parse_date_string(labelled.group(1).strip())
            if date_str:
                return date_str

        # Unlabelled fallback: find any date-like pattern in full text
        return self._parse_date_string(text)

    def _parse_date_string(self, text: str) -> Optional[str]:
        """Find the first date-like pattern in a string."""
        date_patterns = [
            # MM/DD/YYYY or DD/MM/YYYY or YYYY/MM/DD (with / - or .)
            r"\b(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})\b",
            r"\b(\d{4}[/\-\.]\d{1,2}[/\-\.]\d{1,2})\b",
            # Month DD, YYYY  or  DD Month YYYY
            r"\b([A-Za-z]+\.?\s+\d{1,2},?\s+\d{4})\b",
            r"\b(\d{1,2}\s+[A-Za-z]+\.?\s+\d{4})\b",
        ]
        for pat in date_patterns:
            m = re.search(pat, text)
            if m:
                return m.group(1).strip()
        return None

    # ------------------------------------------------------------------
    # Line-item extraction
    # ------------------------------------------------------------------

    def _extract_items(self, text: str) -> list[dict]:
        """
        Extract table rows that look like line items.
        Expected patterns (flexible spacing / separators):
            Description   Qty   Unit Price   Total
            Widget A      2     10.00        20.00
        """
        items: list[dict] = []

        # Pattern: description text, then 2-3 numeric columns
        # Captures: (item_name) (quantity) (unit_price) (line_total)
        row_pattern = re.compile(
            r"^"
            r"(.+?)"                                    # item name (non-greedy)
            r"\s+"
            r"(\d+(?:\.\d+)?)"                          # quantity
            r"\s+"
            r"\$?\s*(\d+(?:[,\d]*\.\d{1,2}))"          # unit price
            r"\s+"
            r"\$?\s*(\d+(?:[,\d]*\.\d{1,2}))"          # line total
            r"\s*$",
            re.MULTILINE,
        )
        for m in row_pattern.finditer(text):
            name = m.group(1).strip()
            # Skip header-like rows
            if re.match(r"^(item|description|product|service|qty|quantity|price|total|#|no)", name, re.IGNORECASE):
                continue
            items.append({
                "name": name,
                "quantity": self._to_number(m.group(2)),
                "unit_price": self._to_number(m.group(3)),
                "total": self._to_number(m.group(4)),
            })

        # Fallback: try 3-column rows (name, qty, total — no separate unit_price)
        if not items:
            row_pattern_3col = re.compile(
                r"^"
                r"(.+?)"
                r"\s+"
                r"(\d+(?:\.\d+)?)"
                r"\s+"
                r"\$?\s*(\d+(?:[,\d]*\.\d{1,2}))"
                r"\s*$",
                re.MULTILINE,
            )
            for m in row_pattern_3col.finditer(text):
                name = m.group(1).strip()
                if re.match(r"^(item|description|product|service|qty|quantity|price|total|#|no)", name, re.IGNORECASE):
                    continue
                qty = self._to_number(m.group(2))
                total = self._to_number(m.group(3))
                unit_price = round(total / qty, 2) if qty else 0.0
                items.append({
                    "name": name,
                    "quantity": qty,
                    "unit_price": unit_price,
                    "total": total,
                })

        return items

    # ------------------------------------------------------------------
    # Total amount extraction
    # ------------------------------------------------------------------

    def _extract_total_amount(self, text: str) -> Optional[float]:
        """Extract the final total / grand total / amount due."""
        patterns = [
            r"(?:grand\s*total|total\s*amount|amount\s*due|total\s*due|balance\s*due|net\s*amount)\s*[:\-]?\s*\$?\s*([\d,]+\.?\d*)",
            r"(?:^|\n)\s*total\s*[:\-]?\s*\$?\s*([\d,]+\.?\d*)",
        ]
        # Walk patterns in priority order; take the LAST match of each
        for pat in patterns:
            matches = list(re.finditer(pat, text, re.IGNORECASE | re.MULTILINE))
            if matches:
                return self._to_number(matches[-1].group(1))
        return None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _to_number(s: str) -> float:
        """Convert a string like '1,234.56' to a float."""
        try:
            return float(s.replace(",", ""))
        except (ValueError, TypeError):
            return 0.0
