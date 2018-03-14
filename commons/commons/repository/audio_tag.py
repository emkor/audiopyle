from typing import List

from commons.db.entity import AudioTag
from commons.db.session import SessionProvider
from commons.models.audio_tag import Id3Tag
from commons.repository.abstract import DbRepository


class AudioTagRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, AudioTag, map_tag_entity_to_object, map_tag_object_to_entity)

    def get_id_by_name(self, artist_name: str, album_name: str, title_name: str) -> int:
        return super()._get_id(artist=artist_name, album=album_name, title=title_name)

    def filter_by_artist(self, artist_name: str) -> List[Id3Tag]:
        return self._query_multiple_with_filters(artist=artist_name)

    def filter_by_album(self, album_name: str) -> List[Id3Tag]:
        return self._query_multiple_with_filters(album=album_name)

    def filter_by_title(self, title_name: str) -> List[Id3Tag]:
        return self._query_multiple_with_filters(title=title_name)

    def filter_by_genre(self, genre_name: str) -> List[Id3Tag]:
        return self._query_multiple_with_filters(genre=genre_name)


def map_tag_entity_to_object(audio_tag: AudioTag) -> Id3Tag:
    return Id3Tag(audio_tag.artist, audio_tag.title, audio_tag.album,
                  audio_tag.date, audio_tag.track, audio_tag.genre)


def map_tag_object_to_entity(audio_tag: Id3Tag) -> AudioTag:
    return AudioTag(artist=audio_tag.artist, album=audio_tag.album, title=audio_tag.title,
                    date=audio_tag.date, genre=audio_tag.genre, track=audio_tag.track)
