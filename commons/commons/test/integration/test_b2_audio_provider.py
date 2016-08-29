import unittest
from assertpy import assert_that

from commons.model.remote_file_meta import RemoteFileMeta
from commons.model.remote_file_source import B2Config
from commons.provider.b2_audio_provider import B2AudioProvider
from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor
from commons.utils.constant import B2_ACCOUNT_ID, B2_APPLICATION_KEY, B2_RESOURCES_BUCKET, PROJECT_HOME_ENV, \
    B2_TEST_FILE_PATH, B2_TEST_FILE_UPLOAD_TIMESTAMP, B2_TEST_FILE_SIZE


class B2AudioProviderIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.b2_test_config = B2Config(B2_ACCOUNT_ID, B2_APPLICATION_KEY,
                                       B2_RESOURCES_BUCKET)
        local_cache_dir = OsEnvAccessor.get_env_variable(PROJECT_HOME_ENV)
        self.audio_provider = B2AudioProvider(local_cache_dir)

    def test_file_should_exists(self):
        test_file_exists = self.audio_provider.remote_file_path_exists(self.b2_test_config,
                                                                       B2_TEST_FILE_PATH)
        assert_that(test_file_exists).is_true()

    def test_made_up_file_should_not_exists(self):
        made_up_file_path = "smthng_smthng/anyfile.txt"
        test_file_exists = self.audio_provider.remote_file_path_exists(self.b2_test_config, made_up_file_path)
        assert_that(test_file_exists).is_false()

    def test_get_files_raw_info_should_contain_anything(self):
        file_infos = self.audio_provider.get_raw_file_infos(self.b2_test_config)
        assert_that(file_infos).is_not_none().is_not_empty()

    def test_get_files_raw_info_should_contain_test_file_meta(self):
        expected_remote_file = RemoteFileMeta(B2_TEST_FILE_PATH, B2_TEST_FILE_SIZE,
                                              B2_TEST_FILE_UPLOAD_TIMESTAMP)
        remote_file_mets = self.audio_provider.get_remote_file_metas(self.b2_test_config)
        self.assertIn(expected_remote_file, remote_file_mets)

    def test_should_download_remote_file(self):
        local_file_path = self.audio_provider.download(self.b2_test_config, B2_TEST_FILE_PATH)
        assert_that(FileAccessor.exists(local_file_path)).is_true()
        FileAccessor.remove_file(local_file_path)
