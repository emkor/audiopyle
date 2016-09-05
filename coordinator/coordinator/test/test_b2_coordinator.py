from commons.provider.redis_queue_client import RedisQueueClient
from mock import Mock
import unittest
from assertpy import assert_that

from commons.model.remote_file_meta import RemoteFileMeta
from commons.provider.b2_audio_provider import B2AudioProvider
from coordinator.service.b2_coordinator import B2Coordinator


class TestB2Coordinator(unittest.TestCase):
    def setUp(self):
        self.audio_provider = Mock(B2AudioProvider)
        self.redis_queue_client = Mock(RedisQueueClient)

    def test_should_filter_audio_file(self):
        self.audio_provider.get_raw_file_infos.return_value = \
            [{u'contentType': u'audio',
              u'fileName': u'audio-file',
              u'size': 100,
              u'uploadTimestamp': 200},
             {u'contentType': u'some-value',
              u'fileName': u'some-file',
              u'size': 300,
              u'uploadTimestamp': 400}]

        coordinator = B2Coordinator(self.audio_provider)

        files = coordinator.get_remote_audio_files()
        assert_that(len(files)).is_equal_to(1)
        assert_that(str(files[0])).contains("audio-file", "100", "200")

    def test_should_push_list_to_redis(self):
        dicts = \
            [{u'contentType': u'audio',
              u'fileName': u'first-file',
              u'size': 100,
              u'uploadTimestamp': 200},
             {u'contentType': u'audio',
              u'fileName': u'second-file',
              u'size': 300,
              u'uploadTimestamp': 400}]

        files = [RemoteFileMeta.from_dict(dict) for dict in dicts]
        self.redis_queue_client.queue_name = "some_name"
        coordinator = B2Coordinator(self.audio_provider, self.redis_queue_client)
        coordinator.push_file_list_to_redis(files, 0)

        assert_that(self.redis_queue_client.add.called).is_true()
