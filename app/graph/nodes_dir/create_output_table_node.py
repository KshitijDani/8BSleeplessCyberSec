import pandas as pd
import os
from datetime import datetime


def map_severity_to_score(severity):
    """
    Map severity level to numeric score.
    
    Mapping:
    - High -> 0
    - Medium -> 1
    - Low -> 2
    
    Args:
        severity (str): Severity level (High, Medium, Low)
        
    Returns:
        int: Numeric score for the severity
    """
    severity_map = {
        'High': 0,
        'Medium': 1,
        'Low': 2
    }
    return severity_map.get(severity, 2)  # Default to 2 (Low) if not found


def transform_vulnerability_data(input_file_path, output_dir="vulnerability_severity"):
    """
    Transform vulnerability data into a new table with renamed columns and severity scoring.
    
    Generic function that can process any CSV file from output_action directory.
    
    Columns mapping:
    - file_name -> file name
    - attack_type -> attack type
    - severity -> bug severity (converted to numeric: High=0, Medium=1, Low=2)
    
    Args:
        input_file_path (str): Path to the input CSV file in output_action directory
        output_dir (str): Name of the output directory (default: "vulnerability_severity")
        
    Returns:
        tuple: (pd.DataFrame with transformed data, str with output path)
    """
    
    # Create output directory if it doesn't exist
    app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_directory = os.path.join(app_dir, output_dir)
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Read the CSV file
    df = pd.read_csv(input_file_path)
    
    # Create a new dataframe with renamed columns
    output_table = df[['file_name', 'attack_type', 'severity']].copy()
    output_table.columns = ['file name', 'attack type', 'bug severity']
    
    # Map severity values to numeric scores
    output_table['bug severity'] = output_table['bug severity'].apply(map_severity_to_score)
    
    # Generate output filename based on input filename
    input_filename = os.path.basename(input_file_path)
    input_name_without_ext = os.path.splitext(input_filename)[0]
    output_filename = f"{input_name_without_ext}_formatted.csv"
    output_path = os.path.join(output_directory, output_filename)
    
    # Save the new table to the output directory
    output_table.to_csv(output_path, index=False)
    
    return output_table, output_path


def create_output_table(state):
    """
    Transform vulnerability data into a new table with renamed columns.
    
    Uses the latest CSV file from output_action directory.
    
    Args:
        state: The graph state containing vulnerabilities data
        
    Returns:
        Updated state with the new formatted table
    """
    
    # Find the latest CSV file in output_action directory
    output_action_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "output_action"
    )
    
    # Get all CSV files and find the most recent one
    csv_files = [f for f in os.listdir(output_action_dir) if f.endswith('.csv')]
    
    if not csv_files:
        return state
    
    # Get the most recent CSV file
    latest_csv = max(csv_files)
    csv_path = os.path.join(output_action_dir, latest_csv)
    
    # Transform the data
    output_table, output_path = transform_vulnerability_data(csv_path)
    
    # Update state with the new table
    state["formatted_vulnerabilities"] = output_table
    state["formatted_vulnerabilities_path"] = output_path
    
    return state
