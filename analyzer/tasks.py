from celery import Celery

app = Celery('tasks', broker='pyamqp://rabbitmq:rabbitmq@rabbit1//', backend="redis://redis1")


@app.task
def add(x, y):
    return x + y
