import logging
from logging import Logger

from flask import Flask

from commons.db.engine import create_db_tables
from commons.db.session import SessionProvider
from commons.repository.audio_file import AudioFileRepository
from commons.repository.audio_tag import AudioTagRepository
from commons.repository.feature_data import FeatureDataRepository
from commons.repository.feature_meta import FeatureMetaRepository
from commons.repository.result import ResultRepository, ResultStatsRepository
from commons.repository.vampy_plugin import VampyPluginRepository
from commons.services.plugin_providing import VampyPluginProvider
from commons.services.store_provider import Mp3FileStore
from commons.utils.env_var import read_env_var
from commons.utils.file_system import AUDIO_FILES_DIR
from commons.utils.logger import setup_logger, get_logger
from coordinator.api.audio_file import AudioFileListApi, AudioFileDetailApi
from coordinator.api.automation import AutomationApi
from coordinator.api.extraction import ExtractionStatusApi, ExtractionApi
from coordinator.api.plugin import PluginListApi, PluginDetailApi
from coordinator.api.root import CoordinatorApi
from coordinator.api.result import ResultListApi, ResultDataApi, ResultMetaApi, ResultStatsApi, ResultDetailsApi

app = Flask(__name__)


def main():
    setup_logger()
    logger = get_logger()
    logger.info("Initializing Coordinator app...")
    create_db_tables(only_if_absent=True)
    start_app(logger, "0.0.0.0", 8080, debug=False)


def start_app(logger: Logger, host: str, port: int, debug: bool = False):
    audio_file_store = Mp3FileStore(AUDIO_FILES_DIR)

    plugin_provider = _initialize_plugin_provider(logger)
    feature_data_repo, feature_meta_repo, result_repo, result_stats_repo = _initialize_db_repositories()

    app.add_url_rule("/automation", view_func=AutomationApi.as_view('automation_api',
                                                                    plugin_provider=plugin_provider,
                                                                    audio_file_store=audio_file_store,
                                                                    result_repo=result_repo,
                                                                    logger=logger))
    app.add_url_rule("/extraction/<task_id>",
                     view_func=ExtractionStatusApi.as_view('extraction_status_api',
                                                           logger=logger))
    app.add_url_rule("/extraction",
                     view_func=ExtractionApi.as_view('extraction_api',
                                                     logger=logger))

    app.add_url_rule("/result/<task_id>/data",
                     view_func=ResultDataApi.as_view('result_data_detail_api',
                                                     feature_data_repo=feature_data_repo,
                                                     logger=logger))
    app.add_url_rule("/result/<task_id>/meta",
                     view_func=ResultMetaApi.as_view('result_meta_detail_api',
                                                     feature_meta_repo=feature_meta_repo,
                                                     logger=logger))
    app.add_url_rule("/result/<task_id>/stats",
                     view_func=ResultStatsApi.as_view('result_stats_detail_api',
                                                      stats_repo=result_stats_repo,
                                                      logger=logger))
    app.add_url_rule("/result/<task_id>",
                     view_func=ResultDetailsApi.as_view('result_detail_api',
                                                        result_repo=result_repo,
                                                        logger=logger))
    app.add_url_rule("/result",
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
    app.add_url_rule("/audio/<identifier>",
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
    feature_data_repo = FeatureDataRepository(db_session_provider)
    feature_meta_repo = FeatureMetaRepository(db_session_provider)
    result_repo = ResultRepository(db_session_provider, audio_meta_repo, audio_tag_repo, plugin_repo)
    result_stats_repo = ResultStatsRepository(db_session_provider)
    return feature_data_repo, feature_meta_repo, result_repo, result_stats_repo


def _initialize_plugin_provider(logger):
    blacklisted_plugins = read_env_var(var_name="BLACKLISTED_PLUGINS", expected_type=str, default="").split(",")
    if blacklisted_plugins:
        logger.warning("Found {} blacklisted plugin keys: {}".format(len(blacklisted_plugins), blacklisted_plugins))
    plugin_provider = VampyPluginProvider(plugin_black_list=blacklisted_plugins, logger=logger)
    return plugin_provider


if __name__ == '__main__':
    main()
