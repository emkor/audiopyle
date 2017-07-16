def run_task(task, *args):
    """
    Method just to have type checking
    :type task: callable
    :rtype: celery.result.AsyncResult
    """
    return task.delay(*args)
