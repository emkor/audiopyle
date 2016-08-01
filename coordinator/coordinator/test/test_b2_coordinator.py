from mock import Mock
import unittest
from assertpy import assert_that

from coordinator.service.b2_coordinator import B2Coordinator


class TestB2Coordinator(unittest.TestCase):
    def setUp(self):
        self.coordinator = B2Coordinator()
        self.coordinator.audio_provider = Mock()
        self.coordinator.audio_provider.get_file_infos.return_value = \
            [{u'contentType': u'audio',
              u'fileName': u'audio-file',
              u'size': 100,
              u'uploadTimestamp': 200},
             {u'contentType': u'some-value',
              u'fileName': u'some-file',
              u'size': 300,
              u'uploadTimestamp': 400}]

    def test_should_filter_audio_file(self):
        files = self.coordinator.get_remote_audio_files()
        assert_that(len(files)).is_equal_to(1)
        assert_that(str(files[0])).contains("audio-file", "100", "200")
