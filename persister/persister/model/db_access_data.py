class DbAccessData(object):
    def __init__(self, user, password, host="127.0.0.1", port=3306):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __str__(self):
        return "<DbAccessData: [{}]>".format(self.__dict__)

    def __repr__(self):
        return self.__str__()
