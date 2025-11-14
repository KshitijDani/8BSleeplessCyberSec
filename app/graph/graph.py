from langgraph.graph import StateGraph
from app.graph.state import AnalysisState
from app.graph.nodes_dir.start_node import start_node
from app.graph.nodes_dir.fetch_repo_node import fetch_repo_node
from app.graph.nodes_dir.cleanup_node import cleanup_node
from app.graph.nodes_dir.extract_php_files_node import extract_php_files_node
from app.graph.nodes_dir.analyze_files_node import analyze_file_node
from app.graph.nodes_dir.save_output_node import save_output_node


def build_graph():
    graph = StateGraph(AnalysisState)
    
    # TO-DO: create a seprate intialize_nodes() to add all nodes and then call the method here
    graph.add_node("start", start_node)
    graph.add_node("fetch_repo", fetch_repo_node)
    graph.add_node("cleanup", cleanup_node)
    graph.add_node("extract_php_files_node", extract_php_files_node)
    graph.add_node("analyze_file_node", analyze_file_node)
    graph.add_node("save_output_node", save_output_node)


    graph.set_entry_point("start")
    graph.add_edge("start", "fetch_repo")
    graph.add_edge("fetch_repo", "extract_php_files_node")
    graph.add_edge("extract_php_files_node", "analyze_file_node")
    graph.add_edge("analyze_file_node", "save_output_node")

    # this edge needs to ochange to whatever the second last node is
    graph.add_edge("save_output_node", "cleanup")

    workflow = graph.compile()
    return workflow
