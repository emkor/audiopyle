from unittest import TestCase

import requests
from assertpy import assert_that

from commons.models.audio_tag import Id3Tag
from testcases.utils import get_api_host


class AudioTagApiTest(TestCase):
    def setUp(self):
        self.audio_api_url = "http://{}:8080/audio".format(get_api_host())
        self.mp3_file_name = "102bpm_drum_loop.mp3"

    def test_should_show_audio_tags_of_mp3_file(self):
        expected_status_code = 200
        response = requests.get(url="{}/{}/tag".format(self.audio_api_url, self.mp3_file_name))
        assert_that(response.status_code).is_equal_to(expected_status_code)
        returned_tag = Id3Tag.from_serializable(response.json())
        assert_that(returned_tag.artist).is_equal_to("Unknown Artist")
        assert_that(returned_tag.title).is_equal_to("Unknown Title")
        assert_that(returned_tag.album).is_equal_to("Unknown Album")
        assert_that(returned_tag.date).is_equal_to(2017)
        assert_that(returned_tag.track).is_equal_to(1)
        assert_that(returned_tag.genre).is_equal_to("Unknown Genre")
