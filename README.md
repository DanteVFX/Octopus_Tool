# Octopus_Tool [BETA]
This is tool is useful for Nuke Artist Who want to organize their project files and have correct paths
- Octopus Tool for Nuke

![octopus](https://github.com/user-attachments/assets/0a20c4be-3d90-4fc1-b079-413dec9b1fd0)


## Table of Contents

1. [How to Use](#how-to-use)
   - [New Project](#new-project)
   - [Config Project](#config-project)
   - [Buttons Configuration](#buttons-configuration)
2. [Instalation](#how-to-use)
  
4. [Recomendation](#how-to-use)

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

#### Result of Create Project
- After create the project, you will find a json file(don't delete it).
This Json containts information such as project path, project name. 
  
![json_create](https://github.com/user-attachments/assets/026f8498-ee3a-411d-b6d1-b1943514f3a6)


## Config Project

![Config_Tool](https://github.com/user-attachments/assets/04437246-ebbc-447a-a825-e8029958d60f)

The option at the beginning will be unable, to activate the option you need to vinculate the json created to the path.


## Buttons Configuration
### Set Project:
This button looks for a JSON file to retrieve the project paths.
Verify that the JSON file connected to the UI is the project you want to work on, or you can modify another project if needed.
In case you've moved the project to a different location, this button will update the paths inside the JSON file, as the current directory will now be where the project is set to work.

### Open Project:
   Available when a JSON file is connected.
This button read the project directory path inside the JSON file and open the project path directly.

### Verify Read Nodes:
   Available when a JSON file is connected.
This button will iterate over all Read nodes and check if their reference files are located outside the project directory.
It will change the color of Read nodes that reference files outside the project.



### Get External Files:
 Available when a JSON file is connected.

This button allows you to copy external files and move them to the project directory. By default, it will create a "footage" folder where the external files will be copied.
If the folder already exists, the files will be placed inside it.

### Convert to Relative Path:
Available when a JSON file is connected.

Working with relative paths is essential when collaborating in a team. This feature converts the file paths of Read nodes into relative paths.

### Package Project:
 Available when a JSON file is connected.
 
The tool will package all project contents, including assets and scripts, into a `.zip` file ready to be shared or archived.
This option makes it easy to deliver the project to other teams or store a well-organized backup.

---

# How To Install Plugin in Nuke

To install a plugin in Nuke, follow these steps:

1. **Create a New Folder for the Plugin:**
   - Navigate to the path `C:/Users/<your-username>/.nuke/` (replace `<your-username>` with your actual username).
   - Create a new folder inside `.nuke/` and name it `"NewPlugin"`. This will be the directory where your plugin files will reside.

2. **Create or Edit the `init.py` File:**
   - Inside the `.nuke/` directory, create a file called `init.py` (if it doesn’t already exist).
   - Open `init.py` in a text editor and add the following code:
     ```python
     import nuke
     
     nuke.pluginAddPath("./NewPlugin")
     nuke.pluginAddPath("./scripts")
     ```

3. **Move the Plugin Files:**
   - Place the plugin files inside the `NewPlugin` folder you created earlier. This is where Nuke will search for the plugin scripts.

4. **Restart Nuke:**
   - After saving the changes to `init.py` and adding the plugin files, restart Nuke to load the plugin.

5. **Verify Installation:**
   - Once Nuke is open, verify that the plugin is correctly installed by checking the relevant menus or running any associated commands.


