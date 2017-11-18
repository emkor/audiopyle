from typing import Text, Optional

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

from commons.models.audio_tag import Id3Tag
from commons.utils.conversion import first_if_collection, safe_cast
from commons.utils.logger import get_logger

logger = get_logger()


def read_id3_tag(input_audio_file_absolute_path: Text) -> Optional[Id3Tag]:
    try:
        audio_tags = EasyID3(input_audio_file_absolute_path)
        id3_tag = _mutagen_id3_to_internal(audio_tags)
        logger.info("Tags extracted from {}: {}".format(input_audio_file_absolute_path, id3_tag))
        return id3_tag
    except ID3NoHeaderError as e:
        logger.warning("File {} does not contain ID3 tag: {}".format(input_audio_file_absolute_path, e))
        return None
    except Exception as e:
        logger.error("Could not read ID3 tags from: {}. Details: {}".format(input_audio_file_absolute_path, e))
        raise IOError(e)


def _mutagen_id3_to_internal(easy_id3: EasyID3) -> Id3Tag:
    maybe_track_number = first_if_collection(easy_id3.get("tracknumber"))
    track_number = maybe_track_number.split("/")[0] if maybe_track_number else None
    return Id3Tag(artist=first_if_collection(easy_id3["artist"]),
                  title=first_if_collection(easy_id3["title"]),
                  album=first_if_collection(easy_id3.get("album")),
                  date=safe_cast(first_if_collection(easy_id3.get("date")), int, None),
                  track=safe_cast(track_number, int, None),
                  genre=safe_cast(first_if_collection(easy_id3.get("genre")), str, None))
