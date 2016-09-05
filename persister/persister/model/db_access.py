class DbAccess(object):
    def __init__(self, user, password, host="localhost", port=3306):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
