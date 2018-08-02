import unittest

import json
from assertpy import assert_that
from datetime import datetime

from audiopyle.lib.models.file_meta import FileMeta


class FileMetaModelTest(unittest.TestCase):
    def setUp(self):
        self.created_on = datetime(year=2018, month=2, day=28, hour=13, minute=34, second=15)
        self.last_modification = datetime(year=2018, month=2, day=28, hour=14, minute=34, second=15)
        self.last_access_time = datetime(year=2018, month=2, day=28, hour=14, minute=35, second=29)
        self.file_meta = FileMeta("some_file.txt", 8192,
                                  last_access=self.last_access_time,
                                  last_modification=self.last_access_time,
                                  created_on=self.last_access_time)

    def test_should_turn_into_serializable_form_and_back(self):
        serializable_form = self.file_meta.to_serializable()
        assert_that(serializable_form).is_not_none()
        assert_that(serializable_form.get("created_on")).is_equal_to("2018-02-28 14:35:29")

        deserialized_form = FileMeta.from_serializable(serializable_form)
        assert_that(deserialized_form).is_equal_to(self.file_meta)

    def test_should_serialize_to_json_and_back(self):
        json_form = json.dumps(self.file_meta.to_serializable())
        assert_that(json_form).is_not_none().is_type_of(str)

        deserialized_form = FileMeta.from_serializable(json.loads(json_form))
        assert_that(deserialized_form).is_equal_to(self.file_meta)
