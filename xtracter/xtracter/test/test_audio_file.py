import unittest

from assertpy import assert_that

from commons.model.audio_meta import AudioMeta
from commons.model.audio_segment import AudioSegment


class AudioMetaTest(unittest.TestCase):
    def setUp(self):
        self.test_meta_1 = AudioMeta('loop-44.1k-mono-110bpm.wav', 1, 44100, 384874, 16)
        self.test_meta_2 = AudioMeta('loop-44.1k-stereo-110bpm.wav', 2, 44100, 384874, 16)
        self.test_meta_3 = AudioMeta('loop-48k-stereo-110bpm.wav', 2, 48000, 418910, 16)

    def test_file_size_kB_calculation(self):
        # given
        test_size_kB_delta = 1
        file_1_expected_size_kB = 769
        file_2_expected_size_kB = 1539
        file_3_expected_size_kB = 1675
        # when
        file_1_actual_size_kB = self.test_meta_1.size_kB()
        file_2_actual_size_kB = self.test_meta_2.size_kB()
        file_3_actual_size_kB = self.test_meta_3.size_kB()
        # then
        assert_that(file_1_actual_size_kB).is_close_to(file_1_expected_size_kB, tolerance=test_size_kB_delta)
        assert_that(file_2_actual_size_kB).is_close_to(file_2_expected_size_kB, tolerance=test_size_kB_delta)
        assert_that(file_3_actual_size_kB).is_close_to(file_3_expected_size_kB, tolerance=test_size_kB_delta)

    def test_kbps_calculation(self):
        # given
        test_bitrate_kbps_delta = 1
        file_1_expected_bitrate_kbps = 705
        file_2_expected_bitrate_kbps = 1411
        file_3_expected_bitrate_kbps = 1536
        # when
        file_1_actual_bitrate_kbps = self.test_meta_1.avg_kbps()
        file_2_actual_bitrate_kbps = self.test_meta_2.avg_kbps()
        file_3_actual_bitrate_kbps = self.test_meta_3.avg_kbps()
        # then
        assert_that(file_1_actual_bitrate_kbps).is_close_to(file_1_expected_bitrate_kbps, test_bitrate_kbps_delta)
        assert_that(file_2_actual_bitrate_kbps).is_close_to(file_2_expected_bitrate_kbps, test_bitrate_kbps_delta)
        assert_that(file_3_actual_bitrate_kbps).is_close_to(file_3_expected_bitrate_kbps, test_bitrate_kbps_delta)

    def test_length_sec_calculation(self):
        # given
        test_length_sec_delta = 0.05
        files_expected_length_sec = 8.727
        # when
        file_1_actual_length_sec = self.test_meta_1.length_sec()
        file_2_actual_length_sec = self.test_meta_2.length_sec()
        file_3_actual_length_sec = self.test_meta_3.length_sec()
        # then
        assert_that(file_1_actual_length_sec).is_close_to(files_expected_length_sec, tolerance=test_length_sec_delta)
        assert_that(file_2_actual_length_sec).is_close_to(files_expected_length_sec, tolerance=test_length_sec_delta)
        assert_that(file_3_actual_length_sec).is_close_to(files_expected_length_sec, tolerance=test_length_sec_delta)


class AudioSegmentTest(unittest.TestCase):
    def setUp(self):
        self.test_segment_1 = AudioSegment([0] * 22050, 44100)
        self.test_segment_2 = AudioSegment([0] * 22050, 22050)
        self.test_segment_3 = AudioSegment([1] * 44100, 44100, 88200)

    def test_offset_set(self):
        assert_that(self.test_segment_1.offset).is_equal_to(0)
        assert_that(self.test_segment_2.offset).is_equal_to(0)
        assert_that(self.test_segment_3.offset).is_equal_to(88200)

    def test_length_frames(self):
        assert_that(self.test_segment_1.length_frames()).is_equal_to(22050)
        assert_that(self.test_segment_2.length_frames()).is_equal_to(22050)
        assert_that(self.test_segment_3.length_frames()).is_equal_to(44100)

    def test_length_sec(self):
        assert_that(self.test_segment_1.length_sec).is_equal_to(0.5)
        assert_that(self.test_segment_2.length_sec).is_equal_to(1)
        assert_that(self.test_segment_3.length_sec).is_equal_to(1)

    def test_next_segment_offset(self):
        assert_that(self.test_segment_1.next_offset()).is_equal_to(22051)
        assert_that(self.test_segment_2.next_offset()).is_equal_to(22051)
        assert_that(self.test_segment_3.next_offset()).is_equal_to(132301)
