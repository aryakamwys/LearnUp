from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):  # <- Harus mewarisi Base dari database
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
