from typing import Type
from unittest import TestCase

import os

from commons.db.engine import get_test_db_engine, create_db_tables, drop_db_tables
from commons.db.session import SessionProvider
from commons.utils.file_system import concatenate_paths, remove_file

TEST_MP3_AUDIO_FILE = "resources/audio/102bpm_drum_loop.mp3"


def setup_db_repository_test_class(cls: Type[TestCase]) -> None:
    cls.db_file_name = "{}_sqlite.db".format(cls.__name__)  # type: ignore
    cls.engine = get_test_db_engine(debug=True)  # type: ignore
    create_db_tables(engine=cls.engine, only_if_absent=False)  # type: ignore
    cls.session_provider = SessionProvider(db_engine=cls.engine)  # type: ignore


def tear_down_db_repository_test_class(cls: Type[TestCase]) -> None:
    drop_db_tables(cls.engine)


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
