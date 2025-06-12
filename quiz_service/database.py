import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import declarative_base

# Ensure data directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_NAME = os.path.join(DATA_DIR, "quiz.db")
print("📂 DB path:", DATABASE_NAME)
engine = create_engine(f"sqlite:///{DATABASE_NAME}", connect_args={"check_same_thread": False})
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    print("📥 Importing Quiz models...")
    from models.quiz import Quiz
    from models.question import Question
    from models.option import Option
    from models.quiz_result import QuizResult
    print("📐 Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized and tables created.")

if __name__ == '__main__':
    init_db() 