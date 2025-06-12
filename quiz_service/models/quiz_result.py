from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class QuizResult(Base):
    __tablename__ = 'quiz_results'

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=True)  # Remove foreign key constraint
    score = Column(Float, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    time_taken = Column(Integer)  # Time taken in seconds
    passed = Column(Integer, default=0)  # 1 = passed, 0 = failed
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    quiz = relationship("Quiz", back_populates="results")

    def __repr__(self):
        return f"<QuizResult(quiz_id={self.quiz_id}, score={self.score}, passed={self.passed})>" 