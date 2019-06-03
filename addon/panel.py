from bpy.types import Panel

from . import interface


class lattice(Panel):
    bl_idname = 'FL_PT_lattice'
    bl_label = 'Lattice'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lattice'

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type in {'MESH', 'LATTICE'}


    def draw(self, context):
        if context.object.type == 'MESH':
            interface.panel_start(self, context)

        elif context.object.type == 'LATTICE':
            interface.panel_finish(self, context)
