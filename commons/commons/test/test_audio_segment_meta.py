import unittest

import json
from assertpy import assert_that

from commons.models.file_meta import WavAudioFileMeta
from commons.models.segment import AudioSegmentMeta


class AudioSegmentMetaTest(unittest.TestCase):
    def setUp(self):
        self.audio_file_meta = WavAudioFileMeta(absolute_path="/some/file.wav", channels_count=2,
                                                sample_rate=44100, frames_count=22050, bit_depth=16)
        self.audio_segment_meta = AudioSegmentMeta(self.audio_file_meta, frame_from=0, frame_to=22049)

    def test_should_calculate_properties_correctly(self):
        assert_that(self.audio_segment_meta.length_frames()).is_equal_to(self.audio_file_meta.frames_count)
        assert_that(self.audio_segment_meta.length_sec()).is_equal_to(self.audio_file_meta.length_sec)

    def test_serializing_and_deserializing(self):
        segment_meta_serialized = self.audio_segment_meta.to_serializable()
        assert_that(segment_meta_serialized).is_not_none()

        segment_meta_deserialized = AudioSegmentMeta.from_serializable(segment_meta_serialized)
        assert_that(segment_meta_deserialized).is_equal_to(self.audio_segment_meta)

    def test_serializing_to_json(self):
        segment_meta_as_json = json.dumps(self.audio_segment_meta.to_serializable())
        assert_that(segment_meta_as_json).is_not_none()

        segment_meta_deserialized = AudioSegmentMeta.from_serializable(json.loads(segment_meta_as_json))
        assert_that(segment_meta_deserialized).is_equal_to(self.audio_segment_meta)
