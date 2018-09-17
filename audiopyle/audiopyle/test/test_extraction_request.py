import unittest
import json
import time

from assertpy import assert_that

from audiopyle.lib.models.extraction_request import ExtractionRequest


class ExtractionRequestModelTest(unittest.TestCase):
    def setUp(self):
        self.extraction_request_1 = ExtractionRequest("some_file_1.mp3", "some_vendor:some_plugin:some_output", {}, {})
        self.extraction_request_2 = ExtractionRequest("some_file_2.mp3", "some_vendor:some_plugin:some_output",
                                                      {"block_size": 1024}, {})
        self.extraction_request_3 = ExtractionRequest("some_file_1.mp3", "some_vendor:some_plugin2:some_output",
                                                      {"step_size": 2048}, {})
        self.extraction_request_4 = ExtractionRequest("some_file_1.mp3", "some_vendor:some_plugin:some_output2",
                                                      {"step_size": 2048, "block_size": 4096}, {"metric_1": {
                "transformation": {
                    "name": "select_row",
                    "args": [
                        5
                    ],
                    "kwargs": {}
                }}})

    def test_should_serialize_and_deserialize_model(self):
        serializable_form = self.extraction_request_1.to_serializable()
        actual_object = ExtractionRequest.from_serializable(serializable_form)
        assert_that(actual_object).is_not_none().is_equal_to(self.extraction_request_1)

    def test_should_serialize_to_json_and_back(self):
        json_form = json.dumps(self.extraction_request_2.to_serializable())
        assert_that(json_form).is_not_none().is_type_of(str)

        actual_object = ExtractionRequest.from_serializable(json.loads(json_form))
        assert_that(actual_object).is_equal_to(self.extraction_request_2)

    def test_same_request_should_generate_same_uuid(self):
        uuid_1 = self.extraction_request_1.uuid
        time.sleep(0.001)  # make sure time does not take part in uuid computation
        uuid_2 = self.extraction_request_1.uuid
        assert_that(uuid_1).is_not_none().is_not_empty().is_equal_to(uuid_2)

    def test_different_requests_should_generate_different_uuids(self):
        uuid_1, uuid_2 = self.extraction_request_1.uuid, self.extraction_request_2.uuid
        uuid_3, uuid_4 = self.extraction_request_3.uuid, self.extraction_request_4.uuid
        assert_that(uuid_1).is_not_none().is_not_equal_to(uuid_2).is_not_equal_to(uuid_3).is_not_equal_to(uuid_4)
        assert_that(uuid_2).is_not_equal_to(uuid_3).is_not_equal_to(uuid_4)
        assert_that(uuid_3).is_not_equal_to(uuid_4)
