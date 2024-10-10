
# Import system modules
import os
import json
import threading
import re
import glob
import shutil

# Import Third-party modules
import nuke
from PySide2 import QtWidgets


def set_project_config(json_path):
    """
    Read a JSON file, update the 'project_directory' with the current directory and the 'project_path' 
    with the basename of the current directory.
    
    Args:
        json_path (str): The path to the JSON file that contains the project configuration.
    """
    try:
        # Get the current directory of the JSON file
        current_directory = os.path.dirname(json_path)
        basename = os.path.dirname(current_directory)
        
        # Read the JSON file
        with open(json_path, 'r') as json_file:
            project_data = json.load(json_file)
        
        # Update 'project_directory' with the current directory
        project_data["project_directory"] = current_directory
        
        # Update 'project_path' with the basename of the current directory
        project_data["project_path"] = basename
        
        # Save the updated JSON file
        with open(json_path, 'w') as json_file:
            json.dump(project_data, json_file, indent=4)

    except FileNotFoundError:
        print(f"JSON file not found: {json_path}")
    
    except json.JSONDecodeError:
        print("Error in decoding JSON file. Valid JSON file is required.")



def open_project_directory(json_path, parent=None):
    """
    Reads a JSON file and looks for the 'project_path', opens the Nuke 
    script in the selected directory.
    
    Args:
        json_path (str): The path to the JSON file to read and it contains
        the project configuration.
        
        parent (QtWidgets.QWidget, optional): The parent widget.
    """
    if os.path.exists(json_path) and json_path.endswith(".json"):
        try:
            # Read JSON to get 'project_path'
            with open(json_path, 'r') as json_file:
                project_data = json.load(json_file)
            
            if "project_directory" in project_data:
                project_dirctory = project_data["project_directory"]
                
                # Verify if project_dirctory exists
                if os.path.isdir(project_dirctory):
                    
                    nk_file, _ = QtWidgets.QFileDialog.getOpenFileName(
                        parent,
                        "Select Nuke Script",
                        project_dirctory,  
                        "Nuke Files (*.nk *.nknc)"
                    )
                    
                    if nk_file:
                        # Open Nuke script using nuke.scriptOpen
                        nuke.scriptOpen(nk_file)
                else:
                    print(f"'project_path' does not exist: {project_dirctory}")
            
        except json.JSONDecodeError:
            print("Error decoding JSON file. Verify format and try.")




def verify_read_nodes(json_path):
    """
    Iterate over all the Read nodes in the Nuke script and verify if the
    file paths are inside the project directory.
    If the file path is relative, convert it to an absolute path using the project root (project_directory).
    If the file path is outside the project directory, change the color of the node to red 
    and display a message.

    Args:
        json_path (str): Json file path containing the project name, project_path, and project_directory.
    """
    # Read the JSON file and get project_name, project_path, and project_directory
    with open(json_path, 'r') as json_file:
        project_data = json.load(json_file)
        project_name = project_data.get("project_name", "")
        project_path = project_data.get("project_path", "")
        project_directory = project_data.get("project_directory", "")

    # Validate that the necessary data exists
    if not project_name or not project_path or not project_directory:
        nuke.message("The JSON file does not contain 'project_name', 'project_path', or 'project_directory'.")
        return

    # Normalize the project directory path
    project_directory = os.path.normpath(project_directory)

    # List to store nodes that are outside the project directory
    external_nodes = []

    # Iterate over all Read nodes
    for read_node in nuke.allNodes("Read"):
        file_path = read_node['file'].value() 

        # If the path is relative, convert it to an absolute path based on the project_directory
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(os.path.join(project_directory, file_path))

        # Check if the file and project directory are on the same drive
        file_drive, project_drive = os.path.splitdrive(file_path)[0], os.path.splitdrive(project_directory)[0]

        if file_drive != project_drive:
            # If they are on different drives, treat the file as external
            read_node['tile_color'].setValue(int(0xFF0000FF))  # Set color to red
            external_nodes.append(f"{read_node.name()} (on different drive)")
        else:
            # Check if the file path is inside the project directory
            try:
                is_in_project_directory = os.path.commonpath([file_path, project_directory]) == project_directory
                contains_project_name = project_name in file_path

                if is_in_project_directory and contains_project_name:
                    # File is inside the project directory and contains the project name
                    read_node['tile_color'].setValue(0)  # Reset to default color
                else:
                    # File is outside the project directory or does not contain the project name
                    read_node['tile_color'].setValue(int(0xFF0000FF))  # Set color to red
                    external_nodes.append(read_node.name())  # Store the node name in the list
            except ValueError:
                # Handle ValueError when comparing paths
                nuke.message(f"Error comparing paths for node '{read_node.name()}'")
                read_node['tile_color'].setValue(int(0xFF0000FF))  # Set color to red

    # Show a message if there are external nodes, otherwise show all paths are within the project
    if external_nodes:
        nuke.message("The following Read Nodes reference files outside the project:\n" + "\n".join(external_nodes))
    else:
        nuke.message("All Read Nodes reference files are within the project directory.")



