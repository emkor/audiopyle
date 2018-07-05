import os

from typing import Text, Type, Any, Optional

from commons.utils.logger import get_logger

logger = get_logger()


def read_env_var(var_name: Text, expected_type: Type, default: Optional[Any] = None) -> Any:
    return _select_value(var_name, expected_type, default, os.environ.get(var_name))


def _select_value(var_name: str, expected_type: Type, default: Optional[Any], actual: Optional[Any]) -> Any:
    if actual is not None:
        try:
            return expected_type(actual)
        except ValueError as e:
            logger.warning("Could not cast {}={} to {}: {}. Using default: {}".format(var_name, actual,
                                                                                      expected_type, e, default))
            return default
        except Exception as e:
            logger.error("Error on reading variable {}: {}. Using default: {}".format(var_name, e, default))
            return default
    else:
        logger.warning("Variable {} was not set. Using default: {}".format(var_name, default))
        return default
