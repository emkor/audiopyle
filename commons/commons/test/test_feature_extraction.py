from unittest import TestCase

from assertpy import assert_that
from numpy import array, float32
from vampyhost import RealTime

from commons.models.feature import VampyConstantStepFeature
from commons.services.feature_extraction import _map_feature


class ExtractedFeatureMappingTest(TestCase):
    def setUp(self):
        self.wrong_feature_type = {'anything': [1.0]}
        self.constant_step_array = array([0.38888031, 0.3144314, 0.46564227, 0.31890243, 0.22512659], dtype=float32)
        self.constant_step_feature = {'vector': (RealTime('milliseconds', 0.023219954 * 1000),
                                                 self.constant_step_array)}

    def test_should_build_constant_step_feature(self):
        feature_object = _map_feature(self.constant_step_feature)
        assert_that(feature_object).is_type_of(VampyConstantStepFeature)
        assert_that(feature_object._time_step).is_equal_to(0.023219954)
        assert_that(feature_object.value_shape()).is_equal_to((5, 1))
        assert_that(feature_object.values()).is_same_as(self.constant_step_array)

    def test_should_raise_error_on_wrong_feature_type(self):
        assert_that(_map_feature).raises(NotImplementedError).when_called_with(self.wrong_feature_type)
