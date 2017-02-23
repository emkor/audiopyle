import datetime
import json
from decimal import Decimal


def to_json(to_serialize):
    """
    :type to_serialize: object | Enum
    :rtype: str
    """
    try:
        return json.dumps(to_serialize)
    except Exception as e:
        print(e)
    return json.dumps(_make_serializable(to_serialize))


def _make_serializable(to_serialize):
    """
    :type to_serialize: object
    :rtype: basestring | dict | list | int | float
    """
    if isinstance(to_serialize, datetime.datetime):
        serializable = to_serialize.isoformat()
    elif isinstance(to_serialize, Decimal):
        serializable = float(to_serialize)
    elif isinstance(to_serialize, set):
        serializable = list(to_serialize)
    else:
        serializable = to_serialize.__dict__
    return serializable
