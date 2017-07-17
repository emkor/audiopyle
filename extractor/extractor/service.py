from extractor.celery import get_celery
from extractor.result import build_extraction_result


def run_task(task, *args):
    """
    Method just to have type checking
    :type task: callable
    :rtype: celery.result.AsyncResult
    """
    return task.delay(*args)


def retrieve_result(task_id):
    """
    Method just to have type checking
    :type task_id: str
    :rtype: extractor.result.ExtractionResult
    """
    celery_app = get_celery()
    async_result = celery_app.AsyncResult(id=task_id)
    return build_extraction_result(async_result)