def convert_to_relative_path(json_path):
    """
    Convert all the file paths in the Nuke script to relative paths based on the project_name and project_path
    obtained from the JSON file.

    Args:
        json_path (str): Json file path containing the main data of the project.
    """

    with open(json_path, 'r') as json_file:
        project_data = json.load(json_file)
        project_path = project_data.get("project_directory", "")
        project_name = project_data.get("project_name", "")
    
    if not project_path or not project_name:
        nuke.message("JSON file does not contain 'project_path' or 'project_name'.")
        return

    # Normalize the project directory path
    project_directory = os.path.normpath(project_path)

    # Get all Read nodes
    read_nodes = nuke.allNodes('Read')

    # Verify if there are Read nodes
    if not read_nodes:
        nuke.message("There are no Read nodes in the project.")
        return

    nuke.root()["project_directory"].setValue("[python {nuke.script_directory()}]")

    # Iterate over all Read nodes
    for node in read_nodes:
        
        file_path = node['file'].value()

        # Convert backslashs (\) to forward slashes (/)
        file_path = file_path.replace("\\", "/")

        file_path_os = os.path.normpath(file_path)

        # Verify if it's an absolute path
        if os.path.isabs(file_path_os):
            # Check if the file and project directory are on the same drive
            if os.path.commonpath([os.path.abspath(file_path_os), project_directory]) == project_directory:
                # Convert the absolute path to a relative path
                relative_path = os.path.relpath(file_path_os, start=project_directory)

                # If the relative path is relative to the project directory, use ./ to indicate that
                if not relative_path.startswith('..'):
                    relative_path = "./" + relative_path 
                
                # Update the file path in the node with the relative path
                relative_path = relative_path.replace("\\", "/")
                node['file'].setValue(relative_path)

            else:
                # If the file and project directory are on different drives, treat the file as external
                relative_path = os.path.relpath(file_path_os, start=project_directory)
                relative_path = relative_path.replace("\\", "/")  
                node['file'].setValue(relative_path)



def normalize_path(path):

    path = os.path.expandvars(path)

    path = os.path.abspath(path)

    path = os.path.normpath(path)
    return path

def extract_base_name(file_path):
    """
    Extract the base name from the file path.
    """
    filename_with_ext = os.path.basename(file_path)
    # Remove placeholder or frame number
    base_name = re.sub(r'\.\%.*|\.\d+.*', '', filename_with_ext)
    # if after removing the placeholder or frame number, the base name is empty, use the filename
    base_name = os.path.splitext(base_name)[0]
    return base_name

def extract_format_and_sequence(file_path):
    """
    Extract the file format and sequence pattern from the file path.
    """
    filename_with_ext = os.path.basename(file_path)
    # Extract the file format
    file_format = os.path.splitext(filename_with_ext)[1][1:]  # Sin el punto inicial
    frame_match = re.search(r'\.(\%.*|\d+)\.', filename_with_ext)
    if frame_match:
        sequence_pattern = frame_match.group(1)
    else:
        sequence_pattern = None
    return sequence_pattern, file_format

