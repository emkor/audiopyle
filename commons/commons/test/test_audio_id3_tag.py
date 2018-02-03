import unittest

import json
from assertpy import assert_that

from commons.models.audio_tag import Id3Tag


class AudioFileId3TagTest(unittest.TestCase):
    def setUp(self):
        self.id3_tag = Id3Tag(artist="Pink Floyd", title="Have a cigar", album="Wish you were here",
                              date=1975, track=3, genre="Progressive rock")

    def test_should_serialize_and_deserialize_id3_tag_object(self):
        serialized = self.id3_tag.to_serializable()
        deserialized = Id3Tag.from_serializable(serialized=serialized)
        assert_that(deserialized).is_equal_to(self.id3_tag)

    def test_should_be_serialized_to_json(self):
        serialized = self.id3_tag.to_serializable()
        serialized_to_json = json.dumps(serialized)
        assert_that(serialized_to_json).is_not_none()

        deserialized_from_json = json.loads(serialized_to_json)
        object_again = Id3Tag.from_serializable(serialized=deserialized_from_json)
        assert_that(object_again).is_equal_to(self.id3_tag)
