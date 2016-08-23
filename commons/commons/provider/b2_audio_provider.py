import logging

from b2.api import B2Api
from b2.download_dest import DownloadDestLocalFile

from commons.model.remote_file_meta import RemoteFileMeta
from commons.service.file_accessor import FileAccessor
from commons.utils.constant import AudiopyleConst


class AbstractRemoteAudioProvider(object):
    def __init__(self, local_destination_dir):
        """
        :type local_destination_dir: basestring
        """
        self.local_destination_dir = local_destination_dir

    def remote_file_path_exists(self, remote_source_config, remote_file_path):
        """
        :type remote_source_config: commons.model.remote_file_source.RemoteFileSource
        :type remote_file_path: basestring
        :rtype: bool
        """
        raise NotImplementedError()

    def get_remote_file_metas(self, remote_source_config):
        """
        :type remote_source_config: commons.model.remote_file_source.RemoteFileSource
        :rtype: list[commons.model.remote_file_meta.RemoteFileMeta]
        """
        raise NotImplementedError()

    def get_raw_file_infos(self, remote_source_config):
        """
        :type remote_source_config: commons.model.remote_file_source.RemoteFileSource
        :rtype: list[dict]
        """
        raise NotImplementedError()

    def download(self, remote_source_config, remote_file_meta):
        """
        Downloads file from remote synchronously and returns path to local, downloaded file
        :type remote_source_config: commons.model.remote_file_source.RemoteFileSource
        :type remote_file_meta: commons.model.remote_file_meta.RemoteFileMeta
        :rtype: basestring
        """
        raise NotImplementedError()


class B2AudioProvider(AbstractRemoteAudioProvider):
    def __init__(self, local_destination_dir, b2_api=None):
        """
        :type local_destination_dir: basestring
        :type b2_api: b2.api.B2Api
        """
        super(B2AudioProvider, self).__init__(local_destination_dir)
        self.b2_api = b2_api or B2Api()

    def remote_file_path_exists(self, remote_source_config, remote_file_path):
        available_remote_file_paths = [file_info.get('fileName') for file_info in
                                       self.get_raw_file_infos(remote_source_config)]
        return remote_file_path in available_remote_file_paths

    def get_raw_file_infos(self, remote_source_config):
        bucket = self._connect_to_bucket(remote_source_config)
        return bucket.list_file_names().get('files')

    def get_remote_file_metas(self, remote_source_config):
        remote_raw_file_data = self.get_raw_file_infos(remote_source_config)
        return map(lambda raw_dict: RemoteFileMeta(name=raw_dict.get('fileName'), size=raw_dict.get('size'),
                                                   upload_timestamp=raw_dict.get('uploadTimestamp')),
                   remote_raw_file_data)

    def download(self, remote_source_config, remote_file_meta):
        bucket = self._connect_to_bucket(remote_source_config)
        destination_object = self._create_destination_object(remote_file_meta.name)
        bucket.download_file_by_name(remote_file_meta.name, destination_object)
        return destination_object.local_file_path

    def _connect_to_bucket(self, remote_source_config):
        try:
            self.b2_api.authorize_account(AudiopyleConst.B2_REALM, remote_source_config.address,
                                          remote_source_config.password)
            bucket = self.b2_api.get_bucket_by_name(remote_source_config.bucket_name)
            if bucket is None:
                raise IOError("Retrieved bucket: {} was None.".format(remote_source_config.bucket_name))
            else:
                return bucket
        except Exception as e:
            logging.error("Error on checking backblaze connectivity. Details: {}".format(e))
            return None

    def _create_destination_object(self, remote_file_path):
        file_name = FileAccessor.get_file_name(remote_file_path)
        dest_file_path = FileAccessor.join(self.local_destination_dir, file_name)
        return DownloadDestLocalFile(dest_file_path)
