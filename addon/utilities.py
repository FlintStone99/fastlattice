from math import pi
from random import random

import bpy
import bmesh

from mathutils import Vector, Matrix, Euler


class create_lattice:

    samples = 1000
    interpolation_type = None
    method = 'DEFAULT'
    minimum_matrix = Matrix()

    def __init__(self, operator, context):

        object = context.active_object

        if object.scale != Vector((1.0, 1.0, 1.0)):

            operator.report({'WARNING'}, '\'{}\' is scaled: canceling.'.format(object.name))

        else:

            self.samples = int(self.samples * context.window_manager.fast_lattice.accuracy)
            self.interpolation_type = context.window_manager.fast_lattice.interpolation_type
            self.method = context.window_manager.fast_lattice.method

            bpy.ops.object.mode_set(mode='OBJECT')

            object.update_from_editmode()

            vertices = [vertex for vertex in object.data.vertices if vertex.select]
            indices = [vertex.index for vertex in vertices]

            mesh = bmesh.new()
            mesh.from_mesh(object.data)

            convex_hull = bmesh.ops.convex_hull(mesh, input=[vertex for vertex in mesh.verts if vertex.select], use_existing_faces=False)
            coordinates = [vertex.co for vertex in convex_hull['geom'] if hasattr(vertex, 'co')]

            vertex_group = object.vertex_groups.new(name='fast-lattice')
            vertex_group.add(indices, 1.0, 'ADD')

            lattice_object = self.add_lattice(object, coordinates)

            mesh.free()

            lattice_modifier = object.modifiers.new(name='fast-lattice', type='LATTICE')
            lattice_modifier.object = lattice_object
            lattice_modifier.vertex_group = vertex_group.name

            context.scene.objects.link(object=lattice_object)
            context.scene.objects.active = lattice_object

            lattice_object['fast-lattice'] = "{},{},{},{},{},{},{}".format(object.name, vertex_group.name, lattice_modifier.name, lattice_object.name, lattice_object.data.name, object.show_wire, object.show_all_edges)

            context.scene.update()

            for i in range(0, 3):

                if lattice_object.dimensions[i] < 0.001:

                    lattice_object.dimensions[i] = 0.1

            object.show_wire = True if operator.show_wire else False
            object.show_all_edges = True if operator.show_all_edges else False

            bpy.ops.object.mode_set(mode='EDIT')


    def add_lattice(self, object, coordinates):

        lattice_data = bpy.data.lattices.new(name='fast-lattice')
        lattice_object = bpy.data.objects.new(name='fast-lattice', object_data=lattice_data)

        lattice_object.rotation_euler = (object.matrix_world.to_quaternion().to_matrix().to_4x4() * self.rotation(object, coordinates)).to_euler()
        lattice_object.location = object.matrix_world * self.location(coordinates)
        lattice_object.scale = self.scale(coordinates, self.minimum_matrix)

        lattice_object.show_x_ray = True

        lattice_data.interpolation_type_u = self.interpolation_type
        lattice_data.interpolation_type_v = self.interpolation_type
        lattice_data.interpolation_type_w = self.interpolation_type
        lattice_data.use_outside = True

        return lattice_object


    def rotation(self, object, coordinates):

        control = self.scale(coordinates, Matrix())

        if self.method in 'DEFAULT':

            vector_samples = [Vector((random(), random(), random())) for i in range(0, self.samples)]

            angles = [
                0.0,
                0.16,
                0.31,
                0.47,
                0.63,
                0.79,
                0.94,
                1.1,
                1.26,
                1.41,
                1.57,
                1.73,
                1.88,
                2.04,
                2.2,
                2.36,
                2.51,
                2.67,
                2.83,
                2.98,
                3.14
            ]

            for vector in vector_samples:

                for angle in angles:

                    matrix = Matrix.Rotation(angle, 4, vector)
                    test = self.scale(coordinates, matrix)

                    if test < control:

                        control = test
                        self.minimum_matrix = matrix

        elif self.method in 'BRUTE_FORCE':

            factor = 1/self.samples

            vector_samples = [Vector((index * factor * random(), index * factor * random(), index * factor * random())) for index in range(0, self.samples)]

            factor = 1/90

            angle_samples = [pi * (index * factor) for index in range(0, 91)]

            for vector in vector_samples:

                for angle in angle_samples:

                    matrix = Matrix.Rotation(angle, 4, vector)
                    test = self.scale(coordinates, matrix)

                    if test < control:

                        control = test
                        self.minimum_matrix = matrix

        elif self.method == 'WORLD':

            self.minimum_matrix = Matrix()

        else: # planar

            pass

        return self.minimum_matrix.inverted()


    def location(self, coordinates):

        vertices = [self.minimum_matrix * vertex for vertex in coordinates]

        x = [vertex.x for vertex in vertices]
        y = [vertex.y for vertex in vertices]
        z = [vertex.z for vertex in vertices]

        return self.minimum_matrix.inverted() * (sum(self.box(x, y, z), Vector()) / len(self.box(x, y, z)))


    @staticmethod
    def scale(coordinates, matrix):

        vertices = [matrix * coordinate for coordinate in coordinates]

        x = [vertex.x for vertex in vertices]
        y = [vertex.y for vertex in vertices]
        z = [vertex.z for vertex in vertices]

        maximum = Vector((max(x), max(y), max(z)))
        minimum = Vector((min(x), min(y), min(z)))

        return maximum - minimum


    @staticmethod
    def box(x, y, z):

        bounds = [
            Vector((min(x), min(y), min(z))),
            Vector((min(x), min(y), max(z))),

            Vector((min(x), max(y), min(z))),
            Vector((min(x), max(y), max(z))),

            Vector((max(x), min(y), min(z))),
            Vector((max(x), min(y), max(z))),

            Vector((max(x), max(y), min(z))),
            Vector((max(x), max(y), max(z))),
        ]

        return bounds

def cleanup(context):

    bpy.ops.object.mode_set(mode='OBJECT')

    prop = context.object['fast-lattice'].split(',')

    object = bpy.data.objects[prop[0]]
    lattice = bpy.data.objects[prop[3]]

    show_wire = prop[5]
    show_all_edges = prop[6]

    object.show_wire = True if show_wire == 'True' else False
    object.show_all_edges = True if show_all_edges == 'True' else False

    context.scene.objects.active = object

    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=object.modifiers[prop[2]].name)

    object.vertex_groups.remove(group=object.vertex_groups[prop[1]])

    bpy.data.objects.remove(object=lattice, do_unlink=True)
    bpy.data.lattices.remove(lattice=bpy.data.lattices[prop[4]], do_unlink=True)

    bpy.ops.object.mode_set(mode='EDIT')


def update(operator, context):

    bpy.data.objects[operator.mesh_object].show_wire = operator.show_wire
    bpy.data.objects[operator.mesh_object].show_all_edges = operator.show_all_edges
