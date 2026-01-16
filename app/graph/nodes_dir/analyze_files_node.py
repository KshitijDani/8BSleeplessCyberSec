import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.agents.cyber_agent import CyberAgent
from app.graph.constants import VULNERABILITY_FIELDNAMES
from openai import RateLimitError

agent = CyberAgent()   # reuse your existing agent

def analyze_file_node(state):
    php_files = state.get("php_files", [])
    if not php_files:
        raise ValueError("[analyze_file_node] No PHP files found in state.")

    all_vulns = []

    print(f"[analyze_file_node] Analyzing {len(php_files)} PHP files...")

    # TO-DO: move configurations to a separtae config file from where we read. Generalize it.
    MAX_FILES = 1  # Set to an int to limit files during testing; None processes all.
    files_to_process = php_files if MAX_FILES is None else php_files[:MAX_FILES]

    def process_file(file_path: str):
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

            cleaned = raw.strip().replace("```json", "").replace("```", "")
            vulns = json.loads(cleaned)

            normalized = []
            if isinstance(vulns, list):
                for vuln in vulns:
                    if not isinstance(vuln, dict):
                        print(f"[analyze_file_node] Skipping non-dict entry in {file_path}: {vuln}")
                        continue
                    normalized.append({field: vuln.get(field, "") for field in VULNERABILITY_FIELDNAMES})
            else:
                print(f"[analyze_file_node] Unexpected format (not a list) in file: {file_path}")

            print(f"[analyze_file_node] Extracted {len(normalized)} vulnerabilities from: {file_path}")
            return normalized

        except Exception as e:
            print(f"[analyze_file_node] Error analyzing {file_path}: {e}")
            return []

    # Parallelize file analysis (I/O-bound LLM calls)
    max_workers = min(8, len(files_to_process)) if files_to_process else 0
    with ThreadPoolExecutor(max_workers=max_workers or 1) as executor:
        future_to_file = {executor.submit(process_file, path): path for path in files_to_process}
        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                all_vulns.extend(future.result())
            except Exception as exc:
                print(f"[analyze_file_node] Unexpected executor error for {file_path}: {exc}")

    print(f"[analyze_file_node] Total vulnerabilities extracted from repo: {len(all_vulns)}")

    # Update state
    state["vulnerabilities"] = all_vulns

    return state
