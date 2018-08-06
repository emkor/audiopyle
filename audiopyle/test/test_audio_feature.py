import unittest
import json

import numpy
from assertpy import assert_that

from audiopyle.commons.models.feature import VampyConstantStepFeature, StepFeature, VampyVariableStepFeature
from audiopyle.commons.models.file_meta import AudioFileMeta


class ConstantStepAudioFeatureModelTest(unittest.TestCase):
    def setUp(self):
        self.audio_file_meta = AudioFileMeta(file_name="file.wav", channels_count=2,
                                             sample_rate=44100, file_size_bytes=88200)
        self.feature_values = numpy.array([1.0, 2.0, 3.0, 4.0])
        self.constant_step_feature = VampyConstantStepFeature(task_id="0f961f20-b036-5740-b526-013523dd88c7",
                                                              time_step=0.5, matrix=self.feature_values)

    def test_should_serialize_and_deserialize_feature(self):
        serialized = self.constant_step_feature.to_serializable()
        deserialized = VampyConstantStepFeature.from_serializable(serialized)
        assert_that(deserialized).is_not_none().is_equal_to(self.constant_step_feature)

    def test_should_serialized_to_json(self):
        as_json = json.dumps(self.constant_step_feature.to_serializable())
        assert_that(as_json).is_not_none().is_not_empty()

    def test_should_calculate_frames_properly(self):
        expected_frames = [0, 22050, 44100, 66150]
        actual_frames = self.constant_step_feature.frames(self.audio_file_meta)
        assert_that(actual_frames).is_equal_to(expected_frames)

    def test_should_list_timestamps_properly(self):
        expected_timestamps = [0., 0.5, 1., 1.5]
        actual_timestamps = self.constant_step_feature.timestamps()
        assert_that(actual_timestamps).is_equal_to(expected_timestamps)

    def test_values_should_have_correct_shape(self):
        assert_that(self.constant_step_feature.values().all()).is_equal_to(self.feature_values.all())
        assert_that(self.constant_step_feature.value_shape()).is_equal_to((4, 1, 0))


class VariableStepAudioFeatureModelTest(unittest.TestCase):
    def setUp(self):
        self.audio_file_meta = AudioFileMeta(file_name="file.wav", channels_count=2,
                                             sample_rate=44100, file_size_bytes=88200)
        self.feature_values = [1.0, 2.0, 3.0, 4.0]
        self.feature_steps = [StepFeature(v, values=numpy.asanyarray(self.feature_values), label="text_{}".format(v))
                              for v in self.feature_values]
        self.variable_step_feature = VampyVariableStepFeature(task_id="0f961f20-b036-5740-b526-013523dd88c7",
                                                              step_features=self.feature_steps)

    def test_should_serialize_and_deserialize_feature(self):
        serialized = self.variable_step_feature.to_serializable()
        deserialized = VampyVariableStepFeature.from_serializable(serialized)
        assert_that(deserialized).is_not_none().is_equal_to(self.variable_step_feature)

    def test_should_serialized_to_json(self):
        as_json = json.dumps(self.variable_step_feature.to_serializable())
        assert_that(as_json).is_not_none().is_not_empty()
