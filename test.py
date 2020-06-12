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
     


# god this is awful please fix
for count, item in  reversed(list(enumerate(scene.my_collection))):
    if item.name.startswith(str(i)):
        scene.my_collection.remove(count)

for count, item in  reversed(list(enumerate(scene.my_idname))):
    if item.value == i:

        scene.my_idname.remove(count)

# delete from dictr
if i in obj_collection:
    del obj_collection[i]

for items in scene.my_idname:
    print(items, "items in scene")