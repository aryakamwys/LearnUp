from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=True)  # Optional link to course
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)  # Optional link to user
    time_limit = Column(Integer, default=0)  # Time limit in minutes, 0 = no limit
    passing_score = Column(Integer, default=70)  # Passing score percentage
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    results = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Quiz(title='{self.title}', id={self.id})>" 