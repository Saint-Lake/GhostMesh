from models import Admin, Agent
from database import SessionLocal
from auth import hash_password, verify_password
from sqlalchemy.future import select

async def create_admin(username: str, password: str):
    async with SessionLocal() as session:
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
