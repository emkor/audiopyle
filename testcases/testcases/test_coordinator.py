import unittest

from assertpy import assert_that
from commons.provider.redis_queue_client import RedisQueueClient
from testcases.docker.container import Container
from testcases.docker.utils import IMAGE_REDIS, IMAGE_COORDINATOR

REDIS_QUEUE_NAME = 'xtracter_tasks'


class RedisCoordinatorIntegrationTest(unittest.TestCase):
    REDIS_CONTAINER = None
    COORDINATOR_CONTAINER = None

    @classmethod
    def setUpClass(cls):
        cls.REDIS_CONTAINER = Container(IMAGE_REDIS, 'RedisClientTestInstance')
        cls.COORDINATOR_CONTAINER = Container(IMAGE_COORDINATOR, 'CoordinatorTestInstance')

    @classmethod
    def tearDownClass(cls):
        cls.REDIS_CONTAINER.destroy()
        cls.COORDINATOR_CONTAINER.destroy()

    def setUp(self):
        self.redis_client = RedisQueueClient(REDIS_QUEUE_NAME)

    def tearDown(self):
        self.redis_client.clear()

    def test_should_push_file_list_to_redis(self):
        assert_that(self.redis_client.length()).is_equal_to(1)
        assert_that(self.redis_client.list()[0][u'remote_file_meta'][u'size']).is_equal_to(207916)
