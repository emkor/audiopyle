from __future__ import absolute_import, unicode_literals

import os
from datetime import datetime
from typing import Any, Text, Dict

from mutagen.easyid3 import EasyID3
from pydub import AudioSegment

from commons.audio.audio_tag import Id3Tag
from commons.audio.segment_providing import read_audio_file_meta, read_segment
from commons.services.extraction import extract_features, ExtractionRequest
from commons.utils.conversion import seconds_between, safe_cast
from commons.utils.file_system import AUDIO_FILES_DIR, extract_extension
from commons.utils.logger import get_logger
from commons.vampy.plugin_providing import build_plugin_from_key
from extractor.celery import app

logger = get_logger()


@app.task
def extract_feature(extraction_request: Dict[Text, Any]) -> Dict[Text, Any]:
    request = ExtractionRequest.deserialize(extraction_request)
    logger.info("Building context for extraction: {}...".format(request))
    audio_file_absolute_path = os.path.join(AUDIO_FILES_DIR, request.audio_file_name)
    audio_file_meta = read_audio_file_meta(audio_file_absolute_path)
    audio_segment = read_segment(audio_file_meta)
    plugin = build_plugin_from_key(str(request.plugin_key))
    logger.info("Built extraction context: {} {} {}".format(audio_segment, plugin, request.plugin_output))
    logger.info("Starting feature extraction...")
    feature = extract_features(audio_segment, plugin, str(request.plugin_output))
    logger.info("Extracted {} feature!".format(feature.__class__.__name__))
    return feature.serialize()


@app.task
def convert_mp3_to_mono_wav(input_file_name: Text) -> Text:
    """Input file name should contain mp3 extension"""
    start_point = datetime.utcnow()
    output_file_name = input_file_name + ".wav"
    logger.info("Building context for conversion: {} -> {}...".format(input_file_name, output_file_name))
    input_audio_file_absolute_path = os.path.join(AUDIO_FILES_DIR, input_file_name)
    output_audio_file_absolute_path = os.path.join(AUDIO_FILES_DIR, output_file_name)
    audio_file = AudioSegment.from_mp3(input_audio_file_absolute_path)
    audio_file.set_channels(1).export(output_audio_file_absolute_path, format="wav")
    took_seconds = seconds_between(start_time_point=start_point)
    logger.info("Ended conversion {} in {}s".format(input_file_name, took_seconds))
    return output_file_name


@app.task
def read_mp3_id3_tag(input_file_name: Text) -> Dict[Text, Any]:
    """Input file name should contain mp3 extension"""
    start_point = datetime.utcnow()
    logger.info("Building context for reading ID3 tags of {}...".format(input_file_name))
    input_audio_file_absolute_path = os.path.join(AUDIO_FILES_DIR, input_file_name)
    audio_tags = EasyID3(input_audio_file_absolute_path)
    id3_tag = Id3Tag(artist=audio_tags["artist"], title=audio_tags["title"],
                     album=audio_tags.get("album"), date=safe_cast(audio_tags.get("date"), int, None),
                     track=safe_cast(audio_tags.get("tracknumber"), int, None),
                     genre=safe_cast(audio_tags.get("date"), int, None))
    took_seconds = seconds_between(start_time_point=start_point)
    logger.info("Ended reading tags {} in {}s".format(input_file_name, took_seconds))
    return id3_tag.serialize()
