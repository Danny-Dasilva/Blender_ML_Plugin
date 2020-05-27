
import bpy

def create_custom_operator(i):
    idname = "object.operator_" + i
    
    
class MakeCustomOperators(bpy.types.Operator):
    """Create custom operators"""
    bl_idname = 'object.add_custom_ops'
    bl_label = 'Add operators'
    bl_description ='Dynamically create multiple operators'

    def execute(self, context):
        for n in ['a','b','c']:
            create_custom_operator(n)
        return {'FINISHED'}