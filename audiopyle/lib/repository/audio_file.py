from typing import Optional

from audiopyle.lib.db.entity import AudioFile
from audiopyle.lib.db.session import SessionProvider
from audiopyle.lib.models.file_meta import CompressedAudioFileMeta
from audiopyle.lib.repository.abstract import DbRepository
from audiopyle.lib.utils.conversion import safe_cast


class AudioFileRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, AudioFile)

    def get_id_by_file_name(self, file_name: str) -> Optional[int]:
        return safe_cast(super()._get_id(file_name=file_name), int, None)

    def get_id_by_model(self, model_object: CompressedAudioFileMeta) -> Optional[int]:
        return self.get_id_by_file_name(model_object.file_name)

    def _map_to_object(self, entity: AudioFile) -> CompressedAudioFileMeta:
        return CompressedAudioFileMeta(entity.file_name, entity.size_bytes, entity.channels_count,
                                       entity.sample_rate, entity.length_sec, entity.bit_rate)

    def _map_to_entity(self, obj: CompressedAudioFileMeta) -> AudioFile:
        return AudioFile(file_name=obj.file_name, size_bytes=obj.file_size_bytes,
                         channels_count=obj.channels_count, sample_rate=obj.sample_rate,
                         length_sec=obj.length_sec, bit_rate=obj.bit_rate_kbps)
