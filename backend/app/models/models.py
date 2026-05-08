from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="student", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    conversations = relationship("Conversation", back_populates="user")

class StudentRecord(Base):
    __tablename__ = "student_records"
    id = Column(Integer, primary_key=True, index=True)
    StudentID = Column(String(50), unique=True, index=True, nullable=False)
    Name = Column(String(255), nullable=False)
    Course = Column(String(255), nullable=False)
    Semester = Column(Integer, nullable=False)
    Marks = Column(Float, nullable=False)
    Attendance = Column(Float, nullable=False)
    CGPA = Column(Float, nullable=False)
    Department = Column(String(50), index=True, nullable=False)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), default="New conversation")
    user_message = Column(Text, nullable=False)
    assistant_message = Column(Text, nullable=False)
    intent = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="conversations")

class UploadedPDF(Base):
    __tablename__ = "uploaded_pdfs"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    pages = Column(Integer, default=0)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    indexed_at = Column(DateTime, default=datetime.utcnow)
