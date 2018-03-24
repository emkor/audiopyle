import unittest

from assertpy import assert_that

from commons.models.compressed_feature import CompressedFeatureDTO, CompressionType
from commons.repository.feature_data import FeatureDataRepository
from commons.test.utils import setup_db_repository_test_class, tear_down_db_repository_test_class


class FeatureDataRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_db_repository_test_class(cls)

    @classmethod
    def tearDownClass(cls):
        tear_down_db_repository_test_class(cls)

    def setUp(self):
        self.task_id = "0f961f20-b036-5740-b526-013523dd88c7"
        self.compression_type = CompressionType.gzip
        self.feature_data_example = CompressedFeatureDTO(self.task_id, self.compression_type, b"some binary data")
        self.feature_repository = FeatureDataRepository(self.session_provider)

    def tearDown(self):
        self.feature_repository.delete_all()

    def test_should_insert_and_retrieve_id_by_task_id(self):
        self.feature_repository.insert(self.feature_data_example)
        identifier = self.feature_repository.get_id_by_model(self.feature_data_example)
        assert_that(identifier).is_not_none().is_equal_to(self.task_id)

    def test_should_insert_and_retrieve_model_by_task_id(self):
        self.feature_repository.insert(self.feature_data_example)
        retrieved_object = self.feature_repository.get_by_id(self.task_id)
        assert_that(retrieved_object).is_equal_to(self.feature_data_example)
