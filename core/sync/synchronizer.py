import shutil
import logging
from pathlib import Path


# FolderSynchronizer handles syncing logic between source and replica directories
class FolderSynchronizer:
    def __init__(self, source: Path, replica: Path, logger: logging.Logger, comparison_strategy):
        self.source = source
        self.replica = replica
        self.logger = logger
        self.comparison_strategy = comparison_strategy

    def synchronize(self):
        self._sync_files()
        self._remove_extra_files()

    def _sync_files(self):
        for src_file in self.source.rglob("*"):
            relative_path = src_file.relative_to(self.source)
            replica_file = self.replica / relative_path

            # Skip symbolic links to avoid potential security risks
            if src_file.is_symlink():
                self.logger.warning(f"Skipped symlink: {relative_path}")
                continue

            try:
                if src_file.is_dir():
                    # Create directory if it doesn't exist in replica
                    replica_file.mkdir(parents=True, exist_ok=True)
                else:
                    # Copy or update file if it’s missing or has changed
                    if not replica_file.exists() or self.comparison_strategy.files_are_different(src_file,
                                                                                                 replica_file):
                        replica_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_file, replica_file)
                        self.logger.info(f"Copied/Updated: {relative_path}")
            except Exception as e:
                self.logger.error(f"Error processing {relative_path}: {e}")

    def _remove_extra_files(self):
        for replica_file in self.replica.rglob("*"):
            relative_path = replica_file.relative_to(self.replica)
            src_file = self.source / relative_path

            # Remove file or folder from replica if it doesn't exist in source
            if not src_file.exists():
                try:
                    if replica_file.is_file():
                        replica_file.unlink()
                        self.logger.info(f"Deleted file: {relative_path}")
                    elif replica_file.is_dir():
                        shutil.rmtree(replica_file)
                        self.logger.info(f"Deleted folder: {relative_path}")
                except Exception as e:
                    self.logger.error(f"Error deleting {relative_path}: {e}")
