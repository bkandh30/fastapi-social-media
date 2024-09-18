from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Database URL
DB_URL = "sqlite:///./db.sql"

#Create Engine
engine = create_engine(DB_URL, pool_pre_ping=True)
#Create Session
SessionLocal = sessionmaker(bind=engine, autoflush = False)
#Used to create base models for data
Base = declarative_base()

#Gets the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()