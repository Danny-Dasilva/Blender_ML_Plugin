from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       Object
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
import bpy





# ------------------------------------------------------------------------
#    Panels
# ------------------------------------------------------------------------
class Inherit_Panel:
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Blender ML"
    bl_context = "objectmode"   
    
class OBJECT_PT_Camera_Settings(Inherit_Panel, Panel):
    bl_label = "My Panel"
    bl_idname = "OBJECT_PT_Camera_Settings"
   
    bpy.types.Scene.prop = PointerProperty(type=Object)
    
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
        

        row.prop(mytool, "toggle_domain")

        if mytool.toggle_domain == True:
            row.label(text="Display", icon='HIDE_OFF')
        else:
            row.label(text="Display", icon='HIDE_ON')

        

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
            
            if item.value == self.bl_description:
                layout.prop(item, "id", text=f"{self.bl_description}")
        
        

        #obj loop
        for item in context.scene.my_collection:
            if int(item.name[0]) == self.bl_description:
                row = self.layout.row(align=True)
                row.prop(item, "tag", text="add custom title here")



        split = layout.split()
        col = split.column()
        op = col.operator("scene.add_obj", icon="PLUS")
        op.unique = self.bl_description
        col = split.column(align=True)

        op = col.operator("scene.remove_obj", icon="TRASH")
        op.unique = self.bl_description

        # spawn obj loop
        for item in context.scene.my_idname:
            
            if item.value == self.bl_description:
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