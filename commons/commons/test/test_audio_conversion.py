import unittest
from datetime import datetime, timedelta

from assertpy import assert_that

from commons.services.audio_conversion import generate_output_wav_file_path, convert_to_wav
from commons.services.file_meta_providing import read_file_meta
from commons.test.utils import TEST_MP3_AUDIO_FILE, get_absolute_path_for_project_file
from commons.utils.conversion import seconds_between
from commons.utils.file_system import TMP_DIR, remove_file, file_exists


class AudioConversionTest(unittest.TestCase):
    def setUp(self):
        self.example_task_id = "aaaa-bbbb-cccc"
        self.mp3_audio_file_path = get_absolute_path_for_project_file(__file__, TEST_MP3_AUDIO_FILE)
        self.mp3_raw_file_meta = read_file_meta(self.mp3_audio_file_path)

    def test_should_generate_proper_output_file_name(self):
        output_wav_file = generate_output_wav_file_path(self.example_task_id)
        assert_that(output_wav_file).is_equal_to("{}/{}.wav".format(TMP_DIR, self.example_task_id))

    def test_should_convert_mp3_audio_to_wav(self):
        output_path = self.mp3_audio_file_path + ".wav"
        converted_path = convert_to_wav(self.mp3_audio_file_path, output_path)
        assert_that(file_exists(converted_path)).is_true()
        assert_that(converted_path).is_equal_to(output_path)
        wav_file_meta = read_file_meta(converted_path)
        assert_that(wav_file_meta.size_bytes()).is_greater_than(self.mp3_raw_file_meta.size_bytes())
        remove_file(converted_path)
        assert_that(file_exists(converted_path)).is_false()


class ConversionUtilsTest(unittest.TestCase):
    def test_should_measure_seconds_since_event(self):
        start_point = datetime.utcnow() - timedelta(seconds=1.5)
        time_that_passed = seconds_between(start_point)
        assert_that(time_that_passed).is_between(1.5, 2.0)

    def test_should_measure_seconds_between_events(self):
        end_point = datetime.utcnow()
        start_point = end_point - timedelta(seconds=2.5)
        time_that_passed = seconds_between(start_point, end_point)
        assert_that(time_that_passed).is_between(2.499, 2.501)
