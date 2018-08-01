from celery import Celery
import pymysql

from audiopyle.commons.utils.logger import setup_logger

pymysql.install_as_MySQLdb()

app = Celery(main='audiopyle.extractor.engine', include=['audiopyle.extractor.engine.tasks'])
app.config_from_object('audiopyle.extractor.engine.config')


def get_celery() -> Celery:
    global app
    return app


def main():
    setup_logger()
    app.worker_main()


if __name__ == '__main__':
    main()
