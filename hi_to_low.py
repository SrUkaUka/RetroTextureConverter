import bpy
import os
from bpy.path import abspath

# Function to save original UV coordinates of an object
def save_uv_coordinates(obj):
    uv_coordinates = []
    mesh = obj.data
    uv_layer = mesh.uv_layers.active.data
    for loop in uv_layer:
        uv_coordinates.append(loop.uv[:])
    return uv_coordinates

# Function to desubdivide all faces of a mesh object using Dissolve Edges operation
def desubdivide_faces(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.dissolve_edges(use_verts=True)
    bpy.ops.object.mode_set(mode='OBJECT')

# Configura la carpeta de salida para las imágenes
output_folder = "your_route_here"
# Configura la resolución deseada para las imágenes
resolution_x = 12
resolution_y = 12

# Paso 1: Recopilar coordenadas UV originales
uv_dict = {}
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        uv_dict[obj.name] = save_uv_coordinates(obj)

# Paso 2: Desubdividir caras de los objetos
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        desubdivide_faces(obj)

# Paso 3: Aplicar las coordenadas UV originales guardadas
for obj_name, uv_coordinates in uv_dict.items():
    obj = bpy.data.objects.get(obj_name)
    if obj and obj.type == 'MESH':
        mesh = obj.data
        uv_layer = mesh.uv_layers.active.data
        for loop_index, uv_coord in zip(range(len(uv_layer)), uv_coordinates):
            uv_layer[loop_index].uv = uv_coord

# Paso 4: Redimensionar y guardar las texturas
for material in bpy.data.materials:
    if material.node_tree is not None:
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                image = node.image
                if image is not None and image.pixels:
                    rotation = node.inputs['Vector'].default_value[2]
                    image.scale(resolution_x, resolution_y)
                    node.inputs['Vector'].default_value[2] = rotation
                    image_path = abspath(image.filepath)
                    image_filename = os.path.basename(image_path)
                    new_image_path = os.path.join(output_folder, image_filename)
                    image.save_render(new_image_path)
                    print("Imagen guardada en:", new_image_path)
