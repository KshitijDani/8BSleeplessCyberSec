
import requests
import tempfile
import zipfile
import io
import os

# Second node in the graoh
def fetch_repo_node(state):
    repo_url = state.get("repo_url")
    if not repo_url:
        raise ValueError("repo_url not found in state")

    repo_url = repo_url.rstrip("/")

    # Build archive URL (assumes 'main' branch for now)
    archive_url = f"{repo_url}/archive/refs/heads/main.zip"
    print(f"[fetch_repo_node] Downloading archive: {archive_url}")

    response = requests.get(archive_url)
    if response.status_code != 200:
        raise ValueError(
            f"Failed to download repo ZIP. Status: {response.status_code}"
        )

    # Create a temporary directory for extraction
    temp_dir = tempfile.mkdtemp()
    print(f"[fetch_repo_node] Extracting into temp directory: {temp_dir}")

    # Extract ZIP
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(temp_dir)

    # GitHub ZIPs extract into a directory like "<repo>-main/"
    extracted_dirs = os.listdir(temp_dir)
    if not extracted_dirs:
        raise ValueError("Extraction produced no directories.")

    # Usually the first directory is the repo folder
    extracted_root = os.path.join(temp_dir, extracted_dirs[0])
    print(f"[fetch_repo_node] Repo extracted root: {extracted_root}")

    # Update graph state
    state["temp_dir"] = temp_dir
    state["repo_dir"] = extracted_root

    return state