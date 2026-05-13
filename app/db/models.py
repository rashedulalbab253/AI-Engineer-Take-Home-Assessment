from sqlalchemy import Column, Integer, String, Text, Float, JSON
from app.db.database import Base

class DocumentRecord(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    status = Column(String) # uploaded, processed, failed
    raw_text = Column(Text, nullable=True)
    structured_data = Column(JSON, nullable=True)

class FeedbackRecord(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    draft_id = Column(String, index=True)
    context = Column(String)
    replace_from = Column(String)
    replace_to = Column(String)
