from fastapi import FastAPI, HTTPException
from database import engine, Base
from schemas import *
from crud import *
from auth import create_token

app = FastAPI()

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/admin/register")
async def register_admin(admin: AdminCreate):
    await create_admin(admin.username, admin.password)
    return {"status": "admin registered"}

@app.post("/admin/login", response_model=TokenResponse)
async def login_admin(admin: AdminLogin):
    user = await authenticate_admin(admin.username, admin.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    token = create_token({"sub": user.username, "role": "admin"})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/agent/register")
async def register_agent_endpoint(agent: AgentRegister):
    await register_agent(agent.agent_id, agent.agent_key)
    return {"status": "agent registered"}

@app.post("/agent/login", response_model=TokenResponse)
async def login_agent(agent: AgentRegister):
    auth = await authenticate_agent(agent.agent_id, agent.agent_key)
    if not auth:
        raise HTTPException(status_code=401, detail="Invalid agent credentials")
    token = create_token({"sub": auth.agent_id, "role": "agent"})
    return {"access_token": token, "token_type": "bearer"}