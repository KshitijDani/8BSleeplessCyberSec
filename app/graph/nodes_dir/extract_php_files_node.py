import os

def extract_php_files_node(state):
    repo_dir = state.get("repo_dir")

    if not repo_dir or not os.path.isdir(repo_dir):
        raise ValueError("[extract_php_files_node] repo_dir is missing or invalid.")

    php_files = []

    # Walk through all directories & files
    for root, _, files in os.walk(repo_dir):
        for f in files:
            if f.lower().endswith(".php"):
                full_path = os.path.join(root, f)
                php_files.append(full_path)

    print(f"[extract_php_files_node] Found {len(php_files)} PHP files.")

    # Update state
    state["php_files"] = php_files

    return state