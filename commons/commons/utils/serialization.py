import datetime
import json
from decimal import Decimal
from typing import Any, Text, Dict, Type
from vampyhost import RealTime

from numpy.core.multiarray import ndarray
from commons.abstractions.model import Model


class DeserializationError(Exception):
    def __init__(self, root_cause: Exception, input_json: Dict[Text, Any], target_class: Type) -> None:
        self.target_class = target_class
        self.input_json = input_json
        self.root_cause = root_cause

    def __str__(self) -> Text:
        return "DeserializationError: could not create model {} from: {}. Root cause: {}".format(self.target_class,
                                                                                                 self.input_json,
                                                                                                 self.root_cause)

    def __repr__(self) -> Text:
        return self.__str__()


def to_json(v: Any) -> Text:
    return json.dumps(v, default=custom_handling)


def from_json(input_json: Text, target_class: Type[Model]) -> Model:
    serialized = json.loads(input_json)
    try:
        return target_class.deserialize(serialized)
    except Exception as e:
        raise DeserializationError(e, input_json=input_json, target_class=target_class)


def custom_handling(v: Any) -> Any:
    if isinstance(v, Model):
        return v.serialize()
    if isinstance(v, datetime.datetime):
        return v.isoformat()
    elif isinstance(v, Decimal):
        return float(v)
    elif isinstance(v, set):
        return list(v)
    elif isinstance(v, ndarray):
        return v.tolist()
    elif isinstance(v, RealTime):
        return v.to_float()
    else:
        return v.__dict__
