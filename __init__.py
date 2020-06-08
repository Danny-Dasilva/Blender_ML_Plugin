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

'''
fix call object id 1, ask devin how to -------




rename - my_tool my_idname my_collection



error for if domain is 0 0 0 


-------------------------------

test button - for seeying how the camera works spawns




--

toggle display does the same for objects


# add unique domains for each obj spawn








for later --

start with 0 instead of 1 for choose object ids



advanced options


info out


toggle cutoff

dynamic objs list generation for classes, more memory efficient and clears the panel

check cutoff for too many loops- warning


fix reverse list enumerate garbage
fix DRAWBOX normalize function 
fix bad loop practice
----
Naming Conventions 
category_Location_name

locations

MT for menut
PT for Panel

OT for operator 

bl_idname = category.name
'''



bl_info = {
    "name" : "Blender_ML",
    "author" : "Danny Dasilva",
    "description" : "Blender Object Detection Data generation",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}
from .ml_class import ML_Gen
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
#    Generative helper functions
# ------------------------------------------------------------------------
def create_custom_operator(scene, i):
    idname = f"Object id#{str(i)}"
    nc = type(  'DynOp_' + idname,
                    (OBJECT_PT_Spawn_Ids, ),
                    {'bl_idname': idname,
                    'bl_label': 'Add a ' + idname,
                    'bl_description': i,
                })
    
    if i not in op_cls.keys(): 
        op_cls[i] = nc
        bpy.utils.register_class(nc)

        #str thing
        id = len(scene.my_idname)
        new = scene.my_idname.add()
        new.name = str(id)
        new.value = id


def remove_custom_operator(scene, i):  
    
    if i in op_cls.keys():

        # remove drawing
        r = i - 1
        print(i, r,  "i to be removed")
        obj = objs[r]
        if obj.registered == True:
            obj.erase()

        #unregister classes
        bpy.utils.unregister_class(op_cls[i])
        del op_cls[i]


        # god this is awful please fix
        for count, item in  reversed(list(enumerate(scene.my_collection))):
            if item.name.startswith(str(i)):
                scene.my_collection.remove(count)
        

        # delete from dictr
        if i in obj_collection:
            del obj_collection[i]

        #str thing
        id = len(scene.my_idname) - 1
        scene.my_idname.remove(id)
        for items in scene.my_idname:
            print(items)

def create_custom_operators(scene, count):
    for i in (number+1 for number in range(9)):
        if i <= count:
            create_custom_operator(scene, i)
        else:
            remove_custom_operator(scene, i)

def set_obj_count(self, context):
    scene = bpy.context.scene
    count = scene.my_tool.obj_num
    create_custom_operators(scene, count)

def init_count():
    scene = bpy.context.scene
    count = scene.my_tool.obj_num
    create_custom_operators(scene, count)



# ------------------------------------------------------------------------
#    Generator Operators
# ------------------------------------------------------------------------

class OT_Add_Obj(Operator):
    bl_idname = "scene.add_obj"
    bl_label = "Add Object"
    unique: bpy.props.IntProperty()
    
    def execute(self, context):
        unique = self.unique
       
        if unique not in obj_collection.keys():
            obj_collection[unique] = 1
        else:
            obj_collection[unique] += 1
        id = f'{unique}{obj_collection[unique]}'
        
        new = context.scene.my_collection.add()
        new.name = id
        new.value = int(id)
        for item in  context.scene.my_collection:
            print(item)
        return {'FINISHED'}

class OT_Remove_Obj(Operator):
    bl_idname = "scene.remove_obj"
    bl_label = "Remove Object"
    unique: IntProperty()
    def execute(self, context):
        unique = self.unique
        id = f'{unique}{obj_collection[unique]}'


        for count, item in  reversed(list(enumerate(context.scene.my_collection))):
            if item.name == id:
                context.scene.my_collection.remove(count)
                obj_collection[unique] -= 1
        
        for item in  context.scene.my_collection:
            print(item)
        
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Draw functions
# ------------------------------------------------------------------------

