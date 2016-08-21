from datetime import datetime

from commons.utils.conversion import utc_datetime_to_timestamp
from commons.model.remote_file_meta import RemoteFileMeta
from commons.model.remote_file_source import RemoteFileSource


class AnalysisTask(object):
    @staticmethod
    def from_dict(analysis_task_dict):
        remote_file_meta = RemoteFileMeta(**analysis_task_dict.get("remote_file_meta"))
        remote_file_source = RemoteFileSource(**analysis_task_dict.get("remote_file_source"))
        created_timestamp = analysis_task_dict.get("created_timestamp")
        return AnalysisTask(remote_file_meta=remote_file_meta, remote_file_source=remote_file_source,
                            created_timestamp=created_timestamp)

    def __init__(self, remote_file_meta, remote_file_source, created_timestamp=None):
        """
        Task created by coordinator, containing file meta and access to server with given file
        :type remote_file_meta: commons.model.remote_file_meta.RemoteFileMeta
        :type remote_file_source: commons.model.remote_file_source.RemoteFileSource
        :type created_timestamp: int
        """
        self.remote_file_meta = remote_file_meta
        self.remote_file_source = remote_file_source
        self.created_timestamp = created_timestamp or utc_datetime_to_timestamp(datetime.utcnow())

    def to_dict(self):
        return {
            "remote_file_meta": self.remote_file_meta.to_dict(),
            "remote_file_source": self.remote_file_source.to_dict(),
            "created": self.created_timestamp
        }

    def __str__(self):
        return "AnalysisTask: {}".format(self.to_dict())

    def __repr__(self):
        return self.__str__()
