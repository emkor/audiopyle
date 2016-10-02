import unittest

from assertpy import assert_that

from commons.model.audio_meta import AudioMeta
from commons.model.audio_segment import AudioSegmentMeta
from commons.model.feature import RawFeature, AudioFeature


class ModelsToDictTest(unittest.TestCase):
    def setUp(self):
        self.audio_meta_example = AudioMeta(filename="/tmp/some_file.wav", channels_count=1, sample_rate=44100,
                                            frames_count=22050, bit_depth=16)
        self.audio_segment_meta = AudioSegmentMeta(sample_rate=44100, length=22050)
        self.raw_feature_1 = RawFeature(timestamp=0, value=0.18)
        self.raw_feature_2 = RawFeature(timestamp=0, value=0.34)
        self.audio_feature = AudioFeature(audio_meta=self.audio_meta_example, segment_meta=self.audio_segment_meta,
                                          plugin_key="bbc:rhytm", plugin_output="rhytm_strength",
                                          raw_features=[self.raw_feature_1, self.raw_feature_2])

    def test_audio_meta_to_dict(self):
        dict_output = self.audio_meta_example.to_dict()
        expected_labels = ["filename", "channels_count", "sample_rate", "frames_count", "bit_depth"]
        expected_values = [self.audio_meta_example.filename, self.audio_meta_example.channels_count,
                           self.audio_meta_example.sample_rate, self.audio_meta_example.frames_count,
                           self.audio_meta_example.bit_depth]
        self._test_to_dict(dict_output, expected_labels, expected_values)

    def test_audio_segment_meta_dict(self):
        dict_output = self.audio_segment_meta.to_dict()
        expected_labels = ["sample_rate", "length"]
        expected_values = [self.audio_segment_meta.sample_rate, self.audio_segment_meta.length]
        self._test_to_dict(dict_output, expected_labels, expected_values)

    def test_raw_feature_to_dict(self):
        dict_output = self.raw_feature_1.to_dict()
        expected_labels = ["timestamp", "value"]
        expected_values = [self.raw_feature_1.timestamp, self.raw_feature_1.value]
        self._test_to_dict(dict_output, expected_labels, expected_values)

    def test_audio_feature_to_dict(self):
        dict_output = self.audio_feature.to_dict()
        expected_labels = ["audio_meta", "segment_meta", "plugin_key", "plugin_output", "raw_features"]
        expected_values = [self.audio_feature.plugin_key, self.audio_feature.plugin_output]
        self._test_to_dict(dict_output, expected_labels, expected_values)

    def _test_to_dict(self, dict_output, expected_labels, expected_values):
        assert_that(dict_output.keys()).contains(*expected_labels)
        assert_that(dict_output.values()).contains(*expected_values)
