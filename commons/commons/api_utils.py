import datetime
import json
from decimal import Decimal
import cherrypy

# def to_json(to_serialize):
#     """
#     :type to_serialize: object | Enum
#     :rtype: str
#     """
#     try:
#         return json.dumps(to_serialize)
#     except Exception as e:
#         print(e)
#     return json.dumps(_make_serializable(to_serialize))
#
#
# def _make_serializable(to_serialize):
#     """
#     :type to_serialize: object
#     :rtype: basestring | dict | list | int | float
#     """
#     if isinstance(to_serialize, datetime.datetime):
#         serializable = to_serialize.isoformat()
#     elif isinstance(to_serialize, Decimal):
#         serializable = float(to_serialize)
#     elif isinstance(to_serialize, set):
#         serializable = list(to_serialize)
#     else:
#         serializable = to_serialize.__dict__
#     return serializable


def jsonResponse(obj, default=None):
    return json.dumps(obj, default=default)


def jsonify(f):
    def wrapped(*args, **kwargs):
        def custom_handling(v):
            if isinstance(v, datetime.datetime):
                return v.isoformat()
            elif isinstance(v, Decimal):
                return float(v)
            else:
                return v.__dict__

        return jsonResponse(f(*args, **kwargs), default=custom_handling)

    return wrapped
