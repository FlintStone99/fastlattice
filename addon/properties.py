import bpy

from bpy.types import PropertyGroup
from bpy.props import FloatProperty, BoolProperty, EnumProperty

class fast_lattice(PropertyGroup):

  accuracy = FloatProperty(
    name = 'Accuracy',
    description = 'How accurate the lattice will conform to the selection. (Increasing this value takes longer to calculate)',
    min = 0.001,
    max = 1.0,
    default = 0.1
  )

  interpolation_type = EnumProperty(
    name = 'Interpolation Type',
    description = 'Interpolation type to use for the created lattice',
    items = [
      ('KEY_BSPLINE', 'BSpline', ''),
      ('KEY_CATMULL_ROM', 'Catmull-Rom', ''),
      ('KEY_CARDINAL', 'Cardinal', ''),
      ('KEY_LINEAR', 'Linear', '')
    ],
    default = 'KEY_BSPLINE'
  )

  method = EnumProperty(
    name = 'Conforming Method',
    description = 'Method to use when conforming the lattice to your selection.',
    items = [
      ('DEFAULT', 'Default', 'The default method that works well with most selections.'),
      ('SIMPLE', 'Simple', 'The simple method that works well with most selections and is the fastest. (Often produces the same result)'),
      ('PLANAR', 'Planar', 'The planar method that works with all selections but is the slowest')
    ],
    default = 'DEFAULT'
  )