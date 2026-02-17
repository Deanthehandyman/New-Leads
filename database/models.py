import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class Lead(Base):
    __tablename__ = 'leads'
    id = Column(Integer, primary_key=True)
    source = Column(String)
    source_id = Column(String, unique=True)
    title = Column(String)
    url = Column(String)
    location = Column(String)
    date_posted = Column(String)
    date_scraped = Column(DateTime, default=datetime.now)
    score = Column(String)
    score_val = Column(Integer)
    status = Column(String, default="NEW")

def get_db_engine():
    os.makedirs('database', exist_ok=True)
    return create_engine('sqlite:///database/leads.db')

def init_db():
    engine = get_db_engine()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
