from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Admin
class AdminCreate(BaseModel):
    username: str
    password: str

class AdminLogin(BaseModel):
    username: str
    password: str

# Agent
class AgentRegister(BaseModel):
    agent_id: str
    agent_key: str
    netbios: Optional[str] = None
    ip: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TaskCreate(BaseModel):
    agent_id: str
    command: str

class BeaconRequest(BaseModel):
    agent_id: str
    netbios: Optional[str] = None
    ip: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: Optional[str] = None
    command: Optional[str] = ""

class ResultSubmit(BaseModel):
    agent_id: str
    task_id: str
    output: str

class TaskView(BaseModel):
    id: str
    agent_id: str
    command: str
    completed: bool
    created_at: datetime

class ResultView(BaseModel):
    id: str
    agent_id: str
    task_id: str
    output: str
    created_at: datetime

class AgentInfo(BaseModel):
    agent_id: str
    netbios: Optional[str]
    ip: Optional[str]
