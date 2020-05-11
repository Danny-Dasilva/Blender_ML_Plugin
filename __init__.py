# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Test_addon",
    "author" : "Danny Dasilva",
    "description" : "Simple test addon",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}
from .ml_class import ML_Gen

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
                       Menu,
                       Operator,
                       PropertyGroup,
                       )


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):

    my_bool: BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    my_int: IntProperty(
        name = "Int Value",
        description="A integer property",
        default = 23,
        min = 10,
        max = 100
        )

    my_float: FloatProperty(
        name = "Float Value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        )


    cam_xyz_max: FloatVectorProperty(
        name = "XYZ+",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= -10000.0, # float
        max = 10000.0
    ) 

    cam_xyz_min: FloatVectorProperty(
        name = "XYZ-",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= -10000.0, # float
        max = 10000.0
    ) 


    my_string: StringProperty(
        name="User Input",
        description=":",
        default="",
        maxlen=1024,
        )

    my_path: StringProperty(
        name = "Directory",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )
        
    my_enum: EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[ ('OP1', "Option 1", ""),
                ('OP2', "Option 2", ""),
                ('OP3', "Option 3", ""),
               ]
        )



gen = ML_Gen()
# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WM_OT_HelloWorld(Operator):
    bl_label = "Print Values Operator"
    bl_idname = "wm.hello_world"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        # print the values to the console
        print("Hello World")
        print("bool state:", mytool.my_bool)
        print("int value:", mytool.my_int)
        print("float value:", mytool.my_float)
        print("string value:", mytool.my_string)
        print("enum state:", mytool.my_enum)
        

        return {'FINISHED'}

class OT_Cam_Spawn(Operator):
    bl_label = "Cam_Spawn"
    bl_idname = "wm.cam_spawn"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        # print the values to the console
        print("Cam_Test")
        
        gen.xyz_max = [val for val in mytool.cam_xyz_max]
        gen.xyz_min = [val for val in mytool.cam_xyz_min]
        gen.randomize_camera(scene)

        print(gen.xyz_max, gen.xyz_min)
        


        return {'FINISHED'}
# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_label = "My Panel"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_context = "objectmode"   


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "my_bool")
        layout.prop(mytool, "my_enum", text="") 
        layout.prop(mytool, "my_string")
        layout.prop(mytool, "my_path")
        layout.operator("wm.hello_world")
        layout.separator()


        layout.label(text="Camera Spawn:")
        layout.prop(mytool, "cam_xyz_max")
        layout.prop(mytool, "cam_xyz_min")

        layout.operator("wm.cam_spawn")
        layout.separator()


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    WM_OT_HelloWorld,
    OBJECT_PT_CustomPanel,
    OT_Cam_Spawn,

)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()

