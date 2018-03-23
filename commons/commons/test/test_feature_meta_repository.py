import unittest

from assertpy import assert_that

from commons.models.result import FeatureMeta, FeatureType, DataStats
from commons.repository.feature_meta import FeatureMetaRepository
from commons.test.utils import setup_db_repository_test_class, tear_down_db_repository_test_class


class FeatureMetaRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_db_repository_test_class(cls)

    @classmethod
    def tearDownClass(cls):
        tear_down_db_repository_test_class(cls)

    def setUp(self):
        self.task_id = "0f961f20-b036-5740-b526-013523dd88c7"
        self.data_stats = DataStats(0.1, 0.95, 0.6, 0.4, 0.01, 0.02)
        self.feature_meta_example = FeatureMeta(self.task_id, FeatureType.ConstantStepFeature, 1024, (10, 1, 0),
                                                self.data_stats)
        self.feature_repository = FeatureMetaRepository(self.session_provider)

    def tearDown(self):
        self.feature_repository.delete_all()

    def test_should_insert_and_retrieve_id_by_task_id(self):
        self.feature_repository.insert(self.feature_meta_example)
        identifier = self.feature_repository.get_id_by_model(self.feature_meta_example)
        assert_that(identifier).is_not_none().is_equal_to(self.task_id)

    def test_should_insert_and_retrieve_model_by_task_id(self):
        self.feature_repository.insert(self.feature_meta_example)
        retrieved_object = self.feature_repository.get_by_id(self.task_id)
        assert_that(retrieved_object).is_equal_to(self.feature_meta_example)
