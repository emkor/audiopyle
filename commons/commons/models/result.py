from typing import Text, Any, Dict

from enum import Enum

from commons.abstractions.model import Model
from commons.models.audio_tag import Id3Tag
from commons.models.file_meta import FileMeta, Mp3AudioFileMeta, WavAudioFileMeta


class ResultVersion(Enum):
    """For future changes in result structure"""
    V1 = "v1"


class FeatureType(Enum):
    ConstantStepFeature = "constant_step"
    VariableStepFeature = "variable_step"


class AnalysisResultData(Model):
    def __init__(self, result_version: ResultVersion, result_id: Text, feature_type: FeatureType):
        self.result_version = result_version
        self.result_id = result_id
        self.feature_type = feature_type

    def to_serializable(self):
        return {"result_id": self.result_id, "result_version": self.result_version.value,
                "feature_type": self.feature_type.value}

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        version_enum_object = ResultVersion(serialized.get("result_version"))
        type_enum_object = FeatureType(serialized.get("feature_type"))
        serialized.update({"result_version": version_enum_object, "feature_type": type_enum_object})
        return AnalysisResultData(**serialized)


class AnalysisResult(Model):
    def __init__(self, file_meta: FileMeta, audio_meta: Mp3AudioFileMeta, raw_audio_meta: WavAudioFileMeta,
                 id3_tag: Id3Tag, data: AnalysisResultData):
        self.file_meta = file_meta
        self.audio_meta = audio_meta
        self.raw_audio_meta = raw_audio_meta
        self.id3_tag = id3_tag
        self.data = data

    def to_serializable(self):
        return {"file_meta": self.file_meta.to_serializable(), "audio_meta": self.audio_meta.to_serializable(),
                "raw_audio_meta": self.raw_audio_meta.to_serializable(), "id3_tag": self.id3_tag.to_serializable(),
                "data": self.data.to_serializable()}

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        file_meta_object = FileMeta.from_serializable(serialized.get("file_meta"))
        audio_meta_object = Mp3AudioFileMeta.from_serializable(serialized.get("audio_meta"))
        raw_audio_meta_object = WavAudioFileMeta.from_serializable(serialized.get("raw_audio_meta"))
        id3_tag_object = Id3Tag.from_serializable(serialized.get("id3_tag"))
        result_data_object = AnalysisResultData.from_serializable(serialized.get("data"))
        serialized.update({"file_meta": file_meta_object, "audio_meta": audio_meta_object,
                           "raw_audio_meta": raw_audio_meta_object, "id3_tag": id3_tag_object,
                           "data": result_data_object})
        return AnalysisResult(**serialized)
