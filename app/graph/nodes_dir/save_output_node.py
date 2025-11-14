import os
from datetime import datetime

def save_output_node(state):
    routes = state.get("routes", [])
    if not isinstance(routes, list):
        raise ValueError("[save_output_node] Invalid routes format")

    # Determine output directory (repo root + output_action)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    output_dir = os.path.join(base_dir, "output_action")
    os.makedirs(output_dir, exist_ok=True)

    # Create timestamped file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"routes_{timestamp}.txt"
    output_path = os.path.join(output_dir, filename)

    print(f"[save_output_node] Writing {len(routes)} routes to: {output_path}")

    # Write file
    with open(output_path, "w") as f:
        for route in routes:
            f.write(route + "\n")

    # Update state with file path
    state["output_file"] = output_path

    return state
