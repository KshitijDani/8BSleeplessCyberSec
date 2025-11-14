import shutil

# Last node in the graph, this is to remove any unnecessary files
def cleanup_node(state):
    temp_dir = state.get("temp_dir")

    if temp_dir and isinstance(temp_dir, str):
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"[cleanup_node] Deleted temp directory: {temp_dir}")
        except Exception as e:
            print(f"[cleanup_node] Error deleting temp directory {temp_dir}: {e}")
    else:
        print("[cleanup_node] No temp_dir found in state.")

    return state