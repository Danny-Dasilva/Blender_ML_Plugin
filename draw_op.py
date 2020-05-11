import bpy
import bgl
import gpu
from gpu.extras.batch import batch_for_shader

from bpy.types import Operator


class OT_Draw_Operator(Operator):
    bl_label = "OT_Draw_Operator"
    bl_idname = "object.draw_op"
    bl_description = "Operator for drawing"   
    bl_options = {'REGISTER'}

    def __init__(self):
        self.draw_handle = None
        self.draw_event = None

        self.widgets = []