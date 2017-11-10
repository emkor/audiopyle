import unittest

from assertpy import assert_that
from datetime import datetime

from commons.audio.file_meta_providing import get_file_meta


class FileMetaGatheringTest(unittest.TestCase):
    def setUp(self):
        self.test_file = "/dev/null"

    def test_file_meta_reading(self):
        test_file_meta = get_file_meta(self.test_file)
        assert_that(test_file_meta).is_not_none()
        assert_that(test_file_meta.size).is_equal_to(0)
        assert_that(test_file_meta.file_base_name).is_equal_to("null")
        assert_that(test_file_meta.extension).is_equal_to("")
        assert_that(test_file_meta.created_on).is_instance_of(datetime)
        assert_that(test_file_meta.last_access).is_instance_of(datetime)
        assert_that(test_file_meta.last_modification).is_instance_of(datetime)
        assert_that(test_file_meta.size_kB).is_equal_to(0)
        assert_that(test_file_meta.size_mB).is_equal_to(0)
        assert_that(test_file_meta.file_name).is_equal_to(self.test_file)
