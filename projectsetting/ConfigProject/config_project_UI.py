""" Config Project Tool UI """

# Import system modules
import sys
import os
import shutil

# Import Local Modules
from .config_project import *
from .package_project import *



# Import third-party modules
from PySide2 import QtCore, QtWidgets, QtGui


class ConfigProject(QtWidgets.QWidget):
   
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Config Project")
        self.setGeometry(900, 500, 450, 300)
        self.build_layout()

        self.load_settings()

        self.json_path_input.textChanged.connect(self.save_settings)
        
    def build_layout(self):
        lyt = QtWidgets.QVBoxLayout()
        self.setLayout(lyt)

        h_buttons_project = QtWidgets.QHBoxLayout()

        self.set_button = QtWidgets.QPushButton("Set Project")
        self.set_button.clicked.connect(self.get_set_project_config)

        self.open_button = QtWidgets.QPushButton("Open Project")
        self.open_button.clicked.connect(self.get_open_project_config)
        
        h_buttons_project.addWidget(self.set_button)
        h_buttons_project.addWidget(self.open_button)

        self.open_button.setEnabled(False)
        
        # Add the horizontal Layout to the Main Layout
        lyt.addLayout(h_buttons_project)

        # Add Line Separator
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        lyt.addWidget(line)

        # Create and add the horizontal layout for json path
        h_path_json = QtWidgets.QHBoxLayout()

        self.jsonLabel = QtWidgets.QLabel("JsonConfig path")
        #self.jsonLabel.clicked.connect(self.get_json_path)

        self.json_path_input = QtWidgets.QLineEdit()   
        self.json_path_input.textChanged.connect(self.enable_buttons_when_json_path_is_valid)  
        
        h_path_json.addWidget(self.jsonLabel)
        h_path_json.addWidget(self.json_path_input)

        # Instead of adding it as a widget, add it as a layout
        lyt.addLayout(h_path_json)

        # Add Line Separator
        line2 = QtWidgets.QFrame()
        line2.setFrameShape(QtWidgets.QFrame.HLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        lyt.addWidget(line2)

        # Create a Grid Layout
        gridlyt = QtWidgets.QGridLayout()

        self.btn = QtWidgets.QPushButton("Verify Nodes")
        self.btn2 = QtWidgets.QPushButton("Get External Files")
        self.btn3 = QtWidgets.QPushButton("Convert Relative Path")
        self.btn4 = QtWidgets.QPushButton("Package Project")

        # Buttons conected to functions
        self.btn.clicked.connect(self.get_verify_nodes)
        self.btn2.clicked.connect(self.get_external_files)
        self.btn3.clicked.connect(self.get_convert_relative_path)
        self.btn4.clicked.connect(self.get_package_project)


        # Diabled Buttons
        self.btn.setEnabled(False)
        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)
        self.btn4.setEnabled(False)
        
        # Add the buttons to the grid layout
        gridlyt.addWidget(self.btn, 0, 0)
        gridlyt.addWidget(self.btn2, 0, 1)
        gridlyt.addWidget(self.btn3, 1, 0)
        gridlyt.addWidget(self.btn4, 1, 1) 
        
        # Add Grid Layout to the Main Layout
        lyt.addLayout(gridlyt)

        # Add Exit Button
        btn_extra = QtWidgets.QPushButton("Exit")
        lyt.addWidget(btn_extra)

        btn_extra.clicked.connect(self.close)



    """ Save and Load Settings on the JsonConfig path """
    def save_settings(self):
        settings = QtCore.QSettings("MyCompany", "MyApp")  
        settings.setValue("json_path", self.json_path_input.text())  

    def load_settings(self):
        settings = QtCore.QSettings("MyCompany", "MyApp")
        saved_text = settings.value("json_path", "")  
        self.json_path_input.setText(saved_text)  

    """Override the closeEvent function to save the settings """

    def closeEvent(self, event):
        self.save_settings()  
        event.accept()

    def get_data_json(self):
        return self.json_path_input.text()

    def get_json_path(self):
        folder = QtWidgets.QFileDialog.getOpenFileName(
        self, "Select JSON File", "", "JSON Files (*.json)"
        )
        if folder[0]: 
            self.json_path_input.setText(folder[0])  


    """Funtions to check if the json path is valid""" 

    def enable_buttons_when_json_path_is_valid(self):
        json_path = self.json_path_input.text()

        # Check if the json path is valid
        if json_path.endswith(".json") and os.path.exists(json_path):
            self.open_button.setEnabled(True)
            self.btn.setEnabled(True)
            self.btn2.setEnabled(True)
            self.btn3.setEnabled(True)
            self.btn4.setEnabled(True)
        else:
            self.open_button.setEnabled(False)
            self.btn.setEnabled(False)
            self.btn2.setEnabled(False)
            self.btn3.setEnabled(False)
            self.btn4.setEnabled(False)

    """Set Project Button Configuration"""

    def get_set_project_config(self):
        json_file, _ =QtWidgets.QFileDialog.getOpenFileName(
            self, "Select JSON File", "", "JSON Files (*.json)"
        )
        if json_file:
            set_project_config(json_file)

            self.json_path_input.setText(json_file)

            set_project_config(json_file)

    """Open Project Button Configuration"""

    def get_open_project_config(self):

        json_file = self.json_path_input.text()
        if json_file:
            open_project_directory(json_file, parent=self)


    """ Verify Nodes Button Configuration """

    def get_verify_nodes(self):
        json_file = self.json_path_input.text()

        if json_file:
            verify_read_nodes(json_file)

    """ Get External Files Button Configuration """

    def get_external_files(self):
        json_file = self.json_path_input.text()
        if json_file:
            move_images_to_project(json_file)

    """ Convert Relative Path Button Configuration """

    def get_convert_relative_path(self):
        json_file = self.json_path_input.text()
        if json_file:
            convert_to_relative_path(json_file)

    """ Package Project Button Configuration """

    def get_package_project(self):
        
        window = show_package_project_UI()
        window.show()

        self.close()
            


