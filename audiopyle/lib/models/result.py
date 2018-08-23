from typing import Text, Any, Dict, Optional, Tuple

from enum import Enum

from audiopyle.lib.abstractions.model import Model
from audiopyle.lib.models.audio_tag import Id3Tag
from audiopyle.lib.models.file_meta import CompressedAudioFileMeta
from audiopyle.lib.models.plugin import VampyPlugin, VampyPluginParams


class FeatureType(Enum):
    ConstantStepFeature = "constant_step"
    VariableStepFeature = "variable_step"


class DataStats(Model):
    def __init__(self, minimum: Optional[float], maximum: Optional[float], median: Optional[float],
                 mean: Optional[float], standard_deviation: Optional[float], variance: Optional[float],
                 sum: Optional[float], count: Optional[int]) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self.median = median
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.variance = variance
        self.sum = sum
        self.count = count


class AnalysisStats(Model):
    def __init__(self, task_id: str, total_time: float, extraction_time: float, compression_time: float,
                 data_stats_build_time: float, encode_audio_time: float, result_store_time: float,
                 metrics_extraction_time: float) -> None:
        self.task_id = task_id
        self.total_time = total_time
        self.extraction_time = extraction_time
        self.compression_time = compression_time
        self.data_stats_build_time = data_stats_build_time
        self.encode_audio_time = encode_audio_time
        self.result_store_time = result_store_time
        self.metrics_extraction_time = metrics_extraction_time


class FeatureMeta(Model):
    def __init__(self, task_id: Text, feature_type: FeatureType, feature_size: int,
                 data_shape: Tuple[int, int, int]) -> None:
        self.task_id = task_id
        self.feature_type = feature_type
        self.feature_size = feature_size
        self.data_shape = data_shape

    def to_serializable(self):
        base_serialized = super().to_serializable()
        base_serialized.update({"feature_type": self.feature_type.value})
        return base_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        type_enum_object = FeatureType(serialized["feature_type"])
        serialized.update({"feature_type": type_enum_object})
        return FeatureMeta(**serialized)


class AnalysisRequest(Model):
    def __init__(self, task_id: Text, audio_meta: CompressedAudioFileMeta, id3_tag: Optional[Id3Tag],
                 plugin: VampyPlugin, plugin_config: VampyPluginParams) -> None:
        self.task_id = task_id
        self.audio_meta = audio_meta
        self.id3_tag = id3_tag
        self.plugin = plugin
        self.plugin_config = plugin_config

    def to_serializable(self):
        base_serialized = super().to_serializable()
        base_serialized.update({"audio_meta": self.audio_meta.to_serializable(),
                                "id3_tag": self.id3_tag.to_serializable() if self.id3_tag else None,
                                "plugin": self.plugin.to_serializable(),
                                "plugin_config": self.plugin_config.to_serializable()})
        return base_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        audio_meta_object = CompressedAudioFileMeta.from_serializable(serialized["audio_meta"])
        id3_tag_object = Id3Tag.from_serializable(serialized["id3_tag"])
        plugin_object = VampyPlugin.from_serializable(serialized["plugin"])
        plugin_config_object = VampyPluginParams.from_serializable(serialized["plugin_config"])
        serialized.update({"audio_meta": audio_meta_object, "id3_tag": id3_tag_object,
                           "plugin": plugin_object, "plugin_config": plugin_config_object})
        return AnalysisRequest(**serialized)
