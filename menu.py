"""Menu Project Setting Tool."""

# Import local module
from projectsetting.NewProject.new_project_UI import show_ui
from projectsetting.ConfigProject.config_project_UI import show_config_ui


# Import third-party module
import nuke


""" ProjectFlow Menu Commands """
project_flow_menu = nuke.menu('Nuke').addMenu('Octopus V0.5 BETA')
project_flow_menu.addCommand('New Project',show_ui , index=0)
project_flow_menu.addCommand('Config Project', show_config_ui , index=1)



