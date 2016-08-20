import unittest
from time import sleep

from assertpy import assert_that
from commons.provider.redis_queue_client import RedisQueueClient
from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor
from commons.utils.constant import AudiopyleConst

DEVOPS_DIR = FileAccessor.join(OsEnvAccessor.get_env_variable(AudiopyleConst.PROJECT_HOME_ENV), 'devops')
SH_STATUS_OK = 0
RUN_REDIS_DOCKER_SH = "run_redis_docker.sh"
KILL_CONTAINER_SH = "kill_container.sh"
REDIS_QUEUE_NAME = 'RedisClientTestQueue'
REDIS_PORT = 6379
REDIS_CONTAINER_NAME = 'RedisClientTestInstance'
REDIS_BOOT_TIME = 8


class RedisClientIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        run_redis_sh = FileAccessor.join(DEVOPS_DIR, RUN_REDIS_DOCKER_SH)
        status = FileAccessor.run_command(run_redis_sh, REDIS_CONTAINER_NAME, REDIS_PORT)
        assert_that(status).is_equal_to(SH_STATUS_OK)
        sleep(REDIS_BOOT_TIME)

    @classmethod
    def tearDownClass(cls):
        kill_container_sh = FileAccessor.join(DEVOPS_DIR, KILL_CONTAINER_SH)
        status = FileAccessor.run_command(kill_container_sh, REDIS_CONTAINER_NAME)
        assert_that(status).is_equal_to(0)

    def setUp(self):
        self.redis_client = RedisQueueClient(REDIS_QUEUE_NAME)
        assert_that(self.redis_client.length()).is_equal_to(0)

    def tearDown(self):
        self.redis_client.clear()

    def test_should_add_simple_types_to_queue(self):
        self.redis_client.add(4.0)
        self.redis_client.add("some text")
        assert_that(self.redis_client.length()).is_equal_to(2)

    def test_should_act_as_queue(self):
        inserted_1 = [4.0, 3.5, 2.1]
        inserted_2 = "some text"

        self.redis_client.add(inserted_1)
        self.redis_client.add(inserted_2)

        taken_1 = self.redis_client.take()
        taken_2 = self.redis_client.take()

        assert_that(taken_1).is_equal_to(inserted_1)
        assert_that(taken_2).is_equal_to(inserted_2)

    def test_should_handle_custom_objects(self):
        inserted_1 = CustomType(number=1, text="some text", my_list=[1, 2])
        inserted_2 = CustomType(number=3, text="some another text", my_list=["first text", "second text"])

        self.redis_client.add(inserted_1)
        self.redis_client.add(inserted_2)

        assert_that(self.redis_client.length()).is_equal_to(2)

        taken_1 = CustomType(**self.redis_client.take())
        taken_2 = CustomType(**self.redis_client.take())

        self.assertEqual(inserted_1, taken_1)
        self.assertEqual(inserted_2, taken_2)

    def test_should_clearing_work(self):
        self.redis_client.add([4.0, 3.5, 2.1])
        assert_that(self.redis_client.length()).is_equal_to(1)

        self.redis_client.clear()
        assert_that(self.redis_client.length()).is_equal_to(0)


class CustomType(object):
    def __init__(self, number, text, my_list):
        self.number = number
        self.text = text
        self.my_list = my_list

    def __hash__(self):
        return hash((self.number, self.text, self.my_list))

    def __eq__(self, other):
        return self.number == other.number and self.text == other.text and self.my_list == other.my_list

    def __str__(self):
        return "CustomType: {}".format(self.__dict__)

    def __repr__(self):
        return self.__str__()
