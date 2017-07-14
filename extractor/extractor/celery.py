from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery(main='extractor', include=['extractor.tasks'])
app.config_from_object('extractor.config')

if __name__ == '__main__':
    app.start()
