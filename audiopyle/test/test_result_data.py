import unittest

from assertpy import assert_that

from audiopyle.lib.models.audio_tag import Id3Tag
from audiopyle.lib.models.file_meta import CompressedAudioFileMeta
from audiopyle.lib.models.plugin import VampyPlugin, VampyPluginParams
from audiopyle.lib.models.result import FeatureMeta, FeatureType, AnalysisResult
from audiopyle.lib.utils.serialization import to_json


class AnalysisResultDataModelTest(unittest.TestCase):
    def setUp(self):
        self.example_vampy_plugin = VampyPlugin("vamp-example-plugins", "amplitudefollower", "amplitude",
                                                library_file_name="/root/vamp/vamp-example-plugins.so")
        self.result_data_example = FeatureMeta("0f961f20-b036-5740-b526-013523dd88c7", FeatureType.ConstantStepFeature,
                                               1024, (1, 10, 0))

    def test_should_serialize_and_deserialize_analysis_result_data_model(self):
        serialized = self.result_data_example.to_serializable()
        deserialized = FeatureMeta.from_serializable(serialized)
        assert_that(deserialized).is_not_none().is_equal_to(self.result_data_example)

    def test_should_serialized_to_json(self):
        as_json = to_json(self.result_data_example.to_serializable())
        assert_that(as_json).is_not_none().is_not_empty()


class AnalysisResultModelTest(unittest.TestCase):
    def setUp(self):
        self.audio_meta_example = CompressedAudioFileMeta("some_file.mp3", 1024 * 1024 * 2, 1, 44100, 45., 128.)
        self.id3_tag_example = Id3Tag(artist="Unknown Artist", title="Unknown Title", album="Unknown Album",
                                      date=2017, track=1, genre="Unknown Genre")
        self.example_vampy_plugin = VampyPlugin("vamp-example-plugins", "amplitudefollower", "amplitude",
                                                library_file_name="/root/vamp/vamp-example-plugins.so")
        self.task_id = "fa3b5d8c-b760-49e0-b8b5-7ce0737621d8"
        self.plugin_config_example = VampyPluginParams(block_size=2048, step_size=512)
        self.analysis_result_example = AnalysisResult(self.task_id, self.audio_meta_example, self.id3_tag_example,
                                                      self.example_vampy_plugin, self.plugin_config_example)

    def test_should_serialize_and_deserialize_analysis_result_data_model(self):
        serialized = self.analysis_result_example.to_serializable()
        deserialized = AnalysisResult.from_serializable(serialized)
        assert_that(deserialized).is_not_none().is_equal_to(self.analysis_result_example)

    def test_should_serialized_to_json(self):
        as_json = to_json(self.analysis_result_example.to_serializable())
        assert_that(as_json).is_not_none().is_not_empty()
