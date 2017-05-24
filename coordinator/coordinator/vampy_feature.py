import vampyhost
import numpy

from commons.model import Model


class VampyFeatureMeta(Model):
    def __init__(self, vampy_plugin, segment_meta, plugin_output):
        """
        :type vampy_plugin: coordinator.vampy_plugin.VampyPlugin
        :type segment_meta: commons.audio_segment.AudioSegmentMeta
        :type plugin_output: str
        """
        self.vampy_plugin = vampy_plugin
        self.segment_meta = segment_meta
        self.plugin_output = plugin_output

    def frames(self):
        """
        :rtype: list[int]
        """
        raise NotImplementedError()

    def timestamps(self):
        """
        :rtype: list[float]
        """
        raise NotImplementedError()

    def values(self):
        """
        :rtype: numpy.ndarray
        """
        raise NotImplementedError()

    def value_shape(self):
        """
        :rtype: tuple[int]
        """
        raise NotImplementedError()


class VampyConstantStepFeature(VampyFeatureMeta):
    def __init__(self, vampy_plugin, segment_meta, plugin_output, time_step, matrix):
        """
        :type vampy_plugin: extracter.vampy_plugin.VampyPlugin
        :type segment_meta: commons.audio_segment.AudioSegmentMeta
        :type plugin_output: str
        :type time_step: vampyhost.RealTime
        :type matrix: numpy.ndarray
        """
        super(VampyConstantStepFeature, self).__init__(vampy_plugin, segment_meta, plugin_output)
        self._time_step = time_step
        self._matrix = matrix

    def frames(self):
        """
        :rtype: list[int]
        """
        return [i * self._step_as_frames() for i in xrange(0, len(self._matrix))]

    def timestamps(self):
        """
        :rtype: list[float]
        """
        return [i * self._step_as_sec() for i in xrange(0, len(self._matrix))]

    def values(self):
        """
        :rtype: numpy.ndarray
        """
        return self._matrix

    def value_shape(self):
        """
        :rtype: tuple[int]
        """
        return (self._matrix.shape[0], 1) if len(self._matrix.shape) < 2 else self._matrix.shape

    def _step_as_sec(self):
        """
        :rtype: float
        """
        return self._time_step.to_float()

    def _step_as_frames(self):
        """
        :rtype: int
        """
        return self._time_step.to_frame(self.segment_meta.source_file_meta.sample_rate)


class VampyVariableStepFeature(VampyFeatureMeta):
    def __init__(self, vampy_plugin, segment_meta, plugin_output, value_list):
        """
        :type vampy_plugin: extracter.vampy_plugin.VampyPlugin
        :type segment_meta: commons.audio_segment.AudioSegmentMeta
        :type plugin_output: str
        :type value_list: list[dict[float, str, numpy.ndarray]]
        """
        super(VampyVariableStepFeature, self).__init__(vampy_plugin, segment_meta, plugin_output)
        self._value_list = value_list

    def frames(self):
        """
        :rtype: list[int]
        """
        return [values_dict.get("timestamp").to_frame(self.segment_meta.source_file_meta.sample_rate) for values_dict in
                self._value_list]

    def timestamps(self):
        """
        :rtype: list[float]
        """
        return [values_dict.get("timestamp").to_float() for values_dict in self._value_list]

    def values(self):
        """
        :rtype: numpy.ndarray
        """
        return numpy.asanyarray([values_dict.get("values") for values_dict in self._value_list])

    def value_shape(self):
        """
        :rtype: tuple[int]
        """
        first_value = self._value_list[0].get("values") or []
        return len(self._value_list), len(first_value)
