from typing import Text, Dict, Any, Callable, Optional

import numpy
import vamp

from commons.abstractions.model import Model
from commons.models.feature import VampyFeatureAbstraction, VampyVariableStepFeature, VampyConstantStepFeature, \
    StepFeature
from commons.models.plugin import VampyPlugin
from commons.models.result import FeatureMeta, DataStats, FeatureType
from commons.models.segment import MonoAudioSegment
from commons.services.uuid_generation import generate_uuid
from commons.utils.logger import get_logger

logger = get_logger()


class ExtractionRequest(Model):
    def __init__(self, audio_file_name: Text, plugin_key: Text, plugin_output: Text) -> None:
        self.audio_file_name = audio_file_name
        self.plugin_key = plugin_key
        self.plugin_output = plugin_output

    def uuid(self) -> Text:
        return generate_uuid("{};{};{}".format(self.audio_file_name, self.plugin_key, self.plugin_output))


def extract_features(audio_segment: MonoAudioSegment, vampy_plugin: VampyPlugin,
                     output_name: Text) -> VampyFeatureAbstraction:
    feature_meta = VampyFeatureAbstraction(vampy_plugin=vampy_plugin, segment_meta=audio_segment.get_meta(),
                                           plugin_output=output_name)
    raw_results = vamp.collect(data=audio_segment.data, sample_rate=audio_segment.source_file_meta.sample_rate,
                               plugin_key=vampy_plugin.key, output=output_name)
    return _map_feature(feature_meta=feature_meta, extracted_data=raw_results)


def _map_feature(feature_meta: VampyFeatureAbstraction, extracted_data: Dict[Text, Any]) -> VampyFeatureAbstraction:
    data_type = list(extracted_data.keys())[0]
    if data_type == "list":
        value_list = [StepFeature(f.get("timestamp").to_float(), f.get("values"), f.get("label") or None)
                      for f in extracted_data.get("list")]
        return VampyVariableStepFeature(vampy_plugin=feature_meta.vampy_plugin, segment_meta=feature_meta.segment_meta,
                                        plugin_output=feature_meta.plugin_output, step_features=value_list)
    elif data_type in ("vector", "matrix"):
        data = extracted_data.get("vector") or extracted_data.get("matrix")
        return VampyConstantStepFeature(vampy_plugin=feature_meta.vampy_plugin, segment_meta=feature_meta.segment_meta,
                                        plugin_output=feature_meta.plugin_output, time_step=data[0].to_float(),
                                        matrix=data[1])
    else:
        raise NotImplementedError("Can not recognize feature type: {}".format(extracted_data.keys()))


def get_feature_meta(vampy_feature: VampyFeatureAbstraction) -> FeatureMeta:
    if isinstance(vampy_feature, VampyVariableStepFeature):
        data_stats = _extract_data_stats(vampy_feature.values())
        return FeatureMeta(plugin=vampy_feature.vampy_plugin, plugin_output=vampy_feature.plugin_output,
                           feature_type=FeatureType.VariableStepFeature, feature_size=vampy_feature.size_bytes(),
                           data_shape=vampy_feature.value_shape(), data_stats=data_stats)
    elif isinstance(vampy_feature, VampyConstantStepFeature):
        data_stats = _extract_data_stats(vampy_feature.values())
        return FeatureMeta(plugin=vampy_feature.vampy_plugin, plugin_output=vampy_feature.plugin_output,
                           feature_type=FeatureType.ConstantStepFeature, feature_size=vampy_feature.size_bytes(),
                           data_shape=vampy_feature.value_shape(), data_stats=data_stats)
    else:
        raise ValueError("Can not extract feature meta from: {}".format(vampy_feature))


def _extract_data_stats(numpy_array: numpy.ndarray) -> DataStats:
    return DataStats(minimum=_try_calculate_data_stat(numpy.amin, numpy_array),
                     maximum=_try_calculate_data_stat(numpy.amax, numpy_array),
                     median=_try_calculate_data_stat(numpy.median, numpy_array),
                     mean=_try_calculate_data_stat(numpy.mean, numpy_array),
                     standard_deviation=_try_calculate_data_stat(numpy.std, numpy_array),
                     variance=_try_calculate_data_stat(numpy.var, numpy_array))


def _try_calculate_data_stat(calc_callable: Callable[..., float], calc_input: numpy.ndarray) -> Optional[float]:
    try:
        return float(calc_callable(calc_input))
    except Exception as e:
        logger.warning(
            "Could not calculate {} from data shaped {}: {}; returning None".format(calc_callable, calc_input.shape, e))
        return None
