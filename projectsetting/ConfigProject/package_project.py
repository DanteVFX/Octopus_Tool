"""Create a package of the project based on the package type."""

# Import Standard Modules
import os
import json
import zipfile

# Import Third-party modules
import nuke



def package_project(package_path, package_name, package_type, json_path):
    # Read the JSON file
    with open(json_path, 'r') as json_file:
        project_data = json.load(json_file)

    project_name = project_data["project_name"]
    project_directory = project_data["project_directory"]

    # Create the package full path
    package_full_path = os.path.join(package_path, f"{package_name}.zip")

    # Verify the package type
    if package_type.lower() != 'zip':
        nuke.message("Currently, only ZIP packages are supported.")
        return

    # Create the ZIP file
    with zipfile.ZipFile(package_full_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        for root, dirs, files in os.walk(project_directory):
            # Add files to the ZIP even if they are empty
            folder_arcname = os.path.relpath(root, os.path.dirname(project_directory)) + '/'
            zip_info = zipfile.ZipInfo(folder_arcname)
            zipf.writestr(zip_info, '')

            # Add files to the ZIP
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(project_directory))
                zipf.write(file_path, arcname=arcname)

    nuke.message("Project exported successfully") 