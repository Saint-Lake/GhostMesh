from sqlalchemy import Column, String
from database import Base

class Admin(Base):
    __tablename__ = "admins"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)

class Agent(Base):
    __tablename__ = "agents"
    agent_id = Column(String, primary_key=True, index=True)
    agent_key = Column(String)