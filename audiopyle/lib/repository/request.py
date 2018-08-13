from typing import Optional

from audiopyle.lib.db.entity import Request
from audiopyle.lib.db.session import SessionProvider
from audiopyle.lib.models.result import AnalysisRequest
from audiopyle.lib.repository.abstract import DbRepository
from audiopyle.lib.repository.audio_file import AudioFileRepository
from audiopyle.lib.repository.audio_tag import AudioTagRepository
from audiopyle.lib.repository.vampy_plugin import VampyPluginRepository, PluginConfigRepository
from audiopyle.lib.utils.conversion import safe_cast


class RequestRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider, audio_file_repository: AudioFileRepository,
                 audio_tag_repository: AudioTagRepository, plugin_repository: VampyPluginRepository,
                 plugin_config_repo: PluginConfigRepository) -> None:
        super().__init__(session_provider, Request)
        self.audio_file_repository = audio_file_repository
        self.audio_tag_repository = audio_tag_repository
        self.plugin_repository = plugin_repository
        self.plugin_config_repo = plugin_config_repo

    def get_id_by_model(self, model_object: AnalysisRequest) -> Optional[str]:
        return safe_cast(self._query_single(id=model_object.task_id), str, None)

    def _map_to_entity(self, obj: AnalysisRequest) -> Request:
        plugin_id = self.plugin_repository.get_or_create(obj.plugin)
        audio_meta_id = self.audio_file_repository.get_or_create(obj.audio_meta)
        audio_tag_id = self.audio_tag_repository.get_or_create(obj.id3_tag) if obj.id3_tag else None
        plugin_config_id = self.plugin_config_repo.get_or_create(obj.plugin_config)
        return Request(id=obj.task_id, vampy_plugin_id=plugin_id, audio_file_id=audio_meta_id,
                       audio_tag_id=audio_tag_id, plugin_config_id=plugin_config_id)

    def _map_to_object(self, entity: Request) -> AnalysisRequest:
        audio_meta = self.audio_file_repository.get_by_id(entity.audio_file_id)
        audio_tag = self.audio_tag_repository.get_by_id(entity.audio_tag_id)
        plugin = self.plugin_repository.get_by_id(entity.vampy_plugin_id)
        plugin_config = self.plugin_config_repo.get_by_id(entity.plugin_config_id)
        return AnalysisRequest(task_id=entity.id, audio_meta=audio_meta, id3_tag=audio_tag,  # type: ignore
                               plugin=plugin, plugin_config=plugin_config)
