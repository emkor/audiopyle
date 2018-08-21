from celery import Task
from celery.result import AsyncResult

from audiopyle.worker.engine.celery import get_celery
from audiopyle.worker.result_model import build_extraction_result, ExtractionResult


def run_task(task: Task, task_id: str, **kwargs) -> AsyncResult:
    """Method just to have type checking"""
    return task.apply_async(kwargs=kwargs, task_id=task_id)


def retrieve_result(task_id: str) -> ExtractionResult:
    """Method just to have type checking"""
    celery_app = get_celery()
    async_result = celery_app.AsyncResult(id=task_id)
    return build_extraction_result(async_result)


def delete_result(task_id: str) -> bool:
    """Deletes the result if present. Returns success or failure in case of no task in DB"""
    celery_app = get_celery()
    async_result = celery_app.AsyncResult(id=task_id)
    if async_result.ready():
        async_result.forget()
        return True
    else:
        return False


def has_finished(task_id: str) -> bool:
    """Deletes the result if present. Returns success or failure in case of no task in DB"""
    celery_app = get_celery()
    async_result = celery_app.AsyncResult(id=task_id)
    return async_result.ready()
