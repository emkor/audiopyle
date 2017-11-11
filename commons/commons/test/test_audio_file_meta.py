import unittest

import json
from assertpy import assert_that

from commons.audio.file_meta import WavAudioFileMeta, Mp3AudioFileMeta


class WavAudioFileMetaTest(unittest.TestCase):
    def setUp(self):
        self.wav_audio_file_meta = WavAudioFileMeta(absolute_path="/some/file.wav", channels_count=2,
                                                    sample_rate=44100, frames_count=22050, bit_depth=16,
                                                    file_size_bytes=88200)
        self.wav_audio_file_meta_avg_kbps = 1410.0
        self.wav_audio_file_meta_length_seconds = 0.5

    def test_should_calculate_properties_correctly(self):
        assert_that(self.wav_audio_file_meta.bit_rate_kbps).is_equal_to(self.wav_audio_file_meta_avg_kbps)
        assert_that(self.wav_audio_file_meta.length_sec).is_equal_to(self.wav_audio_file_meta_length_seconds)

    def test_should_serialize_and_deserialize_audio_meta_file(self):
        audio_file_meta_serialized = self.wav_audio_file_meta.serialize()
        new_audio_file_meta = WavAudioFileMeta.deserialize(audio_file_meta_serialized)
        assert_that(new_audio_file_meta).is_equal_to(self.wav_audio_file_meta)

    def test_should_store_as_json(self):
        audio_file_meta_serialized = self.wav_audio_file_meta.serialize()
        dumps = json.dumps(audio_file_meta_serialized)
        assert_that(dumps).is_not_none()
        audio_file_meta_serialized_2 = json.loads(dumps)
        assert_that(audio_file_meta_serialized).is_equal_to(audio_file_meta_serialized_2)


class Mp3AudioFileMetaTest(unittest.TestCase):
    def setUp(self):
        self.mp3_audio_file_meta = Mp3AudioFileMeta(absolute_path="/some/file.mp3", channels_count=1,
                                                    sample_rate=44100, file_size_bytes=3094, length_sec=0.5,
                                                    bit_rate_kbps=128.)

    def test_should_serialize_and_deserialize_audio_meta_file(self):
        audio_file_meta_serialized = self.mp3_audio_file_meta.serialize()
        new_audio_file_meta = Mp3AudioFileMeta.deserialize(audio_file_meta_serialized)
        assert_that(new_audio_file_meta).is_equal_to(self.mp3_audio_file_meta)

    def test_should_store_as_json(self):
        audio_file_meta_serialized = self.mp3_audio_file_meta.serialize()
        dumps = json.dumps(audio_file_meta_serialized)
        assert_that(dumps).is_not_none()
        audio_file_meta_serialized_2 = json.loads(dumps)
        assert_that(audio_file_meta_serialized).is_equal_to(audio_file_meta_serialized_2)
