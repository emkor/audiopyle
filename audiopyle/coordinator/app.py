import logging
from logging import Logger

from flask import Flask

from audiopyle.commons.db.engine import create_db_tables
from audiopyle.commons.db.session import SessionProvider
from audiopyle.commons.repository.audio_file import AudioFileRepository
from audiopyle.commons.repository.audio_tag import AudioTagRepository
from audiopyle.commons.repository.feature_data import FeatureDataRepository
from audiopyle.commons.repository.feature_meta import FeatureMetaRepository
from audiopyle.commons.repository.metric import MetricDefinitionRepository, MetricValueRepository
from audiopyle.commons.repository.result import ResultRepository, ResultStatsRepository
from audiopyle.commons.repository.vampy_plugin import VampyPluginRepository, PluginConfigRepository
from audiopyle.commons.services.metric_config_provider import MetricConfigProvider
from audiopyle.commons.services.plugin_config_provider import PluginConfigProvider
from audiopyle.commons.services.plugin_providing import VampyPluginProvider
from audiopyle.commons.services.store_provider import Mp3FileStore, JsonFileStore
from audiopyle.commons.utils.file_system import AUDIO_FILES_DIR, CONFIG_DIR, PLUGIN_BLACKLIST_CONFIG_FILE_NAME
from audiopyle.commons.utils.logger import setup_logger, get_logger
from audiopyle.coordinator.api.audio_file import AudioFileListApi, AudioFileDetailApi
from audiopyle.coordinator.api.audio_tag import AudioTagApi
from audiopyle.coordinator.api.automation import AutomationApi
from audiopyle.coordinator.api.config import PluginActiveConfigApi, MetricActiveConfigApi
from audiopyle.coordinator.api.extraction import ExtractionStatusApi, ExtractionApi
from audiopyle.coordinator.api.metric import MetricDefinitionListApi, MetricDefinitionDetailsApi, MetricValueListApi, \
    MetricValueDetailsApi
from audiopyle.coordinator.api.plugin import PluginListApi, PluginDetailApi
from audiopyle.coordinator.api.root import CoordinatorApi
from audiopyle.coordinator.api.result import ResultListApi, ResultDataApi, ResultMetaApi, ResultStatsApi, ResultDetailsApi

app = Flask(__name__)


def main():
    setup_logger()
    logger = get_logger()
    logger.info("Initializing Coordinator app...")
    create_db_tables(only_if_absent=True)
    start_app(logger, "0.0.0.0", 8080, debug=False)


