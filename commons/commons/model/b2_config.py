class B2Config(object):
    def __init__(self, account_id, application_key, bucket_name):
        self.bucket_name = bucket_name
        self.application_key = application_key
        self.account_id = account_id

    def __str__(self):
        return "B2Config: account_id: {}, bucket_name: {}".format(self.account_id, self.bucket_name)

    def __repr__(self):
        return self.__str__()
