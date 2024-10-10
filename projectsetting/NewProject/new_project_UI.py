
# Import system modules
import sys

# Import Third-party modules
from PySide2 import QtWidgets, QtCore

# Import local modules
from ..NewProject.new_project import *


class NewProjectUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Project")
        self.setGeometry(900, 500, 400, 500)
        self.build_layout()

        # Project Path Default
        self.project_path_input.setPlaceholderText("Project Path")

        # Update Text (project Path Complete)
        self.project_name_input.textChanged.connect(self.update_combined_label)
        self.project_path_input.textChanged.connect(self.update_combined_label)

        

    def build_layout(self):

        # Create Main Layout will contain all Widgets
        lyt = QtWidgets.QVBoxLayout()
        self.setLayout(lyt)

        # Create Horizontal Layout Project Name & QLineEdit
        h_name_layout = QtWidgets.QHBoxLayout()

        # Create Label Project Name & QLineEdit
        self.project_name_label = QtWidgets.QLabel("Project Name:")
        self.project_name_input = QtWidgets.QLineEdit()

        # Add to the Horizontal Layout
        h_name_layout.addWidget(self.project_name_label)
        h_name_layout.addWidget(self.project_name_input)

        # Add the Horizontal Layout to the Main Layout
        lyt.addLayout(h_name_layout)

        

        # Create Horizontal Layout to project path & Browser button
        h_project_path = QtWidgets.QHBoxLayout()
        self.project_path_input = QtWidgets.QLineEdit()
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.create_project_action)

        # Button Connected to browse_folder
        self.browse_button.clicked.connect(self.browse_folder)

        # Add QLineEdit & QPushButton to horizontal layout
        h_project_path.addWidget(self.project_path_input)
        h_project_path.addWidget(self.browse_button)

        # Add the horizontal Layout to the Main Layout
        lyt.addLayout(h_project_path)

        # Add label "complete path"
        path_complete_label = QtWidgets.QLabel("Path Complete:")
        lyt.addWidget(path_complete_label)

        # Dynamic label, to the directory project
        self.path_complete_directory = QtWidgets.QLabel()
        self.path_complete_directory.setStyleSheet("color: green;")
        lyt.addWidget(self.path_complete_directory)

        # Add Line Separator
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        lyt.addWidget(line)

        """ First List """

        self.main_folders_label = QtWidgets.QLabel("Project Folders(Default):")
        self.main_folders_list = QtWidgets.QListWidget()

        # List of Main folder
        main_folders = ["comp", "footage", "render", "script", "video"]

        for folder in main_folders:
            # Create a QListWidgetItem with the items
            item = QtWidgets.QListWidgetItem(folder)

            # Make items checklist"
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable |
                          QtCore.Qt.ItemIsEditable)
            item.setCheckState(QtCore.Qt.Checked)

            # Add items to the list
            self.main_folders_list.addItem(item)

        # Add Project Folders & List to the Main Layout
        lyt.addWidget(self.main_folders_label)
        lyt.addWidget(self.main_folders_list)

        # Add Line Separator
        line2 = QtWidgets.QFrame()
        line2.setFrameShape(QtWidgets.QFrame.HLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        lyt.addWidget(line2)

        """ Second List """

        # Optional Folders Label & List
        self.optional_folders_label = QtWidgets.QLabel("Custom Folders:")
        self.optional_folders_list = QtWidgets.QListWidget()

        # List of Optional folder
        optional_folders = ["Custom1", "Custom2", "Custom3", "Custom4",]

        for folder in optional_folders:
            # Get items from the List
            item = QtWidgets.QListWidgetItem(folder)

            # Make CheckList
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable |
                          QtCore.Qt.ItemIsEditable)
            item.setCheckState(QtCore.Qt.Unchecked)

            # Add Items to the List
            self.optional_folders_list.addItem(item)

        # Add Optional Folders & List to the Main Layout
        lyt.addWidget(self.optional_folders_label)
        lyt.addWidget(self.optional_folders_list)

        """ Create Buttons """

        # Create Horizontal Layout for the Buttons
        h_buttons = QtWidgets.QHBoxLayout()

        # Create Buttons ( Create Project & Cancel)
        self.create_project_button = QtWidgets.QPushButton("Create Project")
        self.create_project_button.clicked.connect(self.create_project_action)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        # Add the Buttons to the horizontal Layout
        h_buttons.addWidget(self.create_project_button)
        h_buttons.addWidget(self.cancel_button)

        # Add Horizontal Buttons to the Main Layout
        lyt.addLayout(h_buttons)

    """Functions For labels"""
    def browse_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Project Location")
        if folder:
            self.project_path_input.setText(folder)
        else:
            self.project_path_input.setPlaceholderText("Project Path")

    def update_combined_label(self):

        project_path = self.project_path_input.text()
        project_name = self.project_name_input.text()

        if project_path and project_name:
            combined_text = f"{project_path}/{project_name}"
        else:
            combined_text = f"{project_path}"

            # Update the Dynamic Label
        self.path_complete_directory.setText(combined_text)

    """GET DATA FROM UI"""
    def get_directory(self):
        full_path = self.path_complete_directory.text()

        return full_path

    def get_selected_items_list(self):

        main_folders = self.main_folders_list
        optional_folders = self.optional_folders_list

        # Get selected elements from the Main Folders
        main_folders_selected = [
            item.text() for item in main_folders.findItems(
                '*', QtCore.Qt.MatchWildcard)
            if item.checkState() == QtCore.Qt.Checked
        ]

        # Get selected elements from the Optional Folders
        optional_folders_selected = [
            item.text() for item in optional_folders.findItems(
                '*', QtCore.Qt.MatchWildcard)
            if item.checkState() == QtCore.Qt.Checked
        ]

        # Combine both lists
        selected_items = main_folders_selected + optional_folders_selected

        return selected_items

    def get_project_path(self):
        return self.project_path_input.text()

    def get_project_name(self):
        return self.project_name_input.text()
    
    """ EXECUTE Create Project Button  """

    def create_project_action(self):
        """
        Call function to create the project.
        """
        project_directory = self.get_directory()
        project_path = self.get_project_path()  
        project_name = self.get_project_name()  
        
        if project_path:
            # Functions from new_project.py
            created_project_path = create_project_directory(project_path, project_name)  
                     
            folders_to_create = self.get_selected_items_list()  

            create_folders(created_project_path, folders_to_create)                       
            
            set_default_save_path(self.get_directory())
            
            if set_default_save_path:
                set_script_directory()

            save_project_config(project_name, project_path, project_directory)            
            
            self.close()

        add_project_to_favorites(project_directory, project_name)

    
    
    """MENU COMMANDS"""
    
    def verify_read_node_paths(self):

        # Obtener el directorio del proyecto
        project_directory = nuke.script_directory()
        # Lista para almacenar nodos Read con rutas externas
        external_nodes = []
        
        # Recorremos todos los nodos en el script
        for node in nuke.allNodes('Read'):
            # Obtener la ruta del archivo del nodo
            file_path = node['file'].value()
            
            # Convertir la ruta del archivo a una ruta absoluta
            absolute_file_path = os.path.abspath(file_path)
            
            # Si el archivo es relativo, resolverlo en base al directorio del proyecto
            if not os.path.isabs(file_path):
                absolute_file_path = os.path.abspath(os.path.join(project_directory, file_path))
            
            # Verificar si la ruta del archivo está dentro del directorio del proyecto
            if not is_path_within_directory(absolute_file_path, project_directory):
                # Cambiar el color del nodo a rojo si está fuera del directorio
                node['tile_color'].setValue(4278190335)  # Color rojo (ARGB)
                external_nodes.append(node.name())
            else:
                # Si estaba rojo y ahora está dentro del directorio, restaurar color
                if node['tile_color'].value() == 4278190335:  # Color rojo
                    node['tile_color'].setValue(0)  # Color original (sin color)
        
        # Si hay nodos externos, mostrar un mensaje
        if external_nodes:
            nuke.message("Next nodes paths are not in the project directory:\n" + "\n".join(external_nodes))
        else:
            nuke.message("All File Paths are in the project directory.")

        def is_path_within_directory(file_path, directory):
            # Obtener la ruta absoluta del directorio
            abs_directory = os.path.abspath(directory)
            # Verificar si el archivo comienza con la ruta del directorio
            return os.path.commonprefix([file_path, abs_directory]) == abs_directory
        
        

    def convert_read_node_paths_to_relative():
        # Obtener el nombre del proyecto o la carpeta del proyecto si no tiene nombre
        project_directory = os.path.dirname(nuke.root().name())
        project_name = os.path.basename(project_directory)

        # Normalizar la ruta del directorio del proyecto
        project_directory = os.path.normpath(project_directory)

        # Recorremos todos los nodos 'Read'
        for node in nuke.allNodes('Read'):
            # Obtener la ruta del archivo del nodo
            file_path = node['file'].value()

            # Convertir backslashes (\) a forward slashes (/)
            file_path = file_path.replace("\\", "/")

            # Convertir la ruta a formato del sistema operativo
            file_path_os = os.path.normpath(file_path)

            # Verificar si la ruta es absoluta
            if os.path.isabs(file_path_os):
                # Comprobar si el archivo está dentro del directorio del proyecto
                if os.path.commonpath([os.path.abspath(file_path_os), project_directory]) == project_directory:
                    # Convertir a ruta relativa desde el directorio del proyecto
                    relative_path = os.path.relpath(file_path_os, start=project_directory)

                    # Si el archivo está dentro del proyecto o subdirectorio, usamos ./ o ninguna modificación
                    if not relative_path.startswith('..'):
                        relative_path = "./" + relative_path  # Asegurar el uso de ./ para subdirectorios
                    
                    # Actualizar el nodo con la nueva ruta relativa y reemplazar backslashes por slashes
                    relative_path = relative_path.replace("\\", "/")
                    node['file'].setValue(relative_path)

                else:
                    # Si el archivo está fuera del proyecto, usar ../ para subir niveles
                    relative_path = os.path.relpath(file_path_os, start=project_directory)
                    relative_path = relative_path.replace("\\", "/")  # Reemplazar por forward slashes
                    node['file'].setValue(relative_path)

    

        
"""UI"""
    
def show_ui():
    # Initialize QApplication
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    global new_project_window
    new_project_window = NewProjectUI()
    new_project_window.show()
    