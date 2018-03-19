import json
import gzip
import lzma
from typing import Dict, Any, Union

from commons.models.compressed_feature import CompressionType, CompressedFeatureDTO
from commons.models.feature import VampyConstantStepFeature, VampyVariableStepFeature
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


def to_compressed_feature(task_id: str, feature_model: Union[VampyConstantStepFeature, VampyVariableStepFeature],
                          compression_type: CompressionType) -> CompressedFeatureDTO:
    compressed_feature_bytes = compress_model(compression_type, feature_model.to_serializable())
    return CompressedFeatureDTO(task_id, CompressionType.lzma, compressed_feature_bytes)


def from_compressed_feature(comp_feat: CompressedFeatureDTO) -> Union[VampyConstantStepFeature, VampyVariableStepFeature]:
    decompressed_feature = decompress_model(comp_feat.compression, comp_feat.data)
    if "time_step" in decompressed_feature.keys():
        return VampyConstantStepFeature.from_serializable(decompressed_feature)
    else:
        return VampyVariableStepFeature.from_serializable(decompressed_feature)


def compress_model(compression_type: CompressionType, data: Dict[str, Any]) -> bytes:
    binary_serialized = json.dumps(data).encode(ENCODING_UTF_8)
    return COMPRESSION_FUNCTIONS[compression_type](binary_serialized)  # type: ignore


def decompress_model(compression_type: CompressionType, data: bytes) -> Dict[str, Any]:
    binary_serialized = DECOMPRESSION_FUNCTIONS[compression_type](data)  # type: ignore
    return json.loads(binary_serialized.decode(ENCODING_UTF_8))
