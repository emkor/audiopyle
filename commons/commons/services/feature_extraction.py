from typing import Text, Dict, Any

import vamp

from commons.abstractions.model import Model
from commons.models.feature import VampyFeatureMeta, VampyVariableStepFeature, VampyConstantStepFeature, StepFeature
from commons.models.plugin import VampyPlugin
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


def extract_features(audio_segment: MonoAudioSegment, vampy_plugin: VampyPlugin, output_name: Text) -> VampyFeatureMeta:
    feature_meta = VampyFeatureMeta(vampy_plugin=vampy_plugin, segment_meta=audio_segment.get_meta(),
                                    plugin_output=output_name)
    raw_results = vamp.collect(data=audio_segment.data, sample_rate=audio_segment.source_file_meta.sample_rate,
                               plugin_key=vampy_plugin.key, output=output_name)
    return _map_feature(feature_meta=feature_meta, extracted_data=raw_results)


def _map_feature(feature_meta: VampyFeatureMeta, extracted_data: Dict[Text, Any]) -> VampyFeatureMeta:
    data_type = list(extracted_data.keys())[0]
    if data_type == "list":
        value_list = [StepFeature(f.get("timestamp").to_float(), f.get("values"), f.get("label") or None)
                      for f in extracted_data.get("list")]
        return VampyVariableStepFeature(vampy_plugin=feature_meta.vampy_plugin, segment_meta=feature_meta.segment_meta,
                                        plugin_output=feature_meta.plugin_output, value_list=value_list)
    elif data_type in ("vector", "matrix"):
        data = extracted_data.get("vector") or extracted_data.get("matrix")
        return VampyConstantStepFeature(vampy_plugin=feature_meta.vampy_plugin, segment_meta=feature_meta.segment_meta,
                                        plugin_output=feature_meta.plugin_output, time_step=data[0].to_float(),
                                        matrix=data[1])
    else:
        raise NotImplementedError("Can not recognize feature type: {}".format(extracted_data.keys()))
