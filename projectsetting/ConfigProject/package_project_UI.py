"""Configure the Package Project UI"""


# Import Standard Modules
import os
import sys

# Import third-party modules
from PySide2 import QtWidgets

# Import local modules
from .package_project import *


class PackageProjectUI(QtWidgets.QTabWidget):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Package Project")
        self.setFixedSize(600, 200)

        self.build_layout()
        self.fullpath.setText(self.generate_fullpath())  

        # Conectar señales
        self.project_name_input.textChanged.connect(self.modify_label_path)
        self.project_path_input.textChanged.connect(self.modify_label_path)
        self.combo_box.currentIndexChanged.connect(self.modify_label_path)

        self.modify_label_path()

    def build_layout(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Crear Horizontal Layout para el nombre del proyecto
        h_project_name = QtWidgets.QHBoxLayout()
        self.label_project_name = QtWidgets.QLabel("Package Name:")
        self.project_name_input = QtWidgets.QLineEdit()
        h_project_name.addWidget(self.label_project_name)
        h_project_name.addWidget(self.project_name_input)
        self.layout.addLayout(h_project_name)

        self.label_path_project = QtWidgets.QLabel("Select destination path for the package:")
        self.layout.addWidget(self.label_path_project)

        # Crear Horizontal Layout para la ruta del proyecto y el botón de navegación
        h_project_path = QtWidgets.QHBoxLayout()
        self.project_path_input = QtWidgets.QLineEdit("Package destination path")
        self.browse_button = QtWidgets.QPushButton("Browse")

        # Conectar el botón Browse a la función browse_folder
        self.browse_button.clicked.connect(self.browse_folder)

        # Agregar QLineEdit y QPushButton al layout horizontal
        h_project_path.addWidget(self.project_path_input)
        h_project_path.addWidget(self.browse_button)

        # Agregar el layout horizontal al layout principal
        self.layout.addLayout(h_project_path)

        # QLabel para mostrar la ruta completa
        self.fullpath = QtWidgets.QLabel()
        self.fullpath.setStyleSheet("color: green;")
        self.layout.addWidget(self.fullpath)

        self.label_compresion = QtWidgets.QLabel("Select compression type:")
        self.layout.addWidget(self.label_compresion)

        # ComboBox para seleccionar el tipo de compresión
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItem("ZIP")
        self.combo_box.addItem("TAR")
        self.layout.addWidget(self.combo_box)

        # Crear Horizontal Layout para los botones
        h_buttons = QtWidgets.QHBoxLayout()
        self.create_package = QtWidgets.QPushButton("Package Project")
        self.create_package.clicked.connect(self.accept)
        self.cancel_package = QtWidgets.QPushButton("Cancel")
        self.cancel_package.clicked.connect(self.reject)

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
        # Actualizar el QLabel con la ruta completa del paquete
        self.fullpath.setText(self.generate_fullpath())

    def generate_fullpath(self):
        # Construir la ruta completa usando el nombre del proyecto, la ruta y el tipo de compresión
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

        package_project()


"""Show Package Project UI"""
def show_package_project_UI():
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    global package_project_window
    package_project_window = PackageProjectUI()
    package_project_window.show()

    