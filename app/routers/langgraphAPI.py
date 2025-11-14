from fastapi import APIRouter

from pydantic import BaseModel
from app.graph.graph import build_graph

router = APIRouter()
workflow = build_graph()

class GraphInput(BaseModel):
    repo_url: str

# TO-DO: Rename this endpoint something better
# main API to run app. 127.0.0.1:8000/run-graph
@router.post("/run-graph")
async def run_graph(input: GraphInput):
    # LangGraph expects a dict-like state
    state = {"repo_url": input.repo_url}
    result = workflow.invoke(state)

    return {"result": result}