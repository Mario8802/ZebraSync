import shutil
import tempfile
import zipfile
from pathlib import Path

from celery import shared_task
from django.conf import settings

from core.models import SyncJob, LogLine
from core.sync.logger import LoggerFactory
from core.sync.synchronizer import FolderSynchronizer
from core.sync.md5 import MD5ComparisonStrategy


@shared_task
def run_sync(job_id: int) -> None:
    job: SyncJob = SyncJob.objects.get(pk=job_id)

    log_path = Path(settings.BASE_DIR, "logs", f"job_{job.id}.log")
    logger = LoggerFactory.create_logger(job, log_path)

    job.status = "running"
    job.save(update_fields=["status"])
    logger.info("Job #%s started for ZIP: %s", job.id, job.src_zip.name)

    try:
        tmp_dir = Path(tempfile.mkdtemp())
        with zipfile.ZipFile(job.src_zip.path) as zf:
            zf.extractall(tmp_dir)

        replica_dir = (
                Path(settings.MEDIA_ROOT) / "replicas" / str(job.user_id) / str(job.id)
        )
        replica_dir.mkdir(parents=True, exist_ok=True)

        syncer = FolderSynchronizer(
            tmp_dir,
            replica_dir,
            logger,
            MD5ComparisonStrategy(),
        )
        syncer.synchronize()

        logger.info("Sync completed.")
        sync_success = True

    except Exception as exc:
        logger.exception("Sync failed: %s", exc)
        sync_success = False

    try:
        has_logs = job.logs.exists()
        has_errors = job.logs.filter(level="error").exists()

        if not has_logs:
            LogLine.objects.create(
                job=job,
                level="warning",
                message="No output generated – check handler configuration.",
            )
            sync_success = False

        if not sync_success or has_errors:
            job.status = "failed"
        else:
            job.status = "done"

        job.save(update_fields=["status"])

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
