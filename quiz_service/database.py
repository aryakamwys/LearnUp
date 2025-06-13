import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create data directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Database path
db_path = os.path.join(data_dir, 'quiz.db')
print(f"📂 DB path: {db_path}")

# Create engine
engine = create_engine(f'sqlite:///{db_path}', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    print("📥 Importing Quiz models...")
    # Import all models here
    from models.quiz import Quiz
    from models.question import Question
    from models.option import Option
    from models.quiz_result import QuizResult
    
    print("📐 Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized and tables created.") 