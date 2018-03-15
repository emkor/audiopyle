import logging
from logging import Logger

from flask import Flask

from commons.db.engine import create_db_tables
from commons.services.plugin_providing import VampyPluginProvider
from commons.services.store_provider import Mp3FileStore, LzmaJsonFileStore
from commons.utils.env_var import read_env_var
from commons.utils.file_system import AUDIO_FILES_DIR, RESULTS_DIR
from commons.utils.logger import setup_logger, get_logger
from coordinator.api.audio_file import AudioFileListApi, AudioFileDetailApi
from coordinator.api.automation import AutomationApi
from coordinator.api.extraction import ExtractionStatusApi, ExtractionApi
from coordinator.api.plugin import PluginListApi, PluginDetailApi
from coordinator.api.root import CoordinatorApi
from coordinator.api.result import ResultListApi, ResultDetailsApi

app = Flask(__name__)


def main():
    setup_logger()
    logger = get_logger()
    logger.info("Initializing Coordinator app...")
    flask_logger = logging.getLogger('werkzeug')
    flask_logger.setLevel(logging.WARNING)
    create_db_tables()
    start_app(logger, "0.0.0.0", 8080, debug=False)


def start_app(logger: Logger, host: str, port: int, debug: bool = False):
    audio_file_store = Mp3FileStore(AUDIO_FILES_DIR)

    blacklisted_plugins = read_env_var(var_name="BLACKLISTED_PLUGINS", expected_type=str, default="").split(",")
    plugin_provider = VampyPluginProvider(plugin_black_list=blacklisted_plugins, logger=logger)

    result_data_file_store = LzmaJsonFileStore(RESULTS_DIR, extension="data.json.lzma")
    result_meta_file_store = LzmaJsonFileStore(RESULTS_DIR, extension="meta.json.lzma")
    result_stats_file_store = LzmaJsonFileStore(RESULTS_DIR, extension="stats.json.lzma")

    app.add_url_rule("/automation", view_func=AutomationApi.as_view('automation_api',
                                                                    plugin_provider=plugin_provider,
                                                                    audio_file_store=audio_file_store,
                                                                    logger=logger))
    app.add_url_rule("/extraction/<task_id>",
                     view_func=ExtractionStatusApi.as_view('extraction_status_api',
                                                           logger=logger))
    app.add_url_rule("/extraction",
                     view_func=ExtractionApi.as_view('extraction_api',
                                                     logger=logger))
    app.add_url_rule("/result/<task_id>/data",
                     view_func=ResultDetailsApi.as_view('result_data_detail_api',
                                                        file_store=result_data_file_store,
                                                        logger=logger))
    app.add_url_rule("/result/<task_id>/meta",
                     view_func=ResultDetailsApi.as_view('result_meta_detail_api',
                                                        file_store=result_meta_file_store,
                                                        logger=logger))
    app.add_url_rule("/result/<task_id>/stats",
                     view_func=ResultDetailsApi.as_view('result_stats_detail_api',
                                                        file_store=result_stats_file_store,
                                                        logger=logger))
    app.add_url_rule("/result",
                     view_func=ResultListApi.as_view('result_list_api',
                                                     file_store=result_data_file_store,
                                                     logger=logger))
    app.add_url_rule("/plugin/<vendor>/<name>",
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
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
