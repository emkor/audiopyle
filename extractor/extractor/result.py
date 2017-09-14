from typing import Text, Optional, Any, Dict

from celery.result import AsyncResult

from commons.abstractions.model import Model


class ExtractionResult(Model):
    def __init__(self, task_id: Text, status: Text, data: Optional[Dict[Text, Any]]):
        self.task_id = task_id
        self.status = status
        self.data = data


def build_extraction_result(celery_async_result: AsyncResult) -> ExtractionResult:
    if celery_async_result.successful():
        return ExtractionResult(task_id=str(celery_async_result.id), status=str(celery_async_result.status),
                                data=celery_async_result.result)
    else:
        return ExtractionResult(task_id=str(celery_async_result.id), status=str(celery_async_result.status),
                                data=None)
