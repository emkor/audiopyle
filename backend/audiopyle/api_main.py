#!/usr/bin/env python3

import logging
from logging import Logger

from flask import Flask
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

from audiopyle.lib.db.engine import create_db_tables
from audiopyle.lib.db.session import SessionProvider
from audiopyle.lib.repository.audio_file import AudioFileRepository
from audiopyle.lib.repository.audio_tag import AudioTagRepository
from audiopyle.lib.repository.feature_data import FeatureDataRepository
from audiopyle.lib.repository.feature_meta import FeatureMetaRepository
from audiopyle.lib.repository.metric import MetricDefinitionRepository, MetricValueRepository
from audiopyle.lib.repository.request import RequestRepository
from audiopyle.lib.repository.stats import ResultStatsRepository
from audiopyle.lib.repository.vampy_plugin import VampyPluginRepository, PluginConfigRepository
from audiopyle.lib.services.metric_config_provider import MetricConfigProvider
from audiopyle.lib.services.plugin_config_provider import PluginConfigProvider
from audiopyle.lib.services.plugin_providing import VampyPluginProvider
from audiopyle.lib.services.store_provider import Mp3FileStore, JsonFileStore
from audiopyle.lib.utils.env_var import read_env_var
from audiopyle.lib.utils.file_system import AUDIO_FILES_DIR, CONFIG_DIR, PLUGIN_BLACKLIST_CONFIG_FILE_NAME
from audiopyle.lib.utils.logger import setup_logger, get_logger
from audiopyle.api.audio_file import AudioFileListApi, AudioFileDetailApi
from audiopyle.api.audio_tag import AudioTagApi
from audiopyle.api.automation import AutomationApi
from audiopyle.api.config import PluginActiveConfigApi, MetricActiveConfigApi
from audiopyle.api.metric import MetricDefinitionListApi, MetricDefinitionDetailsApi, MetricValueListApi, \
    MetricValueDetailsApi
from audiopyle.api.plugin import PluginListApi, PluginDetailApi
from audiopyle.api.root import CoordinatorApi
from audiopyle.api.result import ResultDataApi, ResultMetaApi, ResultStatsApi
from audiopyle.api.request import RequestListApi, RequestDetailsApi, RequestStatusApi

app = Flask(__name__)

allowed_origins = read_env_var("API_ALLOWED_ORIGIN", str, "http://localhost:8008,http://ui.local:8080").split(",")
cors = CORS(app, origins=allowed_origins, methods=["GET", "POST", "DELETE", "PUT"])

def main():
    setup_logger()
    logger = get_logger()
    logger.info("Initializing Coordinator app...")
    create_db_tables(only_if_absent=True)
    start_app(logger, "0.0.0.0", 8080)


