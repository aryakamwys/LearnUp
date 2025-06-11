# app/models.py

from sqlalchemy import create_engine, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import os

# Initialize SQLAlchemy
Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    course_id = Column(Integer, nullable=False)
    loan_date = Column(DateTime, default=datetime.datetime.now)
    return_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Loan(id={self.id}, user_id={self.user_id}, course_id={self.course_id})>"

# Database setup
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(DATA_DIR, 'loans.db')
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at {DATABASE_PATH}")