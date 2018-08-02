from celery import Celery
import pymysql

pymysql.install_as_MySQLdb()

app = Celery(main='audiopyle.worker.engine', include=['audiopyle.worker.engine.tasks'])
app.config_from_object('audiopyle.worker.engine.config')


def get_celery() -> Celery:
    global app
    return app
