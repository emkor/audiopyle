from commons.db.entity import AudioFile
from commons.db.session import SessionProvider
from commons.models.file_meta import Mp3AudioFileMeta
from commons.repository.abstract import DbRepository


class AudioFileRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, AudioFile, map_audio_entity_to_object, map_audio_object_to_entity)

    def get_id_by_file_name(self, file_name: str) -> int:
        return super()._get_id(file_name=file_name)


def map_audio_object_to_entity(audio_meta: Mp3AudioFileMeta) -> AudioFile:
    return AudioFile(file_name=audio_meta.file_name, size_bytes=audio_meta.file_size_bytes,
                     channels_count=audio_meta.channels_count, sample_rate=audio_meta.sample_rate,
                     length_sec=audio_meta.length_sec, bit_rate=audio_meta.bit_rate_kbps)


def map_audio_entity_to_object(audio_file: AudioFile) -> Mp3AudioFileMeta:
    return Mp3AudioFileMeta(audio_file.file_name, audio_file.size_bytes, audio_file.channels_count,
                            audio_file.sample_rate, audio_file.length_sec, audio_file.bit_rate)
