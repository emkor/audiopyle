from typing import Optional

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from commons.db.entity import ENTITY_BASE
from commons.utils.env_var import read_env_var
from commons.utils.logger import get_logger

logger = get_logger()

_ENGINE = None  # type: Optional[Engine]
_SESSION_MAKER = None  # type: Optional[sessionmaker]


def get_db_engine() -> Engine:
    global _ENGINE
    if _ENGINE is None:
        db_connection_string = _build_mysql_conn_string()
        logger.info("Creating SQL Alchemy DB engine with {} connection string...".format(db_connection_string))
        _ENGINE = create_engine(db_connection_string, echo=True)
    return _ENGINE


def get_db_session_maker() -> sessionmaker:
    global _SESSION_MAKER
    if _SESSION_MAKER is None:
        logger.info("Creating SQL Alchemy sessions maker...")
        _SESSION_MAKER = sessionmaker(bind=get_db_engine())
    return _SESSION_MAKER


def create_db_tables() -> None:
    pymysql.install_as_MySQLdb()
    ENTITY_BASE.metadata.create_all(get_db_engine(), checkfirst=True)


def _build_mysql_conn_string() -> str:
    return "mysql://audiopyle:audiopyle@{}:{}/audiopyle".format(read_env_var("MYSQL_SERVICE_HOST", str),
                                                                read_env_var("MYSQL_SERVICE_PORT", int))
