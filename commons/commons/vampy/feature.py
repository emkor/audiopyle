from typing import Text, List, Tuple, Dict, Any, Union
from vampyhost import RealTime

import numpy

from commons.abstractions.model import Model
from commons.audio.segment import AudioSegmentMeta
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
                 time_step: RealTime, matrix: numpy.ndarray) -> None:
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
        return self._time_step.to_float()

    def _step_as_frames(self) -> int:
        return self._time_step.to_frame(self.segment_meta.source_file_meta.sample_rate)

    def serialize(self):
        super_serialized = super(VampyConstantStepFeature, self).serialize()
        super_serialized.update({"_time_step": self._time_step.to_float(),
                                 "_matrix": self._matrix.tolist()})
        return super_serialized


class VampyVariableStepFeature(VampyFeatureMeta):
    def __init__(self, vampy_plugin: VampyPlugin, segment_meta: AudioSegmentMeta, plugin_output: Text,
                 value_list: List[Dict[Text, Union[numpy.ndarray, RealTime]]]) -> None:
        super(VampyVariableStepFeature, self).__init__(vampy_plugin, segment_meta, plugin_output)
        self._value_list = value_list

    def frames(self) -> List[int]:
        return [values_dict.get("timestamp").to_frame(self.segment_meta.source_file_meta.sample_rate) for values_dict in
                self._value_list]

    def timestamps(self) -> List[float]:
        return [values_dict.get("timestamp").to_float() for values_dict in self._value_list]

    def values(self) -> numpy.ndarray:
        return numpy.asanyarray([values_dict.get("values") for values_dict in self._value_list])

    def value_shape(self) -> Tuple[int, int]:
        first_value = self._value_list[0].get("values") or []
        return len(self._value_list), len(first_value)

    def serialize(self):
        super_serialized = super(VampyVariableStepFeature, self).serialize()
        super_serialized.update({"_value_list": self._value_list})
        return super_serialized
