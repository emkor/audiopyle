from commons.db.entity import AudioFile
from commons.db.session import SessionProvider
from commons.models.file_meta import Mp3AudioFileMeta
from commons.repository.abstract import DbRepository


class AudioFileRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, AudioFile)

    def get_id_by_file_name(self, file_name: str) -> int:
        return super()._get_id(file_name=file_name)

    def get_id_by_model(self, model_object: Mp3AudioFileMeta) -> int:
        return self.get_id_by_file_name(model_object.file_name)

    def _map_to_object(self, entity: AudioFile) -> Mp3AudioFileMeta:
        return Mp3AudioFileMeta(entity.file_name, entity.size_bytes, entity.channels_count,
                                entity.sample_rate, entity.length_sec, entity.bit_rate)

    def _map_to_entity(self, obj: Mp3AudioFileMeta) -> AudioFile:
        return AudioFile(file_name=obj.file_name, size_bytes=obj.file_size_bytes,
                         channels_count=obj.channels_count, sample_rate=obj.sample_rate,
                         length_sec=obj.length_sec, bit_rate=obj.bit_rate_kbps)
