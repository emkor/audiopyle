from copy import copy
from typing import Type, Any, Text, Dict

from commons.utils.conversion import object_size, object_size_humanized


class Model(object):
    @classmethod
    def deserialize(cls: Type, serialized: Dict[Text, Any]) -> Any:
        return cls(**serialized)

    def serialize(self) -> Dict[Text, Any]:
        return copy(self.__dict__)

    def __str__(self) -> Text:
        return "<{}: {} {}>".format(self.__class__.__name__, self.__dict__, self.size_humanized())

    def __repr__(self) -> Text:
        return self.__str__()

    def __eq__(self, other: Any) -> bool:
        return self.serialize() == other.serialize()

    def __hash__(self) -> int:
        return hash(self.__dict__)

    def size_bytes(self) -> float:
        return object_size(self)

    def size_humanized(self) -> Text:
        return object_size_humanized(self)
