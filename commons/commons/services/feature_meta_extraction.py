from typing import Callable, Optional

import numpy

from commons.models.feature import VampyFeatureAbstraction, VampyVariableStepFeature, VampyConstantStepFeature
from commons.models.result import FeatureMeta, DataStats, FeatureType
from commons.utils.logger import get_logger

logger = get_logger()


def build_feature_meta(task_id: str, vampy_feature: VampyFeatureAbstraction) -> FeatureMeta:
    if isinstance(vampy_feature, VampyVariableStepFeature):
        return FeatureMeta(task_id=task_id, feature_type=FeatureType.VariableStepFeature,
                           feature_size=vampy_feature.size_bytes(),
                           data_shape=vampy_feature.value_shape())
    elif isinstance(vampy_feature, VampyConstantStepFeature):
        return FeatureMeta(task_id=task_id, feature_type=FeatureType.ConstantStepFeature,
                           feature_size=vampy_feature.size_bytes(),
                           data_shape=vampy_feature.value_shape())
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
        numpy_result = calc_callable(calc_input)
        return None if numpy.isnan(numpy_result) else float(numpy_result)
    except Exception as e:
        logger.warning(
            "Could not calculate {} from data shaped {}: {}; returning None".format(calc_callable, calc_input.shape, e))
        return None
