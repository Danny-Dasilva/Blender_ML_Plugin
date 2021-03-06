import bpy
import bgl
import gpu
from gpu_extras.batch import batch_for_shader

from bpy.types import Operator


class OT_Draw_Operator(Operator):
    bl_label = "OT_Draw_Operator"
    bl_idname = "object.draw_op"
    bl_description = "Operator for drawing"   
    bl_options = {'REGISTER'}



    myvar = bpy.props.FloatProperty()
    def __init__(self):
        self.draw_handle = None
        self.draw_event = None
        self.enabled = None
        self.widgets = []
        
        self.x = 0

    def execute(self, context):
        return self.invoke(context, None)
    def invoke(self, context, event):

        self.x += 1
        print(self.x)

        self.create_batch(context)
        
        args = (self, context)
        self.register_handlers(args, context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def register_handlers(self, args, context):
        print(args, "args")
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_px, args, "WINDOW", "POST_VIEW"
        )
        self.draw_event = context.window_manager.event_timer_add(0.1, window = context.window)
    
    def unregister_handlers(self, context):
        
        context.window_manager.event_timer_remove(self.draw_event)
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, "WINDOW")

        self.draw_handle = None
        self.draw_event = None
    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        if event.type in {"ESC"}:
            self.unregister_handlers(context)
            return {"CANCELLED"}
        
        return {"PASS_THROUGH"}
    def finish(self):
        self.unregister_handlers(context)
        return {"FINISHED"}
    
    def create_batch(self, context):
        
        vertices = [(0,self.myvar,self.myvar), (0,3,1), (0,6,1),  (0,6,4), (0,3,4),]
        
        print("create batch", self.myvar)
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINE_STRIP', {'pos': vertices})
    def draw_callback_px(self, op, context):
        
    
        bgl.glLineWidth(5)
        self.shader.bind()
        self.shader.uniform_float("color", (1, 0, 0, 1))
        self.batch.draw(self.shader)


