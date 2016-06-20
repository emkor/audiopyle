import unittest
from assertpy import assert_that

from commons.service.os_env_accessor import OsEnvAccessor


class OsEnvironmentAccessorTest(unittest.TestCase):
    def test_should_get_path_variable(self):
        path_variable_content = OsEnvAccessor.get_env_variable("PATH")
        assert_that(path_variable_content).is_not_none().is_not_empty()

    def test_should_get_alternative_value(self):
        alternative_value = "some_alternative"
        path_variable_content = OsEnvAccessor.get_env_variable_or("fvjeasrio54t", alternative_value)
        assert_that(path_variable_content).is_not_none().is_not_empty().is_equal_to(alternative_value)
