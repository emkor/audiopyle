from __future__ import absolute_import, unicode_literals

import os

from commons.audio.segment_providing import read_audio_file_meta, read_segment
from commons.services.extraction import extract_features, ExtractionRequest
from commons.utils.file_system import AUDIO_FILES_DIR
from commons.utils.logger import get_logger
from commons.vampy.plugin_providing import build_plugin_from_key
from extractor.celery import app

logger = get_logger()


@app.task
def add(x, y):
    return x + y


@app.task
def extract_feature(extraction_request):
    request = ExtractionRequest.deserialize(extraction_request)
    logger.info("Building context for: {}...".format(request))
    audio_file_absolute_path = os.path.join(AUDIO_FILES_DIR, request.audio_file_name)
    audio_file_meta = read_audio_file_meta(audio_file_absolute_path)
    audio_segment = read_segment(audio_file_meta)
    plugin = build_plugin_from_key(str(request.plugin_key))
    logger.info("Built extraction context: {} {} {}".format(audio_segment, plugin, request.plugin_output))
    logger.info("Starting feature extraction...")
    feature = extract_features(audio_segment, plugin, str(request.plugin_output))
    logger.info("Extracted {} feature!".format(feature.__class__.__name__))
    return feature.serialize()
