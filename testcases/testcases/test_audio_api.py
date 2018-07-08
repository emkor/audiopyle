from unittest import TestCase
from assertpy import assert_that

import requests

from testcases.utils import get_api_host, get_api_port


class AudioApiTest(TestCase):
    def setUp(self):
        self.audio_api_url = "http://{}:{}/audio".format(get_api_host(), get_api_port())
        self.audio_file = "102bpm_drum_loop.mp3"

    def test_should_list_audio_file(self):
        expected_status_code = 200
        expected_audio_file_count = 1
        response = requests.get(url=self.audio_api_url)
        assert_that(response.status_code).is_equal_to(expected_status_code)
        actual_response = response.json()
        assert_that(actual_response).is_length(expected_audio_file_count)
        assert_that(actual_response[0]).is_equal_to(self.audio_file)

    def test_should_list_file_details(self):
        expected_status_code = 200
        response = requests.get(url="{}/{}".format(self.audio_api_url, self.audio_file))
        assert_that(response.status_code).is_equal_to(expected_status_code)

        actual_response = response.json()
        assert_that(actual_response["file_name"]).is_equal_to("{}.{}".format(self.audio_file, "mp3"))
        assert_that(actual_response["size"]).is_equal_to(39044)
        assert_that(actual_response["created_on"]).is_not_none()
        assert_that(actual_response["last_access"]).is_not_none()
        assert_that(actual_response["last_modification"]).is_not_none()
