from typing import Text, List, Tuple, Optional, Dict, Any

import numpy

from commons.abstractions.model import Model
from commons.models.segment import AudioSegmentMeta
from commons.utils.conversion import sec_to_frames


class VampyFeatureAbstraction(Model):
    def __init__(self, segment_meta: AudioSegmentMeta) -> None:
        self.segment_meta = segment_meta

    def frames(self) -> List[int]:
        raise NotImplementedError()

    def timestamps(self) -> List[float]:
        raise NotImplementedError()

    def values(self) -> numpy.ndarray:
        raise NotImplementedError()

    def value_shape(self) -> Tuple[int, int]:
        raise NotImplementedError()

    def to_serializable(self):
        return {"segment_meta": self.segment_meta.to_serializable()}


class VampyConstantStepFeature(VampyFeatureAbstraction):
    def __init__(self, segment_meta: AudioSegmentMeta, time_step: float, matrix: numpy.ndarray) -> None:
        super(VampyConstantStepFeature, self).__init__(segment_meta)
        self._time_step = time_step
        self._matrix = matrix

    def frames(self) -> List[int]:
        return [i * self._step_as_frames() for i in range(0, len(self._matrix))]

    def timestamps(self) -> List[float]:
        return [i * self._time_step for i in range(0, len(self._matrix))]

    def values(self) -> numpy.ndarray:
        return self._matrix

    def value_shape(self) -> Tuple[int, int]:
        return (self._matrix.shape[0], 1) if len(self._matrix.shape) < 2 else self._matrix.shape

    def _step_as_frames(self) -> int:
        return sec_to_frames(self._time_step, self.segment_meta.source_file_meta.sample_rate)

    def to_serializable(self):
        super_serialized = super(VampyConstantStepFeature, self).to_serializable()
        super_serialized.update({"matrix": self._matrix.tolist(),
                                 "time_step": self._time_step})
        return super_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        segment_meta = AudioSegmentMeta.from_serializable(serialized.pop("segment_meta"))
        _matrix = numpy.asanyarray(serialized.pop("matrix"))
        serialized.update({"segment_meta": segment_meta,
                           "matrix": _matrix})
        return VampyConstantStepFeature(**serialized)


class StepFeature(Model):
    def __init__(self, timestamp: float, values: Optional[numpy.ndarray], label: Optional[Text] = None) -> None:
        self.timestamp = timestamp
        self.values = values
        self.label = label

    def to_serializable(self):
        super_serialized = super(StepFeature, self).to_serializable()
        if self.values is not None:
            super_serialized.update({"values": self.values.tolist()})
        else:
            super_serialized.update({"values": []})
        return super_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        values = serialized.pop("values")
        if values:
            serialized.update({"values": numpy.asanyarray(values)})
        else:
            serialized.update({"values": None})
        return StepFeature(**serialized)


class VampyVariableStepFeature(VampyFeatureAbstraction):
    def __init__(self, segment_meta: AudioSegmentMeta, step_features: List[StepFeature]) -> None:
        super(VampyVariableStepFeature, self).__init__(segment_meta)
        self.step_features = step_features

    def frames(self) -> List[int]:
        return [sec_to_frames(step_feature.timestamp, self.segment_meta.source_file_meta.sample_rate)
                for step_feature in self.step_features]

    def timestamps(self) -> List[float]:
        return [step_feature.timestamp for step_feature in self.step_features]

    def values(self) -> numpy.ndarray:
        return numpy.asanyarray([step_feature.values for step_feature in self.step_features])

    def value_shape(self) -> Tuple[int, int]:
        first_value = self.step_features[0].values or []
        return len(self.step_features), len(first_value)

    def to_serializable(self):
        super_serialized = super(VampyVariableStepFeature, self).to_serializable()
        super_serialized.update({"value_list": [s.to_serializable() for s in self.step_features]})
        return super_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        segment_meta = AudioSegmentMeta.from_serializable(serialized.pop("segment_meta"))
        step_features_serialized = numpy.asanyarray(serialized.pop("value_list"))
        step_features = [StepFeature.from_serializable(sf) for sf in step_features_serialized]
        serialized.update({"segment_meta": segment_meta,
                           "step_features": step_features})
        return VampyVariableStepFeature(**serialized)
