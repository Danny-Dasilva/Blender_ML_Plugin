

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