def start_app(logger: Logger, host: str, port: int):
    audio_file_store = Mp3FileStore(AUDIO_FILES_DIR)
    config_json_store = JsonFileStore(CONFIG_DIR)
    plugin_config_provider = PluginConfigProvider(config_json_store, logger)
    metric_config_provider = MetricConfigProvider(config_json_store, logger)

    plugin_provider = _initialize_plugin_provider(logger, config_json_store)
    feature_data_repo, feature_meta_repo, request_repo, result_stats_repo, metric_def_repo, metric_value_repo = _initialize_db_repositories()

    app.add_url_rule("/request/automation",
                     view_func=AutomationApi.as_view('automation_api',
                                                     plugin_provider=plugin_provider,
                                                     plugin_config_provider=plugin_config_provider,
                                                     metric_config_provider=metric_config_provider,
                                                     audio_file_store=audio_file_store,
                                                     result_repo=request_repo))

    app.add_url_rule("/request",
                     view_func=RequestListApi.as_view('request_list_api',
                                                      request_repo=request_repo))

    app.add_url_rule("/request/<task_id>",
                     view_func=RequestDetailsApi.as_view('request_detail_api',
                                                         request_repo=request_repo))
    app.add_url_rule("/request/<task_id>/status",
                     view_func=RequestStatusApi.as_view('request_status_api'))
    app.add_url_rule("/request/<task_id>/data",
                     view_func=ResultDataApi.as_view('result_data_detail_api',
                                                     feature_data_repo=feature_data_repo))
    app.add_url_rule("/request/<task_id>/meta",
                     view_func=ResultMetaApi.as_view('result_meta_detail_api',
                                                     feature_meta_repo=feature_meta_repo))
    app.add_url_rule("/request/<task_id>/stats",
                     view_func=ResultStatsApi.as_view('result_stats_detail_api',
                                                      stats_repo=result_stats_repo))
    app.add_url_rule("/request/<task_id>/metric",
                     view_func=MetricValueListApi.as_view('metric_value_list_by_request_api',
                                                          metric_repo=metric_value_repo))
    app.add_url_rule("/request/<task_id>/metric/<name>",
                     view_func=MetricValueDetailsApi.as_view('metric_value_details_by_request_api',
                                                             metric_repo=metric_value_repo))
    app.add_url_rule("/plugin/<vendor>/<name>/<output>",
                     view_func=PluginDetailApi.as_view('plugin_detail_api',
                                                       plugin_provider=plugin_provider))
    app.add_url_rule("/plugin",
                     view_func=PluginListApi.as_view('plugin_list_api',
                                                     plugin_provider=plugin_provider))
    app.add_url_rule("/metric",
                     view_func=MetricDefinitionListApi.as_view('metric_definition_list_api',
                                                               metric_repo=metric_def_repo))
    app.add_url_rule("/metric/<name>",
                     view_func=MetricDefinitionDetailsApi.as_view('metric_definition_details_api',
                                                                  metric_repo=metric_def_repo))
    app.add_url_rule("/metric/<name>/values",
                     view_func=MetricValueListApi.as_view('metric_value_list_by_definition_api',
                                                          metric_repo=metric_value_repo))
    app.add_url_rule("/metric/<name>/values/<task_id>",
                     view_func=MetricValueDetailsApi.as_view('metric_value_details_by_definition_api',
                                                             metric_repo=metric_value_repo))
    app.add_url_rule("/config/plugin",
                     view_func=PluginActiveConfigApi.as_view('plugin_config_api',
                                                             plugin_config_provider=plugin_config_provider))
    app.add_url_rule("/config/metric",
                     view_func=MetricActiveConfigApi.as_view('metric_config_api',
                                                             metric_config_provider=metric_config_provider))
    app.add_url_rule("/audio",
                     view_func=AudioFileListApi.as_view('audio_list_api',
                                                        file_store=audio_file_store))
    app.add_url_rule("/audio/<file_name>/tag",
                     view_func=AudioTagApi.as_view('audio_tag_api'))
    app.add_url_rule("/audio/<file_name>",
                     view_func=AudioFileDetailApi.as_view('audio_detail_api',
                                                          file_store=audio_file_store))
    app.add_url_rule("/", view_func=CoordinatorApi.as_view('coordinator_api'))
    logger.info("Starting API on {} port!".format(port))
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('flask_cors').setLevel(logging.WARNING)
    WSGIServer((host, port), app).serve_forever()


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
    request_repo = RequestRepository(db_session_provider, audio_meta_repo, audio_tag_repo, plugin_repo,
                                     plugin_config_repo)
    result_stats_repo = ResultStatsRepository(db_session_provider)
    return feature_data_repo, feature_meta_repo, request_repo, result_stats_repo, metric_def_repo, metric_value_repo


def _initialize_plugin_provider(logger, config_store: JsonFileStore):
    blacklisted_plugins = config_store.read(PLUGIN_BLACKLIST_CONFIG_FILE_NAME)
    if blacklisted_plugins:
        logger.warning("Found {} blacklisted plugin keys: {}".format(len(blacklisted_plugins), blacklisted_plugins))
    plugin_provider = VampyPluginProvider(plugin_black_list=blacklisted_plugins, logger=logger)  # type: ignore
    return plugin_provider


if __name__ == '__main__':
    main()
