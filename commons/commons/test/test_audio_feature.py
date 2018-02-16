import unittest

import json

import numpy
from assertpy import assert_that

from commons.models.feature import VampyConstantStepFeature, VampyVariableStepFeature, StepFeature
from commons.models.file_meta import WavAudioFileMeta
from commons.models.plugin import VampyPlugin
from commons.models.segment import AudioSegmentMeta


class ConstantStepAudioFeatureModelTest(unittest.TestCase):
    def setUp(self):
        self.audio_file_meta = WavAudioFileMeta(channels_count=2, sample_rate=44100, frames_count=22050, bit_depth=16)
        self.audio_segment_meta = AudioSegmentMeta(self.audio_file_meta, frame_from=0, frame_to=22049)
        self.vampy_plugin = VampyPlugin(key="plugin_provider:plugin_name", categories=["category1"],
                                        outputs=["output1"], library_path="/some/path")
        self.feature_values = numpy.array([1.0, 2.0, 3.0, 4.0])
        self.constant_step_feature = VampyConstantStepFeature(vampy_plugin=self.vampy_plugin,
                                                              segment_meta=self.audio_segment_meta,
                                                              plugin_output="output1", time_step=0.5,
                                                              matrix=self.feature_values)

    def test_should_serialize_and_deserialize_feature(self):
        serialized = self.constant_step_feature.to_serializable()
        deserialized = VampyConstantStepFeature.from_serializable(serialized)
        assert_that(deserialized).is_not_none().is_equal_to(self.constant_step_feature)

    def test_should_serialized_to_json(self):
        as_json = json.dumps(self.constant_step_feature.to_serializable())
        assert_that(as_json).is_not_none().is_not_empty()

    def test_should_calculate_frames_properly(self):
        expected_frames = [0, 22050, 44100, 66150]
        actual_frames = self.constant_step_feature.frames()
        assert_that(actual_frames).is_equal_to(expected_frames)

    def test_should_list_timestamps_properly(self):
        expected_timestamps = [0., 0.5, 1., 1.5]
        actual_timestamps = self.constant_step_feature.timestamps()
        assert_that(actual_timestamps).is_equal_to(expected_timestamps)

    def test_values_should_have_correct_shape(self):
        assert_that(self.constant_step_feature.values().all()).is_equal_to(self.feature_values.all())
        assert_that(self.constant_step_feature.value_shape()).is_equal_to((4, 1))


class VariableStepAudioFeatureModelTest(unittest.TestCase):
    def setUp(self):
        self.audio_file_meta = WavAudioFileMeta(channels_count=2, sample_rate=44100, frames_count=22050, bit_depth=16)
        self.audio_segment_meta = AudioSegmentMeta(self.audio_file_meta, frame_from=0, frame_to=22049)
        self.vampy_plugin = VampyPlugin(key="plugin_provider:plugin_name", categories=["category1"],
                                        outputs=["output1"], library_path="/some/path")
        self.feature_values = [1.0, 2.0, 3.0, 4.0]
        self.feature_steps = [StepFeature(v, values=numpy.asanyarray(self.feature_values), label="text_{}".format(v))
                              for v in self.feature_values]
        self.variable_step_feature = VampyVariableStepFeature(vampy_plugin=self.vampy_plugin,
                                                              segment_meta=self.audio_segment_meta,
                                                              plugin_output="output1", step_features=self.feature_steps)

    def test_should_serialize_and_deserialize_feature(self):
        serialized = self.variable_step_feature.to_serializable()
        deserialized = VampyVariableStepFeature.from_serializable(serialized)
        assert_that(deserialized).is_not_none().is_equal_to(self.variable_step_feature)

    def test_should_serialized_to_json(self):
        as_json = json.dumps(self.variable_step_feature.to_serializable())
        assert_that(as_json).is_not_none().is_not_empty()
