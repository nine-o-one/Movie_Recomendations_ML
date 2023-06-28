import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_file = "../database.sqlite"
directorio = os.path.dirname(os.path.realpath(__file__))
db_url = f"sqlite:///{os.path.join(directorio, db_file)}"

engine = create_engine(
    db_url, connect_args={"check_same_thread": False}
    )
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
