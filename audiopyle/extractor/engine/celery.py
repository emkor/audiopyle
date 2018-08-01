from celery import Celery
import pymysql

from commons.utils.logger import setup_logger

pymysql.install_as_MySQLdb()

app = Celery(main='extractor.engine', include=['extractor.engine.tasks'])
app.config_from_object('extractor.engine.config')


def get_celery() -> Celery:
    global app
    return app


if __name__ == '__main__':
    setup_logger()
    app.start()
