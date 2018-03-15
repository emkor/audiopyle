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
