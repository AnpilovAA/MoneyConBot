from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from settings import DATABASE


try:
    engine = create_engine(DATABASE, pool_pre_ping=True)
    session = scoped_session(sessionmaker(bind=engine))
except Exception as ex:
    print(ex, 'in db.py engine or session')
Base = declarative_base()

Base.metadata.create_all(bind=engine)
