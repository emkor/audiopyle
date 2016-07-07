import json

import redis


class RedisQueueClient(object):
    def __init__(self, queue_name, redis_host="localhost", redis_port=6379):
        self.queue_name = queue_name
        self.client = redis.StrictRedis(redis_host, redis_port, db=0)

    def add(self, element):
        self.client.rpush(self.queue_name, self._to_json(element))

    def take(self):
        json_element = self.client.lpop(self.queue_name)
        return self._from_json(json_element)

    def length(self):
        return self.client.llen(self.queue_name)

    def list(self):
        queue_length = self.length()
        json_elements = self.client.lrange(self.queue_name, 0, queue_length)
        return map(lambda json_task: self._from_json(json_task), json_elements)

    def clear(self):
        return self.client.delete(self.queue_name)

    def _to_json(self, element):
        return json.dumps(element.__dict__)

    def _from_json(self, json_element):
        return json.loads(json_element)
