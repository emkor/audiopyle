import unittest
from sqlite3 import IntegrityError
from unittest.mock import Mock

from assertpy import assert_that

from commons.db.exception import DuplicateEntity, EntityNotFound
from commons.models.plugin import VampyPlugin
from commons.repository.vampy_plugin import VampyPluginRepository
from commons.services.plugin_providing import VampyPluginProvider
from commons.test.utils import setup_db_repository_test_class, tear_down_db_repository_test_class, \
    fake_function_from_method


class VampyPluginDbRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_db_repository_test_class(cls)

    @classmethod
    def tearDownClass(cls):
        tear_down_db_repository_test_class(cls)

    def setUp(self):
        self.plugin_provider_mock = Mock(VampyPluginProvider)
        self.plugin_example_1 = VampyPlugin("my_vendor:my_name", ["Cat1"], ["outputs"], "my_file.so")
        self.plugin_example_2 = VampyPlugin("my_vendor:my_name_2", ["Cat2"], ["outputs"], "my_file_2.so")
        self.plugin_example_3 = VampyPlugin("my_vendor_2:my_name_2", ["Cat3"], ["outputs"], "my_file_2.so")
        self.plugin_repository = VampyPluginRepository(self.session_provider, self.plugin_provider_mock)

    def tearDown(self):
        self.plugin_repository.delete_all()

    def test_repository_should_be_empty_on_start(self):
        all_models = self.plugin_repository.get_all()
        assert_that(all_models).is_empty()

    def test_should_insert_vampy_plugin_and_list_it(self):
        self.plugin_provider_mock.build_plugin_from_key.return_value = self.plugin_example_1
        self.plugin_repository.insert(self.plugin_example_1)
        all_models = self.plugin_repository.get_all()
        assert_that(all_models).is_not_empty().contains_only(self.plugin_example_1)

    def test_should_insert_and_retrieve_vampy_plugin(self):
        self.plugin_repository.insert(self.plugin_example_1)
        retrieved_id = self.plugin_repository.get_id_by_vendor_and_name(vendor=self.plugin_example_1.provider,
                                                                        name=self.plugin_example_1.name)
        assert_that(retrieved_id).is_greater_than_or_equal_to(0)

        self.plugin_provider_mock.build_plugin_from_key.return_value = self.plugin_example_1
        retrieved_object = self.plugin_repository.get_by_id(retrieved_id)
        assert_that(retrieved_object).is_equal_to(self.plugin_example_1)
        self.plugin_provider_mock.build_plugin_from_key.assert_called_with("my_vendor:my_name")

    def test_should_insert_and_delete_vampy_plugin(self):
        self.plugin_repository.insert(self.plugin_example_1)
        retrieved_id = self.plugin_repository.get_id_by_vendor_and_name(vendor=self.plugin_example_1.provider,
                                                                        name=self.plugin_example_1.name)
        assert_that(retrieved_id).is_greater_than_or_equal_to(0)

        self.plugin_repository.delete_by_id(retrieved_id)
        all_models = self.plugin_repository.get_all()
        assert_that(all_models).is_empty()

    def test_should_insert_multiple_and_retrieve_all(self):
        self.plugin_repository.insert(self.plugin_example_1)
        self.plugin_repository.insert(self.plugin_example_2)

        self.plugin_provider_mock.build_plugin_from_key.return_value = self.plugin_example_1
        all_models = self.plugin_repository.get_all()
        assert_that(all_models).is_length(2)

    def test_should_insert_multiple_and_retrieve_one_by_one(self):
        self.plugin_repository.insert(self.plugin_example_1)
        self.plugin_repository.insert(self.plugin_example_2)

        retrieved_id_1 = self.plugin_repository.get_id_by_vendor_and_name(vendor=self.plugin_example_1.provider,
                                                                          name=self.plugin_example_1.name)
        assert_that(retrieved_id_1).is_greater_than_or_equal_to(0)

        retrieved_id_2 = self.plugin_repository.get_id_by_vendor_and_name(vendor=self.plugin_example_2.provider,
                                                                          name=self.plugin_example_2.name)
        assert_that(retrieved_id_2).is_greater_than_or_equal_to(0)
        assert_that(retrieved_id_2).is_not_equal_to(retrieved_id_1)

    def test_should_query_multiple_by_vendor(self):
        self.plugin_repository.insert(self.plugin_example_1)
        self.plugin_repository.insert(self.plugin_example_2)

        self.plugin_provider_mock.build_plugin_from_key.return_value = self.plugin_example_1
        filtered_by_vendor = self.plugin_repository.filter_by_vendor(vendor=self.plugin_example_1.provider)
        assert_that(filtered_by_vendor).is_length(2)

    def test_should_insert_multiple_and_filter_one_of_them(self):
        self.plugin_repository.insert(self.plugin_example_1)
        self.plugin_repository.insert(self.plugin_example_2)
        self.plugin_repository.insert(self.plugin_example_3)

        self.plugin_provider_mock.build_plugin_from_key.return_value = self.plugin_example_3
        filtered_by_vendor = self.plugin_repository.filter_by_vendor(vendor=self.plugin_example_3.provider)
        assert_that(filtered_by_vendor).is_length(1).contains(self.plugin_example_3)

    def test_should_raise_on_duplicate_insert(self):
        self.plugin_repository.insert(self.plugin_example_1)
        assert_that(fake_function_from_method).raises(DuplicateEntity).when_called_with(self.plugin_repository.insert,
                                                                                        self.plugin_example_1)

    def test_should_raise_when_querying_by_absent_identifier(self):
        non_existing_identifier = 112233
        assert_that(fake_function_from_method).raises(EntityNotFound).when_called_with(
            self.plugin_repository.get_by_id, non_existing_identifier)

    def test_should_raise_when_querying_by_absent_model(self):
        assert_that(fake_function_from_method).raises(EntityNotFound).when_called_with(
            self.plugin_repository.get_id_by_vendor_and_name, "non_existing_vendor", "non_existing_name")

    def test_should_raise_when_deleting_by_absent_identifier(self):
        non_existing_identifier = 112233
        assert_that(fake_function_from_method).raises(EntityNotFound).when_called_with(
            self.plugin_repository.delete_by_id, non_existing_identifier)
