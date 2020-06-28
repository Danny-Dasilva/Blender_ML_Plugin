

import bpy

from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       CollectionProperty,
                       )
from .panels import OBJECT_PT_Spawn_Ids
 
# ------------------------------------------------------------------------
#    Callback Functions
# ------------------------------------------------------------------------
def create_custom_operator(scene, i):
    idname = f"Object id#{str(i + 1)}"
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
        
        new = scene.my_idname.add()
        new.name = str(i)
        new.value = i
    print(op_cls.keys())

def remove_custom_operator(scene, i):  
    
    if i in op_cls.keys():

        # remove drawing
     
        obj = objs[i]
        if obj.registered == True:
            obj.erase()

        #unregister classes
        bpy.utils.unregister_class(op_cls[i])
        del op_cls[i]


        # god this is awful please fix
        for count, item in  reversed(list(enumerate(scene.my_collection))):
            if item.name.startswith(str(i)):
                scene.my_collection.remove(count)

        for count, item in  reversed(list(enumerate(scene.my_idname))):
            if item.value == i:

                scene.my_idname.remove(count)

        # delete from dictr
        if i in obj_collection:
            del obj_collection[i]

        for items in scene.my_idname:
            print(items, "items in scene")

        

def create_custom_operators(scene, count):
    for i in range(10):
        if i < count:
            create_custom_operator(scene, i)
        else:
            remove_custom_operator(scene, i)

           
    print(op_cls.keys())



def init_count(scene):
    count = scene.my_tool.obj_num
    create_custom_operators(scene, count)



def cam_domain(self, context):
    scene = bpy.context.scene
    mytool = scene.my_tool


    # do this once
    init_count(scene)

    #when domain updates so does the ml section
    set_cam_dimensions(mytool.cam_xyz_min, mytool.cam_xyz_max)
    
    xyz_min = [val for val in mytool.cam_xyz_min]
    xyz_max = [val for val in mytool.cam_xyz_max]
    
    cam.setxyz(xyz_min, xyz_max)
    cam.run()


def set_obj_count(self, context):
    scene = bpy.context.scene
    count = scene.my_tool.obj_num
    create_custom_operators(scene, count)

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
def toggle_domain(self, context):
    for obj in objs:
        obj.clear()
    if self.toggle_domain == False:
        cam.clear()
        for obj in objs:
            obj.clear()
    else:
        cam.run()
        for obj in objs:
            obj.run()
# ------------------------------------------------------------------------
#    Property Groups
# ------------------------------------------------------------------------


class SceneSettingItem(PropertyGroup):
    tag: PointerProperty(type=bpy.types.Object)
    value: IntProperty()


class StrSettingItem(PropertyGroup):
    id: StringProperty()
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
    toggle_domain: BoolProperty(
        name="",
        description="Visual display for camera domain",
        default = True,
        update=toggle_domain
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
        max = 10,
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


