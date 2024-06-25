from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# SQLAlchemy database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://botuser:jhaytech@localhost/bot_database')
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

class UserProgress(Base):
    __tablename__ = 'user_progress'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    progress_info = Column(String, nullable=False)

# Create tables if they do not exist
Base.metadata.create_all(engine)

# Create a scoped session for interacting with the database
session = Session()
