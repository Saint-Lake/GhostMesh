from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone
from database import Base


def utc_now():
    return datetime.now(timezone.utc)

class Admin(Base):
    __tablename__ = "admins"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)

class Agent(Base):
    __tablename__ = "agents"
    agent_id = Column(String, primary_key=True, index=True)
    agent_key = Column(String)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True)
    agent_id = Column(String, index=True)
    command = Column(Text)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)

class Result(Base):
    __tablename__ = "results"
    id = Column(String, primary_key=True)
    agent_id = Column(String, index=True)
    task_id = Column(String, ForeignKey("tasks.id"))
    output = Column(Text)
    created_at = Column(DateTime, default=utc_now)