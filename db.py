from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from settings import DATABASE

engine = create_engine(DATABASE)
session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

Base.metadata.create_all(bind=engine)
