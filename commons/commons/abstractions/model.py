from copy import copy
from typing import Type, Any, Text, Dict


class Model(object):
    @classmethod
    def deserialize(cls: Type, serialized: Dict[Text, Any]) -> Any:
        return cls(**serialized)

    def serialize(self) -> Dict[Text, Any]:
        return copy(self.__dict__)

    def __str__(self) -> Text:
        return "<{}: {}>".format(self.__class__.__name__, self.__dict__)

    def __repr__(self) -> Text:
        return self.__str__()

    def __eq__(self, other: Any) -> bool:
        return self.serialize() == other.serialize()

    def __hash__(self) -> int:
        return hash(self.__dict__)
