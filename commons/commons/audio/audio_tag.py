from typing import Text, Optional, Any, Dict

from mutagen.easyid3 import EasyID3
from commons.utils.conversion import safe_cast, first_if_collection

from commons.abstractions.model import Model


class Id3Tag(Model):
    @classmethod
    def from_easy_id3_object(cls, easy_id3: EasyID3):
        return _mutagen_id3_to_internal(easy_id3)

    def __init__(self, artist: Text, title: Text, album: Optional[Text] = None, date: Optional[int] = None,
                 track: Optional[int] = None, genre: Optional[Text] = None) -> None:
        self.artist = artist
        self.title = title
        self.album = album
        self.date = date
        self.track = track
        self.genre = genre


def _mutagen_id3_to_internal(easy_id3: EasyID3) -> Id3Tag:
    maybe_track_number = first_if_collection(easy_id3.get("tracknumber"))
    track_number = maybe_track_number.split("/")[0] if maybe_track_number else None
    return Id3Tag(artist=first_if_collection(easy_id3["artist"]),
                  title=first_if_collection(easy_id3["title"]),
                  album=first_if_collection(easy_id3.get("album")),
                  date=safe_cast(first_if_collection(easy_id3.get("date")), int, None),
                  track=safe_cast(track_number, int, None),
                  genre=safe_cast(first_if_collection(easy_id3.get("genre")), str, None))
