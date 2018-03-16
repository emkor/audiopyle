from typing import Text, Any, Dict, Optional, Tuple

from enum import Enum

from commons.abstractions.model import Model
from commons.models.audio_tag import Id3Tag
from commons.models.file_meta import FileMeta, Mp3AudioFileMeta


class FeatureType(Enum):
    ConstantStepFeature = "constant_step"
    VariableStepFeature = "variable_step"


class DataStats(Model):
    def __init__(self, minimum: Optional[float], maximum: Optional[float], median: Optional[float],
                 mean: Optional[float], standard_deviation: Optional[float], variance: Optional[float]) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self.median = median
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.variance = variance


class AnalysisStats(Model):
    def __init__(self, task_id: str, total_time: float, extraction_time: float, compression_time: float,
                 data_stats_build_time: float, encode_audio_time: float) -> None:
        self.task_id = task_id
        self.total_time = total_time
        self.extraction_time = extraction_time
        self.compression_time = compression_time
        self.data_stats_build_time = data_stats_build_time
        self.encode_audio_time = encode_audio_time


class FeatureMeta(Model):
    def __init__(self, task_id: Text, plugin_output: Text, feature_type: FeatureType, feature_size: int,
                 data_shape: Tuple[int, int], data_stats: DataStats) -> None:
        self.task_id = task_id
        self.plugin_output = plugin_output
        self.feature_type = feature_type
        self.feature_size = feature_size
        self.data_shape = data_shape
        self.data_stats = data_stats

    def to_serializable(self):
        base_serialized = super().to_serializable()
        base_serialized.update({"feature_type": self.feature_type.value,
                                "data_stats": self.data_stats.to_serializable()})
        return base_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        type_enum_object = FeatureType(serialized["feature_type"])
        data_stats = DataStats.from_serializable(serialized["data_stats"])
        serialized.update({"feature_type": type_enum_object, "data_stats": data_stats})
        return FeatureMeta(**serialized)


class AnalysisResult(Model):
    def __init__(self, task_id: Text, file_meta: FileMeta, audio_meta: Mp3AudioFileMeta, id3_tag: Id3Tag) -> None:
        self.task_id = task_id
        self.file_meta = file_meta
        self.audio_meta = audio_meta
        self.id3_tag = id3_tag

    def to_serializable(self):
        base_serialized = super().to_serializable()
        base_serialized.update({"file_meta": self.file_meta.to_serializable(),
                                "audio_meta": self.audio_meta.to_serializable(),
                                "id3_tag": self.id3_tag.to_serializable()})
        return base_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        file_meta_object = FileMeta.from_serializable(serialized.get("file_meta"))
        audio_meta_object = Mp3AudioFileMeta.from_serializable(serialized.get("audio_meta"))
        id3_tag_object = Id3Tag.from_serializable(serialized.get("id3_tag"))
        serialized.update({"file_meta": file_meta_object, "audio_meta": audio_meta_object,
                           "id3_tag": id3_tag_object})
        return AnalysisResult(**serialized)
