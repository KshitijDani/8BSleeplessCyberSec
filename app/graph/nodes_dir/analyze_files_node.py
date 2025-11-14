from app.agents.cyber_agent import CyberAgent
import json

agent = CyberAgent()   # reuse your existing agent

def analyze_file_node(state):
    php_files = state.get("php_files", [])
    if not php_files:
        raise ValueError("[analyze_file_node] No PHP files found in state.")

    all_routes = []

    print(f"[analyze_file_node] Analyzing {len(php_files)} PHP files...")

    for file_path in php_files:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Call the CyberAgent LLM extraction
            raw = agent.extract_routes(file_path, content)

            # Clean & parse JSON from LLM output
            cleaned = raw.strip().replace("```json", "").replace("```", "")
            routes = json.loads(cleaned)

            if isinstance(routes, list):
                all_routes.extend(routes)

            print(f"[analyze_file_node] Extracted {len(routes)} routes from: {file_path}")

        except Exception as e:
            print(f"[analyze_file_node] Error reading or analyzing {file_path}: {e}")

    print(f"[analyze_file_node] Total routes extracted from repo: {len(all_routes)}")

    # Update state with aggregated routes
    state["routes"] = all_routes

    return state
