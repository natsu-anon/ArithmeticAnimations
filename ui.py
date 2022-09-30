import bpy


# see https://docs.blender.org/api/current/bpy.types.UILayout.html?highlight=row#bpy.types.UILayout
# Panel in 3D View
class PanelVIEW3D(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_Arithmetic_Animations"
    bl_label = "Arithmetic Animations"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Arithmetic Animations"

    @classmethod
    def poll(self, context):
        return len(bpy.data.actions) > 0

    def draw(self, context):
        aa = context.scene.arithmetic_animations
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Mode:")
        row.prop(aa, "mix_enum", expand=False)
        row = layout.row(align=True)
        row.label(text="Name:")
        row.prop(aa, "new_name", text="",  expand=False)
        row = layout.row(align=True)
        row.label(text="Action A:")
        row.prop(aa, "action_A", text="", expand=False)
        row = layout.row(align=True)
        row.label(text="Action B:")
        row.prop(aa, "action_B", text="", expand=False)
        row = layout.row(align=True)
        if aa.new_name == "":
            row.label(text="Enter a valid name!", icon="ERROR")
        elif aa.action_A is not None and aa.action_B is not None:
            row.label(text="Create \"{}\"".format(aa.new_name))
            row = layout.row(align=True)
            if aa.mix_enum == 'DIFF':
                row.operator('arithmetic_animations.diff', text='Difference of A & B')
            elif aa.mix_enum == 'AVG':
                row.operator('arithmetic_animations.avg', text='Average of A & B')
        else:
            row.label(text="Select two actions!", icon="ERROR")
