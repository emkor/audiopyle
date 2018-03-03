import os

from typing import Text, Type, Any, Optional

from commons.utils.logger import get_logger

logger = get_logger()


def read_env_var(var_name: Text, expected_type: Type, default: Optional[Any] = None):
    env_var = os.environ._get(var_name)
    if env_var is not None:
        try:
            return expected_type(env_var)
        except ValueError as e:
            logger.warning("Could not cast {}={} to {}: {}. Using default: {}".format(var_name, env_var,
                                                                                      expected_type, e, default))
            return default
        except Exception as e:
            logger.error("Error on reading variable {}: {}. Using default: {}".format(var_name, e, default))
            return default
    else:
        logger.warning("Variable {} was not set. Using default: {}".format(var_name, default))
        return default
