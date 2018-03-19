import unittest

import json
from assertpy import assert_that

from commons.models.file_meta import Mp3AudioFileMeta


class Mp3AudioFileMetaTest(unittest.TestCase):
    def setUp(self):
        self.mp3_audio_file_meta = Mp3AudioFileMeta(file_name="file.mp3", channels_count=1,
                                                    sample_rate=44100, file_size_bytes=3094, length_sec=0.5,
                                                    bit_rate_kbps=128.)

    def test_should_serialize_and_deserialize_audio_meta_file(self):
        audio_file_meta_serialized = self.mp3_audio_file_meta.to_serializable()
        new_audio_file_meta = Mp3AudioFileMeta.from_serializable(audio_file_meta_serialized)
        assert_that(new_audio_file_meta).is_equal_to(self.mp3_audio_file_meta)

    def test_should_store_as_json(self):
        audio_file_meta_serialized = self.mp3_audio_file_meta.to_serializable()
        dumps = json.dumps(audio_file_meta_serialized)
        assert_that(dumps).is_not_none()
        audio_file_meta_serialized_2 = json.loads(dumps)
        assert_that(audio_file_meta_serialized).is_equal_to(audio_file_meta_serialized_2)
