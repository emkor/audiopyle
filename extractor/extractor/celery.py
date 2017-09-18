from __future__ import absolute_import, unicode_literals
from celery import Celery
import pymysql

from commons.utils.logger import setup_logger

pymysql.install_as_MySQLdb()

app = Celery(main='extractor', include=['extractor.tasks'])
app.config_from_object('extractor.config')


def get_celery() -> Celery:
    global app
    return app


if __name__ == '__main__':
    setup_logger()
    app.start()
