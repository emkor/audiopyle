from typing import Text, List, Tuple, Optional

import numpy

from commons.abstractions.model import Model
from commons.models.segment import AudioSegmentMeta
from commons.utils.conversion import sec_to_frames
from commons.vampy.plugin import VampyPlugin


class VampyFeatureMeta(Model):
    def __init__(self, vampy_plugin: VampyPlugin, segment_meta: AudioSegmentMeta, plugin_output: Text) -> None:
        self.vampy_plugin = vampy_plugin
        self.segment_meta = segment_meta
        self.plugin_output = plugin_output

    def frames(self) -> List[int]:
        raise NotImplementedError()

    def timestamps(self) -> List[float]:
        raise NotImplementedError()

    def values(self) -> numpy.ndarray:
        raise NotImplementedError()

    def value_shape(self) -> Tuple[int, int]:
        raise NotImplementedError()

    def serialize(self):
        return {"vampy_plugin": self.vampy_plugin.serialize(),
                "segment_meta": self.segment_meta.serialize(),
                "plugin_output": self.plugin_output}


class VampyConstantStepFeature(VampyFeatureMeta):
    def __init__(self, vampy_plugin: VampyPlugin, segment_meta: AudioSegmentMeta, plugin_output: Text,
                 time_step: float, matrix: numpy.ndarray) -> None:
        super(VampyConstantStepFeature, self).__init__(vampy_plugin, segment_meta, plugin_output)
        self._time_step = time_step
        self._matrix = matrix

    def frames(self) -> List[int]:
        return [i * self._step_as_frames() for i in range(0, len(self._matrix))]

    def timestamps(self) -> List[float]:
        return [i * self._step_as_sec() for i in range(0, len(self._matrix))]

    def values(self) -> numpy.ndarray:
        return self._matrix

    def value_shape(self) -> Tuple[int, int]:
        return (self._matrix.shape[0], 1) if len(self._matrix.shape) < 2 else self._matrix.shape

    def _step_as_sec(self) -> float:
        return self._time_step

    def _step_as_frames(self) -> int:
        return sec_to_frames(self._step_as_sec(), self.segment_meta.source_file_meta.sample_rate)

    def serialize(self):
        super_serialized = super(VampyConstantStepFeature, self).serialize()
        super_serialized.update({"_time_step": self._time_step,
                                 "_matrix": self._matrix.tolist()})
        return super_serialized


class StepFeature(Model):
    def __init__(self, timestamp: float, values: numpy.ndarray, label: Optional[Text] = None) -> None:
        self.timestamp = timestamp
        self.values = values
        self.label = label

    def serialize(self):
        super_serialized = super(StepFeature, self).serialize()
        super_serialized.update({"values": self.values.tolist() if self.values else None})
        return super_serialized


class VampyVariableStepFeature(VampyFeatureMeta):
    def __init__(self, vampy_plugin: VampyPlugin, segment_meta: AudioSegmentMeta, plugin_output: Text,
                 value_list: List[StepFeature]) -> None:
        super(VampyVariableStepFeature, self).__init__(vampy_plugin, segment_meta, plugin_output)
        self.step_features = value_list

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

    def serialize(self):
        super_serialized = super(VampyVariableStepFeature, self).serialize()
        super_serialized.update({"step_features": [s.serialize() for s in self.step_features]})
        return super_serialized