def find_matching_files(directory, base_name, sequence_pattern, file_format):
    """
    Find matching files in the given directory based on the base name, sequence pattern, and file format.
    """
    # Covert sequence_pattern to %05d format if it's a number pattern with 5 digits
    if sequence_pattern and sequence_pattern.startswith('%') and sequence_pattern.endswith('d'):
        num_digits = int(sequence_pattern[1:-1])
        search_pattern = f"{base_name}." + "?" * num_digits + f".{file_format}"
    elif sequence_pattern and sequence_pattern.isdigit():
        num_digits = len(sequence_pattern)
        search_pattern = f"{base_name}." + "?" * num_digits + f".{file_format}"

    else:
        search_pattern = f"{base_name}.*.{file_format}"

    # Build the search pattern
    search_path = os.path.join(directory, search_pattern)
    # Use glob to find matching files
    matching_files = glob.glob(search_path)
    return matching_files

def copy_file_with_subprocess(src, dst):
    """
    Copy a file using a subprocess.
    """
    def copy_action():
        try:
            shutil.copy2(src, dst)
        except Exception as e:
            nuke.message(f"Error in copying {src} to {dst}:\n{e}")

    threading.Thread(target=copy_action).start()

def move_images_to_project(json_path):
    """
    Iterate over all the Read nodes and move images to the 'footage' directory within the project
    directory.

    Args:
        json_path (str): Full path to the JSON file.
    """
    with open(json_path, 'r') as json_file:
        project_data = json.load(json_file)
        project_directory = project_data.get("project_directory", "")
    
    if not project_directory:
        nuke.message("JSON File does not contain 'project_directory'.")
        return
    
    project_directory = normalize_path(project_directory)
    
    # Get footage directory from project data
    footage_dir = os.path.join(project_directory, "footage")
    
    # Create 'footage' directory if it doesn't exist
    if not os.path.exists(footage_dir):
        os.makedirs(footage_dir)
    
    # Iterate over all Read nodes
    for read_node in nuke.allNodes("Read"):
        file_path = read_node['file'].value() 
        
        # Normalize the file path
        file_path = normalize_path(file_path)
        
        # Verify if the file path is inside the project directory
        if not file_path.startswith(project_directory):
            
            # Extract base name, sequence pattern, and file format
            base_name = extract_base_name(file_path)
            sequence_pattern, file_format = extract_format_and_sequence(file_path)
            
            # Create the subfolder if it doesn't exist
            subfolder = os.path.join(footage_dir, base_name)
            if not os.path.exists(subfolder):
                os.makedirs(subfolder)

            if sequence_pattern and file_format:
                # Look for matching files in the subfolder and move them
                matching_files = find_matching_files(os.path.dirname(file_path), base_name, sequence_pattern, file_format)

                # Move the files to the subfolder
                for seq_file in matching_files:
                    new_file_path = os.path.join(subfolder, os.path.basename(seq_file))
                    copy_file_with_subprocess(seq_file, new_file_path)

                if sequence_pattern.startswith('%'):
                    new_sequence_path = os.path.join(subfolder, f"{base_name}.{sequence_pattern}.{file_format}")

                elif sequence_pattern.isdigit():
                    
                    num_digits = len(sequence_pattern)
                    new_sequence_pattern = '%' + f'0{num_digits}d'
                    new_sequence_path = os.path.join(subfolder, f"{base_name}.{new_sequence_pattern}.{file_format}")
                else:
                    # General format
                    new_sequence_path = os.path.join(subfolder, f"{base_name}.%04d.{file_format}")  

                new_sequence_path = new_sequence_path.replace("\\", "/")
                read_node['file'].setValue(new_sequence_path)

            else:
                # If no sequence pattern or file format, just copy the file to the subfolder
                new_file_path = os.path.join(subfolder, os.path.basename(file_path))
                copy_file_with_subprocess(file_path, new_file_path)

                # Update the path in the node
                new_file_path_correct = new_file_path.replace("\\", "/")
                read_node['file'].setValue(new_file_path_correct)
        
        # Reaload path to node in case it was changed
        read_node['reload'].execute()