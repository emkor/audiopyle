class RemoteFileMeta(object):
    def __init__(self, name, size, upload_timestamp):
        self.name = name
        self.size = size
        self.upload_timestamp = upload_timestamp

    def __str__(self):
        return "RemoteFileMeta: file name: {}, file size: {}, upload timestamp: {}."\
            .format(self.name, self.size, self.upload_timestamp)

    def __repr__(self):
        return self.__str__()
