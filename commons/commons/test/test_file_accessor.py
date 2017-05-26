import unittest
from assertpy import assert_that

from commons.utils.file_system import get_file_name, extract_extension, file_exists, list_files


class TestFileAccessor(unittest.TestCase):
    def test_checking_if_file_exists(self):
        assert_that(file_exists("/dev/null")).is_true()
        assert_that(file_exists("/dev/24e3re34d17")).is_false()

    def test_getting_file_name(self):
        assert_that(get_file_name('/etc/passwd')).is_equal_to('passwd')
        assert_that(get_file_name('D:/folder/file.txt')).is_equal_to('file.txt')
        assert_that(get_file_name('D://folder//file.txt')).is_equal_to('file.txt')

    def test_getting_extension(self):
        assert_that(extract_extension('song.ogg')).is_equal_to('ogg')
        assert_that(extract_extension('song.ogg.wav')).is_equal_to('wav')
        assert_that(extract_extension('config')).is_equal_to('')
        assert_that(extract_extension('.vimrc')).is_equal_to('')

    def test_getting_dir_name(self):
        assert_that(get_file_name('/home')).is_equal_to('home')

    def test_listing_files(self):
        assert_that(list_files('/etc')).is_not_empty()
