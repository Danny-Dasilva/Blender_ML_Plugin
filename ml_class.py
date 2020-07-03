
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
import mathutils
from random import randint, uniform
from math import *
import os
import json

class ML_Gen():
    def __init__(self):
        self.xyz_max = None
        self.xyz_min = None
        self.pi = 3.14159265
        self.limit = 0.0001
        self.enable_physics = None
        self.frames = None
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
    def randomize_obj(self, scene, obj, xyz_min, xyz_max, rotate):
        pi = self.pi
        if rotate:
            roll = uniform(0, 90)
            pitch = uniform(0, 90)
            yaw = uniform(0, 90)
            obj.rotation_mode = 'XYZ'
            obj.rotation_euler[0] = pitch*(pi/180.0)
            obj.rotation_euler[1] = roll*(pi/180)
            obj.rotation_euler[2] = yaw*(pi/180.0)

        obj.location.x = uniform(xyz_min[0], xyz_max[0])   
        obj.location.y = uniform(xyz_min[1], xyz_max[1])                                                                                                                                       
        obj.location.z = uniform(xyz_min[2], xyz_max[2])
        
        self.update()
    def randomize_objs(self, scene, object_list, xyz_min, xyz_max, rotate):
        pi = self.pi
        for obj in object_list:
            self.randomize_obj(scene, obj, xyz_min, xyz_max, rotate)
    # def randomize_objs(self, scene):
    #     objs = self.objs
    #     print("function called")
    #     print(self.objs, "objs")
    #     for key, ob in objs.items() :
            
            
    #         xyz_min = self.objs[int(key)]['xyz_min']
    #         xyz_max = self.objs[int(key)]['xyz_max']

    #         if xyz_min and xyz_max:
    #             for obj in ob['objects']:
    #                 print(obj, "randomzie", xyz_min, xyz_max)
    #                 self.randomize_obj(scene, obj, xyz_min, xyz_max)


    # run ops
    @staticmethod
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


    def get_cordinates(self, scene, camera,  objects, filename):
        camera_object = camera
        print(objects, "objects in get cordinates")
    
        cordinates = {
                'image': filename,
                'meshes': {}
            }
        for obj, name in objects.items():

            
       
            cordinates['meshes'][name] = {}
 
            
      
            bounding_box = self.camera_view_bounds_2d(scene, camera_object, obj)
            if bounding_box:
                cordinates['meshes'][name][obj.name] = {
                                'x1': bounding_box[0][0],
                                'y1': bounding_box[0][1],
                                'x2': bounding_box[1][0],
                                'y2': bounding_box[1][1]
                            }
            
        return cordinates
    @staticmethod
    def measure (first, second):

        locx = second[0] - first[0]
        locy = second[1] - first[1]
        locz = second[2] - first[2]

        distance = sqrt((locx)**2 + (locy)**2 + (locz)**2) 
        return distance

    def center_obj(self, obj_camera, obj):
        point = obj.matrix_world.to_translation()
        loc_camera = obj_camera.matrix_world.to_translation()

        direction = point - loc_camera
        # point the cameras '-Z' and use its 'Y' as up
        rot_quat = direction.to_track_quat('-Z', 'Y')
        
        # assume we're using euler rotation
        obj_camera.rotation_euler = rot_quat.to_euler()
        self.update()
        
    

    @staticmethod
    def point_at(obj, target, roll=0):
        obj = obj.matrix_world.to_translation()
        """
        Rotate obj to look at target
        :arg obj: the object to be rotated. Usually the camera
        :arg target: the location (3-tuple or Vector) to be looked at
        :arg roll: The angle of rotation about the axis from obj to target in radians. 
        Based on: https://blender.stackexchange.com/a/5220/12947 (ideasman42)      
        """
        if not isinstance(target, mathutils.Vector):
            target = mathutils.Vector(target)
        loc = obj.location
        # direction points from the object to the target
        direction = target - loc

        quat = direction.to_track_quat('-Z', 'Y')

        # /usr/share/blender/scripts/addons/add_advanced_objects_menu/arrange_on_curve.py
        quat = quat.to_matrix().to_4x4()
        rollMatrix = mathutils.Matrix.Rotation(roll, 4, 'Z')

        # remember the current location, since assigning to obj.matrix_world changes it
        loc = loc.to_tuple()
        obj.matrix_world = quat * rollMatrix
        obj.location = loc


    def offset(self, scene, camera, angle):
        
        angle = uniform(-angle, angle)
        height = 480
        width = 640
            
        if width > height:    
            ratio = height / width  
            desired_x = (50 / 2) * (angle/100) * ratio
            desired_y = (50 / 2) * (angle/100) 
        
        elif height > width:
            ratio = width / height  
            desired_x = (50 / 2) * (angle/100)
            desired_y = (50 / 2) * (angle/100) * ratio
            
    
        scene.camera.rotation_mode = 'XYZ'
        x = scene.camera.rotation_euler[0]
        y = scene.camera.rotation_euler[2]
        
        change_x = x + (desired_x * (pi / 180.0))
        change_y = y + (desired_y * (pi / 180.0))
        scene.camera.rotation_euler[0] = change_x 
        scene.camera.rotation_euler[2] = change_y 
        self.update()

    @staticmethod
    def BVHTreeAndVerticesInWorldFromObj( obj ):
        mWorld = obj.matrix_world
        vertsInWorld = [mWorld @ v.co for v in obj.data.vertices]

        bvh = BVHTree.FromPolygons( vertsInWorld, [p.vertices for p in obj.data.polygons] )

        return bvh, vertsInWorld


    # Deselect mesh polygons and vertices
    @staticmethod
    def DeselectEdgesAndPolygons( obj ):
        for p in obj.data.polygons:
            p.select = False
        for e in obj.data.edges:
            e.select = False

    def get_raycast_percentage(self, scene, cam, obj, cutoff):
        limit = self.limit
        # Threshold to test if ray cast corresponds to the original vertex
        viewlayer = bpy.context.view_layer
        # Deselect mesh elements
        self.DeselectEdgesAndPolygons( obj )

        # In world coordinates, get a bvh tree and vertices
        bvh, vertices = self.BVHTreeAndVerticesInWorldFromObj( obj )


        same_count = 0 
        count = 0 
        for i, v in enumerate( vertices ):
            count += 1
            # Get the 2D projection of the vertex
            co2D = world_to_camera_view( scene, cam, v )

            # By default, deselect it
            obj.data.vertices[i].select = False
            
            # If inside the camera view
            if 0.0 <= co2D.x <= 1.0 and 0.0 <= co2D.y <= 1.0: 
                # Try a ray cast, in order to test the vertex visibility from the camera
                location, normal, index, distance, t, ty = scene.ray_cast(viewlayer, cam.location, (v - cam.location).normalized() )
                t = (v-normal).length
                if t < limit:
                    same_count += 1

        del bvh
        ray_percent = same_count/ count
        if ray_percent > cutoff/ 100:
            value = True
        else:
            value = False
        return value, ray_percent 

    def get_raycast_percentages(self, scene, cam, data_store):
        data = {}
        visible = {}
        for objs in data_store:
            for obj in objs.object_list:
                
                name = objs.name or objs.tag
                value, percent = self.get_raycast_percentage(scene, cam, obj, objs.cutoff)
                if value:
                    
                    visible[obj] = name
                data[obj.name] = f'{percent * 100}% vertices visible'

        return visible, data

    @staticmethod
    def find_nearest(camera, obj_list):
        nearest = None
        old_dist = 100000000000
        point = camera.location
        for obj in obj_list:
            dist = (point - obj.location).length
            if dist < old_dist:
                nearest = obj
                old_dist = dist
        return nearest
    
    

    def increment_frames(self, scene):
        
        for i in range(self.frames):
            scene.frame_set(i)
    
    

    def test_render(self, scene, data_store):
        camera = scene.camera

        objects, data = self.get_raycast_percentages(scene, camera, data_store)
        
        return data

    def write(self, filepath, labels):
        
        with open(f'{filepath}/labels.json', 'w+') as f:
            json.dump(labels, f, sort_keys=True, indent=4, separators=(',', ': '))
        
    def randomize(self, scene, data_store):
        for obj in data_store:
            if obj.enable_physics:
                self.randomize_objs(scene, obj.object_list, obj.obj_xyz_min, obj.obj_xyz_max, obj.rotate)
            if self.frames:
                self.increment_frames(scene)
    def batch_render(self, scene, data_store, image_count, filepath, file_format, file_prefix="render", loop_count = 0):
        value = True
        
        while loop_count != image_count:

            self.randomize(scene, data_store)
                
            camera = self.randomize_camera(scene)
            
            
            for data in reversed(data_store):

                # basically if value exists assign it
                if (current := data.object_list):
                    obj_list = current

            #Find the nearest object for the lowest obj in list
            nearest_obj = self.find_nearest(camera, obj_list)
        

            self.center_obj(camera, nearest_obj)

            # add in offset percentage
            self.offset(scene, camera, 50)
            
            value, percent = self.get_raycast_percentage(scene, camera, nearest_obj, 40)
        
            if value == False:
                    loop_count -= 1
                    value = True
            else:
                    #render image in filepath
                    filename = f'{str(file_prefix)}-{str(loop_count)}.{file_format.lower()}'
                    bpy.context.scene.render.filepath = os.path.join(f'{filepath}/', filename)
                    bpy.ops.render.render(write_still=True)

                  
                    
                    # #loop through objects instead
                    objects, data = self.get_raycast_percentages(scene, camera, data_store)
                    
                    # #loop through objects instead
                    scene_labels = self.get_cordinates(scene, camera, objects, filename)
               
                    
                    yield scene_labels

            loop_count += 1
            

# fix adding items does not update when you change them, added light and it stayed there