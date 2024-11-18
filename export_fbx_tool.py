import maya.cmds as cmds
import os

def export_fbx(export_path, file_name):
    # Stelle sicher, dass der Pfad existiert
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    # Vollständiger Exportpfad
    full_path = os.path.join(export_path, file_name)

    # Setze die FBX-Export-Einstellungen
    cmds.loadPlugin("fbxmaya", quiet=True)  # Lade das FBX-Plugin
    cmds.file(full_path, force=True, options="v=0;", type="FBX export", pr=True, exportAll=True)

    print(f"Animation wurde als FBX exportiert: {full_path}")



def get_next_version(export_path, base_name):
    # Finde bestehende Dateien mit dem gleichen Präfix
    files = [f for f in os.listdir(export_path) if f.startswith(base_name) and f.endswith(".fbx")]
    version_numbers = []

    for file in files:
        parts = file.split("_")
        if len(parts) > 1 and parts[-1].startswith("v"):
            try:
                version = int(parts[-1][1:].split(".")[0])  # Nummer nach 'v' extrahieren
                version_numbers.append(version)
            except ValueError:
                continue

    # Bestimme die nächste Version
    return max(version_numbers, default=0) + 1


def create_export_ui():
    if cmds.window("ExportUI", exists=True):
        cmds.deleteUI("ExportUI", window=True)

    window = cmds.window("ExportUI", title="Export FBX for Unreal", widthHeight=(300, 150))
    cmds.columnLayout(adjustableColumn=True)
    
    # Dropdown für Charaktere
    cmds.optionMenu("character_menu", label="Character")
    cmds.menuItem(label="Maurice")
    cmds.menuItem(label="Mother_Golem")
    cmds.menuItem(label="Bird")
    cmds.menuItem(label="Testosteron")
    
    # Dropdown für Szenen
    cmds.optionMenu("scene_menu", label="Scene")
    for i in range(1, 21):  # 1 bis 20
        scene_label = f"Szene{i:03}"  # Formatierung mit führenden Nullen
        cmds.menuItem(label=scene_label)

  
    
    # Export-Button
    cmds.button(label="Export FBX", command=lambda x: on_export_clicked())

    cmds.showWindow(window)

def on_export_clicked():
    # Ausgewählte Werte abrufen
    character = cmds.optionMenu("character_menu", query=True, value=True)
    scene = cmds.optionMenu("scene_menu", query=True, value=True)
    
    # Exportpfad dynamisch anpassen
    base_path = "N:/GOLEMS_FATE/animations"
    export_path = os.path.join(base_path, character, scene)
    
    # Debug-Ausgabe des Pfads
    print(f"Versuche, in diesen Pfad zu exportieren: {export_path}")
    
    # Verzeichnis erstellen, falls nicht vorhanden
    try:
        os.makedirs(export_path, exist_ok=True)
    except OSError as e:
        print(f"Fehler beim Erstellen des Pfads: {e}")
        return
    
    # Berechnung der nächsten Version
    version = get_next_version(export_path, f"{character}_{scene}")
    file_name = f"{character}_{scene}_v{version}.fbx"
    
    # FBX exportieren
    export_fbx(export_path, file_name)




create_export_ui()
