import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_URL= os.getenv('DB_URL')

engine = create_engine(DB_URL, future = True)

SessionLocal = sessionmaker(bind=engine, future = True)

class Base(DeclarativeBase):
    pass
