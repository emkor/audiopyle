from __future__ import absolute_import, unicode_literals
from celery import Celery

from commons.utils.logger import setup_logger

app = Celery(main='extractor', include=['extractor.tasks'])
app.config_from_object('extractor.config')


def get_celery():
    """
    :rtype: celery.Celery
    """
    global app
    return app


if __name__ == '__main__':
    setup_logger()
    app.start()
