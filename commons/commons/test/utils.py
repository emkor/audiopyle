import os

from commons.utils.file_system import concatenate_paths

TEST_MP3_AUDIO_FILE = "resources/audio/102bpm_drum_loop_mono_44.1k.mp3"


def get_absolute_path_for_project_file(caller_file_object, project_file_path):
    """
    :param caller_file_object: caller_file_object
    :type caller_file_object: str
    :type project_file_path: str
    :rtype: str
    """
    return concatenate_paths(get_audiopyle_root_dir(caller_file_object), project_file_path)


def get_audiopyle_root_dir(test_file_object):
    """
    :param test_file_object: usually __file__
    :type test_file_object:
    :return: Project root directory path
    :rtype: str
    """
    current_test_directory = os.path.dirname(os.path.realpath(test_file_object))
    code_directory, audiopyle_directory, _ = current_test_directory.partition("audiopyle/")
    return concatenate_paths(code_directory, audiopyle_directory)


def fake_function_from_method(callable, arg):
    """assert_that(...).raises() must have a function, not method, in place of ..."""
    callable(arg)
