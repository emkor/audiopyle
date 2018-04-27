from unittest import TestCase

from assertpy import assert_that
import requests

from extractor.result_model import TaskStatus
from testcases.utils import get_api_host, keep_polling_until, get_api_port


class CoordinatorApiTest(TestCase):
    def setUp(self):
        self.extraction_api_url = "http://{}:{}/extraction".format(get_api_host(), get_api_port())
        self.result_api_url = "http://{}:{}/extraction/result".format(get_api_host(), get_api_port())
        self.mp3_extraction_request = {
            "audio_file_identifier": "102bpm_drum_loop",
            "plugin_full_key": "vamp-example-plugins:amplitudefollower:amplitude",
            "plugin_config": {}
        }

    def test_should_accept_mp3_task_and_return_extracted_data(self):
        # request extraction
        extraction_request_expected_status_code = 202
        response = requests.post(url=self.extraction_api_url, json=self.mp3_extraction_request)
        assert_that(response.status_code).is_equal_to(extraction_request_expected_status_code)
        extraction_response = response.json()
        assert_that(extraction_response).is_not_none()
        extraction_task_id = extraction_response.get("task_id")

        # wait until extraction completes, verify extraction status
        retrieval_expected_status_code = 200
        status_url = "{}/{}".format(self.extraction_api_url, extraction_task_id)
        status_response = keep_polling_until(url=status_url, expected_status=retrieval_expected_status_code,
                                             timeout=5., tick=0.5)
        json_status_response = status_response.json()
        assert_that(json_status_response["status"]).is_equal_to(TaskStatus.done.value)
        assert_that(json_status_response["task_id"]).is_equal_to(extraction_task_id)

        # retrieve data, meta and stats of an extraction
        result_data_response = requests.get(url="{}/{}/data".format(self.result_api_url, extraction_task_id))
        assert_that(result_data_response.status_code).is_equal_to(retrieval_expected_status_code)
        result_meta_response = requests.get(url="{}/{}/meta".format(self.result_api_url, extraction_task_id))
        assert_that(result_meta_response.status_code).is_equal_to(retrieval_expected_status_code)
        result_stats_response = requests.get(url="{}/{}/stats".format(self.result_api_url, extraction_task_id))
        assert_that(result_stats_response.status_code).is_equal_to(retrieval_expected_status_code)
