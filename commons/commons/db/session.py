from contextlib import contextmanager
from logging import Logger
from typing import Optional

from sqlalchemy.engine import Engine

from commons.db.engine import get_db_session_maker
from commons.utils.logger import get_logger


class SessionProvider(object):
    def __init__(self, db_engine: Optional[Engine] = None, logger: Optional[Logger] = None) -> None:
        self._session_provider = get_db_session_maker(db_engine)
        self._logger = logger or get_logger()

    @contextmanager
    def __call__(self, commit_on_exit=True, *args, **kwargs):
        session = self._session_provider()
        try:
            yield session
        except Exception as e:
            self._logger.warning("Error on DB session: {}; rolling back!".format(e))
            session.rollback()
            raise e
        else:
            if commit_on_exit:
                try:
                    session.commit()
                except Exception as e:
                    self._logger.warning("Could not accomplish commit: {}".format(e))
                    session.rollback()
                    raise e
        finally:
            session.close()
