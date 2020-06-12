objs = {}

def nested_set(dic, keys, value):
    if value is not None:
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
        dic[keys[-1]] = value

def set_objs(value, name=None, xyz_min=None, xyz_max=None):
   
    
    
    nested_set(objs, [value, "name"], name)
  
    nested_set(objs, [value,"xyz_min"], xyz_min)
    
    nested_set(objs, [value, "xyz_max"], xyz_max)
   
    return objs
r = set_objs(0, name="ahh", xyz_min=[0, 3, 2], xyz_max=[0, 4, 5])
print(r)
r = set_objs(1, xyz_min=[0, 3, 2], xyz_max=[0, 4, 5])
print(r)
r = set_objs(0, xyz_min=[0, 3, 2], xyz_max=[0, 4, 2])

print(r)

