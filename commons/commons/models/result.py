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
    def __init__(self, total_time: float, extraction_time: float, feature_store_time: float, result_build_time: float,
                 result_store_time: float, read_input_file_time: float, read_raw_audio_time: float) -> None:
        self.total_time = total_time
        self.extraction_time = extraction_time
        self.feature_store_time = feature_store_time
        self.result_build_time = result_build_time
        self.result_store_time = result_store_time
        self.read_input_file_time = read_input_file_time
        self.read_raw_audio_time = read_raw_audio_time

    @property
    def misc_ops_time(self):
        return self.total_time - sum([self.extraction_time, self.feature_store_time, self.result_build_time,
                                      self.result_store_time, self.read_input_file_time, self.read_raw_audio_time])


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
    def __init__(self, task_id: Text, file_meta: FileMeta, audio_meta: Mp3AudioFileMeta, id3_tag: Id3Tag,
                 feature_meta: FeatureMeta) -> None:
        self.task_id = task_id
        self.file_meta = file_meta
        self.audio_meta = audio_meta
        self.id3_tag = id3_tag
        self.feature_meta = feature_meta

    def to_serializable(self):
        base_serialized = super().to_serializable()
        base_serialized.update({"file_meta": self.file_meta.to_serializable(),
                                "audio_meta": self.audio_meta.to_serializable(),
                                "id3_tag": self.id3_tag.to_serializable(),
                                "feature_meta": self.feature_meta.to_serializable()})
        return base_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        file_meta_object = FileMeta.from_serializable(serialized.get("file_meta"))
        audio_meta_object = Mp3AudioFileMeta.from_serializable(serialized.get("audio_meta"))
        id3_tag_object = Id3Tag.from_serializable(serialized.get("id3_tag"))
        result_data_object = FeatureMeta.from_serializable(serialized.get("feature_meta"))
        serialized.update({"file_meta": file_meta_object, "audio_meta": audio_meta_object,
                           "id3_tag": id3_tag_object, "feature_meta": result_data_object})
        return AnalysisResult(**serialized)
