from datetime import datetime

from commons.utils.conversion import utc_datetime_to_timestamp


class AnalysisResult(object):
    def __init__(self, analysis_task, features, done_timestamp=None):
        """
        :type analysis_task: commons.model.analysis_task.AnalysisTask
        :type features: list[commons.model.feature.AudioFeature]
        :type done_timestamp: int
        """
        self.task = analysis_task
        self.features = features
        self.done_timestamp = done_timestamp or utc_datetime_to_timestamp(datetime.utcnow())

    def to_dict(self):
        """
        :return: dict
        """
        return {
            "task": self.task.to_dict(),
            "features": [feature.to_dict() for feature in self.features],
            "done_timestamp": self.done_timestamp
        }

