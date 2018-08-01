from typing import Text, Optional
from audiopyle.commons.abstractions.model import Model


class Id3Tag(Model):
    def __init__(self, artist: Text, title: Text, album: Optional[Text] = None, date: Optional[int] = None,
                 track: Optional[int] = None, genre: Optional[Text] = None) -> None:
        self.artist = artist
        self.title = title
        self.album = album
        self.date = date
        self.track = track
        self.genre = genre
