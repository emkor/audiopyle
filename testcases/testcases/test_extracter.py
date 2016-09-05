import unittest
from time import sleep

from assertpy import assert_that

from commons.model.analysis_task import AnalysisTask
from commons.model.remote_file_meta import RemoteFileMeta
from commons.model.remote_file_source import B2Config
from commons.provider.redis_queue_client import RedisQueueClient
from commons.utils.constant import PROJECT_HOME_ENV, B2_TEST_FILE_PATH, B2_ACCOUNT_ID, B2_APPLICATION_KEY, \
    B2_RESOURCES_BUCKET

from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor

DEVOPS_DIR = FileAccessor.join(OsEnvAccessor.get_env_variable(PROJECT_HOME_ENV), 'devops')
REDIS_DOCKER_RUN_SH = "run_redis_docker.sh"
XTRACTER_DOCKER_RUN_SH = "run_xtracter_docker.sh"
KILL_CONTAINER_SH = "kill_container.sh"
SH_STATUS_OK = 0

XTRACTER_CONTAINER_NAME = "XtracterTestInstance"
REDIS_CONTAINER_NAME = 'RedisTestInstance'

REDIS_TASK_QUEUE_NAME = 'xtracter_tasks'
REDIS_RESULT_QUEUE_NAME = 'xtracter_results'
REDIS_PORT = 6379

DOCKER_BOOT_TIME = 5
TASK_TAKE_TIME = 4
ANALYSIS_TIMEOUT = 90


class XtracterIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._run_devops_container_boot_script(REDIS_CONTAINER_NAME, REDIS_DOCKER_RUN_SH, REDIS_PORT)
        cls._run_devops_container_boot_script(XTRACTER_CONTAINER_NAME, XTRACTER_DOCKER_RUN_SH)

    @classmethod
    def tearDownClass(cls):
        kill_container_sh = FileAccessor.join(DEVOPS_DIR, KILL_CONTAINER_SH)
        status = FileAccessor.run_command(kill_container_sh, XTRACTER_CONTAINER_NAME)
        assert_that(status).is_equal_to(0)
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

    def test_should_take_task_and_extract_features_from_test_file(self):
        self._add_test_file_task()
        assert_that(self.redis_task_client.length()).is_equal_to(1)
        sleep(TASK_TAKE_TIME)
        assert_that(self.redis_task_client.length()).is_equal_to(0)
        assert_that(self._keep_polling_for_results_until_timeout()).is_true()

    def _add_test_file_task(self):
        remote_file_meta = RemoteFileMeta(B2_TEST_FILE_PATH, 0, 0)
        remote_file_source = B2Config(B2_ACCOUNT_ID, B2_APPLICATION_KEY, B2_RESOURCES_BUCKET)
        task = AnalysisTask(remote_file_meta, remote_file_source)
        self.redis_task_client.add(task.to_dict())

    def _keep_polling_for_results_until_timeout(self):
        analysis_time = 0
        interval_time = 3
        while analysis_time < ANALYSIS_TIMEOUT:
            if self.redis_results_client.length() > 0:
                print("Results appeared after {} seconds!".format(analysis_time))
                return True
            else:
                analysis_time += interval_time
                sleep(interval_time)
                print("Waiting for results next {} seconds...".format(interval_time))
        print("Results did not come up within {} seconds!".format(ANALYSIS_TIMEOUT))
        return False

    @classmethod
    def _run_devops_container_boot_script(cls, container_name, boot_script, *boot_script_params):
        boot_script = FileAccessor.join(DEVOPS_DIR, boot_script)
        boot_status = FileAccessor.run_command(boot_script, container_name, *boot_script_params)
        assert_that(boot_status).is_equal_to(SH_STATUS_OK)
        sleep(DOCKER_BOOT_TIME)

    @classmethod
    def _run_devops_stop_container_script(cls, container_name):
        kill_container_sh = FileAccessor.join(DEVOPS_DIR, KILL_CONTAINER_SH)
        status = FileAccessor.run_command(kill_container_sh, container_name)
        assert_that(status).is_equal_to(0)
