import numpy

from commons.abstractions.model import Model
from commons.models.feature import VampyFeatureAbstraction, VampyConstantStepFeature, VampyVariableStepFeature


class MetricDefinition(Model):
    def __init__(self, name: str, plugin_key: str, function: str, kwargs: dict) -> None:
        self.name = name
        self.plugin_key = plugin_key
        self.function = function
        self.kwargs = kwargs


class MetricTransformation(Model):
    def __init__(self, name, *args, **kwargs) -> None:
        self.name = name
        self.args = args
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
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("none", *args, **kwargs)

    def _call_on_constant_step(self, feature: VampyConstantStepFeature) -> numpy.ndarray:
        return feature.values()

    def _call_on_variable_step(self, feature: VampyVariableStepFeature) -> numpy.ndarray:
        return feature.values()


class SelectRowTransformation(MetricTransformation):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("select_row", *args, **kwargs)

    def _call_on_constant_step(self, feature: VampyConstantStepFeature) -> numpy.ndarray:
        row_index = self.args[0]
        return numpy.asanyarray([vs[row_index] for vs in feature.values()])

    def _call_on_variable_step(self, feature: VampyVariableStepFeature) -> numpy.ndarray:
        row_index = self.args[0]
        return numpy.asanyarray([sf.values[row_index] for sf in feature.step_features])  # type: ignore


class SingleValueTransformation(MetricTransformation):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__("singe_value", *args, **kwargs)

    def _call_on_constant_step(self, feature: VampyConstantStepFeature) -> numpy.ndarray:
        first_value = feature.values()[0]
        return numpy.asanyarray([first_value, first_value])

    def _call_on_variable_step(self, feature: VampyVariableStepFeature) -> numpy.ndarray:
        first_value = feature.step_features[0].values[0]  # type: ignore
        return numpy.asanyarray([first_value, first_value])


METRIC_TRANSFORMATIONS = {
    "none": NoneTransformation,
    "select_row": SelectRowTransformation,
    "singe_value": SingleValueTransformation
}
