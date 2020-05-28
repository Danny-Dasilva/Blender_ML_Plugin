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

# !! check the names and obj ids if I can
# add unregister

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
                       CollectionProperty,
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
    def __init__(self, set_cam):
        self.set_cam = set_cam
    def register(self):
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINE_STRIP', {'pos': self.vertices})
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_px, (), "WINDOW", "POST_VIEW"
            )
    def unregister(self):
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, 'WINDOW')

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
        if self.set_cam != None:
            self.shader.uniform_float("color", (0, 1, 1, 1))
        else:
            self.shader.uniform_float("color", (1, 0, 0, 1))
        self.batch.draw(self.shader)

cam = DrawBox(None)

def cam_domain(self, context):
    scene = bpy.context.scene
    mytool = scene.my_tool
    
    xyz_max = [val for val in mytool.cam_xyz_max]
    xyz_min = [val for val in mytool.cam_xyz_min]
    cam.setxyz(xyz_max, xyz_min)
    cam.run()
    
    
    
   
obj = DrawBox(1)
def obj_domain(self, context):
    scene = bpy.context.scene
    mytool = scene.my_tool
    
    xyz_max = [val for val in mytool.obj_xyz_max]
    xyz_min = [val for val in mytool.obj_xyz_min]
    obj.setxyz(xyz_max, xyz_min)
    obj.run()

def set_obj_count(self, context):
    scene = bpy.context.scene
    count = scene.my_tool.obj_num
    create_custom_operators(count)

def create_custom_operators(count):
    for i in (number+1 for number in range(9)):
        if i <= count:

            create_custom_operator(i)
        else:
            remove_custom_operator(i)



# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):

    my_bool: BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )
    enable_physics: BoolProperty(
        name="Enable Physics",
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
    obj_num: IntProperty(
        name = "Set numbers",
        description="Set values",
        default = 1,
        min = 1,
        max = 9,
        update=set_obj_count
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
        update=cam_domain
        ) 

    cam_xyz_min: FloatVectorProperty(
        name = "XYZ-",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= -10000.0, # float
        max = 10000.0,
        update=cam_domain
        )
        # this is dumb fix this with less code
    obj_xyz_max: FloatVectorProperty(
        name = "XYZ+",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= -10000.0, # float
        max = 10000.0,
        update=obj_domain
        ) 

    obj_xyz_min: FloatVectorProperty(
        name = "XYZ-",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= -10000.0, # float
        max = 10000.0,
        update=obj_domain
        )

    id_name: StringProperty(
        name="name",
        description=":",
        default="",
        maxlen=1024,
        )
    filepath: StringProperty(
        name="filepath",
        description=":",
        default="",
        maxlen=1024,
        subtype="DIR_PATH"
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
class Inherit_Panel:
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Blender ML"
    bl_context = "objectmode"   
    


class OBJECT_PT_CustomPanel(Inherit_Panel, Panel):
    bl_label = "My Panel"
    bl_idname = "OBJECT_PT_CustomPanel"
   
    bpy.types.Scene.prop = PointerProperty(type=bpy.types.Object)
    
    #to go underneath

    
    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "my_bool")
        layout.prop(mytool, "my_enum", text="") 
     
        layout.prop(mytool, "my_path")
        layout.separator()

        layout.label(text="Camera Spawn:")
        layout.prop(mytool, "cam_xyz_max")
        layout.prop(mytool, "cam_xyz_min")

        layout.operator("wm.cam_spawn")
        layout.separator()
        layout.prop(mytool, "obj_num")



class SceneSettingItem(bpy.types.PropertyGroup):
    tag = bpy.props.PointerProperty(type=bpy.types.Object)
    value = bpy.props.IntProperty()

obj_collection = {}
class AddButtonOperator(bpy.types.Operator):
    bl_idname = "scene.add_button_operator"
    bl_label = "Add Object"
    unique = bpy.props.IntProperty()
    def execute(self, context):
        unique = self.unique
        print(unique, "unique",)
        if unique not in obj_collection.keys():
            obj_collection[unique] = 1
        else:
            obj_collection[unique] += 1
        id = f'{unique}-{obj_collection[unique]}'
        new = context.scene.my_collection.add()
        new.name = id
        return {'FINISHED'}

class RemoveButtonOperator(bpy.types.Operator):
    bl_idname = "scene.remove_button_operator"
    bl_label = "Remove Object"

    def execute(self, context):
        id = len(context.scene.my_collection) - 1

        context.scene.my_collection.remove(id)
        return {'FINISHED'}

class ButtonOperator(bpy.types.Operator):
    bl_idname = "scene.button_operator"
    bl_label = "Button"

    id = bpy.props.IntProperty()

    def execute(self, context):
        print("Pressed button ", self.id)
        return {'FINISHED'}


class ExecuteOperator(bpy.types.Operator):
    bl_idname = "scene.execute_operator"
    bl_label = "Button"

    

    def execute(self, context):
        mytool = context.scene.my_tool
        if mytool.enable_physics:#if bool property is true, show rows, else don't
            print("enabled", mytool.obj_xyz_max, mytool.obj_xyz_min)
        for item in context.scene.my_collection:
            print(item)
        print("Pressed button ")
        return {'FINISHED'}

class OBJECT_PT_CustomPanel1(Inherit_Panel, Panel):
    bl_parent_id = "OBJECT_PT_CustomPanel"
    bl_label = "Object id #1"
    bl_options = {"DEFAULT_CLOSED"}

    

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool


        
        
        #split for button loop

        
        for item in context.scene.my_collection:
            row = self.layout.row(align=True)
            print(item)
            row.prop(item, "tag", text="add custom title here")
            # button
            # row.operator("scene.button_operator", text="Button #"+item.name).id = item.value


        #split for button loop

        split = layout.split()
        col = split.column()
        op = col.operator("scene.add_button_operator")
        op.unique = self.bl_description
        col = split.column(align=True)
        
        col.operator("scene.remove_button_operator")

        # ONLY ENABLE PHYSICS IN THE FIRST ITEM
        if self.bl_description == 1:
            layout.prop(mytool, "enable_physics")
      
            if mytool.enable_physics:
                layout.label(text="Obj Spawn:")
                layout.prop(mytool, "obj_xyz_max")
                layout.prop(mytool, "obj_xyz_min")

        # Big render button
        layout.operator("scene.execute_operator")


        
op_cls = {}
def create_custom_operator(i):
    idname = f"Object id#{str(i)}"
    bl_parent_id = "OBJECT_PT_CustomPanel"
    

    nc = type(  'DynOp_' + idname,
                    (OBJECT_PT_CustomPanel1, ),
                    {'bl_idname': idname,
                    'bl_label': 'Add a ' + idname,
                    'bl_description': i,
                })
    
    print(op_cls.keys())

    if i not in op_cls.keys(): 
        op_cls[i] = nc
        bpy.utils.register_class(nc)
def remove_custom_operator(i):  

    if i in op_cls.keys():
        
        bpy.utils.unregister_class(op_cls[i])
        del op_cls[i]

# class OBJECT_PT_CustomPanel2(Inherit_Panel, Panel):
#     bl_parent_id = "OBJECT_PT_CustomPanel"
#     bl_label = "Render Options"
#     @classmethod
#     def poll(self,context):
#         return context.object is not None

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mytool = scene.my_tool
#         if mytool.enable_physics:#if bool property is true, show rows, else don't
#             layout.label(text="frame advance")
#             layout.prop(mytool, "my_int", text="Integer Property")
        
#         # filepath
#         layout.prop(mytool, "filepath")
        
#         # Big render button
#         row = layout.row()
#         row.scale_y = 2.0
#         row.operator("scene.execute_operator")



classes = (
    MyProperties,
    OT_Cam_Spawn,
    OT_Draw_Operator,
    OBJECT_PT_CustomPanel,
    # OBJECT_PT_CustomPanel1,
    # OBJECT_PT_CustomPanel2,
    ButtonOperator,
    AddButtonOperator,
    SceneSettingItem,
    RemoveButtonOperator,
    ExecuteOperator,

)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

    #register dynamic creation see if I can place this elsewhere
    bpy.types.Scene.my_collection = bpy.props.CollectionProperty(type=SceneSettingItem)
    

    # create the initial operator
    create_custom_operators(1)
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":

    register()
    bpy.ops.object.draw_op('INVOKE_DEFAULT')

