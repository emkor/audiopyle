import unittest
from time import sleep

from assertpy import assert_that
from commons.provider.redis_queue_client import RedisQueueClient
from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor
from commons.utils.constant import PROJECT_HOME_ENV

DEVOPS_DIR = FileAccessor.join(OsEnvAccessor.get_env_variable(PROJECT_HOME_ENV), 'devops')
SH_STATUS_OK = 0
RUN_REDIS_DOCKER_SH = "run_redis_docker.sh"
RUN_COORDINATOR_DOCKER_SH = "run_coordinator_docker.sh"
KILL_CONTAINER_SH = "kill_container.sh"
REDIS_QUEUE_NAME = 'xtracter_tasks'
REDIS_PORT = 6379
REDIS_CONTAINER_NAME = 'RedisClientTestInstance'
COORDINATOR_CONTAINER_NAME = 'CoordinatorTestInstance'
REDIS_BOOT_TIME = 8
COORDINATOR_BOOT_TIME = 8


class RedisCoordinatorIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        run_redis_sh = FileAccessor.join(DEVOPS_DIR, RUN_REDIS_DOCKER_SH)
        status_redis = FileAccessor.run_command(run_redis_sh, REDIS_CONTAINER_NAME, REDIS_PORT)
        assert_that(status_redis).is_equal_to(SH_STATUS_OK)
        sleep(REDIS_BOOT_TIME)

        run_coordinator_sh = FileAccessor.join(DEVOPS_DIR, RUN_COORDINATOR_DOCKER_SH)
        status_coordinator = FileAccessor.run_command(run_coordinator_sh, COORDINATOR_CONTAINER_NAME)
        assert_that(status_coordinator).is_equal_to(SH_STATUS_OK)
        sleep(COORDINATOR_BOOT_TIME)

    @classmethod
    def tearDownClass(cls):
        kill_container_sh = FileAccessor.join(DEVOPS_DIR, KILL_CONTAINER_SH)
        status_redis = FileAccessor.run_command(kill_container_sh, REDIS_CONTAINER_NAME)
        assert_that(status_redis).is_equal_to(SH_STATUS_OK)

        status_coordinator = FileAccessor.run_command(kill_container_sh, COORDINATOR_CONTAINER_NAME)
        assert_that(status_coordinator).is_equal_to(SH_STATUS_OK)

    def setUp(self):
        self.redis_client = RedisQueueClient(REDIS_QUEUE_NAME)

    def tearDown(self):
        self.redis_client.clear()

    def test_should_push_file_list_to_redis(self):
        assert_that(self.redis_client.length()).is_equal_to(1)
        assert_that(self.redis_client.list()[0][u'remote_file_meta'][u'size']).is_equal_to(207916)
