"""
processor.py — Pipeline coordinator for invoice vs purchase order comparison.

Replicates the exact logic of the /compare endpoint in main.py,
calling the same services (gemini_service, comparison_service, risk_service)
but reading files from disk instead of receiving uploads.
"""

import os
import shutil
import logging
import mimetypes

from database import SessionLocal, engine
from models import Base, DocumentType, ComparisonResult
from services.gemini_service import extract_document
from services.comparison_service import compare_documents
from services.risk_service import calculate_risk
from utils.timing import timer
from report import generate_report

logger = logging.getLogger(__name__)


def init_database():
    """Create database tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized.")


def _read_file(file_path: str) -> tuple:
    """Read file bytes and determine content type."""
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = "application/octet-stream"

    return file_bytes, content_type


def process_pair(order_id: str, pair: dict, reports_dir: str, processed_dir: str):
    """
    Process a matched invoice + product order pair.

    This function replicates the exact logic of the /compare endpoint
    in main.py, using the same service functions.

    Args:
        order_id: The shared order identifier (e.g. "1001")
        pair: Dict with "invoice" and "order" keys pointing to file paths
        reports_dir: Directory to save the generated report
        processed_dir: Directory to move processed files into
    """
    invoice_path = pair["invoice"]
    order_path = pair["order"]

    logger.info(f"{'='*60}")
    logger.info(f"Processing Order ID: {order_id}")
    logger.info(f"  Invoice:  {os.path.basename(invoice_path)}")
    logger.info(f"  PO:       {os.path.basename(order_path)}")
    logger.info(f"{'='*60}")

    db = SessionLocal()

    try:
        with timer() as total_timer:
            # --- Extract invoice ---
            logger.info("  📤 Extracting invoice data via Gemini...")
            inv_bytes, inv_content_type = _read_file(invoice_path)
            inv_result = extract_document(
                file_bytes=inv_bytes,
                filename=os.path.basename(invoice_path),
                content_type=inv_content_type,
                document_type=DocumentType.invoice,
                db=db,
            )
            logger.info(f"    Source: {inv_result['source']} | Duplicate: {inv_result['duplicate']}")

            # --- Extract purchase order ---
            logger.info("  📤 Extracting purchase order data via Gemini...")
            po_bytes, po_content_type = _read_file(order_path)
            po_result = extract_document(
                file_bytes=po_bytes,
                filename=os.path.basename(order_path),
                content_type=po_content_type,
                document_type=DocumentType.purchase_order,
                db=db,
            )
            logger.info(f"    Source: {po_result['source']} | Duplicate: {po_result['duplicate']}")

            # --- Compare (exact same call as main.py line 115) ---
            logger.info("  🔍 Comparing documents...")
            comparison = compare_documents(inv_result["data"], po_result["data"])

            # --- Risk scoring (exact same call as main.py lines 118-123) ---
            logger.info("  ⚖  Calculating risk score...")
            risk = calculate_risk(
                summary=comparison["summary"],
                line_item_analysis=comparison["line_item_analysis"],
                invoice_currency=inv_result["data"].get("currency"),
                po_currency=po_result["data"].get("currency"),
            )

        # --- Build result dict (exact same structure as main.py lines 125-132) ---
        result = {
            "summary": comparison["summary"].model_dump(),
            "line_item_analysis": [item.model_dump() for item in comparison["line_item_analysis"]],
            "confidence_score": comparison["confidence_score"],
            "risk_score": risk.risk_score,
            "risk_reason": risk.risk_reason,
            "processing_time_ms": total_timer["elapsed_ms"],
        }

        # --- Generate report ---
        report_path = generate_report(order_id, result, reports_dir)
        logger.info(f"  📝 Report saved: {report_path}")

        # --- Store result in database ---
        record = ComparisonResult(
            order_id=order_id,
            match_status=result["summary"]["status"],
            risk_score=result["risk_score"],
            confidence_score=result.get("confidence_score"),
            result_json=result,
        )
        db.add(record)
        db.commit()
        logger.info(f"  💾 Result saved to database")

        # --- Move processed files ---
        _move_to_processed(invoice_path, processed_dir)
        _move_to_processed(order_path, processed_dir)
        logger.info(f"  📁 Files moved to: {processed_dir}")

        logger.info(f"  ✅ Order {order_id} processed in {total_timer['elapsed_ms']:.0f} ms")
        logger.info("")

    except Exception as e:
        logger.error(f"  ❌ Error processing order {order_id}: {e}")
        logger.exception("  Full traceback:")

    finally:
        db.close()


def _move_to_processed(file_path: str, processed_dir: str):
    """Move a file to the processed directory."""
    os.makedirs(processed_dir, exist_ok=True)
    dest = os.path.join(processed_dir, os.path.basename(file_path))

    # If file already exists in processed, add a suffix
    if os.path.exists(dest):
        name, ext = os.path.splitext(os.path.basename(file_path))
        counter = 1
        while os.path.exists(dest):
            dest = os.path.join(processed_dir, f"{name}_{counter}{ext}")
            counter += 1

    shutil.move(file_path, dest)
