from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


Base = declarative_base()

class UserProgress(Base):
    __tablename__ = 'user_progress'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    progress = Column(String)

# Update the engine creation to use a connection URL that is compatible with your database.
DATABASE_URL = "sqlite:///user_progress.db"  # Update this to match your actual database URL.
engine = create_engine(DATABASE_URL)

# Use the new style session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Ensure the models are created in the database
Base.metadata.create_all(bind=engine)