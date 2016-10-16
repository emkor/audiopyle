import unittest

from assertpy import assert_that
from mock import Mock

from commons.model.analysis_result import AnalysisResult
from commons.model.analysis_task import AnalysisTask
from commons.model.audio_meta import AudioMeta
from commons.model.audio_segment import AudioSegmentMeta
from commons.model.feature import AudioFeature
from commons.model.remote_file_meta import RemoteFileMeta
from commons.model.remote_file_source import RemoteFileSource
from commons.provider.b2_audio_provider import B2AudioProvider
from commons.provider.redis_queue_client import RedisQueueClient
from xtracter.provider.audio_meta_provider import LocalAudioMetaProvider
from xtracter.service.feature_extractor import FeatureExtractor
from xtracter.service.xtracter_service import Xtracter


class XtracterTest(unittest.TestCase):
    def setUp(self):
        self.feature_extractor = Mock(FeatureExtractor)
        self.remote_file_provider = Mock(B2AudioProvider)
        self.meta_provider = Mock(LocalAudioMetaProvider)
        self.task_queue = Mock(RedisQueueClient)
        self.results_queue = Mock(RedisQueueClient)
        self.xtracter = Xtracter(self.feature_extractor, self.meta_provider, self.remote_file_provider, self.task_queue,
                                 self.results_queue)
        self.audio_meta = AudioMeta("102bpm_drum_loop_mono_44.1k.wav", 1, 44100, 200000, 16)

    def test_should_call_services_when_downloading_file(self):
        # given
        remote_file_meta = RemoteFileMeta("test/102bpm_drum_loop_mono_44.1k.wav", 2651512, 1467569053000)
        remote_file_source = RemoteFileSource("b2", "address", "bucket_name", "password")
        analysis_task = AnalysisTask(remote_file_meta, remote_file_source)
        mocked_local_path = "/some_path/102bpm_drum_loop_mono_44.1k.wav"
        self.remote_file_provider.download.return_value = mocked_local_path
        self.meta_provider.read_meta_from.return_value = self.audio_meta
        # when
        actual_audio_meta_output = self.xtracter._download_file(analysis_task)
        # then
        self.remote_file_provider.download.assert_called_once_with(remote_file_source, remote_file_meta)
        self.meta_provider.read_meta_from.assert_called_once_with("/some_path/102bpm_drum_loop_mono_44.1k.wav")
        assert_that(actual_audio_meta_output).is_equal_to(self.audio_meta)

    def test_should_call_services_when_extracting_features(self):
        # given
        expected_extracted_features = [AudioFeature(self.audio_meta, None, None, None, None)]
        self.feature_extractor.extract.return_value = expected_extracted_features
        # when
        actual_extracted_features = self.xtracter._extract_features(self.audio_meta)
        self.feature_extractor.extract.assert_called_once_with(self.audio_meta)
        assert_that(actual_extracted_features).is_equal_to(expected_extracted_features)

    def test_should_call_services_when_sending_results_to_redis(self):
        # given
        result = AnalysisResult(analysis_task=Mock(AnalysisTask),
                                features=[AudioFeature(self.audio_meta, Mock(AudioSegmentMeta), "", "", []),
                                          AudioFeature(self.audio_meta, Mock(AudioSegmentMeta), "", "", [])])
        # when
        self.xtracter._send_to_redis(result)
        # then
        self.results_queue.add.assert_called_once_with(result.to_dict())
