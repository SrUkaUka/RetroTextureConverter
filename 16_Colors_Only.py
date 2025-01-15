import bpy
import os
from bpy.props import StringProperty
from bpy.types import Operator, Panel
from bpy_extras.io_utils import ImportHelper
from PIL import Image

# Nueva funcionalidad: Operador para convertir imágenes a 16 colores
class OT_SelectFolder16Colors(Operator, ImportHelper):
    bl_idname = "file.select_folder_16_colors"
    bl_label = "Select Folder for 16 Colors"
    
    directory: StringProperty(
        name="Directory",
        description="Select the folder to convert images to 16 colors",
        maxlen=1024,
        subtype='DIR_PATH',
    )
    
    def execute(self, context):
        folder = self.directory
        print(f"Selected folder: {folder}")
        convert_to_16_colors_recursive(folder)
        return {'FINISHED'}

# Función para convertir imágenes a 16 colores de manera recursiva
def convert_to_16_colors_recursive(folder):
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.endswith(".png") or filename.endswith(".jpg"):
                # Abrir la imagen
                image_path = os.path.join(root, filename)
                image = Image.open(image_path)

                # Convertir a paleta de 16 colores
                image = image.convert("P", palette=Image.ADAPTIVE, colors=16)

                # Guardar la imagen en el mismo directorio
                image.save(image_path)

                print(f"Imagen convertida: {filename}")

# Panel principal en la interfaz de Blender
class PT_16ColorsPanel(Panel):  # Cambiado el identificador del panel
    bl_idname = "PT_16ColorsPanel"  # Cambiado el identificador del panel
    bl_label = "16 Colors Panel"
    bl_category = "16 Colors"  # Cambiado a la nueva categoría
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("file.select_folder_16_colors", text="Convert to 16 Colors")

def register():
    bpy.utils.register_class(OT_SelectFolder16Colors)
    bpy.utils.register_class(PT_16ColorsPanel)

def unregister():
    bpy.utils.unregister_class(OT_SelectFolder16Colors)
    bpy.utils.unregister_class(PT_16ColorsPanel)

if __name__ == "__main__":
    register()
