from pydantic import BaseModel, Field
from typing import List, Optional


# =========================
# LINE ITEM SCHEMA
# =========================
class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None


# =========================
# EXTRACTION SCHEMAS
# =========================
class InvoiceExtract(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    vendor_name: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    confidence_score: Optional[float] = Field(default=None, ge=0, le=100)


class PurchaseOrderExtract(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    vendor_name: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    confidence_score: Optional[float] = Field(default=None, ge=0, le=100)


# =========================
# EXTRACTION RESPONSE
# =========================
class ExtractionResponse(BaseModel):
    status: str = "success"
    source: str  # "cache" or "gemini"
    duplicate: bool
    extracted_data: dict
    extraction_time_ms: float


# =========================
# COMPARISON SCHEMAS
# =========================
class LineItemAnalysis(BaseModel):
    description: str
    invoice_qty: Optional[float] = None
    po_qty: Optional[float] = None
    invoice_price: Optional[float] = None
    po_price: Optional[float] = None
    status: str  # "match", "quantity_mismatch", "price_mismatch", "missing_in_po", "extra_in_invoice"


class ComparisonSummary(BaseModel):
    invoice_total: Optional[float] = None
    po_total: Optional[float] = None
    difference: Optional[float] = None
    status: str  # "match", "mismatch"


class RiskResult(BaseModel):
    risk_score: int
    risk_reason: str


class ComparisonResponse(BaseModel):
    summary: ComparisonSummary
    line_item_analysis: List[LineItemAnalysis]
    confidence_score: Optional[float] = None
    risk_score: int
    risk_reason: str
    processing_time_ms: float
