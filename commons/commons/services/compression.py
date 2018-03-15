import json
import gzip
import lzma
from typing import Dict, Any

from commons.models.compressed_feature import CompressionType
from commons.utils.file_system import ENCODING_UTF_8

COMPRESSION_FUNCTIONS = {
    CompressionType.none: lambda x: x,
    CompressionType.gzip: gzip.compress,
    CompressionType.lzma: lzma.compress
}

DECOMPRESSION_FUNCTIONS = {
    CompressionType.none: lambda x: x,
    CompressionType.gzip: gzip.decompress,
    CompressionType.lzma: lzma.decompress
}


def compress(compression_type: CompressionType, data: Dict[str, Any]) -> bytes:
    binary_serialized = json.dumps(data).encode(ENCODING_UTF_8)
    return COMPRESSION_FUNCTIONS[compression_type](binary_serialized)  # type: ignore


def decompress(compression_type: CompressionType, data: bytes) -> Dict[str, Any]:
    binary_serialized = DECOMPRESSION_FUNCTIONS[compression_type](data)  # type: ignore
    return json.loads(binary_serialized.decode(ENCODING_UTF_8))
