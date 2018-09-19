from typing import Optional

from audiopyle.lib.db.entity import ResultStats
from audiopyle.lib.db.session import SessionProvider
from audiopyle.lib.models.result import AnalysisStats
from audiopyle.lib.repository.abstract import DbRepository
from audiopyle.lib.utils.conversion import safe_cast


class ResultStatsRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, ResultStats)

    def get_id_by_model(self, model_object: AnalysisStats) -> Optional[str]:
        return safe_cast(self._get_id(id=model_object.task_id), str, None)

    def _map_to_entity(self, obj: AnalysisStats) -> ResultStats:
        return ResultStats(id=obj.task_id, total_time=obj.total_time, extraction_time=obj.extraction_time,
                           compression_time=obj.compression_time, data_stats_build_time=obj.data_stats_build_time,
                           encode_audio_time=obj.encode_audio_time, result_store_time=obj.result_store_time,
                           metrics_extraction_time=obj.metrics_extraction_time)

    def _map_to_object(self, entity: ResultStats) -> AnalysisStats:
        return AnalysisStats(task_id=entity.id, total_time=entity.total_time,
                             extraction_time=entity.extraction_time, compression_time=entity.compression_time,
                             data_stats_build_time=entity.data_stats_build_time,
                             encode_audio_time=entity.encode_audio_time, result_store_time=entity.result_store_time,
                             metrics_extraction_time=entity.metrics_extraction_time)