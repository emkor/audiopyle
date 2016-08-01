import unittest
from assertpy import assert_that
from commons.model.b2_config import B2Config
from commons.provider.b2_audio_provider import B2AudioProvider
from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor
from commons.utils.constant import AudiopyleConst


class B2AudioProviderIntegrationTest(unittest.TestCase):
    def setUp(self):
        b2_test_config = B2Config(AudiopyleConst.B2_ACCOUNT_ID, AudiopyleConst.B2_APPLICATION_KEY,
                                  AudiopyleConst.B2_RESOURCES_BUCKET)
        local_cache_dir = OsEnvAccessor.get_env_variable(AudiopyleConst.PROJECT_HOME_ENV)
        self.audio_provider = B2AudioProvider(b2_test_config, local_cache_dir)

    def test_bucket_should_exits(self):
        is_connected_to_bucket = self.audio_provider.is_connected()
        assert_that(is_connected_to_bucket).is_true()

    def test_file_should_exists(self):
        test_file_exists = self.audio_provider.exists(AudiopyleConst.B2_TEST_FILE_PATH)
        assert_that(test_file_exists).is_true()

    def test_made_up_file_should_not_exists(self):
        test_file_exists = self.audio_provider.exists("smthng_smthng/anyfile.txt")
        assert_that(test_file_exists).is_false()

    def test_remote_file_paths_should_contain_test_file(self):
        remote_file_paths = self.audio_provider.get_filepaths_list()
        assert_that(remote_file_paths).contains(AudiopyleConst.B2_TEST_FILE_PATH)

    def test_remote_file_paths_should_not_contain_made_up_file(self):
        remote_file_paths = self.audio_provider.get_filepaths_list()
        assert_that(remote_file_paths).does_not_contain("smthng_smthng/anyfile.txt")

    def test_should_download_remote_file(self):
        local_file_path = self.audio_provider.download(AudiopyleConst.B2_TEST_FILE_PATH)
        assert_that(FileAccessor.exists(local_file_path)).is_true()
        FileAccessor.remove_file(local_file_path)

    def test_get_files_info_should_contain_anything(self):
        file_infos = self.audio_provider.get_file_infos()
        assert_that(file_infos).is_not_none().is_not_empty()
