import logging


def myGetLogger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(funcName)s | %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
