import unittest

from assertpy import assert_that

from commons.utils.conversion import Converter


class UnitConverterTest(unittest.TestCase):
    def test_b_to_B(self):
        assert_that(Converter.b_to_B(8)).is_equal_to(1)
        assert_that(Converter.b_to_B(24)).is_equal_to(3)
        assert_that(Converter.b_to_B(12)).is_equal_to(2)
        assert_that(Converter.b_to_B(29)).is_equal_to(4)

    def test_B_to_b(self):
        assert_that(Converter.B_to_b(4)).is_equal_to(32)
        assert_that(Converter.B_to_b(4.5)).is_equal_to(36)
        assert_that(Converter.B_to_b(1)).is_equal_to(8)

    def test_to_kilo(self):
        assert_that(Converter.to_kilo(1)).is_equal_to(0.001)
        assert_that(Converter.to_kilo(1000)).is_equal_to(1)
        assert_that(Converter.to_kilo(1250)).is_equal_to(1.25)
        assert_that(Converter.to_kilo(6500)).is_equal_to(6.5)

    def test_to_mega(self):
        assert_that(Converter.to_mega(1)).is_equal_to(0.000001)
        assert_that(Converter.to_mega(1000000)).is_equal_to(1)
        assert_that(Converter.to_mega(1250000)).is_equal_to(1.25)
        assert_that(Converter.to_mega(8000000)).is_equal_to(8)

    def frames_to_sec(self):
        assert_that(Converter.frames_to_sec(44100, 44100)).is_equal_to(1)
        assert_that(Converter.frames_to_sec(44100, 22050)).is_equal_to(2)
        assert_that(Converter.frames_to_sec(22050, 44100)).is_equal_to(0.5)
        assert_that(Converter.frames_to_sec(4410, 44100)).is_equal_to(0.1)

    def sec_to_frames(self):
        assert_that(Converter.sec_to_frames(0.5, 44100)).is_equal_to(22050)
        assert_that(Converter.sec_to_frames(0.1, 44100)).is_equal_to(4410)
        assert_that(Converter.sec_to_frames(2, 22050)).is_equal_to(44100)
        assert_that(Converter.sec_to_frames(1, 44100)).is_equal_to(44100)
