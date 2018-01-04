from typing import Text, Any, Dict

from enum import Enum

from commons.abstractions.model import Model
from commons.models.audio_tag import Id3Tag
from commons.models.file_meta import FileMeta, AudioFileMeta


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

    def serialize(self):
        return {"result_id": self.result_id, "result_version": self.result_version.value,
                "feature_type": self.feature_type.value}

    @classmethod
    def deserialize(cls, serialized: Dict[Text, Any]):
        version_enum_object = ResultVersion(serialized.get("result_version"))
        type_enum_object = FeatureType(serialized.get("feature_type"))
        serialized.update({"result_version": version_enum_object, "feature_type": type_enum_object})
        return AnalysisResultData(**serialized)


class AnalysisResult(Model):
    def __init__(self, file_meta: FileMeta, audio_meta: AudioFileMeta,
                 id3_tag: Id3Tag, data: AnalysisResultData):
        self.file_meta = file_meta
        self.audio_meta = audio_meta
        self.id3_tag = id3_tag
        self.data = data

    def serialize(self):
        return {"file_meta": self.file_meta.serialize(), "audio_meta": self.audio_meta.serialize(),
                "id3_tag": self.id3_tag.serialize(), "data": self.data.serialize()}

    @classmethod
    def deserialize(cls, serialized: Dict[Text, Any]):
        file_meta_object = FileMeta.deserialize(serialized.get("file_meta"))
        audio_meta_object = AudioFileMeta.deserialize(serialized.get("audio_meta"))
        id3_tag_object = Id3Tag.deserialize(serialized.get("id3_tag"))
        result_data_object = AnalysisResultData.deserialize(serialized.get("data"))
        serialized.update({"file_meta": file_meta_object, "audio_meta": audio_meta_object,
                           "id3_tag": id3_tag_object, "data": result_data_object})
        return AnalysisResultData(**serialized)
