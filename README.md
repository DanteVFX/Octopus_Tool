# Octopus_Tool [BETA]
This is tool is useful for Nuke Artist Who want to organize their project files and have correct paths
- Octopus Tool for Nuke

![octopus](https://github.com/user-attachments/assets/0a20c4be-3d90-4fc1-b079-413dec9b1fd0)


## Table of Contents

1. [How to Use](#how-to-use)
   - [New Project](#new-project)
   - [2nd. Set Project](#2nd-set-project)
2. [Instalation](#how-to-use)
3. [Recomendation](#how-to-use)
   - [3rd. Open Project](#3rd-open-project)
   - [4th. Verify Read Nodes](#4th-verify-read-nodes)
   - [5th. Get External Files](#5th-get-external-files)
   - [6th. Convert to Relative Path](#6th-convert-to-relative-path)
   - [7th. Package Project](#7th-package-project)

### Description

**Octopus_Tool_BETA** is a project management tool built to simplify project configuration and asset management within the Nuke VFX pipeline. This tool allows users to configure projects, set project directories, manage file paths, get external File from project directory &  create relative paths.
### Features

- **Set Project**: Easily set the active project configuration by selecting a JSON file that defines the project's structure.
- **Open Project**: Open an existing project based on the selected JSON configuration.
- **Verify Read Nodes**: Check if Read nodes in the Nuke script reference files outside the project directory and highlight them.
- **Get External Files**: Automatically copy external files into the project folder for better organization.
- **Convert to Relative Path**: Convert file paths to relative paths based on the project directory.
- **Package Project**: Package the entire project, including assets and scripts, into a `.zip` file for easy sharing or backup


## How to Use

The tool provides a simple graphical interface to manage projects in Nuke. Below are the main functionalities and how to use them:

### New Project:

- In this window, you can select the **project name** and the **directory path** where it will be located. These two pieces of information are crucial to ensure that the project is well organized.

- You have the option to **modify the folder names** if you want to customize the structure to your liking. For example, you can change the default folder names for assets, renders, etc.

- Once you have set the project name and path, you will be prompted to **save the project**. This step is **very important**, as a **JSON file** will be created, containing all relevant information about the project, ensuring that there are no problems with file management in the future.

![Create](https://github.com/user-attachments/assets/aaa89e40-acfb-41d1-b716-8e9d19e2ddd3)

#### Resukt of Create Project
- After create the project, you will find a json file(don't delete it, it the path of the project, it's usefull if you change of project or if you transfer it to other artist)
  
![json_create](https://github.com/user-attachments/assets/026f8498-ee3a-411d-b6d1-b1943514f3a6)


## Config Project

![Config_Tool](https://github.com/user-attachments/assets/04437246-ebbc-447a-a825-e8029958d60f)


### 2nd. Set Project:

- This option allows you to select an existing JSON file that contains the project configuration.
- Once selected, the tool will load all the necessary paths and settings to activate the project in Nuke.

### 3rd. Open Project:

- Use this option to load an existing project based on its JSON configuration file.
- This ensures that all relative paths and referenced files are correctly configured, making it easy to open previously created projects.

### 4th. Verify Read Nodes:

- This option checks all the Read nodes in your Nuke script.
- If any Read node references files located outside the project directory, they will be highlighted, and a message will indicate which nodes are pointing to external files.

### 5th. Get External Files:

- This feature allows you to automatically copy all external files (those outside the project folder) into the project folder structure.
- This way, all assets will be located inside the project, making it easier to manage and share the project.

### 6th. Convert to Relative Path:

- This option converts all file paths in the project to relative paths based on the project directory.
- It is useful to ensure that paths work correctly when moving the project between different computers or operating systems.

### 7th. Package Project:

- The tool will package all project contents, including assets and scripts, into a `.zip` file ready to be shared or archived.
- This option makes it easy to deliver the project to other teams or store a well-organized backup.

---

### Summary

This tool simplifies project management in Nuke by automating many common tasks such as verifying paths, organizing files, and packaging the project. By following these steps, you can manage your projects efficiently and ensure that all paths and files are properly organized for future use.
