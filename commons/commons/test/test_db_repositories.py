import unittest
from unittest.mock import Mock

import os
from assertpy import assert_that

from commons.db.engine import get_test_db_engine, create_db_tables
from commons.db.session import SessionProvider
from commons.models.plugin import VampyPlugin
from commons.repository.vampy_plugin import VampyPluginRepository
from commons.services.plugin_providing import VampyPluginProvider
from commons.utils.file_system import remove_file


class VampyPluginDbRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_file_name = "{}_sqlite.db".format(cls.__name__)
        remove_file(cls.db_file_name, omit_errors=True)
        cls.engine = get_test_db_engine(cls.db_file_name, debug=True)
        create_db_tables(engine=cls.engine, check_first=False)
        cls.session_provider = SessionProvider(db_engine=cls.engine)

    @classmethod
    def tearDownClass(cls):
        remove_file(cls.db_file_name, omit_errors=True)

    def setUp(self):
        self.plugin_provider_mock = Mock(VampyPluginProvider)
        self.plugin_object = VampyPlugin("my_vendor:my_name", ["Cat1"], ["outputs"], "my_file.so")
        self.plugin_repository = VampyPluginRepository(self.session_provider, self.plugin_provider_mock)

    def tearDown(self):
        self.plugin_repository.delete_all()

    def test_repository_should_be_empty_on_start(self):
        all_models = self.plugin_repository.get_all()
        assert_that(all_models).is_empty()

    def test_should_insert_vampy_plugin_and_list_it(self):
        self.plugin_provider_mock.build_plugin_from_key.return_value = self.plugin_object
        self.plugin_repository.insert(self.plugin_object)
        all_models = self.plugin_repository.get_all()
        assert_that(all_models).is_not_empty().contains_only(self.plugin_object)
