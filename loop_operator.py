
import bpy
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
                       
def create_custom_operator(i):
    idname = "object.operator_" + i
    
    def func(self, context):
        print("Hello World", self.bl_idname)
        return {'FINISHED'}

    opclass = type("DynOp" + i,
                   (bpy.types.Operator, ),
                   {"bl_idname": idname, "bl_label": "Test", "execute": func},
                   )
    bpy.utils.register_class(opclass)
    cls.CustomOp = cls.CustomOp + [opclass]
    
    
    
class MakeCustomOperators(bpy.types.Operator):
    """Create custom operators"""
    bl_idname = 'object.add_custom_ops'
    bl_label = 'Add operators'
    bl_description ='Dynamically create multiple operators'

    def execute(self, context):
        for n in ['a','b','c']:
            create_custom_operator(n)
        return {'FINISHED'}


class Inherit_Panel:
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Blender ML"
    bl_context = "objectmode"  
    
    
class CustomPanel(Inherit_Panel, Panel):
    bl_label = "My Panel"
    bl_idname = "OBJECT_PT_CustomPanel"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.operator("object.add_custom_ops")


classes = (
    CustomPanel,
    MakeCustomOperators,
    create_custom_operator,
    
    

)
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()