import unittest

from assertpy import assert_that

from audiopyle.commons.models.audio_tag import Id3Tag
from audiopyle.commons.repository.audio_tag import AudioTagRepository
from audiopyle.test.utils import setup_db_repository_test_class, tear_down_db_repository_test_class


class AudioTagDbRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_db_repository_test_class(cls)

    @classmethod
    def tearDownClass(cls):
        tear_down_db_repository_test_class(cls)

    def setUp(self):
        self.tag_example_1 = Id3Tag(artist="Pink Floyd", title="Have a cigar", album="Wish you were here",
                                    date=1975, track=3, genre="Progressive rock")
        self.tag_example_2 = Id3Tag(artist="Floyd", title="Cigar", album="Wish you were here",
                                    date=1981, track=2, genre="Rock")
        self.tag_example_3 = Id3Tag(artist="Pink Floyd", title="Cigar", album="Some Other Album",
                                    date=1975, track=3, genre="Progressive rock")
        self.plugin_repository = AudioTagRepository(self.session_provider)

    def tearDown(self):
        self.plugin_repository.delete_all()

    def test_should_insert_and_retrieve_tag(self):
        self.plugin_repository.insert(self.tag_example_1)
        identifier = self.plugin_repository.get_id_by_name(self.tag_example_1.artist, self.tag_example_1.album,
                                                           self.tag_example_1.title)
        retrieved = self.plugin_repository.get_by_id(identifier)
        assert_that(retrieved).is_equal_to(self.tag_example_1)

    def test_should_get_id_by_name(self):
        self.plugin_repository.insert(self.tag_example_1)
        identifier = self.plugin_repository.get_id_by_name(self.tag_example_1.artist, self.tag_example_1.album,
                                                           self.tag_example_1.title)
        assert_that(identifier).is_greater_than_or_equal_to(0)

    def test_should_query_multiple_by_param_and_return_none(self):
        self.plugin_repository.insert(self.tag_example_1)
        self.plugin_repository.insert(self.tag_example_2)
        self.plugin_repository.insert(self.tag_example_3)

        tag_list = self.plugin_repository.filter_by_artist(artist_name="non existing artist")
        assert_that(tag_list).is_length(0)

    def test_should_query_multiple_by_param(self):
        self.plugin_repository.insert(self.tag_example_1)
        self.plugin_repository.insert(self.tag_example_2)
        self.plugin_repository.insert(self.tag_example_3)

        tag_list = self.plugin_repository.filter_by_artist(artist_name=self.tag_example_1.artist)
        assert_that(tag_list).is_length(2).contains(self.tag_example_1, self.tag_example_3).does_not_contain(
            self.tag_example_2)

        tag_list = self.plugin_repository.filter_by_album(self.tag_example_2.album)
        assert_that(tag_list).is_length(2).contains(self.tag_example_2, self.tag_example_1).does_not_contain(
            self.tag_example_3)

        tag_list = self.plugin_repository.filter_by_title(self.tag_example_1.title)
        assert_that(tag_list).is_length(1).contains(self.tag_example_1).does_not_contain(self.tag_example_2,
                                                                                         self.tag_example_3)

        tag_list = self.plugin_repository.filter_by_genre(self.tag_example_2.genre)
        assert_that(tag_list).is_length(1).contains(self.tag_example_2).does_not_contain(self.tag_example_1,
                                                                                         self.tag_example_3)
