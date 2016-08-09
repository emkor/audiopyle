import unittest

from assertpy import assert_that

from xtracter.model.audio_meta import AudioMeta
from xtracter.model.audio_segment import AudioSegmentMeta
from xtracter.model.feature import RawFeature, AudioFeature


class ModelsToJsonTest(unittest.TestCase):
    def setUp(self):
        self.audio_meta_example = AudioMeta(filename="/tmp/some_file.wav", channels_count=1, sample_rate=44100,
                                            frames_count=22050, bit_depth=16)
        self.audio_segment_meta = AudioSegmentMeta(sample_rate=44100, length=22050)
        self.raw_feature_1 = RawFeature(timestamp=0, value=0.18)
        self.raw_feature_2 = RawFeature(timestamp=0, value=0.34)
        self.audio_feature = AudioFeature(audio_meta=self.audio_meta_example, segment_meta=self.audio_segment_meta,
                                          plugin_key="bbc:rhytm", plugin_output="rhytm_strength",
                                          raw_features=[self.raw_feature_1, self.raw_feature_2])

    def test_audio_meta_json(self):
        json_output = self.audio_meta_example.to_json()
        expected_labels = ["filename", "channels_count", "sample_rate", "frames_count", "bit_depth"]
        expected_values = [self.audio_meta_example.filename, self.audio_meta_example.channels_count,
                           self.audio_meta_example.sample_rate, self.audio_meta_example.frames_count,
                           self.audio_meta_example.bit_depth]
        self._test_json(json_output, expected_labels, expected_values)

    def test_audio_segment_meta_json(self):
        json_output = self.audio_segment_meta.to_json()
        expected_labels = ["sample_rate", "length"]
        expected_values = [self.audio_segment_meta.sample_rate, self.audio_segment_meta.length]
        self._test_json(json_output, expected_labels, expected_values)

    def test_raw_feature_json(self):
        json_output = self.raw_feature_1.to_json()
        expected_labels = ["timestamp", "value"]
        expected_values = [self.raw_feature_1.timestamp, self.raw_feature_1.value]
        self._test_json(json_output, expected_labels, expected_values)

    def test_audio_feature_json(self):
        json_output = self.audio_feature.to_json()
        expected_labels = ["audio_meta", "segment_meta", "plugin_key", "plugin_output", "raw_features"]
        expected_values = [self.audio_feature.plugin_key, self.audio_feature.plugin_output]
        self._test_json(json_output, expected_labels, expected_values)

    def _test_json(self, json_output, expected_labels, expected_values):
        expected_labels_stringified = [str(value) for value in expected_values]
        assert_that(json_output).contains(*expected_labels)
        assert_that(json_output).contains(*expected_labels_stringified)
