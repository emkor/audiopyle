from unittest import TestCase

from assertpy import assert_that
from numpy import array, float32

from audiopyle.lib.models.feature import VampyConstantStepFeature, VampyVariableStepFeature, StepFeature
from audiopyle.lib.models.file_meta import CompressedAudioFileMeta
from audiopyle.lib.models.metric import NoneTransformation, SelectRowTransformation, SingleValueTransformation, \
    SegmentLabelShareRatioTransformation


class FeatureMetricTransformationTest(TestCase):
    def setUp(self):
        self.audio_meta = CompressedAudioFileMeta("some_name.mp3", 1024, 1, 44100, length_sec=4., bit_rate_kbps=128)
        self.single_dimensional_feature = array([0.38888031], dtype=float32)
        self.two_dimensional_feature = array([0.38888031, 0.3144314, 0.46564227, 0.31890243, 0.22512659], dtype=float32)
        self.three_dimensional_feature = array([[0.38888031, 0.3144314],
                                                [0.46564227, 0.31890243],
                                                [0.22512659, 0.31890243]], dtype=float32)
        self.constant_step_2d_feature = VampyConstantStepFeature("", time_step=0.1, matrix=self.two_dimensional_feature)
        self.constant_step_3d_feature = VampyConstantStepFeature("", time_step=0.1,
                                                                 matrix=self.three_dimensional_feature)
        self.variable_step_single_value_feature = VampyVariableStepFeature("", [StepFeature(timestamp=0.0,
                                                                                            values=array([519.51]))])
        self.constant_step_single_value_feature = VampyConstantStepFeature("", time_step=0.1,
                                                                           matrix=self.single_dimensional_feature)

    def test_should_extract_using_none_transformation_on_2d_feature(self):
        none_transformation = NoneTransformation(audio_meta=self.audio_meta)
        metric_vector = none_transformation.call(self.constant_step_2d_feature)
        assert_that(metric_vector).is_length(len(self.two_dimensional_feature))
        assert_that(metric_vector[0]).is_equal_to(self.two_dimensional_feature[0])

    def test_should_extract_using_select_row_transformation_on_3d_feature(self):
        first_row_transformation = SelectRowTransformation(row_index=0, audio_meta=self.audio_meta)
        second_row_transformation = SelectRowTransformation(row_index=1, audio_meta=self.audio_meta)
        first_row_vector = first_row_transformation.call(self.constant_step_3d_feature)
        second_row_vector = second_row_transformation.call(self.constant_step_3d_feature)
        assert_that(first_row_vector).is_length(len(self.three_dimensional_feature))
        assert_that(second_row_vector).is_length(len(self.three_dimensional_feature))
        assert_that(first_row_vector[0]).is_equal_to(self.three_dimensional_feature[0][0])
        assert_that(first_row_vector[1]).is_equal_to(self.three_dimensional_feature[1][0])
        assert_that(second_row_vector[0]).is_equal_to(self.three_dimensional_feature[0][1])
        assert_that(second_row_vector[1]).is_equal_to(self.three_dimensional_feature[1][1])

    def test_should_extract_using_single_value_transformation(self):
        single_value_transformation = SingleValueTransformation(audio_meta=self.audio_meta)
        single_value_from_variable_step_feature = single_value_transformation.call(
            self.variable_step_single_value_feature)
        single_value_from_constant_step_feature = single_value_transformation.call(
            self.constant_step_single_value_feature)
        assert_that(single_value_from_variable_step_feature).is_length(2)
        assert_that(single_value_from_constant_step_feature).is_length(2)

    def test_should_transform_segment_based_simple_variable_feature_into_ratio_metric(self):
        segment_share_ratio = SegmentLabelShareRatioTransformation(audio_meta=self.audio_meta, label="b")
        segment_variable_step_feature = VampyVariableStepFeature("task_id", [StepFeature(timestamp=0.0,
                                                                                         values=array([0]),
                                                                                         label="a"),
                                                                             StepFeature(timestamp=1.0,
                                                                                         values=array([1]),
                                                                                         label="b"),
                                                                             StepFeature(timestamp=2.0,
                                                                                         values=array([0]),
                                                                                         label="a"),
                                                                             StepFeature(timestamp=3.0,
                                                                                         values=array([1]),
                                                                                         label="b")
                                                                             ])
        actual_metric_vector = segment_share_ratio.call(segment_variable_step_feature)
        assert_that(actual_metric_vector).is_length(2).contains(0.25)
