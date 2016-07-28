import numpy

from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor
from commons.utils.constant import AudiopyleConst
from xtracter.utils.xtracter_const import XtracterConst


class XtracterUtils(object):
    @staticmethod
    def get_test_resources_path():
        project_path = OsEnvAccessor.get_env_variable(AudiopyleConst.PROJECT_HOME_ENV)
        return FileAccessor.join(project_path, XtracterConst.TEST_RESOURCES_PATH)

    @staticmethod
    def get_test_wav_file_path():
        resource_path = XtracterUtils.get_test_resources_path()
        return FileAccessor.join(resource_path, XtracterConst.TEST_WAV_FILE_NAME)

    @staticmethod
    def get_test_mp3_file_name():
        return XtracterConst.TEST_MP3_FILE_NAME

    @staticmethod
    def get_test_csv_file_path():
        resource_path = XtracterUtils.get_test_resources_path()
        return FileAccessor.join(resource_path, XtracterConst.TEST_CSV_FILE_NAME)

    @staticmethod
    def import_test_file_csv_data():
        csv_file_path = XtracterUtils.get_test_csv_file_path()
        return numpy.loadtxt(fname=csv_file_path, delimiter=",")

    @staticmethod
    def get_wav_file_path():
        project_path = OsEnvAccessor.get_env_variable(AudiopyleConst.PROJECT_HOME_ENV)
        return FileAccessor.join(project_path, XtracterConst.AUDIO_FILES_CACHE_PATH)
