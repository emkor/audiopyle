from unittest import TestCase

from assertpy import assert_that
from numpy import array, float32, ndarray
from vampyhost import RealTime

from commons.models.feature import VampyConstantStepFeature, VampyVariableStepFeature
from commons.services.feature_extraction import build_feature_object


class ExtractedFeatureMappingTest(TestCase):
    def setUp(self):
        self.wrong_feature_type = {'anything': [1.0]}
        self.constant_step_array = array([0.38888031, 0.3144314, 0.46564227, 0.31890243, 0.22512659], dtype=float32)
        self.constant_step_feature = {'vector': (RealTime('milliseconds', 0.023219954 * 1000),
                                                 self.constant_step_array)}
        self.variable_step_feature = {'list': [{'timestamp': RealTime('milliseconds', 0.000000000 * 1000),
                                                'label': 'F# minor',
                                                'values': array([19.], dtype=float32)},
                                               {'timestamp': RealTime('milliseconds', 0.743038548 * 1000),
                                                'label': 'D major',
                                                'values': array([3.], dtype=float32)}]}
        self.task_id = "0f961f20-b036-5740-b526-013523dd88c7"

    def test_should_build_constant_step_feature(self):
        feature_object = build_feature_object(self.task_id, self.constant_step_feature)
        assert_that(feature_object).is_type_of(VampyConstantStepFeature)
        assert_that(feature_object._time_step).is_equal_to(0.023219954)
        assert_that(feature_object.value_shape()).is_equal_to((5, 1))
        assert_that(feature_object.values()).is_same_as(self.constant_step_array)
        assert_that(feature_object.timestamps()).is_length(5).contains_only(0.000000000, 0.023219954, 0.046439908,
                                                                            0.069659862, 0.092879816)

    def test_should_build_variable_step_feature(self):
        feature_object = build_feature_object(self.task_id, self.variable_step_feature)
        assert_that(feature_object).is_type_of(VampyVariableStepFeature)
        assert_that(feature_object.value_shape()).is_equal_to((2, 1))
        assert_that(feature_object.values()).is_type_of(ndarray)
        assert_that(feature_object.timestamps()).is_length(2).contains_only(0.000000000, 0.743038548)

    def test_should_raise_error_on_wrong_feature_type(self):
        assert_that(build_feature_object).raises(NotImplementedError).when_called_with(self.task_id, self.wrong_feature_type)
