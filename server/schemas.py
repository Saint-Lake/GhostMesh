from pydantic import BaseModel
from typing import Optional

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

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TaskCreate(BaseModel):
    agent_id: str
    command: str

class BeaconRequest(BaseModel):
    agent_id: str

class TaskResponse(BaseModel):
    task_id: Optional[str] = None
    command: Optional[str] = ""

class ResultSubmit(BaseModel):
    agent_id: str
    task_id: str
    output: str
