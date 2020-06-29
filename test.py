from dataclasses import dataclass, field
from typing import List
@dataclass
class Ml_Data_Store:
    

    tag: int
    name: str = None
    
    enable_physics: bool = False
    obj_xyz_max: tuple = (0, 0, 0)
    obj_xyz_min: tuple = (0, 0, 0)
    toggle_rotate: bool = True
    cutoff: float = 30

    object_list: List[int] = field(default_factory=list)
    # maybe getter and setter for lists
    
    def add(self, value):
        self.object_list.append(value)

    def update_values(self, **kwargs):
        self.__dict__.update(kwargs)
   
 
    

data_store = [Ml_Data_Store(i) for i in range(10)]


print(data_store[0])

data_store[0].update_values(obj_xyz_max=(3, 3, 3))

print(data_store[0])