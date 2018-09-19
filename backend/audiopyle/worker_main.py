#!/usr/bin/env python3

from audiopyle.lib.utils.logger import setup_logger
from audiopyle.worker.engine.celery import get_celery


def main():
    setup_logger()
    app = get_celery()
    app.worker_main()


if __name__ == '__main__':
    main()
