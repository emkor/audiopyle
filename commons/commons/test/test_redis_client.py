import unittest

from assertpy import assert_that
from mock import Mock
from redis import ConnectionError

from commons.model.remote_file_source import create_b2_source_config
from commons.provider.redis_queue_client import RedisQueueClient


class RedisQueueClientTest(unittest.TestCase):
    def setUp(self):
        self.redis_internal_client = Mock()
        self.test_queue_name = "TestQueueName"
        self.redis_client = RedisQueueClient(self.test_queue_name)
        self.redis_client.client = self.redis_internal_client

    def test_should_serialize_primitives(self):
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
        example_object = create_b2_source_config("acc_id", "app_key", "b_name")
        example_object_json = self.redis_client._to_json(example_object)
        assert_that(example_object_json).is_instance_of(basestring).contains("acc_id", "app_key", "b_name")

    def test_should_not_try_deserialize_none(self):
        assert_that(self.redis_client._from_json(None)).is_equal_to(None)

    def test_should_deserialize_primitives(self):
        assert_that(self.redis_client._from_json("-1")).is_equal_to(-1)
        assert_that(self.redis_client._from_json("1.41")).is_equal_to(1.41)

    def test_should_count_properly(self):
        self.redis_internal_client.llen.return_value = 3
        assert_that(self.redis_client.length()).is_equal_to(3)

    def test_should_length_return_zero_if_redis_not_available(self):
        self.redis_internal_client.llen.side_effect = ConnectionError("Connection refused")
        assert_that(self.redis_client.length()).is_equal_to(0)

    def test_listing_queue_on_error_should_return_empty_list(self):
        self.redis_internal_client.lrange.side_effect = ConnectionError("Connection refused")
        assert_that(self.redis_client.list()).is_equal_to([])

    def test_clearing_should_call_internal_delete(self):
        self.redis_client.clear()
        self.redis_internal_client.delete.assert_called_once()

    def test_clearing_should_not_fail_when_redis_is_unavailable(self):
        self.redis_internal_client.delete.side_effect = ConnectionError("Connection refused")
        self.redis_client.clear()
        self.redis_internal_client.delete.assert_called_once()

    def test_adding_should_call_proper_internal_client_methods(self):
        self.redis_client.add(1.4)
        self.redis_internal_client.rpush.assert_called_once()

    def test_adding_should_not_fail_on_connection_error(self):
        self.redis_internal_client.rpush.side_effect = ConnectionError("Connection refused")
        self.redis_client.add(1.4)
        self.redis_internal_client.rpush.assert_called_once()

    def test_taking_should_call_proper_internal_client_methods(self):
        self.redis_client.add(1.4)
        self.redis_internal_client.rpush.assert_called_once()

    def test_taking_should_not_fail_on_connection_error(self):
        self.redis_internal_client.lpop.side_effect = ConnectionError("Connection refused")
        self.redis_client.take()
        self.redis_internal_client.lpop.assert_called_once()
