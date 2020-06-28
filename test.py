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
 
    

data_store = [Ml_Data_Store(i) for i in range(10)]


print(data_store[0])
