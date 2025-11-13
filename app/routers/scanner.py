from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.cyber_agent import CyberAgent
import os
import json
from datetime import datetime

router = APIRouter()

class ScanRequest(BaseModel):
    repo_path: str

agent = CyberAgent()

@router.post("/scan-repo")
async def scan_repo(req: ScanRequest):
    repo_path = req.repo_path

    if not os.path.isdir(repo_path):
        return {"error": "Invalid path"}

    routes_list = []

    # Walk the repo and extract routes
    for root, _, files in os.walk(repo_path):
        for f in files:
            if f.endswith(".php"):
                print("inside file: ", f)
                file_path = os.path.join(root, f)

                with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()

                raw_response = agent.extract_routes(file_path, content)

                try:
                    cleaned = raw_response.strip().replace("```json", "").replace("```", "")
                    extracted = json.loads(cleaned)
                    if isinstance(extracted, list):
                        print("Extracted route: ", extracted)
                        routes_list.extend(extracted)
                except Exception as e:
                    print(f"JSON parse error for {file_path}: {e}")

    # ------------------------------------------
    # NEW PART: Write routes to output_action/
    # ------------------------------------------

    output_dir = os.path.join(os.getcwd(), "output_action")
    os.makedirs(output_dir, exist_ok=True)

    # timestamped output file (prevents overwrite)
    filename = f"routes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w") as f:
        for r in routes_list:
            f.write(r + "\n")

    print(f"Routes written to: {output_path}")

    return {
        "total_routes": len(routes_list),
        "routes": routes_list,
        "output_file": output_path
    }
