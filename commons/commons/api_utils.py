import datetime
import json
from decimal import Decimal


def to_json(to_serialize):
    """
    :type to_serialize: object | Enum
    :rtype: str
    """
    if isinstance(to_serialize, datetime.datetime):
        serializable = to_serialize.isoformat()
    elif isinstance(to_serialize, Decimal):
        serializable = float(to_serialize)
    elif isinstance(to_serialize, set):
        serializable = list(to_serialize)
    else:
        serializable = to_serialize.__dict__
    return json.dumps(serializable)
