import unittest

from assertpy import assert_that
from datetime import datetime

from commons.models.audio_tag import Id3Tag
from commons.models.file_meta import FileMeta, Mp3AudioFileMeta, WavAudioFileMeta
from commons.models.result import AnalysisResultData, ResultVersion, FeatureType, AnalysisResult
from commons.utils.serialization import to_json


class AnalysisResultDataModelTest(unittest.TestCase):
    def setUp(self):
        self.result_data_example = AnalysisResultData(ResultVersion.V1, "fa3b5d8c-b760-49e0-b8b5-7ce0737621d8",
                                                      FeatureType.ConstantStepFeature)

    def test_should_serialize_and_deserialize_analysis_result_data_model(self):
        serialized = self.result_data_example.to_serializable()
        deserialized = AnalysisResultData.from_serializable(serialized)
        assert_that(deserialized).is_not_none().is_equal_to(self.result_data_example)

    def test_should_serialized_to_json(self):
        as_json = to_json(self.result_data_example.to_serializable())
        assert_that(as_json).is_not_none().is_not_empty()


class AnalysisResultModelTest(unittest.TestCase):
    def setUp(self):
        self.file_meta_example = FileMeta("some_file.mp3", 1024 * 1024 * 2,
                                          datetime(2017, 3, 23, 12, 0, 0),
                                          datetime(2017, 3, 23, 11, 0, 0),
                                          datetime(2017, 3, 23, 10, 0, 0))
        self.audio_meta_example = Mp3AudioFileMeta("/audio/some_file.mp3", 1024 * 1024 * 2, 1, 44100, 45., 128.)
        self.raw_audio_meta_example = WavAudioFileMeta("/audio/some_file.wav", 1024 * 1024 * 8, 1, 16, 44100,
                                                       45 * 44100)
        self.id3_tag_example = Id3Tag(artist="Unknown Artist", title="Unknown Title", album="Unknown Album",
                                      date=2017, track=1, genre="Unknown Genre")
        self.result_data_example = AnalysisResultData(ResultVersion.V1, "fa3b5d8c-b760-49e0-b8b5-7ce0737621d8",
                                                      FeatureType.ConstantStepFeature)
        self.analysis_result_example = AnalysisResult(self.file_meta_example, self.audio_meta_example,
                                                      self.raw_audio_meta_example, self.id3_tag_example,
                                                      self.result_data_example)

    def test_should_serialize_and_deserialize_analysis_result_data_model(self):
        serialized = self.analysis_result_example.to_serializable()
        deserialized = AnalysisResult.from_serializable(serialized)
        assert_that(deserialized).is_not_none().is_equal_to(self.analysis_result_example)

    def test_should_serialized_to_json(self):
        as_json = to_json(self.analysis_result_example.to_serializable())
        assert_that(as_json).is_not_none().is_not_empty()
