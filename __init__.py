'''
fix call object id 1
rename - my_tool my_idname my_collection
error for if domain is 0 0 0 

-------------------------------


 valv

 all.value changed to .tag


gen.objs was an object list that was appended in the ml class

.tag was the old call in my collection for actual objects


to do:



this pattern to see if a class instance exists

if not any(d['main_color'] == 'red' for d in a):
    my check = true
    


advanced options ---

toggle rotate on randomize objs
pick camera
set limit
swap to linux and pull offset function
disable find nearest

---

check cutoff for too many loops- warning
fix DRAWBOX normalize function 

----

! 1 datatype dictionary
dict {name, [objlist], spawnmax, spawnmin, cutoff}

Naming Conventions 
category_Location_name

locations

MT for menut
PT for Panel

OT for operator 

bl_idname = category.name
'''



bl_info = {
    "name" : "Object_Ml_Plugin",
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
from bpy.app.handlers import persistent
import bgl
import gpu
from gpu_extras.batch import batch_for_shader
from dataclasses import dataclass, field
from typing import List, Any
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
from time import sleep
@dataclass
class Ml_Data_Store:

    
    tag: int
    name: str = None
    
    enable_physics: bool = False
    obj_xyz_max: tuple = (0, 0, 0)
    obj_xyz_min: tuple = (0, 0, 0)
    rotate: bool = True
    cutoff: float = 30


    panel_class: Any = None


    object_list: List[int] = field(default_factory=list)

    object_count: int = 0
    # maybe getter and setter for lists
    @property
    def remove_id(self):
        #returns a string that corresponds to the name of the ids in object list
        return f'{self.tag}{self.object_count}'
    
    def add(self, value):
        self.object_list.append(value)

    def increment(self):
        self.object_count += 1

    def remove(self):
        self.object_count -= 1

    def update_values(self, **kwargs):
        self.__dict__.update(kwargs)

    def reset(self, tag):
        self.__init__(tag=tag)

data_store = []


def update(my_idname, my_collection):
    #set default values 
    for tag in my_idname:
        xyz_min, xyz_max = unpack_dim(tag.obj_xyz_min, tag.obj_xyz_max)
        data_store[tag.identifier].update_values(name=tag.unique_name,
                                            enable_physics=tag.enable_physics,
                                            obj_xyz_min= xyz_min, 
                                            obj_xyz_max= xyz_max,
                                            rotate= tag.rotate, 
                                            cutoff= tag.cutoff,
                                            object_list= [])
    #add objects                                         
    for item in my_collection:
        if item.object_pointer:
            data_store[item.value].add(item.object_pointer)

# ------------------------------------------------------------------------
#    Generative helper functions
# ------------------------------------------------------------------------
def create_custom_operator(scene, tag):
    idname = f"Object id#{str(tag + 1)}"
    nc = type(  'DynOp_' + idname,
                    (OBJECT_PT_Spawn_Ids, ),
                    {'bl_idname': idname,
                    'bl_label': 'Add a ' + idname,
                    'bl_description': tag,
                    'bl_options' : {"DEFAULT_CLOSED"},
                })
    data_store.append(Ml_Data_Store(tag))

    #add panel to data store
    if data_store[tag].panel_class is None:
     
        bpy.utils.register_class(nc)
        data_store[tag].update_values(panel_class=nc)

        print(len(data_store), "DATA STORE ADD")
    
    #create MLAttributes for new unique id
    new = scene.my_idname.add()
    new.identifier = tag
    new.value = tag
    

def remove_custom_operator(scene, tag):  
    
    if data_store[tag].panel_class is not None:

        # remove drawing
        obj = objs[tag]
        if obj.registered == True:
            obj.erase()

        #remove object per unique id
        to_remove = [count for count, item in enumerate(scene.my_collection) if item.value == tag]
        for count in reversed(to_remove):
            scene.my_collection.remove(count)


        #unregister panel
        bpy.utils.unregister_class(data_store[tag].panel_class)

        # remove data class instance
        del data_store[tag]
      

        #remove scene instance
        scene.my_idname.remove(tag)



        

def create_custom_operators(scene, count):
    print(len(data_store), "len store", count)

    existing = len(data_store)
    
    print(count, existing)
    #basically if the input count is greater or less than the current add or remove accodingly
    if count > existing:
        for tag in range(existing, count):
            print(tag, "tag to ADD")
            create_custom_operator(scene, tag)
    
    elif count < existing:
        for tag in reversed(range(count, existing)):
                print(tag, "tag to REMOVE")
                remove_custom_operator(scene, tag)

           

def set_obj_count(self, context):
    scene = bpy.context.scene
    count = scene.my_tool.obj_num
    create_custom_operators(scene, count)

def init_count(scene):
    count = scene.my_tool.obj_num
    create_custom_operators(scene, count)



# ------------------------------------------------------------------------
#    Generator Operators
# ------------------------------------------------------------------------

class OT_Add_Obj(Operator):
    bl_idname = "scene.add_obj"
    bl_label = "Add Object"
    unique_id: bpy.props.IntProperty()
    
    def execute(self, context):
        unique_id = self.unique_id
        
        data_store[unique_id].increment()
        name = data_store[unique_id].remove_id
        
        #create collection instance for sub
        new = context.scene.my_collection.add()
        new.name = name
        new.value = unique_id
        
        return {'FINISHED'}

class OT_Remove_Obj(Operator):
    bl_idname = "scene.remove_obj"
    bl_label = "Delete Object"
    unique_id: IntProperty()
    def execute(self, context):
        unique_id = self.unique_id
        scene = context.scene

        remove_id = data_store[unique_id].remove_id
        
        for count, item in enumerate(context.scene.my_collection):
            if item.name == remove_id:
                scene.my_collection.remove(count)
                
        data_store[unique_id].remove()

        update(scene.my_idname, scene.my_collection)
                
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
            [255, 0, 255, 1],
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
        if self.registered == True:
            self.unregister()
            self.registered = False
        
    def erase(self):
        self.reset_verts()
        self.unregister()
        self.registered = False
        print(f"zeroed our {self.set_cam}")
        
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

    # do this once
    init_count(scene)

    #when domain updates so does the ml section
    set_cam_dimensions(mytool.cam_xyz_min, mytool.cam_xyz_max)
    
    xyz_min = [val for val in mytool.cam_xyz_min]
    xyz_max = [val for val in mytool.cam_xyz_max]
    
    cam.setxyz(xyz_min, xyz_max)
    cam.run()
    
    
    
def obj_domain(self, context):

    xyz_min = [val for val in self.obj_xyz_min]
    xyz_max = [val for val in self.obj_xyz_max]

    
    obj = objs[self.identifier]

    obj.setxyz(xyz_min, xyz_max)
    obj.run()



def frame_advance(self, context):
    mytool = context.scene.my_tool
    frames = mytool.frame_advance
    gen.frames  = frames

def enable_physics(self, context):
    obj = objs[self.identifier]
    if self.enable_physics == False:
        obj.clear()
    else:
        obj.run()



def toggle_domain(self, context):
    
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
class ObjectHolder(PropertyGroup):
    #my_collection
    object_pointer: bpy.props.PointerProperty(type=bpy.types.Object)
    #change this to identifier later
    value: IntProperty()


class MlAttributes(PropertyGroup):
    #my_idname
    unique_name: bpy.props.StringProperty()

    identifier: IntProperty()

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
    advanced_options: BoolProperty(
        name="Advanced Options",
        description="Advanced Options",
        default = False,
        )
    rotate: BoolProperty(
        name="Rotate Object",
        description="Turn off rotation on random Spawn",
        default = True,
        )
    cutoff: FloatProperty(
        name="Cutoff",
        description="Percent necessary to count the object in frame, test with Read Test",
        default=30, 
        )
       



class MyProperties(PropertyGroup):

    toggle_domain: BoolProperty(
        name="",
        description="Visual display for camera domain",
        default = True,
        update=toggle_domain
        )
    frame_advance: IntProperty(
        name = "frame advance",
        description="Choose the number of frames to advance vefore the camera positions itself",
        default = 1,
        min = 1,
        max = 500,
        update=frame_advance
        )
    image_count: IntProperty(
        name = "image_count",
        description="The number of Images you want rendered",
        default = 1,
        min = 1,
        max = 100
        )
    obj_num: IntProperty(
        name = "Unique Objects",
        description="Val for unique ids",
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





# ------------------------------------------------------------------------
#    Ml Helpers
# ------------------------------------------------------------------------
def set_cam_dimensions(dim_min, dim_max):
    gen.xyz_max = [val for val in dim_max]
    gen.xyz_min = [val for val in dim_min]

def unpack_dim(dim_min, dim_max):
    xyz_max = [val for val in dim_max]
    xyz_min = [val for val in dim_min]

    return xyz_min, xyz_max
    



# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------


class OT_Cam_Spawn(Operator):
    bl_label = "Cam Spawn"
    bl_idname = "scene.cam_spawn"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
          
        set_cam_dimensions(mytool.cam_xyz_min, mytool.cam_xyz_max)
        gen.randomize_camera(scene)

        return {'FINISHED'}

class OT_Obj_Spawn(Operator):
    bl_label = "Obj_Spawn"
    bl_idname = "scene.obj_spawn"

    unique: bpy.props.IntProperty()
    
    def execute(self, context):
        unique = self.unique
        scene = context.scene

        
        update(scene.my_idname, scene.my_collection)
        
        obj = data_store[unique]
        print(obj)
        for pointer in obj.object_list:
            gen.randomize_obj(scene, pointer, obj.obj_xyz_min, obj.obj_xyz_max, obj.rotate)

        #             self.report({"WARNING"}, f"No object selected for id#{item.value}")
                    

        return {'FINISHED'}

class OT_Execute(Operator):
    bl_idname = "scene.execute_operator"
    bl_label = "Batch Render"

    

    def execute(self, context):
        scene = context.scene
        mytool = context.scene.my_tool

        # Check if camera domain Exists
            
        if not(gen.xyz_min and gen.xyz_max):
            self.report({"ERROR"}, "Camera Domain Not Set")
            return {'FINISHED'}
        # Check if objects are selected Exists
        if len(context.scene.my_collection) == 0:
            self.report({"ERROR"}, "No object selected")
            return {'FINISHED'}


        update(scene.my_idname, scene.my_collection)

        print("DATA STORE", data_store)

        # filepath if in plugin else default
        if mytool.filepath:
            filepath = str(mytool.filepath)
        else:
            filepath = bpy.data.scenes[0].render.filepath
            self.report({"WARNING"}, "Filepath not set in plugin, defaulting to Output menu settings")

        file_format = scene.render.image_settings.file_format
        image_count = int(mytool.image_count)
        labels = list(gen.batch_render(scene, data_store,image_count, filepath, file_format))
        # gen.write(filepath, labels)
        print(labels)
        return {'FINISHED'}


class OT_Spawn(bpy.types.Operator):
    bl_idname = "scene.test_spawn"
    bl_label = "Spawn Test"




class OT_Read(bpy.types.Operator):
    bl_idname = "scene.test_read"
    bl_label = "Read Test"
    def execute(self, context):
        scene = context.scene
        mytool = context.scene.my_tool

             
        
        # Check if objects are selected Exists
        if len(context.scene.my_collection) == 0:
            self.report({"ERROR"}, "No object selected")
            return {'FINISHED'}


        update(scene.my_idname, scene.my_collection)
        labels = str(gen.test_render(scene, data_store))
        
        self.report({"INFO"}, labels)
        return {'FINISHED'}


class OT_Test(bpy.types.Operator):
    bl_idname = "scene.test"
    bl_label = "Testing button"

    
    def execute(self, context):
        scene = context.scene
        mytool = context.scene.my_tool
        
        
        for item in  scene.my_collection:
            print(item, "items in test")
        
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
        row = layout.row(align = True)
        row.operator("scene.cam_spawn", icon="OUTLINER_OB_CAMERA")
        
        if mytool.toggle_domain == True:
            icon='HIDE_OFF'
        else:
            icon='HIDE_ON'

        
        row.prop(mytool, "toggle_domain", icon=icon, text="Display", emboss=False)
        
        

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
            
            if item.identifier == self.bl_description:
                layout.prop(item, "unique_name", text=f"{self.bl_description}")
        
        

        #obj loop
        for item in context.scene.my_collection:
            if int(item.name[0]) == self.bl_description:
                row = self.layout.row(align=True)
                row.prop(item, "object_pointer", text="add custom title here")



        split = layout.split()
        col = split.column()
        op = col.operator("scene.add_obj", icon="PLUS")
        op.unique_id = self.bl_description
        col = split.column(align=True)

        op = col.operator("scene.remove_obj", icon="TRASH")
        op.unique_id = self.bl_description

        # spawn obj loop
        for item in context.scene.my_idname:
            
            if item.identifier == self.bl_description:
                row = layout.row()
                row.prop(item, "enable_physics")

                row.prop(item, "advanced_options")

                if item.enable_physics:
                    layout.prop(item, "obj_xyz_min", text=f"{self.bl_description}")
                    layout.prop(item, "obj_xyz_max", text=f"{self.bl_description}")
                    op = layout.operator("scene.obj_spawn")
                    op.unique = self.bl_description
                if item.advanced_options:
                    row = layout.row()
                    row.prop(item, "rotate")
                    row.prop(item, "cutoff")
                    
       




class OBJECT_PT_Render_Settings(Inherit_Panel, Panel):
    bl_parent_id = "OBJECT_PT_Camera_Settings"
    bl_label = "Render Options"
    

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

       
        registered = False

        # bad loop practice
        for obj in objs:
            if obj.registered == True:
                registered = True
                break
        #kinda bad
      

        layout.label(text="frame advance")
        row = layout.row(align=True)
        row.enabled = registered
        row.prop(mytool, "frame_advance", text="Frame Advance")

        layout.label(text="Choose the # of images to render")
        layout.prop(mytool, "image_count", icon="IMAGE_DATA")
        # filepath
        layout.prop(mytool, "filepath")
        
        # Big render button
        row = layout.row()
        row.scale_y = 2.0
        row.operator("scene.execute_operator")


        row = layout.row(align=True)
        
        row.operator("scene.test_spawn")
        row.operator("scene.test_read")

        layout.operator("scene.test")
        
# ------------------------------------------------------------------------
#    Set defaults
# ------------------------------------------------------------------------


@persistent
def addon_search(scene):
    if scene.my_idname:
        scene.my_idname.clear()
    init_count(scene)

    #addon search handler
    # bpy.app.handlers.depsgraph_update_post.remove(addon_search)
    # handler_removed = True



# ------------------------------------------------------------------------
#    Class Inits
# ------------------------------------------------------------------------


objs = [DrawBox(i) for i in range(10)]
gen = ML_Gen()
cam = DrawBox(None)    
# handler_removed = False

classes = (
    MyProperties,
    OT_Cam_Spawn,
    OBJECT_PT_Camera_Settings,
    OBJECT_PT_Render_Settings,
    OT_Obj_Spawn,
    OT_Add_Obj,
    OT_Remove_Obj,
    ObjectHolder,
    OT_Execute,
    MlAttributes,
    OT_Spawn,
    OT_Read,
    OT_Test,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

    #dynamic property for object selection
    bpy.types.Scene.my_collection = bpy.props.CollectionProperty(type=ObjectHolder)
    
    #dynamic property for id names
    bpy.types.Scene.my_idname = bpy.props.CollectionProperty(type=MlAttributes)

    # bpy.app.handlers.depsgraph_update_post.append(addon_search)
    

def unregister():
    from bpy.utils import unregister_class
    # clear gpu
    cam.clear()

    # remove drawings
    for obj in objs:
        if obj.registered == True:
            obj.erase()


    for ml_clss in reversed(data_store):
        #unregister classes
        unregister_class(ml_clss.panel_class)
        del ml_clss.panel_class

    
        
    

    for cls in reversed(classes):
        unregister_class(cls)
    # bpy.types.Scene.my_idname.clear()
    
    

    bpy.context.scene.my_collection.clear()
    bpy.context.scene.my_idname.clear()
       
            

    del bpy.types.Scene.my_tool
    del bpy.types.Scene.my_collection
    del bpy.types.Scene.my_idname
    


if __name__ == "__main__":

    register()
