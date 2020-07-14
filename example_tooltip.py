import bpy
 
 
 
class ADDONNAME_PT_TemplatePanel(bpy.types.Panel):
    bl_label = "Name of the Panel"
    bl_idname = "ADDONNAME_PT_TemplatePanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "Template Tab"
   
    def draw(self, context):
        layout = self.layout
       
        layout.operator("wm.template_operator")
       
 
 
 
 
 
class ADDONAME_OT_TemplateOperator(bpy.types.Operator):
    bl_label = "Template Operator"
    bl_idname = "wm.template_operator"
   
    preset_enum : bpy.props.EnumProperty(
        name = "",
        description = "select an option", 
        items = [ 
            ("op1", "CUBE", "add a cube to scene" ),
            ("op2", "sphere", "add a sphere to scene" ),
            ("op3", "Suzzane", "add a monke to scene" )
        ]
        
    
    )
   
   
   
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
   
   
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "preset_enum")
       
   
    def execute(self, context):
       
        return {'FINISHED'}    
 
 
 
 
 
 
 
 
classes = [ADDONNAME_PT_TemplatePanel, ADDONAME_OT_TemplateOperator]
 
 
 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
 
 
 
if __name__ == "__main__":
    register()