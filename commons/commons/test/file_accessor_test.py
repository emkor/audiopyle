import unittest
from assertpy import assert_that
from commons.service.file_accessor import FileAccessor


class TestFileAccessor(unittest.TestCase):
    def test_existing_file_or_dir_should_be_found(self):
        assert_that(FileAccessor.exists('/etc/passwd')).is_true()
        assert_that(FileAccessor.exists('/home')).is_true()

    def test_not_existing_file_or_dir_should_not_be_found(self):
        assert_that(FileAccessor.exists('/dass/ghsdcv')).is_false()

    def test_for_checking_is_dir(self):
        assert_that(FileAccessor.is_dir('/home')).is_true()
        assert_that(FileAccessor.is_dir('/etc/passwd')).is_false()

    def test_getting_file_name(self):
        assert_that(FileAccessor.get_file_name('/etc/passwd')).is_equal_to('passwd')
        assert_that(FileAccessor.get_file_name('D:/folder/file.txt')).is_equal_to('file.txt')
        assert_that(FileAccessor.get_file_name('D://folder//file.txt')).is_equal_to('file.txt')

    def test_getting_dir_name(self):
        assert_that(FileAccessor.get_file_name('/home')).is_equal_to('home')

    def test_join_path_from_two_elements(self):
        path_part_1 = '/etc/init.d'
        path_part_2 = 'something/elem.txt'
        expected_path = '/etc/init.d/something/elem.txt'
        assert_that(FileAccessor.join(path_part_1, path_part_2)).is_equal_to(expected_path)
