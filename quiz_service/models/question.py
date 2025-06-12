from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20), default='multiple_choice')  # multiple_choice, true_false, essay
    points = Column(Integer, default=1)  # Points for this question
    order_index = Column(Integer, default=0)  # Order of question in quiz

    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Question(question_text='{self.question_text[:50]}...', id={self.id})>" 