class DrawBox():

    draw_handle = None
    vertices = None


    def __init__(self, set_cam):
        self.set_cam = set_cam
        self.registered = False
        self.col = [
            [255, 128, 0, 1],
            [255, 255, 0, 1],
            [0, 255, 0, 1],
            [0, 255, 128, 1],
            [0, 255, 255, 1],
            [0, 128, 255, 1],
            [0, 0, 255, 1],
            [127, 0, 255, 1],
            [255, 0, 127, 1],
        ]
        self.color = self.normalize(self.col)
    @staticmethod
    def normalize(a):
        amin, amax = 0, 255
        for count, v in enumerate(a):
            for i, val in enumerate(v):
                a[count][i] = (val-amin) / (amax-amin)

        return a

    def register(self):
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINE_STRIP', {'pos': self.vertices})
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_px, (), "WINDOW", "POST_VIEW"
            )
    def unregister(self):

        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, 'WINDOW')
    def reset_verts(self):
        self.vertices = [(0, 0, 0)]
    def clear(self):
        self.unregister()
        self.registered = False
        
    def erase(self):
        self.reset_verts()
        self.unregister()
        self.registered = False
        
    def setxyz(self, xyz_min, xyz_max):
        
        x_min = xyz_min[0]
        x_max = xyz_max[0]
        y_min = xyz_min[1]
        y_max = xyz_max[1]
        z_min = xyz_min[2]
        z_max = xyz_max[2]
        
        self.vertices = [(x_min, y_min, z_max), (x_max,y_min,z_max), (x_max,y_min,z_min),  (x_max,y_max, z_min), (x_max,y_max, z_max), (x_min,y_max, z_max), (x_min,y_max,z_min),(x_min,y_min,z_min), (x_min,y_min,z_max),
        (x_min,y_max,z_max), (x_min,y_max,z_min), (x_max,y_max,z_min), (x_max, y_max, z_max), (x_max, y_min, z_max), (x_max, y_min, z_min), (x_min,y_min,z_min)]


    def run(self):
        if self.registered == True:
            try:
                self.unregister()
        
            except:
                print("weird error")
        
        if self.vertices:
            self.register()
            self.registered = True
        
    def draw_callback_px(self):
        bgl.glLineWidth(3)
        self.shader.bind()

        if self.set_cam == None:
            self.shader.uniform_float("color", (1, 0, 0, 1))
            
        else:
            
            
            self.shader.uniform_float("color", self.color[self.set_cam])
        self.batch.draw(self.shader)



def cam_domain(self, context):
    scene = bpy.context.scene
    mytool = scene.my_tool

    #when domain updates so does the ml section
    set_cam_dimensions(mytool.cam_xyz_min, mytool.cam_xyz_max)
    
    xyz_min = [val for val in mytool.cam_xyz_min]
    xyz_max = [val for val in mytool.cam_xyz_max]
    
    cam.setxyz(xyz_min, xyz_max)
    cam.run()
    
    
    
def obj_domain(self, context):

    xyz_min = [val for val in self.obj_xyz_min]
    xyz_max = [val for val in self.obj_xyz_max]


    obj = objs[self.value]

    obj.setxyz(xyz_min, xyz_max)
    obj.run()



def frame_advance(self, context):
    mytool = context.scene.my_tool
    frames = mytool.frame_advance
    gen.frames  = frames

def enable_physics(self, context):
    obj = objs[self.value]
    if self.enable_physics == False:
        obj.clear()
    else:
        obj.run()
def toggle_cam(self, context):
    
    if self.toggle_cam_domain == False:
        cam.clear()
    else:
        cam.run()
# ------------------------------------------------------------------------
#    Property Groups
# ------------------------------------------------------------------------
class SceneSettingItem(PropertyGroup):
    tag: bpy.props.PointerProperty(type=bpy.types.Object)
    value: IntProperty()


class StrSettingItem(PropertyGroup):
    id: bpy.props.StringProperty()
    value: IntProperty()

    obj_xyz_max: FloatVectorProperty(
        name = "XYZ+",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= -10000.0,
        max = 10000.0,
        update=obj_domain
        ) 

    obj_xyz_min: FloatVectorProperty(
        name = "XYZ-",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= -10000.0, 
        max = 10000.0,
        update=obj_domain
        )
    enable_physics: BoolProperty(
        name="Enable Physics",
        description="A bool property",
        default = False,
        update=enable_physics
        )

