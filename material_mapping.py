from pathlib import Path
import json
import pymel.core as pc

# Returns the materials associated with the given shape node.
def get_materials(shape):
    shading_groups = shape.listConnections(type="shadingEngine")
    materials = []
    for sg in shading_groups:
        materials.extend(sg.surfaceShader.listConnections())
    return materials

# Returns the file path of a texture connected to a specific material channel.
# Handles normal maps as a special case.
def get_file(material, channel):
    file_nodes = material.attr(channel).listConnections(type="file")
    if file_nodes:
        return file_nodes[0].attr("fileTextureName").get()

# Creates a mapping of objects to their materials and texture file paths for specified channels.
def get_object_to_material_map(object_list, channel_list):
    object_to_material_map = {}
    for obj in object_list:
        shape = obj.getShape()
        if not shape:
            continue
        materials = get_materials(shape)
        if not materials:
            continue
        material = materials[0]
        file_map = {channel: get_file(material, channel) for channel in channel_list}
        object_to_material_map[obj.name()] = file_map
    return object_to_material_map

# Returns the currently selected objects in the Maya scene.
def get_selected_objects():
    return pc.ls(selection=True)

# Save the result to a JSON file.
def save_to_json(data, path):
    path = Path(path)
    path.write_text(json.dumps(data, indent=4))

# UI Function
def create_ui():
    # Close existing window if it exists.
    if pc.window("exportUI", exists=True):
        try:
            pc.deleteUI("exportUI")
        except RuntimeError:
            pass  # Falls das Fenster bereits gelöscht wurde, keine Aktion nötig.

    # Create a new window.
    export_window = pc.window("exportUI", title="Export Material Info", widthHeight=(300, 400))
    with pc.columnLayout(adjustableColumn=True):
        pc.text(label="Select Channels:")
        channel_checkboxes = {}
        channels = ["baseColor", "opacity", "normalCamera", "metalness", "specularRoughness"]
        
        # Create checkboxes for each channel.
        for channel in channels:
            channel_checkboxes[channel] = pc.checkBox(label=channel, value=True)

        pc.separator(height=10)
        pc.text(label="Output File Path:")
        output_path_field = pc.textField(text=str(Path.home() / "material_info.json"))

        pc.separator(height=10)
        pc.button(label="Export", command=lambda *args: export_data(channel_checkboxes, output_path_field))
    
    # Show the window.
    pc.showWindow(export_window)


# Export Function
def export_data(channel_checkboxes, output_path_field):
    selected_objects = get_selected_objects()
    if not selected_objects:
        pc.warning("No objects selected. Please select at least one object.")
        return

    # Get selected channels.
    selected_channels = [channel for channel, checkbox in channel_checkboxes.items() if checkbox.getValue()]

    if not selected_channels:
        pc.warning("No channels selected. Please select at least one channel.")
        return

    # Get the output path.
    output_path = pc.textField(output_path_field, query=True, text=True)
    if not output_path:
        pc.warning("No output path specified.")
        return

    # Generate the mapping and save to JSON.
    try:
        object_to_material_map = get_object_to_material_map(selected_objects, selected_channels)
        save_to_json(object_to_material_map, output_path)
        pc.confirmDialog(title="Success", message=f"Data exported to {output_path}", button=["OK"])
    except Exception as e:
        pc.error(f"Failed to export data: {e}")

# Run the UI
create_ui()
