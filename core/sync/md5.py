import hashlib
import logging
from pathlib import Path


# MD5ComparisonStrategy uses md5 hashes to determine if files differ
class MD5ComparisonStrategy:
    @staticmethod
    def files_are_different(file1: Path, file2: Path) -> bool:
        try:
            return MD5ComparisonStrategy._calculate_md5(file1) != MD5ComparisonStrategy._calculate_md5(file2)
        except Exception as e:
            logger = logging.getLogger("FolderSyncLogger")
            logger.warning(f"⚠ Failed to compare files: {file1} and {file2} due to error: {e}")
            return True  # Treat as different if comparison fails

    @staticmethod
    def _calculate_md5(file_path: Path) -> str:
        # Efficiently compute md5 hash by reading file in chunks
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
