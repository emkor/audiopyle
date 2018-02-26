import os
import unittest

from assertpy import assert_that

from commons.services.store_provider import JsonFileStore


class JsonFileStoreTest(unittest.TestCase):
    def setUp(self):
        self.non_existing_file_name = "0e9a96cb-67bf-579b-ab8d-dec9d37118dd"
        self.test_file_name = "0bf0d777-3486-57c3-98a0-4ac9ebc0944a"
        self.example_content = {"integer_key": 1,
                                "dict_key": {"list_key": [1, 2, 3],
                                             "bool_key": True},
                                "none_key": None,
                                "special_char_key": "źdźbło"}
        self.tmp_base_dir = "/tmp/audiopyle_tests"
        self.json_file_store = JsonFileStore(self.tmp_base_dir)
        os.makedirs(self.tmp_base_dir, exist_ok=True)

    def test_should_report_file_does_not_exist(self):
        exists = self.json_file_store.exists(self.non_existing_file_name)
        assert_that(exists).is_false()

    def test_should_create_file_and_report_it_exists_then_remove_it(self):
        exists = self.json_file_store.exists(self.test_file_name)
        assert_that(exists).is_false()

        self.json_file_store.store(self.test_file_name, {})

        exists = self.json_file_store.exists(self.test_file_name)
        assert_that(exists).is_true()

        removal_success = self.json_file_store.remove(self.test_file_name)
        assert_that(removal_success).is_true()

        exists = self.json_file_store.exists(self.test_file_name)
        assert_that(exists).is_false()

    def test_should_return_false_on_removal_of_non_existing_file(self):
        removal_failure = self.json_file_store.remove(self.non_existing_file_name)
        assert_that(removal_failure).is_false()

    def test_should_none_on_read_of_non_existing_file(self):
        stored_content = self.json_file_store.read(self.test_file_name)
        assert_that(stored_content).is_none()

    def test_should_create_file_and_make_sure_it_is_on_the_list(self):
        file_list = self.json_file_store.list()
        assert_that(file_list).is_empty()

        self.json_file_store.store(self.test_file_name, {})

        file_list = self.json_file_store.list()
        assert_that(file_list).is_length(1).contains_only(self.test_file_name)

        self.json_file_store.remove(self.test_file_name)
        file_list = self.json_file_store.list()
        assert_that(file_list).is_empty()

    def test_should_create_file_and_read_it(self):
        self.json_file_store.store(self.test_file_name, self.example_content)
        stored_content = self.json_file_store.read(self.test_file_name)
        assert_that(stored_content).is_equal_to(self.example_content)

        self.json_file_store.remove(self.test_file_name)
