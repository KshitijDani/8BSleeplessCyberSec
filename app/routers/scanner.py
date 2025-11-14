import os
from fastapi import APIRouter

router = APIRouter()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
OUTPUT_ACTION_DIR = os.path.join(BASE_DIR, "output_action")


# gets all the latest routes in the output_action directory text file, then opens the file and returns all the endpoints
@router.get("/latest-routes")
async def get_latest_routes():
    output_dir = OUTPUT_ACTION_DIR

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