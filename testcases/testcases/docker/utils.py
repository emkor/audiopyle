from subprocess import CalledProcessError

IMAGE_COORDINATOR = "endlessdrones/audiopyle-coordinator"
IMAGE_XTRACTER = "endlessdrones/audiopyle-xtracter"
IMAGE_PERSISTER = "endlessdrones/audiopyle-persister"
IMAGE_MYSQL = "mysql"
IMAGE_REDIS = "redis"


class ContainerException(CalledProcessError):
    def __init__(self, root_error, message=None):
        """
        :type root_error: subprocess.CalledProcessError
        :type message: str
        """
        self.root_error = root_error
        self.message = message

    def __str__(self):
        return "{} - container exception occurred: {} while running: {}. Details: {}".format(self.message,
                                                                                             self.root_error,
                                                                                             build_commands_string(
                                                                                                 self.root_error.cmd),
                                                                                             self.root_error.output)

    def __repr__(self):
        self.__str__()


def build_commands_string(commands_list):
    return " ".join(commands_list)
