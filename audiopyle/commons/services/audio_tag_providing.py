from enum import Enum
from typing import Optional, Callable, Union

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.id3 import ID3NoHeaderError

from audiopyle.commons.models.audio_tag import Id3Tag
from audiopyle.commons.utils.conversion import first_if_collection, safe_cast
from audiopyle.commons.utils.file_system import extract_extension, file_exists
from audiopyle.commons.utils.logger import get_logger

logger = get_logger()


class Extension(Enum):
    MP3 = "mp3"
    FLAC = "flac"


ACCEPTED_EXTENSIONS = [Extension.MP3.value, Extension.FLAC.value]


def read_audio_tag(input_audio_file_absolute_path: str) -> Optional[Id3Tag]:
    if file_exists(input_audio_file_absolute_path):
        file_ext = extract_extension(input_audio_file_absolute_path)
        if file_ext == Extension.MP3.value:
            return read_audio_tag_using(input_audio_file_absolute_path, EasyID3)
        elif file_ext == Extension.FLAC.value:
            return read_audio_tag_using(input_audio_file_absolute_path, FLAC)
        else:
            raise ValueError("Unsupported file for reading tags: {}".format(input_audio_file_absolute_path))
    else:
        logger.error("File {} does not exists, could not read tags".format(input_audio_file_absolute_path))
        return None


def read_audio_tag_using(input_audio_file_absolute_path: str, method_extracting_tag: Callable = Union[EasyID3, FLAC]) -> \
        Optional[Id3Tag]:
    try:
        audio_tags = method_extracting_tag(input_audio_file_absolute_path)
        id3_tag = _mutagen_tag_to_internal(audio_tags)
        logger.debug("Tags extracted from {}: {}".format(input_audio_file_absolute_path, id3_tag))
        return id3_tag
    except ID3NoHeaderError as e:
        logger.warning("File {} does not contain tag: {}".format(input_audio_file_absolute_path, e))
        return None
    except KeyError as e:
        logger.warning("File {} does not contain crucial tag values: {}".format(input_audio_file_absolute_path, e))
        return None
    except Exception as e:
        logger.error("Could not read tags from: {}. Details: {}".format(input_audio_file_absolute_path, e))
        return None


def _mutagen_tag_to_internal(mutagen_tag: Union[EasyID3, FLAC]) -> Id3Tag:
    maybe_track_number = first_if_collection(mutagen_tag.get("tracknumber"))
    track_number = maybe_track_number.split("/")[0] if maybe_track_number else None
    return Id3Tag(artist=first_if_collection(mutagen_tag["artist"]),
                  title=first_if_collection(mutagen_tag["title"]),
                  album=first_if_collection(mutagen_tag.get("album")),
                  date=safe_cast(first_if_collection(mutagen_tag.get("date")), int, None),
                  track=safe_cast(track_number, int, None),
                  genre=safe_cast(first_if_collection(mutagen_tag.get("genre")), str, None))
