from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Option(Base):
    __tablename__ = 'options'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, nullable=False)  # Remove foreign key constraint
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    order_index = Column(Integer, default=0)  # Order of option in question

    # Relationships
    question = relationship("Question", back_populates="options")

    def __repr__(self):
        return f"<Option(option_text='{self.option_text[:30]}...', is_correct={self.is_correct})>" 