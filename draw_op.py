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
    def invoke(self, context, event):
        self.create_batch()

        args = (self, context)
        self.register_handlers(args, context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    def register_handlers(self, args, context):
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_px, args, "WINDOW", "POST_VIEW"
        )
        self.draw_event = context.window_manager.event_timer_add(0.1, window = context.window)
    
    def unregister_handler(self, context):
        context.window_manager.event_timer_remove(self.draw_event)
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")

        self.draw_handle = None
        self.draw_event = None
    def modal(self, context, event):
        if context.area:
            context.area