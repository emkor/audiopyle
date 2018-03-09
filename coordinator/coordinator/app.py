from logging import Logger

from flask import Flask

from commons.utils.logger import setup_logger, get_logger
from coordinator.api.audio_file import AudioFileApi
from coordinator.api.audio_meta import AudioMetaApi, AudioTagApi
from coordinator.api.automation import AutomationApi
from coordinator.api.plugin import PluginApi
from coordinator.api.root import CoordinatorApi
from coordinator.api.extraction import ExtractionApi, ResultApi

app = Flask(__name__)


def main():
    setup_logger()
    logger = get_logger()
    logger.info("Initializing Coordinator app...")
    start_app(logger, "0.0.0.0", 8080, debug=False)


def start_app(logger: Logger, host: str, port: int, debug: bool = False):
    app.add_url_rule("/automation", view_func=AutomationApi.as_view('automation_api', logger=logger))
    app.add_url_rule("/extraction", view_func=ExtractionApi.as_view('extraction_api', logger=logger))
    app.add_url_rule("/result/<task_id>", view_func=ResultApi.as_view('result_api', logger=logger))
    app.add_url_rule("/plugin", view_func=PluginApi.as_view('plugin_api', logger=logger))
    app.add_url_rule("/audio/meta/<identifier>", view_func=AudioMetaApi.as_view('audio_meta_api', logger=logger))
    app.add_url_rule("/audio/tag/<identifier>", view_func=AudioTagApi.as_view('audio_tag_api', logger=logger))
    app.add_url_rule("/audio", view_func=AudioFileApi.as_view('audio_api', logger=logger))
    app.add_url_rule("/", view_func=CoordinatorApi.as_view('coordinator_api', logger=logger))
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
