from app.agents.cyber_agent import CyberAgent
from openai import RateLimitError
import json
import time

agent = CyberAgent()   # reuse your existing agent

def analyze_file_node(state):
    php_files = state.get("php_files", [])
    if not php_files:
        raise ValueError("[analyze_file_node] No PHP files found in state.")

    all_vulns = []

    print(f"[analyze_file_node] Analyzing {len(php_files)} PHP files...")

    # TO-DO: move configurations to a separtae config file from where we read. Generalize it.
    # TEMPORARY testing limiter
    # if you want only 2 files max
    MAX_FILES = 1  # To-DO change/remove later
    files_to_process = php_files[:MAX_FILES]

    # TO-DO: we should do this parallely instead of sequentially
    for file_path in files_to_process:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Call the vulnerability extraction LLM with simple backoff on 429s
            max_retries = 3
            base_wait = 20  # seconds
            attempt = 0
            raw = None

            while attempt <= max_retries:
                try:
                    raw = agent.extract_vulnerabilities(file_path, content)
                    break
                except RateLimitError as e:
                    attempt += 1
                    if attempt > max_retries:
                        raise
                    wait_time = base_wait * attempt
                    print(f"[analyze_file_node] Rate limited on {file_path}. Attempt {attempt}/{max_retries}. Waiting {wait_time}s.")
                    time.sleep(wait_time)

            if raw is None:
                raise RuntimeError("Failed to fetch vulnerabilities after retries.")

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
