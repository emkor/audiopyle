import numpy
from vampyhost import RealTime

import unittest
from assertpy import assert_that

from xtracter.service.feature_mapper import FeatureMapper


class FeatureMapperTest(unittest.TestCase):
    def test_should_map_list_type_feature_without_values(self):
        list_type_feature = {'list': [
            {'timestamp': RealTime('seconds', 0.000000000), 'label': 'some_label'},
            {'timestamp': RealTime('seconds', 0.011609977), 'label': 'some_label'},
            {'timestamp': RealTime('seconds', 0.023219955), 'label': 'some_label'},
            {'timestamp': RealTime('seconds', 0.034829932), 'label': 'some_label'}
        ]}
        mapped_features = FeatureMapper.from_dict(list_type_feature)
        assert_that(mapped_features).is_not_empty().is_length(4)
        assert_that(mapped_features[0].label).is_equal_to('some_label')
        assert_that(mapped_features[0].timestamp).is_equal_to(0.0)
        assert_that(mapped_features[1].timestamp).is_equal_to(0.011609977)

    def test_should_map_list_type_feature(self):
        list_type_feature = {'list': [
            {'timestamp': RealTime('seconds', 0.000000000), 'values': numpy.asarray([0.02])},
            {'timestamp': RealTime('seconds', 0.011609977), 'values': numpy.asarray([0.031])}]
        }
        mapped_features = FeatureMapper.from_dict(list_type_feature)
        assert_that(mapped_features).is_not_empty().is_length(2)

    def test_should_map_vector_type_feature(self):
        list_type_feature = {'vector': (
            RealTime('seconds', 0.005804988),
            numpy.asarray([0.23947874, 0.61372721, -0.7251808, 0.4235664]))
        }
        mapped_features = FeatureMapper.from_dict(list_type_feature)
        assert_that(mapped_features).is_not_empty().is_length(4)
        assert_that(mapped_features[1].timestamp).is_equal_to(0.005804988)
        assert_that(mapped_features[2].timestamp).is_equal_to(2 * 0.005804988)

    def test_should_map_matrix_type_feature(self):
        list_type_feature = {'matrix': (
            RealTime('seconds', 0.023219954),
            numpy.asarray([[0.34790778, 0.06657285, 0.11234169, 0.17648846, 0.17510542, 0.11202326, 0.00956102],
                           [0.41738406, 0.00981532, 0.05403747, 0.10079852, 0.19992393, 0.19602031, 0.02202023]])
        )}
        mapped_features = FeatureMapper.from_dict(list_type_feature)
        assert_that(mapped_features).is_not_empty().is_length(2)
        first_feature = mapped_features[0]
        assert_that(first_feature.value).is_length(7)
        assert_that(mapped_features[1].timestamp).is_equal_to(0.023219954)
