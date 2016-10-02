from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from persister.entity.track import Track
from persister.service.db_engine import DbEngine


class TrackSource(DbEngine.get_base_entity_class()):
    __tablename__ = 'track_source'

    id = Column(Integer, primary_key=True)

    source_type = Column(String(20))
    bucket_address = Column(String(100))
    bucket_name = Column(String(50))

    tracks = relationship("Track", order_by=Track.filename, back_populates="source")
