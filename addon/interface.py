def operator(self, context):

    layout = self.layout

    object = bpy.data.objects[context.object['fast-lattice'].split(',')[0]]

    row = layout.row()
    row.prop(context.object.data, 'points_u')
    row.prop(context.object.data, 'interpolation_type_u', text='')

    row = layout.row()
    row.prop(context.object.data, 'points_v')
    row.prop(context.object.data, 'interpolation_type_v', text='')

    row = layout.row()
    row.prop(context.object.data, 'points_w')
    row.prop(context.object.data, 'interpolation_type_w', text='')

    row = layout.row()
    row.prop(context.object.data, 'use_outside')

    row = layout.row()
    row.label(text='Display:')

    row = layout.row()
    row.prop(object, 'show_wire')
    row.prop(object, 'show_all_edges')


def panel_mesh(self, context):

    layout = self.layout

    column = layout.column(align=True)

    column.label(text='Fast Lattice:')

    column.prop(context.window_manager.fast_lattice, 'method', text='')

    column.prop(context.window_manager.fast_lattice, 'interpolation_type', text='')

    column.prop(context.window_manager.fast_lattice, 'accuracy', slider=True)

    column.operator('object.fast_lattice')


def panel_lattice(self, context):

    layout = self.layout

    if context.object.get('fast-lattice'):

        column = layout.column(align=True)

        column.label(text='Fast Lattice:')

        column.operator('object.fast_lattice_cleanup')
