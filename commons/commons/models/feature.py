from typing import Text, List, Tuple, Optional, Dict, Any

import numpy

from commons.abstractions.model import Model
from commons.models.plugin import VampyPlugin
from commons.models.segment import AudioSegmentMeta
from commons.utils.conversion import sec_to_frames


class VampyFeatureAbstraction(Model):
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

    def to_serializable(self):
        return {"vampy_plugin": self.vampy_plugin.to_serializable(),
                "segment_meta": self.segment_meta.to_serializable(),
                "plugin_output": self.plugin_output}


class VampyConstantStepFeature(VampyFeatureAbstraction):
    def __init__(self, vampy_plugin: VampyPlugin, segment_meta: AudioSegmentMeta, plugin_output: Text,
                 time_step: float, matrix: numpy.ndarray) -> None:
        super(VampyConstantStepFeature, self).__init__(vampy_plugin, segment_meta, plugin_output)
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
        vampy_plugin = VampyPlugin.from_serializable(serialized.pop("vampy_plugin"))
        segment_meta = AudioSegmentMeta.from_serializable(serialized.pop("segment_meta"))
        _matrix = numpy.asarray(serialized.pop("matrix"))
        serialized.update({"vampy_plugin": vampy_plugin,
                           "segment_meta": segment_meta,
                           "matrix": _matrix})
        return VampyConstantStepFeature(**serialized)


class StepFeature(Model):
    def __init__(self, timestamp: float, values: numpy.ndarray, label: Optional[Text] = None) -> None:
        self.timestamp = timestamp
        self.values = values
        self.label = label

    def to_serializable(self):
        super_serialized = super(StepFeature, self).to_serializable()
        super_serialized.update({"values": self.values.tolist()})
        return super_serialized
    
    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        values = serialized.pop("values")
        serialized.update({"values": numpy.asarray(values)})
        return StepFeature(**serialized)


class VampyVariableStepFeature(VampyFeatureAbstraction):
    def __init__(self, vampy_plugin: VampyPlugin, segment_meta: AudioSegmentMeta, plugin_output: Text,
                 step_features: List[StepFeature]) -> None:
        super(VampyVariableStepFeature, self).__init__(vampy_plugin, segment_meta, plugin_output)
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
        vampy_plugin = VampyPlugin.from_serializable(serialized.pop("vampy_plugin"))
        segment_meta = AudioSegmentMeta.from_serializable(serialized.pop("segment_meta"))
        step_features_serialized = numpy.asarray(serialized.pop("value_list"))
        step_features = [StepFeature.from_serializable(sf) for sf in step_features_serialized]
        serialized.update({"vampy_plugin": vampy_plugin,
                           "segment_meta": segment_meta,
                           "step_features": step_features})
        return VampyVariableStepFeature(**serialized)
