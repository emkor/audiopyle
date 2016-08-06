import unittest

from assertpy import assert_that

from commons.model.b2_config import B2Config
from commons.provider.redis_queue_client import RedisQueueClient


class RedisQueueClientTest(unittest.TestCase):
    def setUp(self):
        self.redis_client = RedisQueueClient(None)

    def test_should_serialize_simple_types(self):
        number = 3
        floating_point = 1.31
        example_text = "some text"

        number_json = self.redis_client._to_json(number)
        floating_point_json = self.redis_client._to_json(floating_point)
        example_text_json = self.redis_client._to_json(example_text)

        assert_that(number_json).is_equal_to('3')
        assert_that(floating_point_json).is_equal_to('1.31')
        assert_that(example_text_json).is_equal_to(example_text_json)

    def test_should_serialize_dict(self):
        example_dict = {"some_key": 1.2, "inner_dict": {"another_key": "hash"}}
        example_dict_json = self.redis_client._to_json(example_dict)
        assert_that(example_dict_json).is_instance_of(basestring).contains("some_key", "another_key", "1.2", "hash")

    def test_should_serialize_list(self):
        example_list = [1, 2, "text", ["inner", 4]]
        example_list_json = self.redis_client._to_json(example_list)
        assert_that(example_list_json).is_instance_of(basestring).contains("1", "2", "text", "inner", "4")

    def test_should_serialize_custom_objects(self):
        example_object = B2Config("acc_id", "app_key", "b_name")
        example_object_json = self.redis_client._to_json(example_object)
        assert_that(example_object_json).is_instance_of(basestring).contains("acc_id", "app_key", "b_name")

    def test_should_serialize_nested_objects(self):
        example_object = B2Config("acc_id", "app_key", B2Config(None, "app2_key", "b_name"))
        example_object_json = self.redis_client._to_json(example_object)
        assert_that(example_object_json).is_instance_of(basestring).contains("acc_id", "app_key", "app2_key", "b_name")
