from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base # Assuming database.py is in the parent directory

class Quiz(Base):
    __tablename__ = 'quizzes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    time_limit = Column(Integer, default=0)  # in minutes
    passing_score = Column(Integer, default=70) # percentage
    is_active = Column(Boolean, default=True) # Soft delete for quizzes
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan") 