import unittest

import json

from assertpy import assert_that
from commons.models.result import AnalysisResultData, ResultVersion, FeatureType


class AnalysisResultDataModelTest(unittest.TestCase):
    def setUp(self):
        self.result_data_example = AnalysisResultData(ResultVersion.V1, "fa3b5d8c-b760-49e0-b8b5-7ce0737621d8",
                                                      FeatureType.ConstantStepFeature)

    def test_should_serialize_and_deserialize_analysis_result_data_model(self):
        serialized = self.result_data_example.serialize()
        deserialized = AnalysisResultData.deserialize(serialized)
        assert_that(deserialized).is_not_none().is_equal_to(self.result_data_example)

    def test_should_serialized_to_json(self):
        as_json = json.dumps(self.result_data_example.serialize())
        assert_that(as_json).is_not_none().is_not_empty()