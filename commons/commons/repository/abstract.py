from logging import Logger
from typing import Optional, Type, List, Callable, Any

from commons.db.session import SessionProvider
from commons.utils.logger import get_logger


class DbRepository(object):
    def __init__(self, session_provider: SessionProvider,
                 entity_class: Type,
                 entity_to_object_mapper: Callable[..., Any],
                 object_to_entity_mapper: Callable[..., Any],
                 logger: Optional[Logger] = None) -> None:
        self.session_provider = session_provider
        self.entity_class = entity_class
        self.object_to_entity_mapper = object_to_entity_mapper
        self.entity_to_object_mapper = entity_to_object_mapper
        self.logger = logger or get_logger()

    def get_all(self) -> List[Any]:
        return self._query_multiple_with_filters()

    def get_by_id(self, identifier: int) -> Optional[Any]:
        return self._query_single_with_filters(id=identifier)

    def delete_by_id(self, identifier: int) -> None:
        with self.session_provider() as session:
            entity = session.query(self.entity_class).filter_by(id=identifier).first()
            if entity is not None:
                session.delete(entity)

    def insert(self, audio_meta: Any) -> None:
        try:
            with self.session_provider() as session:
                new_entity = self.object_to_entity_mapper(audio_meta)
                session.add(new_entity)
        except Exception as e:
            self.logger.error("Could not store audio entity: {}".format(e))

    def _get_id(self, **kwargs) -> int:
        with self.session_provider() as session:
            entity = session.query(self.entity_class).filter_by(**kwargs).first()
        the_id = entity.id
        return the_id

    def _query_single_with_filters(self, **kwargs) -> Optional[Any]:
        with self.session_provider() as session:
            entity = session.query(self.entity_class).filter_by(**kwargs).first()
            return self.entity_to_object_mapper(entity) if entity is not None else None

    def _query_multiple_with_filters(self, **kwargs) -> List[Any]:
        with self.session_provider() as session:
            if kwargs:
                entities = session.query(self.entity_class).filter_by(**kwargs).all()
            else:
                entities = session.query(self.entity_class).all()
            return [self.entity_to_object_mapper(e) for e in entities] if entities else []
