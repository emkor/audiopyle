import json

import redis
from redis import ConnectionError
from commons.utils.logging_setup import GetLogger


class RedisQueueClient(object):
    def __init__(self, queue_name, redis_host="localhost", redis_port=6379):
        self.queue_name = queue_name
        self.client = redis.StrictRedis(redis_host, redis_port, db=0)
        self.logger = GetLogger()

    def add(self, element):
        try:
            self.client.rpush(self.queue_name, self._to_json(element))
        except ConnectionError as e:
            self.logger.error(
                "Could not add element: {} to Redis queue {} Details: {}".format(element, self.queue_name, e))

    def take(self):
        try:
            json_element = self.client.lpop(self.queue_name)
            return self._from_json(json_element)
        except ConnectionError as e:
            self.logger.error("Could not read from Redis queue {} Details: {}".format(self.queue_name, e))
            return None

    def length(self):
        try:
            return self.client.llen(self.queue_name)
        except ConnectionError as e:
            self.logger.error("Could not check length of Redis queue {} Details: {}".format(self.queue_name, e))
            return 0

    def list(self):
        try:
            queue_length = self.length()
            json_elements = self.client.lrange(self.queue_name, 0, queue_length)
            return map(lambda json_task: self._from_json(json_task), json_elements)
        except ConnectionError as e:
            self.logger.error("Could not list Redis {} queue elements. Details: {}".format(self.queue_name, e))
            return []

    def clear(self):
        try:
            return self.client.delete(self.queue_name)
        except ConnectionError as e:
            self.logger.error("Could not clear Redis {} queue. Details: {}".format(self.queue_name, e))

    def _to_json(self, element):
        if isinstance(element, (int, float, basestring, list, set, dict)):
            return json.dumps(element)
        else:
            return json.dumps(element.__dict__)

    def _from_json(self, json_element):
        return json.loads(json_element) if json_element else None
