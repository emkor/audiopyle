from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, String, Integer, Float, UniqueConstraint, LargeBinary
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import relationship, backref

ENTITY_BASE = declarative_base()  # type: Optional[DeclarativeMeta]


class AudioFile(ENTITY_BASE):
    __tablename__ = 'audio_file'
    id = Column(Integer, primary_key=True)
    file_name = Column(String(255), unique=True, index=True, nullable=False)

    channels_count = Column(Integer, nullable=False)
    sample_rate = Column(Integer, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    length_sec = Column(Float, nullable=False)
    bit_rate = Column(Float, nullable=False)

    artist = Column(String(255), index=True, nullable=True)
    album = Column(String(255), index=True, nullable=True)
    title = Column(String(255), index=True, nullable=True)
    date = Column(Integer, index=True, nullable=True)
    genre = Column(String(255), index=True, nullable=True)
    track = Column(Integer, nullable=True)


class VampyPlugin(ENTITY_BASE):
    __tablename__ = 'vampy_plugin'
    id = Column(Integer, primary_key=True)
    vendor = Column(String(255), index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    output = Column(String(255), index=True, nullable=False)
    UniqueConstraint('vendor', 'name', 'output', name='unique_plugin')


class Result(ENTITY_BASE):
    __tablename__ = 'result'
    task_id = Column(String(32), unique=True, index=True, nullable=False, primary_key=True, autoincrement=False)
    vampy_plugin = relationship(VampyPlugin, backref=backref('results',
                                                             uselist=True,
                                                             cascade='delete,all'))
    audio_file = relationship(AudioFile, backref=backref('results',
                                                         uselist=True,
                                                         cascade='delete,all'))
    UniqueConstraint('vampy_plugin', 'audio_file', name='unique_result')

    done_at = Column(DateTime, default=datetime.utcnow)
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
    feature_data = Column(LargeBinary, index=False, nullable=False)

    analysis_time = Column(Float, index=False, nullable=False)
