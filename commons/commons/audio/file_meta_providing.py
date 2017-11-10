import os
from typing import Text
from commons.audio.file_meta import FileMeta
from commons.utils.conversion import utc_timestamp_to_datetime


def get_file_meta(file_name: Text) -> FileMeta:
    file_stats = os.stat(file_name)
    last_access_utc = utc_timestamp_to_datetime(file_stats.st_atime)
    last_modification_utc = utc_timestamp_to_datetime(file_stats.st_mtime)
    created_on_utc = utc_timestamp_to_datetime(file_stats.st_ctime)
    return FileMeta(file_name=file_name, size=file_stats.st_size, last_access=last_access_utc,
                    last_modification=last_modification_utc, created_on=created_on_utc)
