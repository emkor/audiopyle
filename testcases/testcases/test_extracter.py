import unittest
from time import sleep

from assertpy import assert_that

from commons.provider.redis_queue_client import RedisQueueClient
from commons.utils.constant import AudiopyleConst

from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor

DEVOPS_DIR = FileAccessor.join(OsEnvAccessor.get_env_variable(AudiopyleConst.PROJECT_HOME_ENV), 'devops')
SH_STATUS_OK = 0
RUN_REDIS_DOCKER_SH = "run_redis_docker.sh"
KILL_CONTAINER_SH = "kill_container.sh"
REDIS_TASK_QUEUE_NAME = 'XtracterIntegrationTestTaskQueue'
REDIS_RESULT_QUEUE_NAME = 'XtracterIntegrationTestResultsQueue'
REDIS_PORT = 6379
REDIS_CONTAINER_NAME = 'RedisClientTestInstance'
REDIS_BOOT_TIME = 8


class XtracterIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        run_redis_sh = FileAccessor.join(DEVOPS_DIR, RUN_REDIS_DOCKER_SH)
        status = FileAccessor.run_command(run_redis_sh, REDIS_PORT, REDIS_CONTAINER_NAME)
        assert_that(status).is_equal_to(SH_STATUS_OK)
        sleep(REDIS_BOOT_TIME)

    @classmethod
    def tearDownClass(cls):
        kill_container_sh = FileAccessor.join(DEVOPS_DIR, KILL_CONTAINER_SH)
        status = FileAccessor.run_command(kill_container_sh, REDIS_CONTAINER_NAME)
        assert_that(status).is_equal_to(0)

    def setUp(self):
        self.redis_task_client = RedisQueueClient(REDIS_TASK_QUEUE_NAME)
        self.redis_results_client = RedisQueueClient(REDIS_RESULT_QUEUE_NAME)
        assert_that(self.redis_task_client.length()).is_equal_to(0)
        assert_that(self.redis_results_client.length()).is_equal_to(0)

    def tearDown(self):
        self.redis_task_client.clear()
        self.redis_results_client.clear()

    def test_shoud_extract_faetures_from_test_file(self):
        FileAccessor.run_command("docker", "run", "endlessdrones/audiopyle-xtracter")