import os
import csv
from fastapi import APIRouter

router = APIRouter()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
OUTPUT_ACTION_DIR = os.path.join(BASE_DIR, "output_action")


@router.get("/latest-vulnerabilities")
async def get_latest_vulnerabilities():
    output_dir = OUTPUT_ACTION_DIR

    if not os.path.isdir(output_dir):
        return {"error": "output_action directory does not exist"}

    # Get all .csv files
    csv_files = [
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.endswith(".csv")
    ]

    if not csv_files:
        return {"error": "No vulnerability CSV files found"}

    # Find the newest file
    latest_file = max(csv_files, key=os.path.getctime)

    # Read CSV into a list of JSON objects
    json_rows = []
    with open(latest_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert CSV row (OrderedDict) → normal dict
            json_rows.append(dict(row))

    return {
        "file": os.path.basename(latest_file),
        "count": len(json_rows),
        "results": json_rows
    }
