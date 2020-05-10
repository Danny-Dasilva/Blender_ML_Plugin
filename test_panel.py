import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )


def main(context):
    for ob in context.scene.objects:
        print(ob)



class MySettings(PropertyGroup):

    my_bool : BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    my_int : IntProperty(
        name = "Set a value",
        description="A integer property",
        default = 23,
        min = 10,
        max = 100
        )

    my_float : FloatProperty(
        name = "Set a value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        )
    my_string : StringProperty(
        name = "Set a value",
        description = "A float property",
        )


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

class test():
    def __init__(self):

        self.count = 0
t = test()
class AddButtonOperator(bpy.types.Operator):
    bl_idname = "scene.add_button_operator"
    bl_label = "Add Button"
    
    def execute(self, context):
        print(context.scene.collection)
        t.count += 1
        print(t.count)
        ids = t.count
        # ids = len(context.scene.collection)
        return {'FINISHED'}

class ButtonOperator(bpy.types.Operator):
    bl_idname = "scene.button_operator"
    bl_label = "Button"

    id = bpy.props.IntProperty()

    def execute(self, context):
        print("Pressed button ", self.id)
        return {'FINISHED'}




class Test_PT_Panel(bpy.types.Panel):
    bl_idname = "Test+_PT_Panel"
    bl_label = "Test panel"
    bl_category = "Test Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bpy.types.Scene.theChosenObject = PointerProperty(type=bpy.types.Object)
    def draw(self, context):
        # layout = self.layout
        # row = layout.row
        #
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool


        # Create a simple row.
        layout.label(text=" Simple Row:")

        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")


        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="Column One:")
        col.prop(scene, "frame_end")
        col.prop(scene, "frame_start")

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Column Two:")
        col.prop(scene, "frame_start")
        col.prop(scene, "frame_end")
       


        # display the properties
        layout.prop(mytool, "my_bool", text="Bool Property")
        layout.prop(mytool, "my_int", text="Integer Property")
        layout.prop(mytool, "my_float", text="Float Property")
        layout.prop(mytool, "my_string", text="Float Property")

        # check if bool property is enabled
        if (mytool.my_bool == True):
            print ("Property Enabled11")
        else:
            print ("Property Disabled")

        self.layout.operator("scene.add_button_operator")
        for item in range(t.count):
               self.layout.operator("scene.button_operator", text="Button #"+str( t.count)).id =  t.count



        # print(mytool.my_int, "int")
        # print(mytool.my_float, "float")




        layout.prop_search(scene, "theChosenObject", scene, "objects")
        # layout.prop_search(scene, "theChosenMaterial", bpy.data, "materials")
        # Big render button
        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.simple_operator")

        # Different sizes in a row
        layout.label(text="Different button sizes:")
        row = layout.row(align=True)
        row.operator("render.render")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("render.render")

        row.operator("render.render")
