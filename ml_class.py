import bpy
from random import uniform

import bpy
import mathutils
from random import randint, uniform
from math import *
import os
import json
from time import sleep

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

    def camera_view_bounds_2d(scene, camera_object, mesh_object):
        """
        Returns camera space bounding box of the mesh object.
        Gets the camera frame bounding box, which by default is returned without any transformations applied.
        Create a new mesh object based on mesh_object and undo any transformations so that it is in the same space as the
        camera frame. Find the min/max vertex coordinates of the mesh visible in the frame, or None if the mesh is not in view.
        :param scene:
        :param camera_object:
        :param mesh_object:
        :return:
        """

        """ Get the inverse transformation matrix. """
        matrix = camera_object.matrix_world.normalized().inverted()
        """ Create a new mesh data block, using the inverse transform matrix to undo any transformations. """
        dg = bpy.context.evaluated_depsgraph_get()
        
        ob = mesh_object.evaluated_get(dg) #this gives us the evaluated version of the object. Aka with all modifiers and deformations applied.
        mesh = ob.to_mesh()
        #mesh = mesh_object.to_mesh()
        mesh.transform(mesh_object.matrix_world)
        mesh.transform(matrix)

        """ Get the world coordinates for the camera frame bounding box, before any transformations. """
        frame = [-v for v in camera_object.data.view_frame(scene=scene)[:3]]


        lx = []
        ly = []
        
        for v in mesh.vertices:
            co_local = v.co
            z = -co_local.z

            if z <= 0.0:
                """ Vertex is behind the camera; ignore it. """
                continue
            else:
                """ Perspective division """
                frame = [(v / (v.z / z)) for v in frame]
            
            min_x, max_x = frame[1].x, frame[2].x
            min_y, max_y = frame[0].y, frame[1].y
            
            x = (co_local.x - min_x) / (max_x - min_x)
            y = (co_local.y - min_y) / (max_y - min_y)
            lx.append(x)
            ly.append(y)
        
        mesh_object.to_mesh_clear()

        """ Image is not in view if all the mesh verts were ignored """
        if not lx or not ly:
            return None

        min_x = np.clip(min(lx), 0.0, 1.0)
        min_y = np.clip(min(ly), 0.0, 1.0)
        max_x = np.clip(max(lx), 0.0, 1.0)
        max_y = np.clip(max(ly), 0.0, 1.0)

        """ Image is not in view if both bounding points exist on the same side """
        if min_x == max_x or min_y == max_y:
            return None

        """ Figure out the rendered image size """
        render = scene.render
        fac = render.resolution_percentage * 0.01
        dim_x = render.resolution_x * fac
        dim_y = render.resolution_y * fac

        return (min_x, min_y), (max_x, max_y)

    