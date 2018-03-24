from logging import Logger
from typing import Optional, Type, List, Any, Union
from pymysql import IntegrityError as PyMysqlIntegrityError
from sqlite3 import IntegrityError as SqLite3IntegrityError
from sqlalchemy.exc import IntegrityError as SqlAlchemyIntegrityError

from commons.db.exception import EntityNotFound, DuplicateEntity
from commons.db.session import SessionProvider
from commons.utils.logger import get_logger


class DbRepository(object):
    IDENTIFIER_TYPE = Optional[Union[int, str]]

    def __init__(self, session_provider: SessionProvider, entity_class: Type, logger: Optional[Logger] = None) -> None:
        self.session_provider = session_provider
        self.entity_class = entity_class
        self.logger = logger or get_logger()

    def get_all(self) -> List[Any]:
        return self._query_multiple()

    def get_all_keys(self) -> List[IDENTIFIER_TYPE]:
        return self._query_multiple_keys()

    def get_by_id(self, identifier: IDENTIFIER_TYPE) -> Optional[Any]:
        return self._query_single(id=identifier)

    def get_id_by_model(self, model_object: Any) -> IDENTIFIER_TYPE:
        raise NotImplementedError()

    def get_or_create(self, model_object: Any) -> IDENTIFIER_TYPE:
        try:
            self.insert(model_object)
        except DuplicateEntity as e:
            self.logger.debug(
                "Could not insert model object {}: {}; omitting and returning by ID...".format(model_object, e))
        return self.get_id_by_model(model_object)

    def exists_by_model(self, model_object: Any) -> bool:
        return self.get_id_by_model(model_object) is not None

    def exists_by_id(self, identifier: IDENTIFIER_TYPE) -> bool:
        return self.get_by_id(identifier) is not None

    def delete_by_id(self, identifier: IDENTIFIER_TYPE) -> None:
        with self.session_provider() as session:
            entity = session.query(self.entity_class).filter_by(id=identifier).first()
            if entity is not None:
                session.delete(entity)
            else:
                raise EntityNotFound(
                    "Could not delete {} with id {} because id does not exist.".format(self.entity_class, identifier))

    def delete_all(self) -> None:
        with self.session_provider() as session:
            session.query(self.entity_class).delete()

    def insert(self, model_object: Any) -> None:
        try:
            with self.session_provider() as session:
                new_entity = self._map_to_entity(model_object)
                session.add(new_entity)
        except (PyMysqlIntegrityError, SqlAlchemyIntegrityError, SqLite3IntegrityError) as e:
            raise DuplicateEntity(e)

    def _get_id(self, **filters) -> Optional[IDENTIFIER_TYPE]:
        with self.session_provider() as session:
            entity = session.query(self.entity_class).filter_by(**filters).first()
            the_id = entity.id if entity is not None else None
        return the_id

    def _query_single(self, **filters) -> Optional[Any]:
        with self.session_provider() as session:
            entity = session.query(self.entity_class).filter_by(**filters).first()
            return self._map_to_object(entity) if entity is not None else None

    def _query_multiple(self, **filters) -> List[Any]:
        with self.session_provider() as session:
            if filters:
                entities = session.query(self.entity_class).filter_by(**filters).all()
            else:
                entities = session.query(self.entity_class).all()
            return [self._map_to_object(e) for e in entities] if entities else []

    def _query_multiple_keys(self, **filters):
        with self.session_provider() as session:
            if filters:
                entities = session.query(self.entity_class.id).filter_by(**filters).all()
            else:
                entities = session.query(self.entity_class.id).all()
            return [r[0] for r in entities]

    def _map_to_entity(self, obj: Any) -> Any:
        raise NotImplementedError()

    def _map_to_object(self, entity: Any) -> Any:
        raise NotImplementedError()
