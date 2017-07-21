from unittest import TestCase
from assertpy import assert_that

import requests

from testcases.utils import get_service_host_name


class AudioApiTest(TestCase):
    def setUp(self):
        self.audio_api_url = "http://{}:8080/audio".format(get_service_host_name("coordinator"))

    def test_should_list_audio_file(self):
        expected_status_code = 200
        expected_audio_file_count = 1
        expected_audio = [{'created_on': '2017-07-19T17:42:15', 'last_modification': '2017-07-19T17:42:15',
                           'last_access': '2017-07-19T17:42:15', 'file_name': '/audio/102bpm_drum_loop_mono_44.1k.wav',
                           'size': 207916}]
        response = requests.get(url=self.audio_api_url)
        assert_that(response.status_code).is_equal_to(expected_status_code)
        actual_response = response.json()
        assert_that(actual_response).is_length(expected_audio_file_count)
        assert_that(actual_response[0].get("file_name")).is_equal_to(expected_audio[0].get("file_name"))
        assert_that(actual_response[0].get("created_on")).is_not_empty()
        assert_that(actual_response[0].get("last_modification")).is_not_empty()
        assert_that(actual_response[0].get("last_access")).is_not_empty()
