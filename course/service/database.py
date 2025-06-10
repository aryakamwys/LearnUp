from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_NAME = "courses.db"
engine = create_engine(f'sqlite:///{DATABASE_NAME}')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # Import all modules here that might define models
    from auth.models.user import User
    from auth.models.session import Session
    Base.metadata.create_all(bind=engine)
    
    # Create courses table
    engine.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()
