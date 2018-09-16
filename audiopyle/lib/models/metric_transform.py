import numpy

from audiopyle.lib.abstractions.model import Model
from audiopyle.lib.models.feature import VampyFeatureAbstraction, VampyConstantStepFeature, VampyVariableStepFeature


class MetricTransformation(Model):
    def __init__(self, name, audio_meta, **kwargs) -> None:
        self.name = name
        self.audio_meta = audio_meta
        self.kwargs = kwargs

    def call(self, vampy_feature: VampyFeatureAbstraction) -> numpy.ndarray:
        if isinstance(vampy_feature, VampyConstantStepFeature):
            return self._call_on_constant_step(vampy_feature)
        elif isinstance(vampy_feature, VampyVariableStepFeature):
            return self._call_on_variable_step(vampy_feature)
        else:
            raise ValueError("Input parameter is not feature: {}".format(vampy_feature))

    def _call_on_constant_step(self, feature: VampyConstantStepFeature) -> numpy.ndarray:
        raise NotImplementedError("Called abstract _call_on_constant_step")

    def _call_on_variable_step(self, feature: VampyVariableStepFeature) -> numpy.ndarray:
        raise NotImplementedError("Called abstract _call_on_variable_step")


class NoneTransformation(MetricTransformation):
    def __init__(self, audio_meta, **kwargs) -> None:
        super().__init__("none", audio_meta, **kwargs)

    def _call_on_constant_step(self, feature: VampyConstantStepFeature) -> numpy.ndarray:
        return feature.values()

    def _call_on_variable_step(self, feature: VampyVariableStepFeature) -> numpy.ndarray:
        return feature.values()


class SelectRowTransformation(MetricTransformation):
    def __init__(self, audio_meta, **kwargs) -> None:
        super().__init__("select_row", audio_meta, **kwargs)

    def _call_on_constant_step(self, feature: VampyConstantStepFeature) -> numpy.ndarray:
        row_index = self.kwargs["row_index"]
        return numpy.asanyarray([vs[row_index] for vs in feature.values()])

    def _call_on_variable_step(self, feature: VampyVariableStepFeature) -> numpy.ndarray:
        row_index = self.kwargs["row_index"]
        return numpy.asanyarray([sf.values[row_index] for sf in feature.step_features])  # type: ignore


class SingleValueTransformation(MetricTransformation):
    def __init__(self, audio_meta, **kwargs) -> None:
        super().__init__("single_value", audio_meta, **kwargs)

    def _call_on_constant_step(self, feature: VampyConstantStepFeature) -> numpy.ndarray:
        first_value = feature.values()[0]
        return numpy.asanyarray([first_value, first_value])

    def _call_on_variable_step(self, feature: VampyVariableStepFeature) -> numpy.ndarray:
        first_value = feature.step_features[0].values[0]  # type: ignore
        return numpy.asanyarray([first_value, first_value])


class SegmentLabelShareRatioTransformation(MetricTransformation):
    def __init__(self, audio_meta, **kwargs) -> None:
        super().__init__("segment_share_ratio", audio_meta, **kwargs)

    def _call_on_constant_step(self, feature: VampyConstantStepFeature) -> numpy.ndarray:
        raise NotImplementedError("Can not run segment_share_ratio transformation on constant step feature!")

    def _call_on_variable_step(self, feature: VampyVariableStepFeature) -> numpy.ndarray:
        segment_label = self.kwargs["label"]
        segment_lengths_seconds = []
        last_segment_start_sec = None
        for step in feature.step_features:
            if last_segment_start_sec is not None:
                # case when segment with selected label has ended and step.timestamp represents next segment start time
                segment_lengths_seconds.append(step.timestamp - last_segment_start_sec)
                last_segment_start_sec = None
            elif step.label == segment_label:
                # case when step.timestamp is start of segment with selected label
                last_segment_start_sec = step.timestamp
            else:
                # case when step is point between two segments without selected label
                last_segment_start_sec = None
        if last_segment_start_sec is not None:
            # case when last segment was selected
            segment_lengths_seconds.append(self.audio_meta.length_sec - last_segment_start_sec)
        return numpy.asanyarray([sls / self.audio_meta.length_sec for sls in segment_lengths_seconds])  # type: ignore
