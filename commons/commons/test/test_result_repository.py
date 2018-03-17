import unittest
from unittest.mock import Mock

from assertpy import assert_that

from commons.models.audio_tag import Id3Tag
from commons.models.file_meta import Mp3AudioFileMeta
from commons.models.plugin import VampyPlugin
from commons.models.result import AnalysisResult
from commons.repository.audio_file import AudioFileRepository
from commons.repository.audio_tag import AudioTagRepository
from commons.repository.result import ResultRepository
from commons.repository.vampy_plugin import VampyPluginRepository
from commons.services.plugin_providing import VampyPluginProvider
from commons.test.utils import setup_db_repository_test_class, tear_down_db_repository_test_class


class ResultRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_db_repository_test_class(cls)

    @classmethod
    def tearDownClass(cls):
        tear_down_db_repository_test_class(cls)

    def setUp(self):
        self.task_id = "0f961f20-b036-5740-b526-013523dd88c7"
        self.audio_meta_example_1 = Mp3AudioFileMeta("some_file.mp3", 1024 * 1024 * 2, 1, 44100, 45., 128.)
        self.audio_meta_example_2 = Mp3AudioFileMeta("some_file_2.mp3", 1024 * 1024 * 2, 1, 44100, 45., 128.)
        self.tag_example_1 = Id3Tag(artist="Pink Floyd", title="Have a cigar", album="Wish you were here",
                                    date=1975, track=3, genre="Progressive rock")
        self.tag_example_2 = Id3Tag(artist="Floyd", title="Cigar", album="Wish you were here",
                                    date=1981, track=2, genre="Rock")
        self.plugin_example_1 = VampyPlugin("my_vendor:my_name", ["Cat1"], ["outputs"], "my_file.so")
        self.plugin_example_2 = VampyPlugin("my_vendor:my_name_2", ["Cat2"], ["outputs"], "my_file_2.so")
        self.result = AnalysisResult(task_id=self.task_id, audio_meta=self.audio_meta_example_1,
                                     id3_tag=self.tag_example_1, plugin=self.plugin_example_1)
        self.plugin_provider_mock = Mock(VampyPluginProvider)
        self.plugin_repository = VampyPluginRepository(self.session_provider, self.plugin_provider_mock)
        self.audio_repository = AudioFileRepository(self.session_provider)
        self.audio_tag_repository = AudioTagRepository(self.session_provider)
        self.repository = ResultRepository(self.session_provider, self.audio_repository, self.audio_tag_repository,
                                           self.plugin_repository)

    def tearDown(self):
        self.repository.delete_all()

    def test_should_insert_descendants_of_result_and_then_result_and_list_it(self):
        self.plugin_provider_mock.build_plugin_from_key.return_value = self.plugin_example_1
        self.plugin_repository.insert(self.plugin_example_1)
        self.audio_repository.insert(self.audio_meta_example_1)
        self.audio_tag_repository.insert(self.tag_example_1)

        result_list = self.repository.get_all()
        assert_that(result_list).is_length(0)

        self.repository.insert(self.result)

        result_list = self.repository.get_all()
        assert_that(result_list).is_length(1)
        assert_that(result_list[0]).is_equal_to(self.result)
