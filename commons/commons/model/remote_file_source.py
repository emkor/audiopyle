class RemoteFileSource(object):
    @staticmethod
    def from_dict(remote_file_meta_dict):
        """
        :type remote_file_meta_dict: dict
        :rtype: commons.model.remote_file_source.RemoteFileSource
        """
        return RemoteFileSource(**remote_file_meta_dict)

    def __init__(self, type, address, bucket_name, password, **kwargs):
        """
        :type type: basestring
        :type address: basestring
        :type bucket_name: basestring
        :type password: basestring
        :type kwargs: dict
        """
        self.type = type
        self.address = address
        self.bucket_name = bucket_name
        self.password = password

    def to_dict(self):
        return self.__dict__

    def __hash__(self):
        return hash((self.type, self.address, self.bucket_name))

    def __eq__(self, other):
        return self.type == other.type and self.address == other.address and self.bucket_name == other.bucket_name

    def __str__(self):
        return "RemoteFileSource: {}".format(self.__dict__)

    def __repr__(self):
        return self.__str__()


class B2Config(RemoteFileSource):
    def __init__(self, account_id, application_key, bucket_name):
        super(B2Config, self).__init__(type="b2", address=account_id, bucket_name=bucket_name, password=application_key)
