objs = {}

def nested_set(dic, keys, value):
    if value is not None:
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
        dic[keys[-1]] = value

def set_objs(d, value, name=None, xyz_min=None, xyz_max=None):
   
    nested_set(d, [value, "name"], name)
    nested_set(d, [value,"xyz_min"], xyz_min)
    nested_set(d, [value, "xyz_max"], xyz_max)
    return d

r = set_objs(objs, 0, name="ahh", xyz_min=[0, 3, 2], xyz_max=[0, 4, 5])
print(r)
r = set_objs(objs, 1, xyz_min=[0, 3, 2], xyz_max=[0, 4, 5])
print(r)
r = set_objs(objs, 0, xyz_min=[0, 3, 2], xyz_max=[0, 4, 2])

print(r)




############## append list 


d = {'b': ['a']}

val = 32


b = d.setdefault('b', [])

if val not in b:
    b.append(val)
print(d)
 
