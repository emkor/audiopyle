from mock import Mock
import unittest
from assertpy import assert_that

from coordinator.service.b2_coordinator import B2Coordinator


class TestB2Coordinator(unittest.TestCase):
    def setUp(self):
        coordinator = B2Coordinator()
        coordinator.audio_provider = Mock()
        coordinator.audio_provider.get_file_infos.return_value = \
            [{u'contentType': u'audio',
              u'fileName': u'audio-file',
              u'size': 100,
              u'uploadTimestamp': 200},
             {u'contentType': u'some-value',
              u'fileName': u'some-file',
              u'size': 300,
              u'uploadTimestamp': 400}]
        self.files = coordinator.get_remote_audio_files()

    def test_should_filter_audio_file(self):
        file_string = "RemoteFileMeta: file name: "\
            "audio-file, file size: 100, upload timestamp: 200."
        assert_that(str(self.files[0])).is_equal_to(file_string)
