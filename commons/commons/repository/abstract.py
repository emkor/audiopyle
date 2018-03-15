from logging import Logger
from typing import Optional, Type, List, Any

from pymysql import IntegrityError as PyMysqlIntegrityError
from sqlite3 import IntegrityError as SqLite3IntegrityError
from sqlalchemy.exc import IntegrityError as SqlAlchemyIntegrityError

from commons.db.exception import EntityNotFound, DuplicateEntity
from commons.db.session import SessionProvider
from commons.utils.logger import get_logger


class DbRepository(object):
    def __init__(self, session_provider: SessionProvider, entity_class: Type, logger: Optional[Logger] = None) -> None:
        self.session_provider = session_provider
        self.entity_class = entity_class
        self.logger = logger or get_logger()

    def get_all(self) -> List[Any]:
        return self._query_multiple_with_filters()

    def get_by_id(self, identifier: int) -> Optional[Any]:
        return self._query_single_with_filters(id=identifier)

    def get_or_create(self, model_object: Any) -> int:
        try:
            self.insert(model_object)
        except DuplicateEntity:
            return self._get_id_by_model(model_object)

    def delete_by_id(self, identifier: int) -> None:
        with self.session_provider() as session:
            entity = session.query(self.entity_class).filter_by(id=identifier).first()
            if entity is not None:
                session.delete(entity)
            else:
                raise EntityNotFound("Could not delete {}; no entity with id {}".format(self.entity_class.__name__,
                                                                                        identifier))

    def delete_all(self) -> None:
        with self.session_provider() as session:
            session.query(self.entity_class).delete()

    def insert(self, model_object: Any) -> None:
        try:
            with self.session_provider() as session:
                new_entity = self._map_to_entity(model_object)
                session.add(new_entity)
        except (PyMysqlIntegrityError, SqlAlchemyIntegrityError, SqLite3IntegrityError) as e:
            message = "Could not store {} of object {}".format(self.entity_class.__name__, model_object)
            raise DuplicateEntity(message)

    def _get_id(self, **kwargs) -> int:
        the_id = None
        with self.session_provider() as session:
            entity = session.query(self.entity_class).filter_by(**kwargs).first()
            if entity is not None:
                the_id = entity.id
            else:
                raise EntityNotFound("Could not retrieve id of {} with filters: {}".format(self.entity_class.__name__,
                                                                                           kwargs))
        return the_id

    def _query_single_with_filters(self, **kwargs) -> Optional[Any]:
        with self.session_provider() as session:
            entity = session.query(self.entity_class).filter_by(**kwargs).first()
            if entity is not None:
                return self._map_to_object(entity)
            if entity is None:
                raise EntityNotFound(
                    "Could not found entity {} that satisfy filters {}".format(self.entity_class.__name__, kwargs))
        return None

    def _query_multiple_with_filters(self, **kwargs) -> List[Any]:
        with self.session_provider() as session:
            if kwargs:
                entities = session.query(self.entity_class).filter_by(**kwargs).all()
            else:
                entities = session.query(self.entity_class).all()
            return [self._map_to_object(e) for e in entities] if entities else []

    def _get_id_by_model(self, model_object: Any) -> int:
        raise NotImplementedError()

    def _map_to_entity(self, obj: Any) -> Any:
        raise NotImplementedError()

    def _map_to_object(self, entity: Any) -> Any:
        raise NotImplementedError()
