import datetime
import json
from decimal import Decimal


def to_json(v):
    """
    :type v: object
    :rtype: str
    """
    return json.dumps(v, default=custom_handling)


def custom_handling(v):
    """
    :type v: object
    :rtype: basestring | int | float | list | dict | None
    """
    if isinstance(v, datetime.datetime):
        return v.isoformat()
    elif isinstance(v, Decimal):
        return float(v)
    elif isinstance(v, set):
        return list(v)
    else:
        return v.__dict__
