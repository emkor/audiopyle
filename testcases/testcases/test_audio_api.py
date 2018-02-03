from unittest import TestCase
from assertpy import assert_that

import requests

from testcases.utils import get_service_host_name


class AudioApiTest(TestCase):
    def setUp(self):
        self.audio_api_url = "http://{}:8080/audio".format(get_service_host_name("coordinator"))

    def test_should_list_audio_file(self):
        expected_status_code = 200
        expected_audio_file_count = 2
        response = requests.get(url=self.audio_api_url)
        assert_that(response.status_code).is_equal_to(expected_status_code)
        actual_response = response.json()
        assert_that(actual_response).is_length(expected_audio_file_count)
        assert_that(actual_response[0].get("file_name")).is_not_none()
        assert_that(actual_response[0].get("created_on")).is_not_none()
        assert_that(actual_response[0].get("last_modification")).is_not_none()
        assert_that(actual_response[0].get("last_access")).is_not_none()


class AudioMetaApiTest(TestCase):
    def setUp(self):
        self.audio_api_url = "http://{}:8080/audio/meta".format(get_service_host_name("coordinator"))
        self.file_name = "102bpm_drum_loop_mono_44.1k.mp3"

    def test_should_return_correct_mp3_meta(self):
        expected_status_code = 200
        response = requests.get(url="{}?file={}".format(self.audio_api_url, self.file_name))
        assert_that(response.status_code).is_equal_to(expected_status_code)
        actual_response = response.json()
        assert_that(actual_response).is_not_empty()
        assert_that(actual_response.get("channels_count")).is_equal_to(1)
        assert_that(actual_response.get("sample_rate")).is_equal_to(44100)
        assert_that(actual_response.get("file_size_bytes")).is_equal_to(39044)
        assert_that(actual_response.get("length_sec")).is_between(2.4, 2.5)
        assert_that(actual_response.get("bit_rate_kbps")).is_between(127, 129)
