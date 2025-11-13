from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.cyber_agent import CyberAgent

router = APIRouter()
agent = CyberAgent()

class AgentInput(BaseModel):
    query: str

@router.post("/agent")
async def run_agent(input: AgentInput):
    print("inside agent route\n")
    result = agent.run(input.query)
    return {"response": result}
