import maya.cmds as cmds
import sys


def add_custom_menu():
    if cmds.menu("CustomToolsMenu", exists=True):
        cmds.deleteUI("CustomToolsMenu", menu=True)
    
    # Menü erstellen
    cmds.menu("CustomToolsMenu", label="Custom Tools", parent="MayaWindow")
    cmds.menuItem(label="Export FBX Tool", command=lambda _: load_export_tool())

def load_export_tool():
    sys.path.append(r"N:\GOLEMS_FATE\crew\Jan\Scripts\MayaScripts")
    import export_fbx_tool
    export_fbx_tool.create_export_ui()

# Menü hinzufügen
add_custom_menu()
print("userSetup.py wird geladen")