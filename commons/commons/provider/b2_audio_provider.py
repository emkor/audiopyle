import logging

from b2.api import B2Api
from b2.download_dest import DownloadDestLocalFile

from commons.service.file_accessor import FileAccessor
from commons.utils.constant import AudiopyleConst


class B2AudioProvider(object):
    def __init__(self, b2_config, local_wave_dir, b2_api=None):
        self.b2_api = b2_api or B2Api()
        self.b2_config = b2_config
        self.local_wave_dir = local_wave_dir
        self.logger = logging.getLogger(__name__)

    def is_connected(self):
        return self._connect_to_bucket() is not None

    def get_file_infos(self):
        bucket = self._connect_to_bucket()
        return bucket.list_file_names().get('files')

    def get_filepaths_list(self):
        return [file_info.get('fileName') for file_info in self.get_file_infos()]

    def exists(self, remote_file_path):
        return remote_file_path in self.get_filepaths_list()

    def download(self, remote_file_path):
        bucket = self._connect_to_bucket()
        destination_object = self._create_destination_object(remote_file_path)
        bucket.download_file_by_name(remote_file_path, destination_object)
        return destination_object.local_file_path

    def _connect_to_bucket(self):
        try:
            self.b2_api.authorize_account(AudiopyleConst.B2_REALM, self.b2_config.account_id,
                                          self.b2_config.application_key)
            bucket = self.b2_api.get_bucket_by_name(self.b2_config.bucket_name)
            if bucket is None:
                raise IOError("Retrieved bucket: {} was None.".format(self.b2_config.bucket_name))
            else:
                return bucket
        except Exception as e:
            self.logger.exception("Error on checking backblaze connectivity. Details: {}".format(e))
            return None

    def _create_destination_object(self, remote_file_path):
        file_name = FileAccessor.get_file_name(remote_file_path)
        dest_file_path = FileAccessor.join(self.local_wave_dir, file_name)
        destination_object = DownloadDestLocalFile(dest_file_path)
        return destination_object