class MyProperties(PropertyGroup):

    enable_physics: BoolProperty(
        name="Enable Physics",
        description="A bool property",
        default = False,
        )
    toggle_cam_domain: BoolProperty(
        name="Display",
        description="Visual display for camera domain",
        default = True,
        update=toggle_cam
        )
    frame_advance: IntProperty(
        name = "frame advance",
        description="A integer property",
        default = 1,
        min = 1,
        max = 500,
        update=frame_advance
        )
    image_count: IntProperty(
        name = "image_count",
        description="A integer property",
        default = 1,
        min = 1,
        max = 100
        )
    obj_num: IntProperty(
        name = "Unique Objects",
        description="Set values",
        default = 1,
        min = 1,
        max = 9,
        update=set_obj_count
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

    filepath: StringProperty(
        name="Output",
        description="Directory to save images to",
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





# ------------------------------------------------------------------------
#    Ml Helpers
# ------------------------------------------------------------------------
def set_cam_dimensions(dim_min, dim_max):
    gen.xyz_max = [val for val in dim_max]
    gen.xyz_min = [val for val in dim_min]

def set_obj_dimensions(dim_min, dim_max):
    xyz_max = [val for val in dim_max]
    xyz_min = [val for val in dim_min]

    return xyz_min, xyz_max
    
    # gen.ob_xyz_max = [val for val in dim_max]
    # gen.ob_xyz_min = [val for val in dim_min]

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------


class OT_Cam_Spawn(Operator):
    bl_label = "Cam Spawn"
    bl_idname = "scene.cam_spawn"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        # print the values to the console
        print("Cam_Test")
        
        set_cam_dimensions(mytool.cam_xyz_min, mytool.cam_xyz_max)
        gen.randomize_camera(scene)

        print(gen.xyz_max, gen.xyz_min)
        


        return {'FINISHED'}

class OT_Obj_Spawn(Operator):
    bl_label = "Obj_Spawn"
    bl_idname = "scene.obj_spawn"

    unique: bpy.props.IntProperty()
    
    def execute(self, context):
        unique = self.unique
        scene = context.scene

        #for test spawn
        for item in scene.my_idname:
            if item.value + 1 == unique:
                xyz_min, xyz_max = set_obj_dimensions(item.obj_xyz_min, item.obj_xyz_max)


        for item in context.scene.my_collection:

            if int(item.name[0]) == unique:
                obj = item.tag
                if obj:
                    gen.randomize_obj(scene, obj, xyz_min, xyz_max)
                else:
                    self.report({"WARNING"}, "No object selected")
                    

        return {'FINISHED'}

class OT_Execute(Operator):
    bl_idname = "scene.execute_operator"
    bl_label = "Batch Render"

    

    def execute(self, context):
        scene = context.scene
        mytool = context.scene.my_tool
        gen.reset()

        print(gen.xyz_min, gen.xyz_max, "callllllll")
        # Check if camera domain Exists
            
        if not(gen.xyz_min and gen.xyz_max):
            self.report({"ERROR"}, "Camera Domain Not Set")
            return {'FINISHED'}
        # Check if objects are selected Exists
        if len(context.scene.my_collection) == 0:
            self.report({"ERROR"}, "No object selected")
            return {'FINISHED'}

        # self.report({"ERROR"}, "Something isn't right")
        # self.report({"WARNING"}, "Something isn't right")


        if mytool.enable_physics:#if bool property is true, show rows, else don't
            print("enabled",gen.ob_xyz_max, gen.ob_xyz_min)
            # set_obj_dimensions(mytool.obj_xyz_min, mytool.obj_xyz_max)
            gen.enable_physics = True
        
        for item in context.scene.my_idname:
            gen.names_dict[item.value + 1] = item.id


        


        for item in context.scene.my_collection:
            if item.tag:
                gen.add(item.tag, item.name[0])
        
        
        # filepath if in plugin else default
        if mytool.filepath:
            filepath = str(mytool.filepath)
        else:
            filepath = bpy.data.scenes[0].render.filepath
            self.report({"WARNING"}, "Filepath not set in plugin, defaulting to Output menu settings")

        file_format = scene.render.image_settings.file_format
        gen.batch_render(scene, int(mytool.image_count), filepath, file_format)
        return {'FINISHED'}


class OT_Spawn(bpy.types.Operator):
    bl_idname = "scene.spawn_first"
    bl_label = "Test Button"

    
    def execute(self, context):
        scene = context.scene
        mytool = context.scene.my_tool
        self.report({"DEBUG"}, "Camera Domain Not Set")
        return {'FINISHED'}



# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------
class Inherit_Panel:
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Blender ML"
    bl_context = "objectmode"   
    
class OBJECT_PT_Camera_Settings(Inherit_Panel, Panel):
    bl_label = "My Panel"
    bl_idname = "OBJECT_PT_Camera_Settings"
   
    bpy.types.Scene.prop = PointerProperty(type=bpy.types.Object)
    
    #to go underneath



    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.label(text="Camera Spawn Domain:")
        layout.prop(mytool, "cam_xyz_max")
        layout.prop(mytool, "cam_xyz_min")

        # test spawn and toggle display
        row = layout.row()
        row.operator("scene.cam_spawn")
        row.prop(mytool, "toggle_cam_domain")

        layout.separator()
        layout.prop(mytool, "obj_num")





class OBJECT_PT_Spawn_Ids(Inherit_Panel, Panel):
    
    # custom op
    i = 1
    idname = f"Object id#{str(i)}"
    bl_idname = idname
    bl_label  = f'Add a {idname}' 
    bl_description = i
    
            
    #default
    bl_parent_id = "OBJECT_PT_Camera_Settings"
    bl_options = {"DEFAULT_CLOSED"}


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        #str loop
        for item in context.scene.my_idname:
            
            if item.value + 1 == self.bl_description:
                layout.prop(item, "id", text=f"{self.bl_description}")
        
        

        #obj loop
        for item in context.scene.my_collection:
            if int(item.name[0]) == self.bl_description:
                row = self.layout.row(align=True)
                row.prop(item, "tag", text="add custom title here")



        split = layout.split()
        col = split.column()
        op = col.operator("scene.add_obj")
        op.unique = self.bl_description
        col = split.column(align=True)

        op = col.operator("scene.remove_obj")
        op.unique = self.bl_description

        # spawn obj loop
        for item in context.scene.my_idname:
            
            if item.value + 1 == self.bl_description:
                layout.prop(item, "enable_physics")

                if item.enable_physics:
                    layout.prop(item, "obj_xyz_min", text=f"{self.bl_description}")
                    layout.prop(item, "obj_xyz_max", text=f"{self.bl_description}")
                    op = layout.operator("scene.obj_spawn")
                    op.unique = self.bl_description

       




class OBJECT_PT_Render_Settings(Inherit_Panel, Panel):
    bl_parent_id = "OBJECT_PT_Camera_Settings"
    bl_label = "Render Options"
    

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

       


        # bad loop practice
        for obj in objs:
            if obj.registered == True:
                layout.label(text="frame advance")
                layout.prop(mytool, "frame_advance", text="Frame Advance")
                break


        layout.prop(mytool, "image_count")
        # filepath
        layout.prop(mytool, "filepath")
        
        # Big render button
        row = layout.row()
        row.scale_y = 2.0
        row.operator("scene.execute_operator")
        layout.operator("scene.spawn_first")
        
        
# ------------------------------------------------------------------------
#    Class Inits
# ------------------------------------------------------------------------

op_cls = {}
obj_collection = {}

objs = [DrawBox(i) for i in range(9)]

gen = ML_Gen()
cam = DrawBox(None)    




classes = (
    MyProperties,
    OT_Cam_Spawn,
    OBJECT_PT_Camera_Settings,
    OBJECT_PT_Render_Settings,
    OT_Obj_Spawn,
    OT_Add_Obj,
    OT_Remove_Obj,
    SceneSettingItem,
    OT_Execute,
    StrSettingItem,
    OT_Spawn,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

    #dynamic property for object selection
    bpy.types.Scene.my_collection = bpy.props.CollectionProperty(type=SceneSettingItem)
    
    #dynamic property for id names
    bpy.types.Scene.my_idname = bpy.props.CollectionProperty(type=StrSettingItem)
    

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.my_tool
    del bpy.types.Scene.my_idname
    del bpy.types.Scene.my_collection


if __name__ == "__main__":

    register()
    
    bpy.ops.object.draw_op('INVOKE_DEFAULT')
