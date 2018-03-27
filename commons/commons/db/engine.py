from typing import Optional

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool, StaticPool

from commons.db.entity import ENTITY_BASE
from commons.utils.env_var import read_env_var
from commons.utils.logger import get_logger

logger = get_logger()

_ENGINE = None  # type: Optional[Engine]
_SESSION_MAKER = None  # type: Optional[sessionmaker]


def get_db_engine(host: str = None, port: int = None, debug: bool = False) -> Engine:
    pymysql.install_as_MySQLdb()
    global _ENGINE
    if _ENGINE is None:
        db_connection_string = _build_mysql_conn_string(host, port)
        logger.debug("Creating SQL Alchemy DB engine with {} connection string...".format(db_connection_string))
        _ENGINE = create_engine(db_connection_string, echo=debug, poolclass=NullPool)
    return _ENGINE


def get_test_db_engine(debug: bool = False) -> Engine:
    """Snippet for in-memory DB: http://www.sameratiani.com/2013/09/17/flask-unittests-with-in-memory-sqlite.html"""
    global _ENGINE
    if _ENGINE is None:
        db_connection_string = 'sqlite:///'
        logger.debug("Creating sqlite DB engine with {} connection string...".format(db_connection_string))
        _ENGINE = create_engine(db_connection_string, echo=debug, poolclass=StaticPool)
    return _ENGINE


def get_db_session_maker(db_engine: Optional[Engine] = None) -> sessionmaker:
    global _SESSION_MAKER
    if _SESSION_MAKER is None:
        logger.debug("Creating SQL Alchemy sessions maker...")
        _SESSION_MAKER = sessionmaker(bind=db_engine or get_db_engine())
    return _SESSION_MAKER


def create_db_tables(engine: Optional[Engine] = None, only_if_absent: bool = True) -> None:
    ENTITY_BASE.metadata.create_all(engine or get_db_engine(), checkfirst=only_if_absent)


def drop_db_tables(engine: Optional[Engine] = None) -> None:
    ENTITY_BASE.metadata.drop_all(engine or get_db_engine())


def _build_mysql_conn_string(host: str = None, port: int = None) -> str:
    return "mysql://audiopyle:audiopyle@{}:{}/audiopyle".format(
        host or read_env_var("MYSQL_SERVICE_HOST", str, "localhost"),
        port or read_env_var("MYSQL_SERVICE_PORT", int, 3306))
