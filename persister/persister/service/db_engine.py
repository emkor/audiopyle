from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class DbEngine(object):
    _ENTITY_BASE_CLASS = None
    _ENGINE = None

    @staticmethod
    def get_base_entity_class():
        """
        :rtype: sqlalchemy.ext.declarative.api.DeclarativeMeta
        """
        if not DbEngine._ENTITY_BASE_CLASS:
            DbEngine._ENTITY_BASE_CLASS = declarative_base()
        return DbEngine._ENTITY_BASE_CLASS

    @staticmethod
    def get_engine(db_access_data, db_name, db_type="mysql"):
        """
        :type db_access_data: persister.model.db_access_data.DbAccessData
        :type db_name: str
        :type db_type: str
        """
        if not DbEngine._ENGINE:
            DbEngine._ENGINE = create_engine(DbEngine._get_connection_url(db_access_data, db_name, db_type))
        return DbEngine._ENGINE

    @staticmethod
    def _get_connection_url(db_access_data, db_name, db_type):
        return '{}://{}:{}@{}/{}'.format(db_type, db_access_data.user, db_access_data.password,
                                         db_access_data.host, db_name)

