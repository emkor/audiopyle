import unittest
from assertpy import assert_that

from coordinator.model.remote_file_meta import RemoteFileMeta
from coordinator.service.b2_coordinator import B2Coordinator


class B2CoordinatorIntegrationTest(unittest.TestCase):
    def setUp(self):
        coordinator = B2Coordinator()
        self.files = coordinator.get_remote_audio_files()

    def test_should_get_remote_audio_file(self):
        assert_that(self.files[0]).is_instance_of(RemoteFileMeta)
        file_string = "RemoteFileMeta: file name: "\
            "test/102bpm_drum_loop_mono_44.1k.wav, "\
            "file size: 207916, upload timestamp: 1467569056000."
        assert_that(str(self.files[0])).is_equal_to(file_string)
