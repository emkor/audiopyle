from typing import Optional
from audiopyle.lib.abstractions.model import Model


class Id3Tag(Model):
    def __init__(self, artist: str, title: str, album: Optional[str] = None, date: Optional[int] = None,
                 track: Optional[int] = None, genre: Optional[str] = None) -> None:
        self.artist = artist
        self.title = title
        self.album = album
        self.date = date
        self.track = track
        self.genre = genre
