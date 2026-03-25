"""
run_watcher.py — Entry point for the automated file monitoring system.

Creates the required folder structure, initializes the database,
and starts watching for invoice/product order files.

Usage:
    python run_watcher.py
"""

import os
import sys
import time
import logging

# Ensure the backend directory is on the import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from watcher import start_watching
from processor import process_pair, init_database

# =========================
# CONFIGURATION
# =========================
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Documents")
INVOICE_DIR = os.path.join(BASE_DIR, "invoice")
ORDER_DIR = os.path.join(BASE_DIR, "product_order")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")

# =========================
# LOGGING SETUP
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_directories():
    """Create the required folder structure."""
    for d in [INVOICE_DIR, ORDER_DIR, REPORTS_DIR, PROCESSED_DIR]:
        os.makedirs(d, exist_ok=True)
        logger.info(f"  📁 Ready: {d}")


def on_pair_ready(order_id: str, pair: dict):
    """Callback invoked by the watcher when both files for an ID are available."""
    process_pair(order_id, pair, REPORTS_DIR, PROCESSED_DIR)


def main():
    print()
    print("=" * 60)
    print("  📄 Invoice & PO Validator — File Watcher")
    print("=" * 60)
    print()

    # 1. Create folders
    logger.info("Setting up directories...")
    create_directories()
    print()

    # 2. Initialize database
    logger.info("Initializing database...")
    init_database()
    print()

    # 3. Start watching
    logger.info("Starting file watcher...")
    observer = start_watching(INVOICE_DIR, ORDER_DIR, on_pair_ready)
    print()

    logger.info("🟢 System is running. Drop files into the folders above.")
    logger.info("   Press Ctrl+C to stop.")
    print()
    logger.info("Expected filename formats:")
    logger.info("   invoice_1001.jpg      → Documents/invoice/")
    logger.info("   productorder_1001.jpg → Documents/product_order/")
    print()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("")
        logger.info("🛑 Shutting down watcher...")
        observer.stop()

    observer.join()
    logger.info("👋 Goodbye!")


if __name__ == "__main__":
    main()
