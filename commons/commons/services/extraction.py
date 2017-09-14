from typing import Text, List, Tuple, Union, Dict

import vamp

from commons.abstractions.model import Model
from commons.audio.segment import MonoAudioSegment
from commons.vampy.feature import VampyFeatureMeta, VampyVariableStepFeature, VampyConstantStepFeature
from commons.vampy.plugin import VampyPlugin


class ExtractionRequest(Model):
    def __init__(self, audio_file_name: Text, plugin_key: Text, plugin_output: Text) -> None:
        self.audio_file_name = audio_file_name
        self.plugin_key = plugin_key
        self.plugin_output = plugin_output


def extract_features(audio_segment: MonoAudioSegment, vampy_plugin: VampyPlugin, output_name: Text, step_size: int = 0,
                     block_size: int = 0) -> VampyFeatureMeta:
    feature_meta = VampyFeatureMeta(vampy_plugin=vampy_plugin, segment_meta=audio_segment.get_meta(),
                                    plugin_output=output_name)
    raw_results = vamp.collect(data=audio_segment.data, sample_rate=audio_segment.source_file_meta.sample_rate,
                               plugin_key=vampy_plugin.key, output=output_name, step_size=step_size,
                               block_size=block_size)
    return _map_feature(feature_meta=feature_meta, extracted_data=raw_results)


def _map_feature(feature_meta: VampyFeatureMeta, extracted_data: Dict[Text, Union[Tuple, List]]) -> VampyFeatureMeta:
    data_type = list(extracted_data.keys())[0]
    if data_type == "list":
        return VampyVariableStepFeature(vampy_plugin=feature_meta.vampy_plugin, segment_meta=feature_meta.segment_meta,
                                        plugin_output=feature_meta.plugin_output, value_list=extracted_data.get("list"))
    elif data_type in ("vector", "matrix"):
        data = extracted_data.get("vector") or extracted_data.get("matrix")

        print(
            "feature_meta: {} / {} is a {}".format(feature_meta.vampy_plugin.key, feature_meta.plugin_output,
                                                   data_type))

        return VampyConstantStepFeature(vampy_plugin=feature_meta.vampy_plugin, segment_meta=feature_meta.segment_meta,
                                        plugin_output=feature_meta.plugin_output, time_step=data[0], matrix=data[1])
    else:
        raise NotImplementedError("Can not recognize feature type: {}".format(extracted_data.keys()))
