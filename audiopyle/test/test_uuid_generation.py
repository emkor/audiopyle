import unittest

from assertpy import assert_that

from audiopyle.commons.services.uuid_generation import generate_uuid


class TestUuidGeneration(unittest.TestCase):
    def test_should_generate_uuid(self):
        actual_uuid_str = generate_uuid("some content")
        actual_uuid_float = generate_uuid(21.37)
        assert_that(actual_uuid_str).is_not_none()
        assert_that(actual_uuid_str).is_not_empty()
        assert_that(actual_uuid_float).is_not_none()
        assert_that(actual_uuid_float).is_not_empty()

    def test_should_generate_same_uuid_for_same_content(self):
        test_content = "some content"
        actual_uuid1 = generate_uuid(test_content)
        actual_uuid2 = generate_uuid(test_content)
        assert_that(actual_uuid1).is_equal_to(actual_uuid2)
