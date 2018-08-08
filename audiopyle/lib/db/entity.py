from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, String, Integer, Float, UniqueConstraint, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

ENTITY_BASE = declarative_base()  # type: Optional[DeclarativeMeta]


class VampyPlugin(ENTITY_BASE):  # type: ignore
    __tablename__ = 'vampy_plugin'

    id = Column(Integer, primary_key=True, autoincrement=True)

    vendor = Column(String(255), index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    output = Column(String(255), index=True, nullable=False)
    library_file_name = Column(String(255), index=True, nullable=False)

    __table_args__ = (UniqueConstraint('vendor', 'name', 'output', name='unique_plugin'),)


class AudioFile(ENTITY_BASE):  # type: ignore
    __tablename__ = 'audio_file'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(255), unique=True, index=True, nullable=False)

    channels_count = Column(Integer, nullable=False)
    sample_rate = Column(Integer, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    length_sec = Column(Float, nullable=False)
    bit_rate = Column(Float, nullable=False)


class PluginConfig(ENTITY_BASE):  # type: ignore
    __tablename__ = 'plugin_config'

    id = Column(Integer, primary_key=True, autoincrement=True)

    block_size = Column(Integer, index=False, nullable=False)
    step_size = Column(Integer, index=False, nullable=False)
    additional_params = Column(String(1023), index=False, nullable=False)

    __table_args__ = (UniqueConstraint('block_size', 'step_size', 'additional_params', name='unique_plugin_config'),)


class AudioTag(ENTITY_BASE):  # type: ignore
    __tablename__ = 'audio_tag'

    id = Column(Integer, primary_key=True, autoincrement=True)

    artist = Column(String(255), index=True, nullable=False)
    title = Column(String(255), index=True, nullable=False)
    album = Column(String(255), index=True, nullable=True)
    date = Column(Integer, index=True, nullable=True)
    genre = Column(String(63), index=True, nullable=True)
    track = Column(Integer, index=False, nullable=True)

    __table_args__ = (UniqueConstraint('artist', 'title', name='unique_id3_tag'),)


class MetricDefinition(ENTITY_BASE):  # type: ignore
    __tablename__ = 'metric_definition'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plugin_id = Column(Integer, ForeignKey("vampy_plugin.id", ondelete="CASCADE"),
                       nullable=False, index=True)

    name = Column(String(255), unique=True, index=True, nullable=False)
    function = Column(String(255), index=False, nullable=False)
    kwargs = Column(String(511), index=False, nullable=True)


class Request(ENTITY_BASE):  # type: ignore
    __tablename__ = 'request'

    id = Column(String(36), primary_key=True, unique=True, index=True, nullable=False)

    vampy_plugin_id = Column(Integer, ForeignKey("vampy_plugin.id", ondelete="CASCADE"),
                             nullable=False, index=True)
    plugin_config_id = Column(Integer, ForeignKey("plugin_config.id", ondelete="CASCADE"),
                              nullable=False, index=True)
    audio_file_id = Column(Integer, ForeignKey("audio_file.id", ondelete="CASCADE"),
                           nullable=False, index=True)
    audio_tag_id = Column(Integer, ForeignKey("audio_tag.id", ondelete="CASCADE"),
                          nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.now())


class FeatureMeta(ENTITY_BASE):  # type: ignore
    __tablename__ = 'feature_meta'

    id = Column(String(36), ForeignKey("request.id", ondelete="CASCADE"), primary_key=True)

    feature_type = Column(String(63), index=True, nullable=False)
    feature_shape_x = Column(Integer, index=False, nullable=False)
    feature_shape_y = Column(Integer, index=False, nullable=False)
    feature_shape_z = Column(Integer, index=False, nullable=False)
    feature_size_bytes = Column(Integer, index=False, nullable=False)


class FeatureData(ENTITY_BASE):  # type: ignore
    __tablename__ = 'feature_data'

    id = Column(String(36), ForeignKey("request.id", ondelete="CASCADE"), primary_key=True)

    compression = Column(String(31), index=True, nullable=False)
    feature_data = Column(LargeBinary(16777215), index=False, nullable=False)


class ResultStats(ENTITY_BASE):  # type: ignore
    __tablename__ = 'result_stats'

    id = Column(String(36), ForeignKey("request.id", ondelete="CASCADE"), primary_key=True)

    total_time = Column(Float, index=False, nullable=True)
    extraction_time = Column(Float, index=False, nullable=True)
    compression_time = Column(Float, index=False, nullable=True)
    data_stats_build_time = Column(Float, index=False, nullable=True)
    encode_audio_time = Column(Float, index=False, nullable=True)
    result_store_time = Column(Float, index=False, nullable=True)
    metrics_extraction_time = Column(Float, index=False, nullable=True)


class Metric(ENTITY_BASE):  # type: ignore
    __tablename__ = 'metric'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(36), ForeignKey("request.id", ondelete="CASCADE"), nullable=False, index=True)
    definition_id = Column(Integer, ForeignKey("metric_definition.id", ondelete="CASCADE"),
                           nullable=False, index=True)

    minimum = Column(Float, index=False, nullable=True)
    maximum = Column(Float, index=False, nullable=True)
    median = Column(Float, index=False, nullable=True)
    mean = Column(Float, index=False, nullable=True)
    standard_deviation = Column(Float, index=False, nullable=True)
    variance = Column(Float, index=False, nullable=True)

    __table_args__ = (UniqueConstraint('task_id', 'definition_id', name='unique_metric'),)
