from commons.provider.redis_queue_client import RedisQueueClient
from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor
from commons.utils.constant import AudiopyleConst
from commons.utils.logging_setup import GetLogger

from commons.model.b2_config import B2Config
from commons.provider.b2_audio_provider import B2AudioProvider
from xtracter.provider.audio_meta_provider import LocalAudioMetaProvider
from xtracter.provider.audio_segment_provider import LocalAudioSegmentProvider
from xtracter.provider.plugin_provider import VampyPluginProvider
from xtracter.service.feature_extractor import FeatureExtractor
from xtracter.service.segment_analyzer import AudioSegmentAnalyzer
from xtracter.service.xtracter_service import Xtracter


AUDIO_FILES_PATH = FileAccessor.join(OsEnvAccessor.get_env_variable("AUDIOPYLE_HOME"), "xtracter", "wav_temp")
TASK_QUEUE_NAME = "xtracter_tasks"
RESULTS_QUEUE_NAME = "xtracter_results"

logger = GetLogger()
audio_meta_provider = LocalAudioMetaProvider()
segment_provider = LocalAudioSegmentProvider(audio_files_path=AUDIO_FILES_PATH)
plugin_provider = VampyPluginProvider()
segment_analyzer = AudioSegmentAnalyzer()
feature_extractor = FeatureExtractor(segment_provider=segment_provider, plugin_provider=plugin_provider,
                                     segment_analyzer=segment_analyzer)

b2_config = B2Config(AudiopyleConst.B2_ACCOUNT_ID, AudiopyleConst.B2_APPLICATION_KEY,
                     AudiopyleConst.B2_RESOURCES_BUCKET)
b2_client = B2AudioProvider(b2_config=b2_config, local_wave_dir=AUDIO_FILES_PATH)
redis_task_queue_client = RedisQueueClient(queue_name=TASK_QUEUE_NAME)
redis_results_queue_client = RedisQueueClient(queue_name=RESULTS_QUEUE_NAME)

# CREATE Xtracter SERVICE INSTANCE
logger.info("Initializing xtracter...")
xtracter_service = Xtracter(feature_extractor=feature_extractor, audio_meta_provider=audio_meta_provider,
                            b2_client=b2_client, redis_task_client=redis_task_queue_client,
                            redis_results_client=redis_results_queue_client)

# STARTING FEATURE EXTRACTION
logger.info("Starting xtracter...")
xtracter_service.init()
