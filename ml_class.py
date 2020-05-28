import bpy
from random import uniform


class ML_Gen():
    def __init__(self):
        self.xyz_max = [0, 0, 0]
        self.xyz_min = [0, 0, 0]
        self.ob_xyz_max  = [0, 0, 0]
        self.ob_xyz_min  = [0, 0, 0]
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
    def randomize_obj(self, scene, obj):
        pi = 3.1415
        roll = uniform(0, 90)
        pitch = uniform(0, 90)
        yaw = uniform(0, 90)
        obj.rotation_mode = 'XYZ'
        obj.rotation_euler[0] = pitch*(pi/180.0)
        obj.rotation_euler[1] = roll*(pi/180)
        obj.rotation_euler[2] = yaw*(pi/180.0)
        print(self.ob_xyz_min, self.ob_xyz_max)
        obj.location.x = uniform(self.ob_xyz_min[0], self.ob_xyz_max[0])   
        obj.location.y = uniform(self.ob_xyz_min[1], self.ob_xyz_max[1])                                                                                                                                       
        obj.location.z = uniform(self.ob_xyz_min[2], self.ob_xyz_max[2])
        
        self.update()

    # run ops

    def center_obj(obj_camera, point):
        point = point.matrix_world.to_translation()

        loc_camera = obj_camera.matrix_world.to_translation()

        direction = point - loc_camera
        # point the cameras '-Z' and use its 'Y' as up
        rot_quat = direction.to_track_quat('-Z', 'Y')
        
        # assume we're using euler rotation
        obj_camera.rotation_euler = rot_quat.to_euler()
        update()
        eulers = [degrees(a) for a in obj_camera.matrix_world.to_euler()]
        z = eulers[2]
        distance = measure(point, loc_camera)
        return distance, z

