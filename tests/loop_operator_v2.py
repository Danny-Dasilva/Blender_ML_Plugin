
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
class MyProperties(PropertyGroup):

    
    my_int: IntProperty(
        name = "Int Value",
        description="A integer property",
        default = 23,
        min = 1,
        max = 15
        )
                            
def create_custom_operator(i):
    idname = "object.operator_" + i
    bl_parent_id = "OBJECT_PT_CustomPanel"
    
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Column One:")
    def func(self, context):
        print("Hello World", self.bl_idname)
        return {'FINISHED'}

    nc = type(  'DynOp_' + idname,
                    (CustomObjectBase, ),
                    {'bl_idname': idname,
                    'bl_label': 'Add a ' + idname,
                    'bl_description': 'This adds an ' + idname,
                })
    bpy.utils.register_class(nc)
    print("finishedd creation")
#    cls.CustomOp = cls.CustomOp + [opclass]
    
    

        
        
class MakeCustomOperators(bpy.types.Operator):
    """Create custom operators"""
    bl_idname = 'object.add_custom_ops'
    bl_label = 'Add operators'
    bl_description ='Dynamically create multiple operators'

    def execute(self, context):
        for n in ['a','b','c']:
            create_custom_operator(n)
        return {'FINISHED'}

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
    bl_category = "TEST"
    bl_context = "objectmode"  
    
    
class CustomPanel(Inherit_Panel, Panel):
    bl_label = "My Panel"
    bl_idname = "OBJECT_PT_CustomPanel"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.operator("object.add_custom_ops")

class CustomObjectBase(Inherit_Panel, Panel):
    idname = "object.example_test"
    bl_parent_id = "OBJECT_PT_CustomPanel"
    bl_label = 'Add aaaa'
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Column One:")
        
        
classes = (
    MyProperties,
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