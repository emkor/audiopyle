from commons.db.entity import ResultStats
from commons.db.session import SessionProvider
from commons.models.result import AnalysisStats
from commons.repository.abstract import DbRepository


class ResultStatsRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, ResultStats)

    def get_by_task_id(self, task_id: str) -> AnalysisStats:
        return self._query_single_with_filters(task_id=task_id)

    def _get_id_by_model(self, model_object: AnalysisStats) -> int:
        return self._get_id(task_id=model_object.task_id)

    def _map_to_entity(self, obj: AnalysisStats) -> ResultStats:
        return ResultStats(task_id=obj.task_id, total_time=obj.total_time, extraction_time=obj.extraction_time,
                           compression_time=obj.compression_time, data_stats_build_time=obj.data_stats_build_time,
                           encode_audio_time=obj.encode_audio_time)

    def _map_to_object(self, entity: ResultStats) -> AnalysisStats:
        return AnalysisStats(task_id=entity.task_id, total_time=entity.total_time,
                             extraction_time=entity.extraction_time, compression_time=entity.compression_time,
                             data_stats_build_time=entity.data_stats_build_time,
                             encode_audio_time=entity.encode_audio_time)
