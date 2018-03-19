import unittest

import json
from assertpy import assert_that

from commons.models.compressed_feature import CompressedFeatureDTO, CompressionType


class CompressedFeatureModelTest(unittest.TestCase):
    def setUp(self):
        self.model_example = CompressedFeatureDTO(task_id="0f961f20-b036-5740-b526-013523dd88c7",
                                                  compression=CompressionType.none,
                                                  data=b"some_bytes_data")

    def test_should_serialize_and_deserialize_model(self):
        serializable = self.model_example.to_serializable()
        assert_that(serializable).is_not_none().is_not_empty()

        deserialized = CompressedFeatureDTO.from_serializable(serializable)
        assert_that(deserialized).is_equal_to(self.model_example)
        assert_that(deserialized.size_bytes()).is_equal_to(self.model_example.size_bytes())

    def test_should_serialize_to_json_and_back(self):
        serialized = json.dumps(self.model_example.to_serializable())
        assert_that(serialized).is_not_none().is_not_empty()

        deserialized = CompressedFeatureDTO.from_serializable(json.loads(serialized))
        assert_that(deserialized).is_equal_to(self.model_example)
