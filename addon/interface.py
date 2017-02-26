def draw_mesh(self, context):

    layout = self.layout

    column = layout.column(align=True)

    column.label(text='Fast Lattice:')

    column.prop(context.window_manager.fast_lattice, 'method', text='')

    column.prop(context.window_manager.fast_lattice, 'interpolation_type', text='')

    column.prop(context.window_manager.fast_lattice, 'accuracy', slider=True)

    column.operator('object.fast_lattice')


def draw_lattice(self, context):

    layout = self.layout

    if context.object.get('fast-lattice'):

        column = layout.column(align=True)

        column.label(text='Fast Lattice:')

        column.operator('object.fast_lattice_cleanup')
