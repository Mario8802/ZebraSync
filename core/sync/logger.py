# core/sync/logger.py
import logging
from pathlib import Path
from core.models import SyncJob, LogLine


class DatabaseLogHandler(logging.Handler):
    """Записва всеки лог ред в таблица LogLine."""

    def __init__(self, job: SyncJob):
        super().__init__()
        self.job = job

    def emit(self, record):
        try:
            LogLine.objects.create(
                job=self.job,
                level=record.levelname.lower(),
                message=self.format(record)
            )
        except Exception:
            # Не спираме задачата, ако БД временно не отговори
            pass


class LoggerFactory:

    @staticmethod
    def create_logger(job: SyncJob, log_path: Path | None = None) -> logging.Logger:
        logger = logging.getLogger(f"FolderSyncJob{job.id}")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()

        # Format
        file_fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        db_fmt = logging.Formatter("%(message)s")

        # File-
        if log_path:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(log_path, encoding="utf-8")
            fh.setFormatter(file_fmt)
            logger.addHandler(fh)

        # Console
        ch = logging.StreamHandler()
        ch.setFormatter(file_fmt)
        logger.addHandler(ch)

        # DB
        db = DatabaseLogHandler(job)
        db.setFormatter(db_fmt)
        logger.addHandler(db)

        logger.propagate = False
        return logger
