# backend/database.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URI = 'sqlite:///documents.db'
engine = create_engine(DATABASE_URI, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = Column(String, nullable=False)
    keywords = Column(String, default="")

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()