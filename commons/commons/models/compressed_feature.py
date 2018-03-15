from typing import Text, Any

from enum import Enum

from commons.abstractions.model import Model


class CompressionType(Enum):
    none = "none"
    gzip = "gzip"
    lzma = "lzma"


class CompressedFeatureDTO(Model):
    def __init__(self, task_id: str, compression: CompressionType, data: bytes):
        self.task_id = task_id
        self.compression = compression
        self.data = data

    def __str__(self) -> Text:
        return "<{}: {} {}>".format(self.__class__.__name__,
                                    {"task_id": self.task_id, "compression": self.compression},
                                    self.size_humanized())

    def __repr__(self) -> Text:
        return self.__str__()

    def __eq__(self, other: Any) -> bool:
        return self.task_id == other.task_id and self.compression == other.compression

    def __hash__(self) -> int:
        return hash((self.task_id, self.compression))
