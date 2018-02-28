import os
import unittest

from assertpy import assert_that

from commons.services.store_provider import JsonFileStore, GzipJsonFileStore, StoreError, LzmaJsonFileStore
from commons.test.utils import fake_function_from_method


class JsonFileStoreTest(unittest.TestCase):
    def setUp(self):
        self.non_existing_file_name = "0e9a96cb-67bf-579b-ab8d-dec9d37118dd"
        self.test_file_name = "0bf0d777-3486-57c3-98a0-4ac9ebc0944a"
        self.example_content = {"integer_key": 1,
                                "dict_key": {"list_key": [1, 2, 3],
                                             "bool_key": True},
                                "none_key": None,
                                "special_char_key": "źdźbło"}
        self.tmp_base_dir = "/tmp/audiopyle_json_tests"
        self.json_file_store = JsonFileStore(self.tmp_base_dir)
        os.makedirs(self.tmp_base_dir, exist_ok=True)

    def test_should_report_file_does_not_exist(self):
        exists = self.json_file_store.exists(self.non_existing_file_name)
        assert_that(exists).is_false()

    def test_should_create_file_with_correct_permissions_and_report_it_exists_then_remove_it(self):
        exists = self.json_file_store.exists(self.test_file_name)
        assert_that(exists).is_false()

        self.json_file_store.store(self.test_file_name, {})

        exists = self.json_file_store.exists(self.test_file_name)
        assert_that(exists).is_true()

        self.json_file_store.remove(self.test_file_name)

        exists = self.json_file_store.exists(self.test_file_name)
        assert_that(exists).is_false()

    def test_should_raise_exception_on_removal_of_non_existing_file(self):
        assert_that(fake_function_from_method).raises(StoreError).when_called_with(callable=self.json_file_store.remove,
                                                                                   arg=self.non_existing_file_name)

    def test_should_none_on_read_of_non_existing_file(self):
        assert_that(fake_function_from_method).raises(StoreError).when_called_with(callable=self.json_file_store.read,
                                                                                   arg=self.test_file_name)

    def test_created_file_should_be_on_the_list(self):
        file_list = self.json_file_store.list()
        assert_that(file_list).is_empty()

        self.json_file_store.store(self.test_file_name, {})

        assert_that(self.json_file_store.list()).is_length(1).contains_only(self.test_file_name)
        assert_that(self.json_file_store.list_file_names()).is_length(1).contains_only(
            "{}.json".format(self.test_file_name))
        assert_that(self.json_file_store.list_full_paths()).is_length(1).contains_only(
            "/tmp/audiopyle_json_tests/{}.json".format(self.test_file_name))

        self.json_file_store.remove(self.test_file_name)
        file_list = self.json_file_store.list()
        assert_that(file_list).is_empty()

    def test_should_create_file_and_read_it(self):
        self.json_file_store.store(self.test_file_name, self.example_content)
        stored_content = self.json_file_store.read(self.test_file_name)
        assert_that(stored_content).is_equal_to(self.example_content)

        self.json_file_store.remove(self.test_file_name)


class GzippedJsonFileStoreTest(unittest.TestCase):
    def setUp(self):
        self.non_existing_file_name = "0eaedf40-39a4-5df4-8bf3-d3e2d993e55b"
        self.test_file_name = "0f6b5bdc-cf7a-50e8-8aba-9ec762a31a14"
        self.example_content = {"integer_key": 1,
                                "dict_key": {"list_key": [1, 2, 3],
                                             "bool_key": True},
                                "none_key": None,
                                "special_char_key": "źdźbło"}
        self.tmp_base_dir = "/tmp/audiopyle_gzipped_json_tests"
        self.gzip_json_file_store = GzipJsonFileStore(self.tmp_base_dir)
        os.makedirs(self.tmp_base_dir, exist_ok=True)

    def test_should_create_file_and_read_it(self):
        self.gzip_json_file_store.store(self.test_file_name, self.example_content)
        stored_content = self.gzip_json_file_store.read(self.test_file_name)
        assert_that(stored_content).is_equal_to(self.example_content)

        self.gzip_json_file_store.remove(self.test_file_name)


class LzmaJsonFileStoreTest(unittest.TestCase):
    def setUp(self):
        self.non_existing_file_name = "0eaedf40-39a4-5df4-8bf3-d3e2d993e55b"
        self.test_file_name = "0f6b5bdc-cf7a-50e8-8aba-9ec762a31a14"
        self.example_content = {"integer_key": 1,
                                "dict_key": {"list_key": [1, 2, 3],
                                             "bool_key": True},
                                "none_key": None,
                                "special_char_key": "źdźbło"}
        self.tmp_base_dir = "/tmp/audiopyle_gzipped_json_tests"
        self.lzma_json_file_store = LzmaJsonFileStore(self.tmp_base_dir)
        os.makedirs(self.tmp_base_dir, exist_ok=True)

    def test_should_create_file_and_read_it(self):
        self.lzma_json_file_store.store(self.test_file_name, self.example_content)
        stored_content = self.lzma_json_file_store.read(self.test_file_name)
        assert_that(stored_content).is_equal_to(self.example_content)

        self.lzma_json_file_store.remove(self.test_file_name)
