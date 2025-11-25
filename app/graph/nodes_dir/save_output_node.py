import os
import csv
from datetime import datetime
from app.graph.constants import VULNERABILITY_FIELDNAMES

def save_output_node(state):
    vulnerabilities = state.get("vulnerabilities", [])
    if not isinstance(vulnerabilities, list):
        raise ValueError("[save_output_node] Invalid vulnerabilities format")

    # Resolve project root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    output_dir = os.path.join(base_dir, "output_action")
    os.makedirs(output_dir, exist_ok=True)

    # Timestamped CSV file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"vulnerabilities_{timestamp}.csv"
    output_path = os.path.join(output_dir, filename)

    print(f"[save_output_node] Writing {len(vulnerabilities)} rows to: {output_path}")

    # Write CSV
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=VULNERABILITY_FIELDNAMES)
        writer.writeheader()

        for entry in vulnerabilities:
            # Ensure missing fields don't break the CSV
            row = {key: entry.get(key, "") for key in VULNERABILITY_FIELDNAMES}
            writer.writerow(row)

    # Save output path into state
    state["output_file"] = output_path

    return state
