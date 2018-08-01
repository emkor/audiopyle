from contextlib import contextmanager
from typing import Optional

from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound

from audiopyle.commons.db.engine import get_db_session_maker
from audiopyle.commons.db.exception import EntityNotFound


class SessionProvider(object):
    def __init__(self, db_engine: Optional[Engine] = None) -> None:
        self._session_provider = get_db_session_maker(db_engine)

    @contextmanager
    def __call__(self, commit_on_exit=True, *args, **kwargs):
        session = self._session_provider()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        else:
            if commit_on_exit:
                try:
                    session.commit()
                except NoResultFound as e:
                    raise EntityNotFound(e)
                except Exception as e:
                    session.rollback()
                    raise e
        finally:
            session.close()
