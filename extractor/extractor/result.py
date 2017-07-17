from commons.abstractions.model import Model


def build_extraction_result(celery_async_result):
    if celery_async_result.successful():
        return ExtractionResult(task_id=str(celery_async_result.id), status=str(celery_async_result.status),
                                data=celery_async_result.result)
    else:
        return ExtractionResult(task_id=str(celery_async_result.id), status=str(celery_async_result.status),
                                data=None)


class ExtractionResult(Model):
    def __init__(self, task_id, status, data):
        self.task_id = task_id
        self.status = status
        self.data = data
