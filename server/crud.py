from models import Admin, Agent, Task, Result
from database import SessionLocal
from auth import hash_password, verify_password
from sqlalchemy.future import select
import uuid

async def seed_admin_if_needed(username: str, password: str):
    async with SessionLocal() as session:
        result = await session.execute(select(Admin).where(Admin.username == username))
        if result.scalar_one_or_none():
            return  # Admin already exists
        admin = Admin(username=username, hashed_password=hash_password(password))
        session.add(admin)
        await session.commit()

async def authenticate_admin(username: str, password: str):
    async with SessionLocal() as session:
        result = await session.execute(select(Admin).where(Admin.username == username))
        admin = result.scalar_one_or_none()
        if admin and verify_password(password, admin.hashed_password):
            return admin
        return None

async def register_agent(agent_id: str, agent_key: str):
    async with SessionLocal() as session:
        agent = Agent(agent_id=agent_id, agent_key=agent_key)
        session.add(agent)
        await session.commit()

async def authenticate_agent(agent_id: str, agent_key: str):
    async with SessionLocal() as session:
        result = await session.execute(select(Agent).where(Agent.agent_id == agent_id))
        agent = result.scalar_one_or_none()
        if agent and agent.agent_key == agent_key:
            return agent
        return None

async def queue_task(agent_id: str, command: str):
    task = Task(id=str(uuid.uuid4()), agent_id=agent_id, command=command)
    async with SessionLocal() as session:
        session.add(task)
        await session.commit()
        return task

async def fetch_pending_task(agent_id: str):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Task).where(Task.agent_id == agent_id, Task.completed == False)
        )
        return result.scalar_one_or_none()

async def mark_task_complete(task_id: str):
    async with SessionLocal() as session:
        task = await session.get(Task, task_id)
        if task:
            task.completed = True
            await session.commit()

async def store_result(agent_id: str, task_id: str, output: str):
    result = Result(id=str(uuid.uuid4()), agent_id=agent_id, task_id=task_id, output=output)
    async with SessionLocal() as session:
        session.add(result)
        await session.commit()