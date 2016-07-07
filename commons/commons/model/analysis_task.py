import json
from datetime import datetime

from commons.utils.conversion import utc_datetime_to_timestamp, utc_timestamp_to_datetime


class AnalysisTask(object):
    def __init__(self, analyzed_file_name, task_created=None):
        self.task_created = task_created or utc_datetime_to_timestamp(datetime.utcnow())
        self.file_name = analyzed_file_name

    def __str__(self):
        return "AnalysisTask file: {} created at: {}".format(self.file_name,
                                                             utc_timestamp_to_datetime(self.task_created))

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_task):
        task_dict = json.loads(json_task)
        return AnalysisTask(**task_dict)
