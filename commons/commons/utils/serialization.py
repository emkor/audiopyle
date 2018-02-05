import json
from typing import Any, Text, Dict, Type
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
    return json.dumps(v)


def from_json(input_json: Text, target_class: Type[Model]) -> Model:
    serialized = json.loads(input_json)
    try:
        return target_class.from_serializable(serialized)
    except Exception as e:
        raise DeserializationError(e, input_json=serialized, target_class=target_class)
