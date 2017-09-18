import logging
import time
from typing import Text

GLOBAL_LOGGER = None


def setup_logger(level: int = logging.INFO) -> None:
    print("*** Initializing logger, should happen once per app! ***")
    logging.basicConfig(format='%(levelname)s | %(asctime)s UTC | %(message)s', level=level)
    logging.Formatter.converter = time.gmtime


def get_logger(calling_module: Text = "audiopyle") -> logging.Logger:
    global GLOBAL_LOGGER
    if GLOBAL_LOGGER is None:
        GLOBAL_LOGGER = logging.getLogger(calling_module)
    return GLOBAL_LOGGER
