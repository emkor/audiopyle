import json
import os
from typing import Text, Optional, Any, Dict

from celery.result import AsyncResult

from commons.abstractions.model import Model
from commons.utils.file_system import RESULTS_DIR


class ExtractionResult(Model):
    def __init__(self, task_id: Text, status: Text, data: Optional[Dict[Text, Any]]) -> None:
        self.task_id = task_id
        self.status = status
        self.data = data


def build_extraction_result(celery_async_result: AsyncResult) -> ExtractionResult:
    if celery_async_result.successful():
        result_file_absolute_path = os.path.join(RESULTS_DIR, celery_async_result.result)
        with open(result_file_absolute_path) as result_file:
            data = json.load(result_file)
        return ExtractionResult(task_id=str(celery_async_result.id), status=str(celery_async_result.status),
                                data=data)
    else:
        return ExtractionResult(task_id=str(celery_async_result.id), status=str(celery_async_result.status),
                                data=None)
