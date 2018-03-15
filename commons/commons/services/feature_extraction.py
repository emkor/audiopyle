from typing import Text, Dict, Any

import numpy
import vamp

from commons.models.feature import VampyFeatureAbstraction, VampyVariableStepFeature, VampyConstantStepFeature, \
    StepFeature
from commons.utils.logger import get_logger

logger = get_logger()


def extract_raw_feature(wav_data: numpy.ndarray, sample_rate: int, vampy_plugin_key: Text,
                        output_name: Text) -> Dict[Text, Any]:
    return vamp.collect(data=wav_data, sample_rate=sample_rate,
                        plugin_key=vampy_plugin_key, output=output_name)


def build_feature_object(task_id: str, extracted_data: Dict[Text, Any]) -> VampyFeatureAbstraction:
    data_type = list(extracted_data.keys())[0]
    if data_type == "list":
        value_list = [StepFeature(f.get("timestamp").to_float(), f.get("values"), f.get("label") or None)
                      for f in extracted_data.get("list")]
        return VampyVariableStepFeature(task_id, step_features=value_list)
    elif data_type in ("vector", "matrix"):
        data = extracted_data.get("vector") or extracted_data.get("matrix")
        return VampyConstantStepFeature(task_id, time_step=data[0].to_float(), matrix=data[1])
    else:
        raise NotImplementedError("Can not recognize feature type: {}".format(extracted_data.keys()))
