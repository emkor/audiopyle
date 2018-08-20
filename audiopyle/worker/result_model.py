from typing import Any, Dict
from celery.result import AsyncResult
import celery.states as celery_state
from enum import Enum

from audiopyle.lib.abstractions.model import Model
from audiopyle.lib.utils.logger import get_logger

logger = get_logger()


class TaskStatus(Enum):
    not_known = "not_known"
    in_progress = "in_progress"
    done = "done"
    failed = "failed"
    ignored = "ignored"


CELERY_TO_AUDIOPYLE_STATUS_MAP = {celery_state.PENDING: TaskStatus.not_known,
                                  celery_state.RECEIVED: TaskStatus.in_progress,
                                  celery_state.STARTED: TaskStatus.in_progress,
                                  celery_state.RETRY: TaskStatus.in_progress,
                                  celery_state.SUCCESS: TaskStatus.done,
                                  celery_state.FAILURE: TaskStatus.failed,
                                  celery_state.REVOKED: TaskStatus.ignored,
                                  celery_state.REJECTED: TaskStatus.ignored,
                                  celery_state.IGNORED: TaskStatus.ignored}


def map_celery_status(celery_status: str) -> TaskStatus:
    return CELERY_TO_AUDIOPYLE_STATUS_MAP[celery_status]


class ExtractionResult(Model):
    def __init__(self, task_id: str, status: TaskStatus) -> None:
        self.task_id = task_id
        self.status = status

    def to_serializable(self):
        super_serialized = super().to_serializable()
        super_serialized.update({"status": super_serialized["status"].value})
        return super_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[str, Any]):
        status_value = serialized["status"]
        serialized.update({"status": TaskStatus(status_value)})
        return serialized


def build_extraction_result(celery_async_result: AsyncResult) -> ExtractionResult:
    celery_task_id = str(celery_async_result.id)
    celery_task_status = str(celery_async_result.status)
    logger.debug("Building result from task id {} and status {}...".format(celery_task_id, celery_task_status))
    return ExtractionResult(task_id=celery_task_id, status=map_celery_status(celery_task_status))
