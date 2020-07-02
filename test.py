def randomize_objs(self, scene, object_list, xyz_min, xyz_max, rotate):
        pi = self.pi
        for obj in object_list:
            self.randomize_obj(scene, obj, xyz_min, xyz_max, rotate)
        
def batch_render(self, scene, data_store, image_count, filepath, file_format, file_prefix="render", loop_count = 0):
    
        scene_setup_steps = int(image_count)
        value = True
        ball_lst = self.objs[0]["objects"]
        ball_dict = self.objs

        while loop_count != image_count:

            for obj in data_store:
                if obj.enable_physics:
                    self.randomize_objs(scene, obj.object_list, obj.obj_xyz_min, obj.obj_xyz_max, obj.rotate)
                if self.frames:
                    self.increment_frames(scene)
                
            camera = self.randomize_camera(scene)
                
            

            nearest_obj = self.find_nearest(camera, data_store[0].object_list)
        

            self.center_obj(camera, nearest_obj)

            # add in offset percentage
            # self.offset(scene, camera, 50)
            
            value, percent = self.get_raycast_percentage(scene, camera, nearest_obj, 40)

            if value == False:
                    loop_count -= 1
                    value = True
            else:
                    
                    filename = f'{str(file_prefix)}-{str(loop_count)}.{file_format.lower()}'
                
                    bpy.context.scene.render.filepath = os.path.join(f'{filepath}/', filename)
                    bpy.ops.render.render(write_still=True)

                    #loop through objects instead
                    objects, data = self.get_raycast_percentages(scene, camera, self.objs, 30)
                    #loop through objects instead
                    scene_labels = self.get_cordinates(scene, camera, objects, filename)
            
                    
                    yield scene_labels

            loop_count += 1
            