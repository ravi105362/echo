from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src import settings

if settings.DATABASE_LOCAL is True:
    database_url = settings.SQLALCHEMY_DATABASE_URL
else:
    database_url = settings.POSTGRES_DATABASE_URL

engine = create_engine(database_url)

sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