def start_app(logger: Logger, host: str, port: int, debug: bool = False):
    audio_file_store = Mp3FileStore(AUDIO_FILES_DIR)
    config_json_store = JsonFileStore(CONFIG_DIR)
    plugin_config_provider = PluginConfigProvider(config_json_store, logger)
    metric_config_provider = MetricConfigProvider(config_json_store, logger)

    plugin_provider = _initialize_plugin_provider(logger, config_json_store)
    feature_data_repo, feature_meta_repo, result_repo, result_stats_repo, metric_def_repo, metric_value_repo = _initialize_db_repositories()

    app.add_url_rule("/extraction/automation", view_func=AutomationApi.as_view('automation_api',
                                                                               plugin_provider=plugin_provider,
                                                                               plugin_config_provider=plugin_config_provider,
                                                                               metric_config_provider=metric_config_provider,
                                                                               audio_file_store=audio_file_store,
                                                                               result_repo=result_repo,
                                                                               logger=logger))
    app.add_url_rule("/extraction/<task_id>",
                     view_func=ExtractionStatusApi.as_view('extraction_status_api',
                                                           logger=logger))
    app.add_url_rule("/extraction",
                     view_func=ExtractionApi.as_view('extraction_api', logger=logger))

    app.add_url_rule("/extraction/result/<task_id>/data",
                     view_func=ResultDataApi.as_view('result_data_detail_api',
                                                     feature_data_repo=feature_data_repo,
                                                     logger=logger))
    app.add_url_rule("/extraction/result/<task_id>/meta",
                     view_func=ResultMetaApi.as_view('result_meta_detail_api',
                                                     feature_meta_repo=feature_meta_repo,
                                                     logger=logger))
    app.add_url_rule("/extraction/result/<task_id>/stats",
                     view_func=ResultStatsApi.as_view('result_stats_detail_api',
                                                      stats_repo=result_stats_repo,
                                                      logger=logger))
    app.add_url_rule("/extraction/result/<task_id>",
                     view_func=ResultDetailsApi.as_view('result_detail_api',
                                                        result_repo=result_repo,
                                                        logger=logger))
    app.add_url_rule("/extraction/result",
                     view_func=ResultListApi.as_view('result_list_api',
                                                     result_repo=result_repo,
                                                     logger=logger))
    app.add_url_rule("/plugin/<vendor>/<name>/<output>",
                     view_func=PluginDetailApi.as_view('plugin_detail_api',
                                                       plugin_provider=plugin_provider,
                                                       logger=logger))
    app.add_url_rule("/plugin",
                     view_func=PluginListApi.as_view('plugin_list_api',
                                                     plugin_provider=plugin_provider,
                                                     logger=logger))
    app.add_url_rule("/metric/def",
                     view_func=MetricDefinitionListApi.as_view('metric_definition_list_api',
                                                               metric_repo=metric_def_repo,
                                                               logger=logger))
    app.add_url_rule("/metric/def/<id>",
                     view_func=MetricDefinitionDetailsApi.as_view('metric_definition_details_api',
                                                                  metric_repo=metric_def_repo,
                                                                  logger=logger))
    app.add_url_rule("/metric/val",
                     view_func=MetricValueListApi.as_view('metric_value_list_api',
                                                          metric_repo=metric_value_repo,
                                                          logger=logger))
    app.add_url_rule("/metric/val/<id>",
                     view_func=MetricValueDetailsApi.as_view('metric_value_details_api',
                                                             metric_repo=metric_value_repo,
                                                             logger=logger))
    app.add_url_rule("/config/plugin",
                     view_func=PluginActiveConfigApi.as_view('plugin_config_api',
                                                             plugin_config_provider=plugin_config_provider,
                                                             logger=logger))
    app.add_url_rule("/config/metric",
                     view_func=MetricActiveConfigApi.as_view('metric_config_api',
                                                             metric_config_provider=metric_config_provider,
                                                             logger=logger))
    app.add_url_rule("/audio/<file_name>/tag",
                     view_func=AudioTagApi.as_view('audio_tag_api',
                                                   logger=logger))
    app.add_url_rule("/audio/<file_name>",
                     view_func=AudioFileDetailApi.as_view('audio_detail_api',
                                                          file_store=audio_file_store,
                                                          logger=logger))

    app.add_url_rule("/audio",
                     view_func=AudioFileListApi.as_view('audio_list_api',
                                                        file_store=audio_file_store,
                                                        logger=logger))

    app.add_url_rule("/", view_func=CoordinatorApi.as_view('coordinator_api', logger=logger))
    logger.info("Starting Coordinator API on {} port!".format(port))
    flask_logger = logging.getLogger('werkzeug')
    flask_logger.setLevel(logging.WARNING)
    app.run(host=host, port=port, debug=debug)


def _initialize_db_repositories():
    db_session_provider = SessionProvider()
    audio_tag_repo = AudioTagRepository(db_session_provider)
    audio_meta_repo = AudioFileRepository(db_session_provider)
    plugin_repo = VampyPluginRepository(db_session_provider)
    plugin_config_repo = PluginConfigRepository(db_session_provider)
    feature_data_repo = FeatureDataRepository(db_session_provider)
    feature_meta_repo = FeatureMetaRepository(db_session_provider)
    metric_def_repo = MetricDefinitionRepository(db_session_provider, plugin_repo)
    metric_value_repo = MetricValueRepository(db_session_provider, metric_def_repo)
    result_repo = ResultRepository(db_session_provider, audio_meta_repo, audio_tag_repo, plugin_repo,
                                   plugin_config_repo)
    result_stats_repo = ResultStatsRepository(db_session_provider)
    return feature_data_repo, feature_meta_repo, result_repo, result_stats_repo, metric_def_repo, metric_value_repo


def _initialize_plugin_provider(logger, config_store: JsonFileStore):
    blacklisted_plugins = config_store.read(PLUGIN_BLACKLIST_CONFIG_FILE_NAME)
    if blacklisted_plugins:
        logger.warning("Found {} blacklisted plugin keys: {}".format(len(blacklisted_plugins), blacklisted_plugins))
    plugin_provider = VampyPluginProvider(plugin_black_list=blacklisted_plugins, logger=logger)  # type: ignore
    return plugin_provider


if __name__ == '__main__':
    main()
