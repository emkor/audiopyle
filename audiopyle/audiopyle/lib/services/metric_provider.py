from typing import Dict, Any, Callable, Optional

import numpy

from audiopyle.lib.models.feature import VampyFeatureAbstraction
from audiopyle.lib.models.file_meta import CompressedAudioFileMeta
from audiopyle.lib.models.metric import MetricValue, MetricDefinition
from audiopyle.lib.models.metric_transform import NoneTransformation, SelectRowTransformation, \
    SingleValueTransformation, SegmentLabelShareRatioTransformation, MetricTransformation
from audiopyle.lib.models.result import DataStats
from audiopyle.lib.utils.logger import get_logger

logger = get_logger()

_REGISTERED_METRIC_TRANSFORMATIONS = {
    "none": NoneTransformation,
    "select_row": SelectRowTransformation,
    "single_value": SingleValueTransformation,
    "segment_share_ratio": SegmentLabelShareRatioTransformation
}


def get_transformation(function_name: str, audio_meta: CompressedAudioFileMeta,function_kwargs: Dict[str, Any]) -> MetricTransformation:
    return _REGISTERED_METRIC_TRANSFORMATIONS[function_name](audio_meta, **function_kwargs)


def extract_metric_value(task_id: str, definition: MetricDefinition, transformation: MetricTransformation,
                         feature: VampyFeatureAbstraction) -> MetricValue:
    data_vector = transformation.call(feature)
    metric_stats = _extract_data_stats(data_vector)
    return MetricValue(task_id, definition, metric_stats)


def _extract_data_stats(numpy_array: numpy.ndarray) -> DataStats:
    return DataStats(minimum=_try_calculate_data_stat(numpy.amin, numpy_array),
                     maximum=_try_calculate_data_stat(numpy.amax, numpy_array),
                     median=_try_calculate_data_stat(numpy.median, numpy_array),
                     mean=_try_calculate_data_stat(numpy.mean, numpy_array),
                     standard_deviation=_try_calculate_data_stat(numpy.std, numpy_array),
                     variance=_try_calculate_data_stat(numpy.var, numpy_array),
                     sum=_try_calculate_data_stat(numpy.sum, numpy_array),
                     count=len(numpy_array))


def _try_calculate_data_stat(calc_callable: Callable[..., float], calc_input: numpy.ndarray) -> Optional[float]:
    try:
        numpy_result = calc_callable(calc_input)
        return None if numpy.isnan(numpy_result) else float(numpy_result)
    except Exception as e:
        logger.warning(
            "Could not calculate {} from data shaped {}: {}; returning None".format(calc_callable, calc_input.shape, e))
        return None
