import unittest
from assertpy import assert_that

from coordinator.model.remote_file_meta import RemoteFileMeta
from coordinator.service.b2_coordinator import B2Coordinator


class B2CoordinatorIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.coordinator = B2Coordinator()

    def test_should_get_remote_audio_file(self):
        files = self.coordinator.get_remote_audio_files()
        assert_that(len(files)).is_equal_to(1)
        assert_that(files[0]).is_instance_of(RemoteFileMeta)
        assert_that(str(files[0])).contains("102bpm_drum_loop_mono_44.1k.wav",
                                            "207916")
