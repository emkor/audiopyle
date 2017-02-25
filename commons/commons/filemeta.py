import os

from commons.conversion import utc_timestamp_to_datetime, to_kilo, to_mega
from commons.file_system import get_file_name, extract_extension
from commons.model import Model


def get_file_meta(file_name):
    """
    :type file_name: str
    :rtype: commons.filemeta.FileMeta
    """
    file_stats = os.stat(file_name)
    last_access_utc = utc_timestamp_to_datetime(file_stats.st_atime)
    last_modification_utc = utc_timestamp_to_datetime(file_stats.st_mtime)
    created_on_utc = utc_timestamp_to_datetime(file_stats.st_ctime)
    return FileMeta(file_name=file_name, size=file_stats.st_size, last_access=last_access_utc,
                    last_modification=last_modification_utc, created_on=created_on_utc)


class FileMeta(Model):
    def __init__(self, file_name, size, last_access, last_modification, created_on):
        """
        :type file_name: str
        :type size: int
        :type last_access: datetime.datetime
        :type last_modification: datetime.datetime
        :type created_on: datetime.datetime
        """
        self.created_on = created_on
        self.last_modification = last_modification
        self.last_access = last_access
        self.size = size
        self.file_name = file_name

    @property
    def size_kB(self):
        """
        :rtype: float
        """
        return to_kilo(self.size)

    @property
    def size_mB(self):
        """
        :rtype: float
        """
        return to_mega(self.size)

    @property
    def file_base_name(self):
        """
        :rtype: str
        """
        return get_file_name(self.file_name)

    @property
    def extension(self):
        """
        :rtype: str
        """
        return extract_extension(self.file_name)


print(get_file_meta("/home/mkorzeni/projects/audiopyle/resources/102bpm_drum_loop_mono_44.1k.wav"))
