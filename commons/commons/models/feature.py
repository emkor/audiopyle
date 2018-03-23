from typing import Text, List, Tuple, Optional, Dict, Any

import numpy

from commons.abstractions.model import Model
from commons.models.file_meta import AudioFileMeta
from commons.utils.conversion import sec_to_frames


class VampyFeatureAbstraction(Model):
    def __init__(self, task_id: str) -> None:
        self.task_id = task_id

    def frames(self, audio_meta: AudioFileMeta) -> List[int]:
        raise NotImplementedError()

    def timestamps(self) -> List[float]:
        raise NotImplementedError()

    def values(self) -> numpy.ndarray:
        raise NotImplementedError()

    def value_shape(self) -> Tuple[int, int, int]:
        raise NotImplementedError()


class VampyConstantStepFeature(VampyFeatureAbstraction):
    def __init__(self, task_id: str, time_step: float, matrix: numpy.ndarray) -> None:
        super().__init__(task_id)
        self._time_step = time_step
        self._matrix = matrix

    def frames(self, audio_meta: AudioFileMeta) -> List[int]:
        return [i * self._step_as_frames(audio_meta) for i in range(0, len(self._matrix))]

    def timestamps(self) -> List[float]:
        return [i * self._time_step for i in range(0, len(self._matrix))]

    def values(self) -> numpy.ndarray:
        return self._matrix

    def value_shape(self) -> Tuple[int, int, int]:
        if len(self._matrix) == 0:
            return 0, 0, 0
        numpy_shape = self._matrix.shape
        if len(numpy_shape) == 1:
            return numpy_shape[0], 1, 0
        elif len(numpy_shape) == 2:
            return numpy_shape[0], numpy_shape[1], 1
        elif len(numpy_shape) == 3:
            return numpy_shape[0], numpy_shape[1], numpy_shape[2]
        else:
            raise ValueError("Got error on value shape {}".format(numpy_shape))

    def _step_as_frames(self, audio_meta: AudioFileMeta) -> int:
        return sec_to_frames(self._time_step, audio_meta.sample_rate)

    def to_serializable(self):
        return {"task_id": self.task_id, "matrix": self._matrix.tolist(), "time_step": self._time_step}

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        _matrix = numpy.asanyarray(serialized.pop("matrix"))
        _time_step = serialized.pop("time_step")
        _task_id = serialized.pop("task_id")
        serialized.update({"matrix": _matrix, "time_step": _time_step, "task_id": _task_id})
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
    def __init__(self, task_id: str, step_features: List[StepFeature]) -> None:
        super().__init__(task_id)
        self.step_features = step_features

    def frames(self, audio_meta: AudioFileMeta) -> List[int]:
        return [sec_to_frames(step_feature.timestamp, audio_meta.sample_rate)
                for step_feature in self.step_features]

    def timestamps(self) -> List[float]:
        return [step_feature.timestamp for step_feature in self.step_features]

    def values(self) -> numpy.ndarray:
        return numpy.asanyarray([step_feature.values for step_feature in self.step_features])

    def labels(self) -> List[str]:
        return [step_feature.label for step_feature in self.step_features]

    def value_shape(self) -> Tuple[int, int, int]:
        x_size = len(self.step_features)
        if len(self.step_features[0].values) == 0:
            return x_size, 0, 0
        first_value_shape = self.step_features[0].values.shape
        if len(first_value_shape) == 1:
            return x_size, first_value_shape[0], 0
        elif len(first_value_shape) == 2:
            return x_size, first_value_shape[0], first_value_shape[1]
        else:
            raise ValueError("Got error on first value shape {}".format(first_value_shape))

    def to_serializable(self):
        return {"task_id": self.task_id, "value_list": [s.to_serializable() for s in self.step_features]}

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        _task_id = serialized.pop("task_id")
        step_features_serialized = numpy.asanyarray(serialized.pop("value_list"))
        step_features = [StepFeature.from_serializable(sf) for sf in step_features_serialized]
        serialized.update({"step_features": step_features, "task_id": _task_id})
        return VampyVariableStepFeature(**serialized)
