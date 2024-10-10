import os
import json

import nuke
import nukescripts


def create_project_directory(base_path, project_name=None):
    """
    Create a project directory in the specified base path.
    
    Args:
        base_path (str): The base path where the project directory will be created.
        project_name (str): The name of the project. If not provided, the project directory will be created in the base path.

    Returns:
        str: The full path of the created project directory.
    """
    
    full_project_path = base_path if not project_name else os.path.join(base_path, project_name)

    # Create the project directory
    if not os.path.exists(full_project_path):
        os.makedirs(full_project_path)

    return full_project_path


def create_folders(project_path, folders):
    """
    Create the specified folders in the project path.

    Args:
        project_path (str): The path of the project.
        folders (list): A list of folders to create.

    """
    for folder in folders:
        full_folder_path = os.path.join(project_path, folder)
        if not os.path.exists(full_folder_path):
            os.makedirs(full_folder_path)


def set_default_save_path(save_path):
    """
    set the default save path
    """
    if not save_path.endswith("/"):
        save_path += "/"
    nuke.scriptSaveAs(save_path)

def set_script_directory():
    """
    set the script directory
    """
    
    directory_script = "[python {nuke.script_directory()}]"
    nuke.root()["project_directory"].setValue(directory_script)


def set_default_path_read_node():
    
    read_node = nukescripts.create_read()
    read_node["file"].setValue("[python {nuke.root().project_directory()}]")


def create_project_json(project_name, base_path, folders):
    """
    Create a JSON file with the project data.

    Args:
        project_name (str): Project name.
        base_path (str): Project base path.
        folders (list): A list of project folders.
    """
  
    # Get the script directory from the Nuke script path                                                         
    script_directory = nuke.script_directory()  

    # Calculate the relative path from the base path to the script directory
    relative_base_path = os.path.relpath(base_path, script_directory)

    project_data = {
        "project_name": project_name,
        "base_path": relative_base_path,
        "folders": folders
    }
    
    # Define JSON file path
    json_file_path = os.path.join(base_path, "project_config.json")

    # Create JSON file with project data
    with open(json_file_path, 'w') as json_file:
        json.dump(project_data, json_file, indent=4)



def convert_read_node_paths_to_relative():
   
    project_directory = os.path.dirname(nuke.root().name())
    project_name = os.path.basename(project_directory)

    project_directory = os.path.normpath(project_directory)

    # Iterate over all Read nodes
    for node in nuke.allNodes('Read'):
        # Get the file path
        file_path = node['file'].value()

        # Convert \ to /
        file_path = file_path.replace("\\", "/")

        file_path_os = os.path.normpath(file_path)

        if os.path.isabs(file_path_os):
            # Check if the file path is inside the project directory
            if os.path.commonpath([os.path.abspath(file_path_os), project_directory]) == project_directory:
                # Convert to relative path
                relative_path = os.path.relpath(file_path_os, start=project_directory)

                if not relative_path.startswith('..'):
                    relative_path = "./" + relative_path 
                
                # Update the file path  
                relative_path = relative_path.replace("\\", "/")
                node['file'].setValue(relative_path)

            else:
                # If the file path is outside the project directory, do nothing
                relative_path = os.path.relpath(file_path_os, start=project_directory)
                relative_path = relative_path.replace("\\", "/")  # Reemplazar por forward slashes
                node['file'].setValue(relative_path)

        


def remove_project_from_favorites(project_name):
    """
    Eliminate favorite directories for the project with the given name.
    """
    try:
        nuke.removeFavoriteDir(project_name)
    except RuntimeError:
        pass

def add_project_to_favorites(project_dir, project_name):
    project_name = os.path.basename(project_dir)
    
    remove_project_from_favorites(project_name)
    
    nuke.addFavoriteDir(
        name=project_name, 
        directory=project_dir, 
        type=(nuke.IMAGE | nuke.SCRIPT | nuke.GEO),  
        tooltip=f'Project Directory: {project_name}'
    )
    

def save_project_config(project_name, project_path, project_directory):
    """
    Save the project configuration in a JSON file, including relative paths.

    Args:
        project_name (str): Project name.
        project_path (str): Project path.
        project_directory (str): Project directory.
    """
    project_dir = os.path.normpath(project_directory)
    
    # Define the JSON file path
    config_file = os.path.join(project_dir, "project_config.json")
    
    # Create a dictionary with the project data to save
    project_data = {
        "project_name": project_name,
        "project_path": project_path,
        "project_directory": project_dir
    }
    
    # Save JSON file
    try:
        with open(config_file, 'w') as json_file:
            json.dump(project_data, json_file, indent=4)
        
    except IOError as e:
        nuke.message(f"Error al guardar la configuración del proyecto: {e}")