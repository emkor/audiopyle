import unittest

from assertpy import assert_that

from commons.model.analysis_task import AnalysisTask
from commons.model.remote_file_meta import RemoteFileMeta
from commons.model.remote_file_source import RemoteFileSource


class TestAnalysistaskObject(unittest.TestCase):
    def setUp(self):
        self.remote_file_meta = RemoteFileMeta("/somedir/somefile.wav", 1024, 0)
        self.remote_file_source = RemoteFileSource("b2", "some_key", "some_bucket_name", "pass")
        self.task = AnalysisTask(self.remote_file_meta, self.remote_file_source)

    def test_casting_to_dict_and_back(self):
        task_dict = self.task.to_dict()
        assert_that(task_dict).is_not_empty()

        task = AnalysisTask.from_dict(task_dict)
        self.assertEqual(task.remote_file_meta, self.task.remote_file_meta)
        self.assertEqual(task.remote_file_source, self.task.remote_file_source)
        self.assertEqual(task, self.task)
