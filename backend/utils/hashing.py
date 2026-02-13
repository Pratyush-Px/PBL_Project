import hashlib


def calculate_file_hash(file_bytes: bytes) -> str:
    """
    Create a stable SHA256 fingerprint for uploaded files.
    Same file content => same hash.
    """
    return hashlib.sha256(file_bytes).hexdigest()
