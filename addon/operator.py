import bpy

from bpy.types import Operator

from . import interface, utilities


class fast_lattice(Operator):
    bl_idname = 'object.fast_lattice'
    bl_label = 'Create Lattice'
    bl_description = 'Create and edit a lattice that effects and conforms to the selection.'
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):

        return context.object.type == 'MESH' and context.object.mode == 'EDIT' and context.object.data.total_vert_sel > 2 and not context.area.spaces.active.local_view


    def draw(self, context):

        interface.operator(self, context)


    def execute(self, context):

        utilities.create_lattice(self, context)

        return {'FINISHED'}


class fast_lattice_cleanup(Operator):
    bl_idname = 'object.fast_lattice_cleanup'
    bl_label = 'Finished'
    bl_description = 'Finalize the fast lattice operation.'
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        utilities.cleanup(context)

        return {'FINISHED'}
