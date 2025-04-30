from pydantic import BaseModel

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
