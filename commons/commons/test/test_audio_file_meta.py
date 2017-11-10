import unittest

import json
from assertpy import assert_that

from commons.audio.file_meta import LocalAudioFileMeta


class AudioFileMetaTest(unittest.TestCase):
    def setUp(self):
        self.audio_file_meta = LocalAudioFileMeta(absolute_path="/some/file.wav", channels_count=2,
                                                  sample_rate=44100, frames_count=22050, bit_depth=16)

    def test_should_serialize_and_deserialize_audio_meta_file(self):
        audio_file_meta_serialized = self.audio_file_meta.serialize()
        new_audio_file_meta = LocalAudioFileMeta.deserialize(audio_file_meta_serialized)
        assert_that(new_audio_file_meta).is_equal_to(self.audio_file_meta)

    def test_should_store_as_json(self):
        audio_file_meta_serialized = self.audio_file_meta.serialize()
        dumps = json.dumps(audio_file_meta_serialized)
        assert_that(dumps).is_not_none()
        audio_file_meta_serialized_2 = json.loads(dumps)
        assert_that(audio_file_meta_serialized).is_equal_to(audio_file_meta_serialized_2)
