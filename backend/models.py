from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import os

# Load environment variables from .env file
load_dotenv()

# SQLAlchemy database setup
Base = declarative_base()
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://botuser:jhaytech@localhost/bot_database')
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

class UserProgress(Base):
    __tablename__ = 'user_progress'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    progress_info = Column(String, nullable=False)

# Create tables here
Base.metadata.create_all(engine)
