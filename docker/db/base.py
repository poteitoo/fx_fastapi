from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

pgconfig = {
    "host": "localhost",
    "port": "5432",
    "database": "fx_postgres",
    "user": "postgres_kun",
    "password": "postgres12345",
}
DATABASE_URL = "postgresql://{user}:{password}@{host}:{port}/{database}".format(
    **pgconfig
)


# DATABASE_URL = "sqlite:///./work/data/candles.db"
engine = sqlalchemy.create_engine(DATABASE_URL)
Base = declarative_base()

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    Base.metadata.create_all(bind=engine)