def show_config_ui():
    # Initialize QApplication
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    global new_project_window
    new_project_window = ConfigProject()
    new_project_window.show()


"""
Here we create the Package Project UI
it is a subclass Widget for the Main Window

"""

class PackageProjectUI(QtWidgets.QTabWidget):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Package Project")
        self.setFixedSize(600, 200)

        self.build_layout()
        self.fullpath.setText(self.generate_fullpath())  

        # Connect signal    
        self.project_name_input.textChanged.connect(self.modify_label_path)
        self.project_path_input.textChanged.connect(self.modify_label_path)
        self.combo_box.currentIndexChanged.connect(self.modify_label_path)

        self.modify_label_path()

    def build_layout(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Create an Horizontal Layout for project name
        h_project_name = QtWidgets.QHBoxLayout()
        self.label_project_name = QtWidgets.QLabel("Package Name:")
        self.project_name_input = QtWidgets.QLineEdit()
        h_project_name.addWidget(self.label_project_name)
        h_project_name.addWidget(self.project_name_input)
        self.layout.addLayout(h_project_name)

        self.label_path_project = QtWidgets.QLabel("Select destination path for the package:")
        self.layout.addWidget(self.label_path_project)

        # Create an Horizontal Layout for project path and browse button
        h_project_path = QtWidgets.QHBoxLayout()
        self.project_path_input = QtWidgets.QLineEdit("Package destination path")
        self.browse_button = QtWidgets.QPushButton("Browse")

        # Connect the browse button to the browse_folder function
        self.browse_button.clicked.connect(self.browse_folder)

        # Add the QLineEdit and QPushButton to the layout horizontal
        h_project_path.addWidget(self.project_path_input)
        h_project_path.addWidget(self.browse_button)

        # Add the layout horizontal to the layout vertical
        self.layout.addLayout(h_project_path)

        # QLabel to show full path
        self.fullpath = QtWidgets.QLabel()
        self.fullpath.setStyleSheet("color: green;")
        self.layout.addWidget(self.fullpath)

        self.label_compresion = QtWidgets.QLabel("Select compression type:")
        self.layout.addWidget(self.label_compresion)

        # ComboBox to select compression type
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItem("ZIP")
        self.combo_box.addItem("TAR")
        self.layout.addWidget(self.combo_box)

        # Create an Horizontal Layout for Buttons
        h_buttons = QtWidgets.QHBoxLayout()
        self.create_package = QtWidgets.QPushButton("Package Project")
        self.create_package.clicked.connect(self.accept)
        self.cancel_package = QtWidgets.QPushButton("Cancel")
        self.cancel_package.clicked.connect(self.close)

        h_buttons.addWidget(self.create_package)
        h_buttons.addWidget(self.cancel_package)
        self.layout.addLayout(h_buttons)

    """Funciones que trabajan con la UI"""
    def browse_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Project Location")
        if folder:
            self.project_path_input.setText(folder)
        else:
            self.project_path_input.setPlaceholderText("Project Path")

    def modify_label_path(self):
        # Update QLabel with project path and project name
        self.fullpath.setText(self.generate_fullpath())

    def generate_fullpath(self):
        # Build full path using project name, project path and package type
        path = self.project_path_input.text()
        name = self.project_name_input.text()
        extension = self.combo_box.currentText().lower()
        if path and name:
            return f"{path}/{name}.{extension}"
        else:
            return "Please provide a valid path and package name."

    def get_package_path(self):
        return self.project_path_input.text()

    def get_package_name(self):
        return self.project_name_input.text()

    def get_package_type(self):
        return self.combo_box.currentText().lower()
    
    """ Triggered when the user clicks on the "Package Project" button"""

    def accept(self):

        package_path = self.get_package_path()
        package_name = self.get_package_name()
        package_type = self.get_package_type()

        js = ConfigProject()
        json_path = js.json_path_input.text()
        package_project(package_path, package_name, package_type, json_path)

        self.close()



"""Show Package Project UI"""

def show_package_project_UI():
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    global package_project_window
    package_project_window = PackageProjectUI()
    package_project_window.show()

