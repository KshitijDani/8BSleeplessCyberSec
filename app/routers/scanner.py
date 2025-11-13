import requests
import zipfile
import tempfile
import io
import os
import json

from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.cyber_agent import CyberAgent

from datetime import datetime

router = APIRouter()
agent = CyberAgent()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
OUTPUT_ACTION_DIR = os.path.join(BASE_DIR, "output_action")


# TO-DO: merge these two classes into single abstract class
class ScanRequest(BaseModel):
    repo_path: str

class GitHubScanRequest(BaseModel):
    repo_url: str  # e.g. https://github.com/user/repo


# scans local machine's repo
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

    os.makedirs(OUTPUT_ACTION_DIR, exist_ok=True)

    # timestamped output file (prevents overwrite)
    filename = f"routes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    output_path = os.path.join(OUTPUT_ACTION_DIR, filename)

    with open(output_path, "w") as f:
        for r in routes_list:
            f.write(r + "\n")

    print(f"Routes written to: {output_path}")

    return {
        "total_routes": len(routes_list),
        "routes": routes_list,
        "output_file": output_path
    }


# gets all the latest routes in the output_action directory text file, then opens the file and returns all the endpoints
@router.get("/latest-routes")
async def get_latest_routes():
    output_dir = OUTPUT_ACTION_DIR #os.path.join(os.getcwd(), "output_action")

    if not os.path.isdir(output_dir):
        return {"error": "output_action directory does not exist"}

    # Get all .txt files
    txt_files = [
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.endswith(".txt")
    ]

    if not txt_files:
        return {"error": "No route files found"}

    # Find the newest file
    latest_file = max(txt_files, key=os.path.getctime)

    # Read content
    with open(latest_file, "r") as fp:
        content = fp.read()

    return content

# scans a public github repo by first cloning it and then parsing all filed.
@router.post("/scan-github")
async def scan_github(req: GitHubScanRequest):
    print("inside scan_github")
    repo_url = req.repo_url.rstrip("/")
    # TO-DO: update this to make the choice between master or main parameterized
    archive_url = repo_url + "/archive/refs/heads/main.zip"

    print(f"Downloading GitHub repo: {archive_url}")

    response = requests.get(archive_url)
    if response.status_code != 200:
        return {"error": "Could not download repo. Check if 'main' branch exists."}

    print("Extract to temporary folder")
    # Extract to temporary folder
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(temp_dir)

    # The repo extracts into a folder like repo-main/
    extracted_root = next(
        (os.path.join(temp_dir, d) for d in os.listdir(temp_dir)),
        None
    )
    print("extracting to: ", extracted_root)
    if not extracted_root:
        return {"error": "Extraction failed"}

    routes_list = []

    # Walk all PHP files recursively
    for root, _, files in os.walk(extracted_root):
        for f in files:
            if f.endswith(".php"):
                file_path = os.path.join(root, f)
                print(f"Scanning: {file_path}")

                with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()

                raw = agent.extract_routes(file_path, content)

                try:
                    cleaned = raw.strip().replace("```json", "").replace("```", "")
                    json_routes = json.loads(cleaned)
                    if isinstance(json_routes, list):
                        routes_list.extend(json_routes)
                except Exception as e:
                    print(f"JSON error in {file_path}: {e}")

    print("extracted routes, writing to output file. routes list length: ", len(routes_list))
    # TO-DO: Write to output_action, move this to common private method

    os.makedirs(OUTPUT_ACTION_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"routes_github_{timestamp}.txt"
    output_path = os.path.join(OUTPUT_ACTION_DIR, file_name)

    with open(output_path, "w") as f:
        for route in routes_list:
            f.write(route + "\n")

    return {
        "total_routes": len(routes_list),
        "output_file": output_path,
        "routes": routes_list
    }
