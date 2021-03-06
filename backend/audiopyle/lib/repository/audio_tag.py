from typing import List, Optional

from audiopyle.lib.db.entity import AudioTag
from audiopyle.lib.db.session import SessionProvider
from audiopyle.lib.models.audio_tag import Id3Tag
from audiopyle.lib.repository.abstract import DbRepository
from audiopyle.lib.utils.conversion import safe_cast


class AudioTagRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, AudioTag)

    def get_id_by_name(self, artist_name: str, album_name: str, title_name: str) -> Optional[int]:
        return safe_cast(super()._get_id(artist=artist_name, album=album_name, title=title_name), int, None)

    def filter_by_artist(self, artist_name: str) -> List[Id3Tag]:
        return self._query_multiple(artist=artist_name)

    def filter_by_album(self, album_name: str) -> List[Id3Tag]:
        return self._query_multiple(album=album_name)

    def filter_by_title(self, title_name: str) -> List[Id3Tag]:
        return self._query_multiple(title=title_name)

    def filter_by_genre(self, genre_name: str) -> List[Id3Tag]:
        return self._query_multiple(genre=genre_name)

    def get_id_by_model(self, model_object: Id3Tag) -> Optional[int]:
        return self.get_id_by_name(model_object.artist, model_object.album, model_object.title)  # type: ignore

    def _map_to_object(self, audio_tag: AudioTag) -> Id3Tag:
        return Id3Tag(audio_tag.artist, audio_tag.title, audio_tag.album,
                      audio_tag.date, audio_tag.track, audio_tag.genre)

    def _map_to_entity(self, obj: Id3Tag) -> AudioTag:
        return AudioTag(artist=obj.artist, album=obj.album, title=obj.title,
                        date=obj.date, genre=obj.genre, track=obj.track)
