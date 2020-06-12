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
 
r = {0: {'name': 'cube', 'xyz_min': [0.0, 0.0, 0.0], 'xyz_max': [0.0, 0.0, 0.0], 'cutoff': [0.0, 0.0, 0.0]}, '0': {'objects': ["retarderd"]}}

print(r[0])