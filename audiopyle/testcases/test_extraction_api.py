from typing import Any, Dict, Tuple
from unittest import TestCase

from assertpy import assert_that
import requests

from audiopyle.lib.abstractions.api_model import HttpStatusCode
from audiopyle.worker.result_model import TaskStatus
from audiopyle.testcases.utils import get_api_host, keep_polling_until, get_api_port


class CoordinatorApiTest(TestCase):
    def setUp(self):
        self.request_api_url = "http://{}:{}/request".format(get_api_host(), get_api_port())
        self.metric_def_api_url = "http://{}:{}/metric/def".format(get_api_host(), get_api_port())
        self.metric_val_api_url = "http://{}:{}/metric/val".format(get_api_host(), get_api_port())
        self.mp3_extraction_request = {
            "audio_file_name": "102bpm_drum_loop.mp3",
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
        self.flac_extraction_request = {
            "audio_file_name": "102bpm_drum_loop.flac",
            "plugin_full_key": "vamp-example-plugins:amplitudefollower:amplitude",
            "plugin_config": {
                "block_size": 8192,
                "step_size": 8192
            },
            "metric_config": {"my_metric": {
                "transformation": {
                    "name": "none"
                }
            }}
        }

    def test_should_accept_mp3_task_and_return_extracted_data(self):
        # request extraction
        extraction_task_id = self._request_extraction_and_verify(self.request_api_url,
                                                                 self.mp3_extraction_request,
                                                                 HttpStatusCode.accepted.value)

        # wait until extraction completes, verify extraction status
        self._wait_for_extraction_to_complete_and_verify(extraction_task_id, HttpStatusCode.ok.value, 5., 0.5,
                                                         self.request_api_url)

        # retrieve and assert request params
        mp3_audio_meta = {"bit_rate_kbps": 128.0, "channels_count": 1, "file_name": "102bpm_drum_loop.mp3",
                          "file_size_bytes": 39044, "length_sec": 2.403, "sample_rate": 44100}
        audio_tag = {"album": "Unknown Album", "artist": "Unknown Artist", "date": 2017, "genre": "Unknown Genre",
                     "title": "Unknown Title", "track": 1}
        plugin_meta = {"library_file_name": "vamp-example-plugins.so", "name": "amplitudefollower",
                       "output": "amplitude",
                       "vendor": "vamp-example-plugins"}
        self._retrieve_and_verify_request_details(extraction_task_id, self.request_api_url, HttpStatusCode.ok.value,
                                                  mp3_audio_meta, audio_tag, plugin_meta, 4096, 4096)

        # retrieve data, meta and stats of an extraction
        self._retrieve_and_verify_analysis_data(extraction_task_id, self.request_api_url,
                                                HttpStatusCode.ok.value, 26, (0.092, 0.093))

        result_meta_response = requests.get(url="{}/{}/meta".format(self.request_api_url, extraction_task_id))
        assert_that(result_meta_response.status_code).is_equal_to(HttpStatusCode.ok.value)
        result_meta_response_json = result_meta_response.json()
        assert_that(result_meta_response_json["data_shape"]).is_equal_to([26, 1, 0])
        assert_that(result_meta_response_json["feature_type"]).is_equal_to("constant_step")

        result_stats_response = requests.get(url="{}/{}/stats".format(self.request_api_url, extraction_task_id))
        assert_that(result_stats_response.status_code).is_equal_to(HttpStatusCode.ok.value)
        result_stats_response_json = result_stats_response.json()
        assert_that(result_stats_response_json["total_time"]).is_between(0.01, 1.5)
        assert_that(result_stats_response_json["task_id"]).is_not_empty()

        # retrieve metrics from raw feature data
        metric_definitions_response = requests.get(url=self.metric_def_api_url)
        assert_that(metric_definitions_response.status_code).is_equal_to(HttpStatusCode.ok.value)
        metric_definitions_json = metric_definitions_response.json()
        assert_that(metric_definitions_json).is_not_empty()

        metric_values_response = requests.get(url=self.metric_val_api_url)
        assert_that(metric_values_response.status_code).is_equal_to(HttpStatusCode.ok.value)
        metric_definitions_json = metric_values_response.json()
        assert_that(metric_definitions_json).is_not_empty()

    def test_should_accept_flac_task_and_return_extracted_data(self):
        # request extraction
        extraction_task_id = self._request_extraction_and_verify(self.request_api_url,
                                                                 self.flac_extraction_request,
                                                                 HttpStatusCode.accepted.value)

        # wait until extraction completes, verify extraction status
        self._wait_for_extraction_to_complete_and_verify(extraction_task_id, HttpStatusCode.ok.value, 5., 0.5,
                                                         self.request_api_url)

        # retrieve and assert request params
        expected_flac_audio_meta = {"bit_rate_kbps": 371.7, "channels_count": 1, "file_name": "102bpm_drum_loop.flac",
                                    "file_size_bytes": 111690, "length_sec": 2.378, "sample_rate": 44100}
        expected_audio_tag = {"album": "Unknown Album", "artist": "Unknown Artist", "date": 2017,
                              "genre": "Unknown Genre",
                              "title": "Unknown Title", "track": 1}
        expected_plugin_meta = {"library_file_name": "vamp-example-plugins.so", "name": "amplitudefollower",
                                "output": "amplitude",
                                "vendor": "vamp-example-plugins"}
        self._retrieve_and_verify_request_details(extraction_task_id, self.request_api_url, HttpStatusCode.ok.value,
                                                  expected_flac_audio_meta, expected_audio_tag, expected_plugin_meta,
                                                  expected_plugin_block_size=8192, expected_plugin_step_size=8192)

        # retrieve data, meta and stats of an extraction
        self._retrieve_and_verify_analysis_data(extraction_task_id, self.request_api_url,
                                                HttpStatusCode.ok.value, 13, (0.185, 0.186))

    def _retrieve_and_verify_analysis_data(self, extraction_task_id: str, request_api_url: str,
                                           expected_status_code: int, expected_result_len: int,
                                           expected_time_step_range: Tuple[float, float]):
        result_data_response = requests.get(url="{}/{}/data".format(request_api_url, extraction_task_id))
        assert_that(result_data_response.status_code).is_equal_to(expected_status_code)
        result_data_response_json = result_data_response.json()
        assert_that(result_data_response_json["matrix"]).is_length(expected_result_len)
        assert_that(result_data_response_json["time_step"]).is_between(*expected_time_step_range)
        assert_that(result_data_response_json["task_id"]).is_not_empty()

    def _request_extraction_and_verify(self, api_url: str, request: Dict[str, Any], expected_status_code: int) -> str:
        response = requests.post(url=api_url, json=request)
        assert_that(response.status_code).is_equal_to(expected_status_code)
        extraction_response = response.json()
        assert_that(extraction_response).is_not_none()
        extraction_task_id = extraction_response.get("task_id")
        return extraction_task_id

    def _wait_for_extraction_to_complete_and_verify(self, extraction_task_id, expected_status_code: int, timeout: float,
                                                    tick: float, api_url: str):
        status_response = keep_polling_until(url="{}/{}/status".format(api_url, extraction_task_id),
                                             expected_status=expected_status_code,
                                             timeout=timeout, tick=tick)
        json_status_response = status_response.json()
        assert_that(json_status_response["status"]).is_equal_to(TaskStatus.done.value)
        assert_that(json_status_response["task_id"]).is_equal_to(extraction_task_id)


    def _retrieve_and_verify_request_details(self, extraction_task_id: str,
                                             result_api_url: str, status_code: int,
                                             expected_audio_meta: Dict[str, Any],
                                             expected_audio_tag: Dict[str, Any],
                                             expected_plugin_meta: Dict[str, Any],
                                             expected_plugin_block_size: int,
                                             expected_plugin_step_size: int):
        request_response = requests.get(url="{}/{}".format(result_api_url, extraction_task_id))
        assert_that(request_response.status_code).is_equal_to(status_code)
        result_request_response_json = request_response.json()
        assert_that(result_request_response_json["audio_meta"]).is_equal_to(expected_audio_meta)
        assert_that(result_request_response_json["id3_tag"]).is_equal_to(expected_audio_tag)
        assert_that(result_request_response_json["plugin"]).is_equal_to(expected_plugin_meta)
        assert_that(result_request_response_json["plugin_config"]["block_size"]).is_equal_to(expected_plugin_block_size)
        assert_that(result_request_response_json["plugin_config"]["step_size"]).is_equal_to(expected_plugin_step_size)
        assert_that(result_request_response_json["task_id"]).is_not_empty()
