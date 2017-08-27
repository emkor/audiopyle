import os


def get_environment_variable(variable_name, default=None):
    return os.environ.get(variable_name, default=default)
