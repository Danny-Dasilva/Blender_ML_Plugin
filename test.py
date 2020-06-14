# objs = {}

# def nested_set(dic, keys, value):
#     if value is not None:
        
#         for key in keys[:-1]:
            
            
#             dic = dic.setdefault(key, {})

#         #check for objs set
#         if keys[-1] == "objects":
#             b = dic.setdefault('objects', [])
#             if value not in b:
#                 b.append(value)
        
#         else:
#             dic[keys[-1]] = value

# def set_objs(d, key, name=None, objects=None, xyz_min=None, xyz_max=None, cutoff=None,):
   
#     nested_set(d, [key, "name"], name)
   

#     nested_set(d, [key,"objects"], objects)

#     nested_set(d, [key, "xyz_min"], xyz_max)
#     nested_set(d, [key, "xyz_max"], xyz_max)
#     nested_set(d, [key, "cutoff"], xyz_max)
#     return d

# r = set_objs(objs, 0, name="ahh", xyz_min=[0, 3, 2], xyz_max=[0, 4, 5])
# print(r)
# r = set_objs(objs, 1, xyz_min=[0, 3, 2], xyz_max=[0, 4, 5])
# print(r)
# r = set_objs(objs, 0, xyz_min=[0, 3, 2], xyz_max=[0, 4, 2])

# r = set_objs(objs, 0, objects="yee")
# print(r)
# r = set_objs(objs, 0, objects="yaw")



        






# # b = objs[0].setdefault('objects', [])

# # if val not in b:
# #     b.append(val)
# # print(objs)
 
# remove drawing
     
def batch_render_test(self, scene, image_count, filepath, file_format, file_prefix="render", loop_count = 0):
    
    scene_setup_steps = int(image_count)
    value = True
    ball_lst = self.objs[0]["objects"]
    ball_dict = self.objs

    while loop_count != image_count:

        camera = self.randomize_camera(scene)
        if self.enable_physics:
            self.randomize_objs(scene)
            
        if self.frames:
            self.increment_frames(scene)

        nearest_ball = self.find_nearest(camera, ball_lst)
      

        self.center_obj(camera, nearest_ball)

        # add in offset percentage
        # self.offset(scene, camera, 50)
        value, percent = self.get_raycast_percentage(scene, camera, nearest_ball, 40)
        if value == False:
                loop_count -= 1
                value = True
        else:
                
                filename = f'{str(file_prefix)}-{str(loop_count)}.{file_format.lower()}'
            
                bpy.context.scene.render.filepath = os.path.join(f'{filepath}/', filename)
                bpy.ops.render.render(write_still=True)

                objects, data = self.get_raycast_percentages(scene, camera, self.objs, 30)
                
                scene_labels = self.get_cordinates(scene, camera, objects, self.names_dict, filename)
          
                
                yield scene_labels

        loop_count += 1

for item in self.batch_render_test(image_count=6):
    print(item)