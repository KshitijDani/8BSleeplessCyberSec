from app.agents.cyber_agent import CyberAgent
import json

agent = CyberAgent()   # reuse your existing agent

def analyze_file_node(state):
    php_files = state.get("php_files", [])
    if not php_files:
        raise ValueError("[analyze_file_node] No PHP files found in state.")

    all_vulns = []

    print(f"[analyze_file_node] Analyzing {len(php_files)} PHP files...")

    # TEMPORARY testing limiter
    # if you want only 2 files max
    MAX_FILES = 1   # To-DO change/remove later
    files_to_process = php_files[:MAX_FILES]

    for file_path in files_to_process:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Call the vulnerability extraction LLM
            raw = agent.extract_vulnerabilities(file_path, content)

            # Clean & parse JSON LLM output
            cleaned = raw.strip().replace("```json", "").replace("```", "")
            vulns = json.loads(cleaned)

            if isinstance(vulns, list):
                all_vulns.extend(vulns)
            else:
                print(f"[analyze_file_node] Unexpected format (not a list) in file: {file_path}")

            print(f"[analyze_file_node] Extracted {len(vulns)} vulnerabilities from: {file_path}")

        except Exception as e:
            print(f"[analyze_file_node] Error analyzing {file_path}: {e}")

    print(f"[analyze_file_node] Total vulnerabilities extracted from repo: {len(all_vulns)}")

    # Update state
    state["vulnerabilities"] = all_vulns

    return state
