from typing import Text, Any, Dict

from enum import Enum

from audiopyle.lib.abstractions.model import Model
from audiopyle.lib.utils.file_system import ENCODING_UTF_8


class CompressionType(Enum):
    none = "none"
    gzip = "gzip"
    lzma = "lzma"


class CompressedFeatureDTO(Model):
    def __init__(self, task_id: str, compression: CompressionType, data: bytes) -> None:
        self.task_id = task_id
        self.compression = compression
        self.data = data

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]) -> Any:
        compression_object = CompressionType(serialized["compression"])
        data_bytes = serialized["data"].encode(ENCODING_UTF_8)
        serialized.update({"compression": compression_object,
                           "data": data_bytes})
        return CompressedFeatureDTO(**serialized)

    def to_serializable(self) -> Dict[Text, Any]:
        super_serialized = super(CompressedFeatureDTO, self).to_serializable()
        super_serialized.update({"compression": self.compression.value})
        super_serialized.update({"data": self.data.decode(ENCODING_UTF_8)})
        return super_serialized

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
