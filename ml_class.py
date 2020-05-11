import bpy
from random import uniform


class ML_Gen():
    def __init__(self):
        self.xyz_max = [0, 0, 0]
        self.xyz_min = [0, 0, 0]
        self.pi = 3.14159265
        
    @staticmethod
    def update():
        dg = bpy.context.evaluated_depsgraph_get() 
        dg.update()
    

    def randomize_camera(self, scene):
        x = uniform(self.xyz_min[0], self.xyz_max[0])   
        y = uniform(self.xyz_min[1], self.xyz_max[1])                                                                                                                                       
        z = uniform(self.xyz_min[2], self.xyz_max[2])
       

        
        # Set camera translation
        scene.camera.location.x = x
        scene.camera.location.y = y
        scene.camera.location.z = z
        # #call update
        self.update()

        return scene.camera
