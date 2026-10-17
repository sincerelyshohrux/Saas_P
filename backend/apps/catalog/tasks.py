import logging

from celery import shared_task

from .importers.excel import ImportFileError, run_import
from .models import ImportJob

logger = logging.getLogger(__name__)


@shared_task
def process_product_import(job_id: str) -> None:
    job = ImportJob.objects.get(pk=job_id)
    job.status = ImportJob.Status.PROCESSING
    job.save(update_fields=["status", "updated_at"])
    try:
        run_import(job)
    except ImportFileError as exc:
        job.status, job.error_message = ImportJob.Status.FAILED, str(exc)[:255]
        job.save(update_fields=["status", "error_message", "updated_at"])
    except Exception:  # kutilmagan xato: tafsilotni foydalanuvchiga ko'rsatmaymiz
        logger.exception("Product import failed: job=%s", job_id)
        job.status = ImportJob.Status.FAILED
        job.error_message = "Import vaqtida kutilmagan xatolik. Qayta urinib ko'ring."
        job.save(update_fields=["status", "error_message", "updated_at"])