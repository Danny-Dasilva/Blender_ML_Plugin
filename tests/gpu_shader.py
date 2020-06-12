
vertices = [(0, 0, 4), (4,0,4), (4,0,0),  (4,4,0), (4,4,4), (0,4,4), (0,4,0),(0,0,0), (0,0,4),
    (0,4,4), (0,4,0), (4,4,0), (4, 4, 4), (4, 0, 4), (4, 0, 0), (0,0,0)]
        
        
shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
batch = batch_for_shader(shader, 'LINE_STRIP', {'pos': vertices})

def draw_callback_px():
    bgl.glLineWidth(5)
    shader.bind()
    shader.uniform_float("color", (1, 0, 0, 1))
    batch.draw(shader)


if data.draw_handle != None:
    bpy.types.SpaceView3D.draw_handler_remove(data.draw_handle, 'WINDOW')


data.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
    draw_callback_px, (), "WINDOW", "POST_VIEW"
    )
