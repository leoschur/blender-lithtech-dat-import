import bpy
import bmesh
from .lithtech_dat_import import ImportLithtechDat
from mathutils import Vector

bl_info = {
    "name": "Lithtech DAT Map Format (.dat)",
    "author": "leos",
    "description": "This plugins allows you to import Lithtech Map files.",
    "blender": (3, 4, 1),
    "version": (0, 0, 3),
    "location": "File > Import > Lithtech DAT",
    "warning": "",
    "category": "Import-Export"
}

# Register and add to the "file selector" menu (required to use F3 search)


def menu_func_import(self, context):
    self.layout.operator(ImportLithtechDat.bl_idname,
                         text="Import Lithtech DAT map (.dat)")


def register():
    bpy.utils.register_class(ImportLithtechDat)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportLithtechDat)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.import_scene.lithtech_dat('INVOKE_DEFAULT')
