from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, String, Integer, Float, UniqueConstraint, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

ENTITY_BASE = declarative_base()  # type: Optional[DeclarativeMeta]


class AudioFile(ENTITY_BASE):  # type: ignore
    __tablename__ = 'audio_file'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(255), unique=True, index=True, nullable=False)

    channels_count = Column(Integer, nullable=False)
    sample_rate = Column(Integer, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    length_sec = Column(Float, nullable=False)
    bit_rate = Column(Float, nullable=False)


class AudioTag(ENTITY_BASE):  # type: ignore
    __tablename__ = 'audio_tag'

    id = Column(Integer, primary_key=True, autoincrement=True)

    artist = Column(String(255), index=True, nullable=True)
    album = Column(String(255), index=True, nullable=True)
    title = Column(String(255), index=True, nullable=True)
    date = Column(Integer, index=True, nullable=True)
    genre = Column(String(255), index=True, nullable=True)
    track = Column(Integer, nullable=True)

    UniqueConstraint('artist', 'album', 'title', name='unique_plugin')


class VampyPlugin(ENTITY_BASE):  # type: ignore
    __tablename__ = 'vampy_plugin'

    id = Column(Integer, primary_key=True, autoincrement=True)

    vendor = Column(String(255), index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)

    UniqueConstraint('vendor', 'name', name='unique_plugin')


class FeatureMeta(ENTITY_BASE):  # type: ignore
    __tablename__ = 'feature_meta'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    task_id = Column(String(32), unique=True, index=True, nullable=False)

    plugin_output = Column(String(255), index=True, nullable=False)
    feature_type = Column(String(255), index=True, nullable=False)
    feature_shape_x = Column(Integer, index=False, nullable=False)
    feature_shape_y = Column(Integer, index=False, nullable=False)
    feature_size_bytes = Column(Integer, index=False, nullable=False)

    feature_minimum = Column(Float, index=False, nullable=True)
    feature_maximum = Column(Float, index=False, nullable=True)
    feature_median = Column(Float, index=False, nullable=True)
    feature_mean = Column(Float, index=False, nullable=True)
    feature_standard_deviation = Column(Float, index=False, nullable=True)
    feature_variance = Column(Float, index=False, nullable=True)


class FeatureData(ENTITY_BASE):  # type: ignore
    __tablename__ = 'feature_data'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    task_id = Column(String(32), unique=True, index=True, nullable=False)

    feature_data = Column(LargeBinary, index=False, nullable=False)


class Result(ENTITY_BASE):  # type: ignore
    __tablename__ = 'result'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    task_id = Column(String(32), unique=True, index=True, nullable=False)

    vampy_plugin_id = Column(Integer, ForeignKey("vampy_plugin.id", ondelete="CASCADE"),
                             nullable=False, index=True)
    audio_file_id = Column(Integer, ForeignKey("audio_file.id", ondelete="CASCADE"),
                           nullable=False, index=True)
    audio_tag_id = Column(Integer, ForeignKey("audio_tag.id", ondelete="CASCADE"),
                          nullable=False, index=True, primary_key=True)
    feature_meta_id = Column(Integer, ForeignKey("feature_meta.id", ondelete="CASCADE"),
                             nullable=False, index=True, primary_key=True)
    feature_data_id = Column(Integer, ForeignKey("feature_data.id", ondelete="CASCADE"),
                             nullable=False, index=True, primary_key=True)

    done_at = Column(DateTime, default=datetime.utcnow)
    analysis_time = Column(Float, index=False, nullable=False)
