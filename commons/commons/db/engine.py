from typing import Optional

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from commons.db.entity import ENTITY_BASE
from commons.utils.env_var import read_env_var
from commons.utils.logger import get_logger

logger = get_logger()

_ENGINE = None  # type: Optional[Engine]
_SESSION_MAKER = None  # type: Optional[sessionmaker]


def get_db_engine(host: str = None, port: int = None) -> Engine:
    pymysql.install_as_MySQLdb()
    global _ENGINE
    if _ENGINE is None:
        db_connection_string = _build_mysql_conn_string(host, port)
        logger.info("Creating SQL Alchemy DB engine with {} connection string...".format(db_connection_string))
        _ENGINE = create_engine(db_connection_string, echo=True, poolclass=NullPool)
    return _ENGINE


def get_test_db_engine(file_name: str, debug: bool = False) -> Engine:
    global _ENGINE
    if _ENGINE is None:
        db_connection_string = 'sqlite:///{}'.format(file_name)
        logger.info("Creating sqlite DB engine with {} connection string...".format(db_connection_string))
        _ENGINE = create_engine(db_connection_string, echo=debug, poolclass=NullPool)
    return _ENGINE


def get_db_session_maker(db_engine: Optional[Engine] = None) -> sessionmaker:
    global _SESSION_MAKER
    if _SESSION_MAKER is None:
        logger.info("Creating SQL Alchemy sessions maker...")
        _SESSION_MAKER = sessionmaker(bind=db_engine or get_db_engine())
    return _SESSION_MAKER


def create_db_tables(engine: Optional[Engine] = None, check_first: bool = True) -> None:
    ENTITY_BASE.metadata.create_all(engine or get_db_engine(), checkfirst=check_first)


def _build_mysql_conn_string(host: str = None, port: int = None) -> str:
    return "mysql://audiopyle:audiopyle@{}:{}/audiopyle".format(host or read_env_var("MYSQL_SERVICE_HOST", str),
                                                                port or read_env_var("MYSQL_SERVICE_PORT", int))
