
'''
Fast Lattice Addon
Copyright (C) 2016 Trentin Frederick (proxe)

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
  'name': 'Fast Lattice',
  'author': 'Trentin Frederick (proxe)',
  'version': (0, '5b', 7),
  'blender': (2, 68, 0),
  'location': '3D View \N{Rightwards Arrow} Edit Mode \N{Rightwards Arrow} Mesh Tools',
  'description': 'Quickly add and edit a lattice object that effects and conforms to the mesh selection.',
  'warning': 'Beta',
  # 'wiki_url': '',
  # 'tracker_url': '',
  'category': 'Mesh'
}

import bpy
from bpy.utils import register_module, unregister_module
from bpy.props import PointerProperty

from .addon import interface, operator, properties


def register():

  bpy.types.VIEW3D_PT_tools_meshedit.append(interface.draw_mesh)
  bpy.types.VIEW3D_PT_tools_latticeedit.append(interface.draw_lattice)

  register_module(__name__)

  bpy.types.WindowManager.fast_lattice = PointerProperty(
    type = properties.fast_lattice,
    name = 'Fast Lattice',
    description = 'Storage location for fast lattice settings.'
  )

def unregister():

  bpy.types.VIEW3D_PT_tools_meshedit.remove(interface.draw_mesh)
  bpy.types.VIEW3D_PT_tools_latticeedit.remove(interface.draw_lattice)

  unregister_module(__name__)

  del bpy.types.WindowManager.fast_lattice
