from typing import Text, Optional

from mutagen.easyid3 import EasyID3

from commons.abstractions.model import Model
from commons.utils.conversion import first_element_or, safe_cast


class Id3Tag(Model):
    @classmethod
    def from_easy_id3_object(cls, easy_id3: EasyID3):
        return Id3Tag(artist=first_element_or(easy_id3["artist"]), title=first_element_or(easy_id3["title"]),
                      album=first_element_or(easy_id3.get("album")),
                      date=safe_cast(first_element_or(easy_id3.get("date")), int, None),
                      track=safe_cast(first_element_or(easy_id3.get("tracknumber")), int, None),
                      genre=safe_cast(first_element_or(easy_id3.get("genre")), str, None))

    def __init__(self, artist: Text, title: Text, album: Optional[Text] = None, date: Optional[int] = None,
                 track: Optional[int] = None, genre: Optional[Text] = None) -> None:
        self.artist = artist
        self.title = title
        self.album = album
        self.date = date
        self.track = track
        self.genre = genre
