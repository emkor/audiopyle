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
            "plugin_config": {
                "block_size": 4096,
                "step_size": 4096
            },
            "metric_config": {"my_metric": {
                "transformation": {
                    "name": "none"
                }
            }}
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

        # retrieve and assert request params
        result_request_response = requests.get(url="{}/{}".format(self.result_api_url, extraction_task_id))
        assert_that(result_request_response.status_code).is_equal_to(retrieval_expected_status_code)
        result_request_response_json = result_request_response.json()
        assert_that(result_request_response_json["audio_meta"]).is_equal_to({
            "bit_rate_kbps": 128.0,
            "channels_count": 1,
            "file_name": "102bpm_drum_loop.mp3",
            "file_size_bytes": 39044,
            "length_sec": 2.403,
            "sample_rate": 44100
        })
        assert_that(result_request_response_json["id3_tag"]).is_equal_to({
            "album": "Unknown Album",
            "artist": "Unknown Artist",
            "date": 2017,
            "genre": "Unknown Genre",
            "title": "Unknown Title",
            "track": 1
        })
        assert_that(result_request_response_json["plugin"]).is_equal_to({
            "library_file_name": "vamp-example-plugins.so",
            "name": "amplitudefollower",
            "output": "amplitude",
            "vendor": "vamp-example-plugins"
        })
        assert_that(result_request_response_json["plugin_config"]["block_size"]).is_equal_to(4096)
        assert_that(result_request_response_json["plugin_config"]["step_size"]).is_equal_to(4096)
        assert_that(result_request_response_json["task_id"]).is_not_empty()

        # retrieve data, meta and stats of an extraction
        result_data_response = requests.get(url="{}/{}/data".format(self.result_api_url, extraction_task_id))
        assert_that(result_data_response.status_code).is_equal_to(retrieval_expected_status_code)
        result_data_response_json = result_data_response.json()
        assert_that(result_data_response_json["matrix"]).is_length(26)
        assert_that(result_data_response_json["time_step"]).is_between(0.092, 0.093)
        assert_that(result_data_response_json["task_id"]).is_not_empty()

        result_meta_response = requests.get(url="{}/{}/meta".format(self.result_api_url, extraction_task_id))
        assert_that(result_meta_response.status_code).is_equal_to(retrieval_expected_status_code)
        result_meta_response_json = result_meta_response.json()
        assert_that(result_meta_response_json["data_shape"]).is_equal_to([26, 1, 0])
        assert_that(result_meta_response_json["feature_type"]).is_equal_to("constant_step")

        result_stats_response = requests.get(url="{}/{}/stats".format(self.result_api_url, extraction_task_id))
        assert_that(result_stats_response.status_code).is_equal_to(retrieval_expected_status_code)
        result_stats_response_json = result_stats_response.json()
        assert_that(result_stats_response_json["total_time"]).is_between(0.01, 1.5)
        assert_that(result_stats_response_json["task_id"]).is_not_empty()
