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
    if channel != "normalCamera":
        # General case: Retrieve file node for the specified channel.
        file_nodes = material.attr(channel).listConnections(type="file")
        if file_nodes:
            return file_nodes[0].attr("fileTextureName").get()
    # Special case: Normal map, accessed via a connected bump node.
    bump_node = material.attr(channel).listConnections()[0]
    normal_file_node = bump_node.listConnections(type="file")
    return normal_file_node[0].attr("fileTextureName").get()

# Creates a mapping of objects to their materials and texture file paths for specified channels.
def get_object_to_material_map(object_list, channel_list):
    # Initialize the object-to-material map.
    object_to_material_map = {}
    for obj in object_list:
        # Get the shape node associated with the object.
        shape = obj.getShape()
        # Retrieve the first material assigned to the shape.
        material = get_materials(shape)[0]
        
        # Map texture file paths for each specified channel.
        file_map = {}
        for channel in channel_list:
            print(channel)  # Debug: Print the current channel being processed.
            file_map[channel] = get_file(material, channel)
        
        # Add the object and its texture file map to the dictionary.
        object_to_material_map[obj.name()] = file_map
    return object_to_material_map

# Returns the currently selected objects in the Maya scene.
def get_selected_objects():
    return pc.ls(selection=True)

# List of material channels to extract texture file paths from.
channels = ["baseColor", "normalCamera", "metalness", "specularRoughness"]

# Get the currently selected objects.
objects = get_selected_objects()

# Check if any objects are selected.
if not objects:
    raise RuntimeError("No objects selected. Please select at least one object.")

# Generate the mapping and save it as a JSON file.
object_to_material_map = get_object_to_material_map(objects, channels)

# Save the result to a JSON file.
output_path = Path(r"N:\GOLEMS_FATE\crew\Jan\Scripts\NachhilfeMitJochen\test.json")
output_path.write_text(json.dumps(object_to_material_map))
