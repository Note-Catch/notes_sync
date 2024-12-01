from contextlib import contextmanager
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.orm import Session, sessionmaker

from notes_sync.config import get_settings


def retry_connect(dialect, conn_rec, cargs, cparams):
    retries = get_settings().DB_CONNECT_RETRY - 1
    while retries:
        try:
            return dialect.connect(*cargs, **cparams)
        except OperationalError:
            retries -= 1
        except Exception as e:
            raise e
    return dialect.connect(*cargs, **cparams)


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance

    def get_session(self) -> Session:
        return self.session_local()

    def refresh(self) -> None:
        self.engine = create_engine(
            get_settings().database_uri,
            pool_size=get_settings().DB_POOL_SIZE,
            pool_pre_ping=True,
        )
        self.session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        listen(self.engine, "do_connect", retry_connect)


def get_db() -> Session:
    database = SessionManager().get_session()
    try:
        yield database
    finally:
        database.close()


db_context = contextmanager(get_db)
