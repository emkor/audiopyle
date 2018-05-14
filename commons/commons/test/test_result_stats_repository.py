import unittest

from assertpy import assert_that

from commons.models.result import AnalysisStats
from commons.repository.result import ResultStatsRepository
from commons.test.utils import setup_db_repository_test_class, tear_down_db_repository_test_class


class ResultStatsRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_db_repository_test_class(cls)

    @classmethod
    def tearDownClass(cls):
        tear_down_db_repository_test_class(cls)

    def setUp(self):
        self.task_id = "0f961f20-b036-5740-b526-013523dd88c7"
        self.example_stats = AnalysisStats(self.task_id, 12., 4., 1.3, 0.5, 1., 0.2, 0.1)
        self.repository = ResultStatsRepository(self.session_provider)

    def tearDown(self):
        self.repository.delete_all()

    def test_should_insert_example_stats_and_retrieve_by_model(self):
        self.repository.insert(self.example_stats)

        identifier = self.repository.get_id_by_model(self.example_stats)
        assert_that(identifier).is_not_none().is_equal_to(self.task_id)

        retrieved_model = self.repository.get_by_id(identifier)
        assert_that(retrieved_model).is_equal_to(self.example_stats)

    def test_should_insert_and_retrieve_by_task_id(self):
        self.repository.insert(self.example_stats)

        retrieved_model = self.repository.get_by_id(self.example_stats.task_id)
        assert_that(retrieved_model).is_equal_to(self.example_stats)
