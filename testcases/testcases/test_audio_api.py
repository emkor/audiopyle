from unittest import TestCase
from assertpy import assert_that

import requests

from testcases.utils import get_service_host_name


class AudioApiTest(TestCase):
    def setUp(self):
        self.audio_api_url = "http://{}:8080/audio".format(get_service_host_name("coordinator"))

    def test_should_list_audio_file(self):
        expected_status_code = 200
        expected_plugin_count = 1
        expected_audio = "102bpm_drum_loop_mono_44.1k.wav"
        response = requests.get(url=self.audio_api_url)
        assert_that(response.status_code).is_equal_to(expected_status_code)
        actual_response = response.json()
        assert_that(actual_response).is_length(expected_plugin_count)
        assert_that(actual_response).contains(expected_audio)
