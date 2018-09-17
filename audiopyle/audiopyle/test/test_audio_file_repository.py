import unittest

from assertpy import assert_that

from audiopyle.lib.models.file_meta import CompressedAudioFileMeta
from audiopyle.lib.repository.audio_file import AudioFileRepository
from audiopyle.test.utils import setup_db_repository_test_class, tear_down_db_repository_test_class


class AudioFileDbRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_db_repository_test_class(cls)

    @classmethod
    def tearDownClass(cls):
        tear_down_db_repository_test_class(cls)

    def setUp(self):
        self.audio_meta_example_1 = CompressedAudioFileMeta("some_file.mp3", 1024 * 1024 * 2, 1, 44100, 45., 128.)
        self.audio_repository = AudioFileRepository(self.session_provider)

    def tearDown(self):
        self.audio_repository.delete_all()

    def test_should_insert_and_retrieve_entity_by_name(self):
        self.audio_repository.insert(self.audio_meta_example_1)

        identifier = self.audio_repository.get_id_by_file_name(self.audio_meta_example_1.file_name)
        assert_that(identifier).is_greater_than_or_equal_to(0)

        retrieved_object = self.audio_repository.get_by_id(identifier=identifier)
        assert_that(retrieved_object).is_equal_to(self.audio_meta_example_1)
