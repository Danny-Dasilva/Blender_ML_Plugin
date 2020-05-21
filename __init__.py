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
# to do
# cube draw 
# panel for object select
# display pabel for obj spawn and cube draw
# batch render
# id name, obj, enable physics, xyz spawn, add another id, outer frame advance and add another id
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
from . draw_op import OT_Draw_Operator
import bpy

import bgl
import gpu
from gpu_extras.batch import batch_for_shader

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
#    Update functions
# ------------------------------------------------------------------------

class DrawBox():

    draw_handle = None
    vertices = None
    def register(self):
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINE_STRIP', {'pos': self.vertices})
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_px, (), "WINDOW", "POST_VIEW"
            )
    def unregister(self):
        bpy.types.SpaceView3D.draw_handler_remove(data.draw_handle, 'WINDOW')

    def setxyz(self, xyz_max, xyz_min):
        print(xyz_min, "in data class")
        x_min = xyz_min[0]
        x_max = xyz_max[0]
        y_min = xyz_min[1]
        y_max = xyz_max[1]
        z_min = xyz_min[2]
        z_max = xyz_max[2]
        
        self.vertices = [(x_min, y_min, z_max), (x_max,y_min,z_max), (x_max,y_min,z_min),  (x_max,y_max, z_min), (x_max,y_max, z_max), (x_min,y_max, z_max), (x_min,y_max,z_min),(x_min,y_min,z_min), (x_min,y_min,z_max),
        (x_min,y_max,z_max), (x_min,y_max,z_min), (x_max,y_max,z_min), (x_max, y_max, z_max), (x_max, y_min, z_max), (x_max, y_min, z_min), (x_min,y_min,z_min)]


    def run(self):
        if self.draw_handle != None:
            self.unregister()

        self.register()
        
    def draw_callback_px(self):
        bgl.glLineWidth(3)
        self.shader.bind()
        self.shader.uniform_float("color", (1, 0, 0, 1))
        self.batch.draw(self.shader)

data = DrawBox()

def my_update_func(self, context):
    scene = bpy.context.scene
    mytool = scene.my_tool
    
    xyz_max = [val for val in mytool.cam_xyz_max]
    xyz_min = [val for val in mytool.cam_xyz_min]
    data.setxyz(xyz_max, xyz_min)
    data.run()
    
    
    
   
    
    


 # vertices = [(0, 0, 4), (4,0,4), (4,0,0),  (4,4,0), (4,4,4), (0,4,4), (0,4,0),(0,0,0), (0,0,4),
    # (0,4,4), (0,4,0), (4,4,0), (4, 4, 4), (4, 0, 4), (4, 0, 0), (0,0,0)]
        
        
# shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
# batch = batch_for_shader(shader, 'LINE_STRIP', {'pos': vertices})

# def draw_callback_px():
#     bgl.glLineWidth(5)
#     shader.bind()
#     shader.uniform_float("color", (1, 0, 0, 1))
#     batch.draw(shader)


# if data.draw_handle != None:
#     bpy.types.SpaceView3D.draw_handler_remove(data.draw_handle, 'WINDOW')


# data.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
#     draw_callback_px, (), "WINDOW", "POST_VIEW"
#     )



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
        max = 10000.0,
        update=my_update_func
        ) 

    cam_xyz_min: FloatVectorProperty(
        name = "XYZ-",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= -10000.0, # float
        max = 10000.0,
        update=my_update_func
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

class OT_Obj_Spawn(Operator):
    bl_label = "Obj_Spawn"
    bl_idname = "wm.obj_spawn"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        


        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_label = "My Panel"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Blender ML"
    bl_context = "objectmode"   

    bpy.types.Scene.prop = PointerProperty(type=bpy.types.Object)

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

            
            # layout.prop(scene, "prop")



# class OBJECT_PT_CustomPanel:
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "Blender ML"
#     bl_context = "objectmode"   
#     bl_options = {"DEFAULT_CLOSED"}



# class OBJECT_PT_Cam(OBJECT_PT_CustomPanel,  bpy.types.Panel):
#     bl_label = "My Panel"
#     bl_idname = "OBJECT_PT_custom_panel"
   

#     bpy.types.Scene.prop = PointerProperty(type=bpy.types.Object)

#     @classmethod
#     def poll(self,context):
#         return context.object is not None

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool




#         layout.prop(mytool, "my_bool")
#         layout.prop(mytool, "my_enum", text="") 
#         layout.prop(mytool, "my_string")
#         layout.prop(mytool, "my_path")
#         layout.operator("wm.hello_world")
#         layout.separator()

#         layout.label(text="Camera Spawn:")
#         layout.prop(mytool, "cam_xyz_max")
#         layout.prop(mytool, "cam_xyz_min")

#         layout.operator("wm.cam_spawn")
#         layout.separator()

            
#             # layout.prop(scene, "prop")

# class HELLO_PT_World2(OBJECT_PT_CustomPanel,  bpy.types.Panel):
#     bl_parent_id = "OBJECT_PT_Cam"
#     bl_label = "Panel 2"

#     def draw(self, context):
#         layout = self.layout
#         layout.label(text="First Sub Panel of Panel 1.")


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    WM_OT_HelloWorld,
    OBJECT_PT_CustomPanel,
    OT_Cam_Spawn,
    OT_Draw_Operator,

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
    bpy.ops.object.draw_op('INVOKE_DEFAULT')

