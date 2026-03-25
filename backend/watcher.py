"""
watcher.py — Watchdog-based folder monitoring for invoice & product order images.

Watches two directories for new image files, extracts order IDs from filenames,
and triggers the processing pipeline when both files for an ID are available.
"""

import os
import re
import time
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)

# Supported image extensions
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp", ".pdf"}


class DocumentPairTracker:
    """Thread-safe tracker for invoice/product-order file pairs."""

    def __init__(self):
        self._pairs: dict = {}
        self._lock = threading.Lock()

    def add_file(self, order_id: str, doc_type: str, file_path: str) -> dict | None:
        """
        Register a file and return the pair dict if both files are now available.

        Args:
            order_id: The shared identifier (e.g. "1001")
            doc_type: Either "invoice" or "order"
            file_path: Absolute path to the file

        Returns:
            The pair dict {"invoice": path, "order": path} if complete, else None.
        """
        with self._lock:
            if order_id not in self._pairs:
                self._pairs[order_id] = {}

            self._pairs[order_id][doc_type] = file_path
            logger.info(f"  Registered {doc_type} for ID {order_id}: {os.path.basename(file_path)}")

            # Check if pair is complete
            pair = self._pairs[order_id]
            if "invoice" in pair and "order" in pair:
                # Remove from tracker and return the complete pair
                complete_pair = self._pairs.pop(order_id)
                return complete_pair

            return None

    def get_pending_ids(self) -> list:
        """Return list of IDs that have only one file registered."""
        with self._lock:
            return list(self._pairs.keys())


def parse_filename(filename: str) -> tuple:
    """
    Extract document type and order ID from filename.

    Supported patterns:
        invoice_1001.jpg      → ("invoice", "1001")
        productorder_1001.jpg → ("order",   "1001")

    Returns:
        (doc_type, order_id) or (None, None) if not recognized.
    """
    basename = os.path.splitext(filename)[0].lower()

    # Match invoice_XXXX
    match = re.match(r"^invoice[_\-]?(\w+)$", basename)
    if match:
        return "invoice", match.group(1)

    # Match productorder_XXXX or product_order_XXXX
    match = re.match(r"^product[_\-]?order[_\-]?(\w+)$", basename)
    if match:
        return "order", match.group(1)

    return None, None


class FolderEventHandler(FileSystemEventHandler):
    """
    Watchdog event handler that detects new files in monitored folders
    and triggers processing when both invoice and PO arrive for the same ID.
    """

    def __init__(self, tracker: DocumentPairTracker, process_callback, delay: float = 2.0):
        super().__init__()
        self.tracker = tracker
        self.process_callback = process_callback
        self.delay = delay

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()

        # Ignore unsupported files
        if ext not in SUPPORTED_EXTENSIONS:
            logger.debug(f"  Ignoring non-image file: {filename}")
            return

        logger.info(f"📄 New file detected: {filename}")

        # Wait for file to be fully copied
        time.sleep(self.delay)

        # Parse filename to get doc type and order ID
        doc_type, order_id = parse_filename(filename)
        if doc_type is None or order_id is None:
            logger.warning(f"  ⚠ Could not parse filename: {filename}")
            logger.warning(f"    Expected format: invoice_XXXX.jpg or productorder_XXXX.jpg")
            return

        # Register file and check if pair is complete
        complete_pair = self.tracker.add_file(order_id, doc_type, file_path)

        if complete_pair:
            logger.info(f"✅ Pair complete for ID {order_id} — triggering processing...")
            # Run processing in a separate thread to not block the watcher
            thread = threading.Thread(
                target=self.process_callback,
                args=(order_id, complete_pair),
                daemon=True,
            )
            thread.start()
        else:
            logger.info(f"  ⏳ Waiting for matching file for ID {order_id}...")


def start_watching(invoice_dir: str, order_dir: str, process_callback) -> Observer:
    """
    Start watching both directories for new files.

    Args:
        invoice_dir: Path to the invoice folder
        order_dir: Path to the product order folder
        process_callback: Function to call when a pair is complete.
                          Signature: callback(order_id: str, pair: dict)

    Returns:
        The watchdog Observer instance (already started).
    """
    tracker = DocumentPairTracker()
    handler = FolderEventHandler(tracker, process_callback)

    observer = Observer()
    observer.schedule(handler, invoice_dir, recursive=False)
    observer.schedule(handler, order_dir, recursive=False)
    observer.start()

    logger.info(f"👁  Watching: {invoice_dir}")
    logger.info(f"👁  Watching: {order_dir}")

    return observer
