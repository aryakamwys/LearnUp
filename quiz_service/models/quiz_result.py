from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class QuizResult(Base):
    __tablename__ = 'quiz_results'
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    user_id = Column(Integer) # Assuming a user ID from an authentication service
    score = Column(Integer)
    time_taken = Column(Integer) # in seconds
    completed_at = Column(DateTime, server_default=func.now())

    quiz = relationship("Quiz", back_populates="quiz_results") 