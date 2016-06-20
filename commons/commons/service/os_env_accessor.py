import os


class OsEnvAccessor(object):
    @staticmethod
    def get_env_variable(var_name):
        return os.getenv(var_name)

    @staticmethod
    def get_env_variable_or(var_name, alternative):
        return os.getenv(var_name, alternative)
