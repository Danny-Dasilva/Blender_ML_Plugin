import bpy

class SceneSettingItem(bpy.types.PropertyGroup):
    tag = bpy.props.PointerProperty(type=bpy.types.Object)
    value = bpy.props.IntProperty()
class AddButtonOperator(bpy.types.Operator):
    bl_idname = "scene.add_button_operator"
    bl_label = "Add Button"

    def execute(self, context):
        id = len(context.scene.my_collection)
        new = context.scene.my_collection.add()
        new.name = str(id)
        new.value = id
        return {'FINISHED'}

class ButtonOperator(bpy.types.Operator):
    bl_idname = "scene.button_operator"
    bl_label = "Button"

    id = bpy.props.IntProperty()

    def execute(self, context):
        print("Pressed button ", self.id)
        return {'FINISHED'}

class FancyPanel(bpy.types.Panel):
    bl_label = "Fancy Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        self.layout.operator("scene.add_button_operator")
        for item in context.scene.my_collection:
            row = self.layout.row(align=True)
            row.prop(item, "tag")
            row.operator("scene.button_operator", text="Button #"+item.name).id = item.value


bpy.utils.register_class(AddButtonOperator)
bpy.utils.register_class(ButtonOperator)
bpy.utils.register_class(FancyPanel)
bpy.utils.register_class(SceneSettingItem)
bpy.types.Scene.my_collection = bpy.props.CollectionProperty(type=SceneSettingItem)