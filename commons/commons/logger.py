import logging

import time

GLOBAL_LOGGER = None


def setup_logger(level=logging.INFO):
    print("*** Initializing logger, should happen once per app! ***")
    logging.basicConfig(format='%(levelname)s | %(asctime)s UTC | %(message)s', level=level)
    logging.Formatter.converter = time.gmtime


def get_logger(calling_module="audiopyle"):
    """
    :type calling_module: str
    :rtype: logging.Logger
    """
    global GLOBAL_LOGGER
    if GLOBAL_LOGGER is None:
        GLOBAL_LOGGER = logging.getLogger(calling_module)
    return GLOBAL_LOGGER
