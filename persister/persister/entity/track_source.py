from sqlalchemy import Column, Integer, String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from persister.entity.track import Track
from persister.service.db_engine import DbEngine


class TrackSource(DbEngine.get_base_entity_class()):
    __tablename__ = 'track_source'

    id = Column(Integer, primary_key=True)

    source_type = Column(String(20), nullable=False)
    bucket_address = Column(String(100), nullable=False)
    bucket_name = Column(String(50), nullable=False)

    tracks = relationship("Track", order_by=Track.filename, back_populates="source")

    UniqueConstraint(source_type, bucket_address, bucket_name, name='uix_track_source')
