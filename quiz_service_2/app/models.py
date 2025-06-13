# app/models.py

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
import os

# Initialize SQLAlchemy
Base = declarative_base()

class Quiz(Base):
    __tablename__ = 'quizzes'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    course_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    is_active = Column(Boolean, default=True)
    
    # Relationship with questions
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}', course_id={self.course_id})>"

class QuizQuestion(Base):
    __tablename__ = 'quiz_questions'
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(String(500), nullable=False)
    option_b = Column(String(500), nullable=False)
    option_c = Column(String(500), nullable=False)
    option_d = Column(String(500), nullable=False)
    correct_answer = Column(String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    points = Column(Integer, default=1)
    
    # Relationship with quiz
    quiz = relationship("Quiz", back_populates="questions")

    def __repr__(self):
        return f"<QuizQuestion(id={self.id}, quiz_id={self.quiz_id}, question='{self.question_text[:50]}...')>"

class QuizAttempt(Base):
    __tablename__ = 'quiz_attempts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    score = Column(Integer, default=0)
    total_points = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.datetime.now)
    completed_at = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)

    def __repr__(self):
        return f"<QuizAttempt(id={self.id}, user_id={self.user_id}, quiz_id={self.quiz_id}, score={self.score})>"

# Database setup
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(DATA_DIR, 'quizzes.db')
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"Quiz database initialized at {DATABASE_PATH}") 