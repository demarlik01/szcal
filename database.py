from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///./db.sqlite', echo=True)
Base = declarative_base()
session = sessionmaker(bind=engine)()