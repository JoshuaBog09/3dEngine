import numpy as np

class Cube():
    
    def __init__(self, x:int = 0, y:int = 0, z:int = 0, size:int = 10) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        
    def initialize(self):
        self.generate_coordinates()
        self.generate_triangles()


    def generate_coordinates(self) -> None:
        self.coordinates = np.array((
            (self.x + self.size//2, self.y + self.size//2, self.z + self.size//2),     # [+1,+1,+1]    node: 0
            (self.x + self.size//2, self.y - self.size//2, self.z + self.size//2),     # [+1,-1,+1]    node: 1
            (self.x - self.size//2, self.y - self.size//2, self.z + self.size//2),     # [-1,-1,+1]    node: 2
            (self.x - self.size//2, self.y + self.size//2, self.z + self.size//2),     # [-1,+1,+1]    node: 3
            (self.x + self.size//2, self.y + self.size//2, self.z - self.size//2),     # [+1,+1,-1]    node: 4
            (self.x + self.size//2, self.y - self.size//2, self.z - self.size//2),     # [+1,-1,-1]    node: 5
            (self.x - self.size//2, self.y - self.size//2, self.z - self.size//2),     # [-1,-1,-1]    node: 6
            (self.x - self.size//2, self.y + self.size//2, self.z - self.size//2))     # [-1,+1,-1]    node: 7
            )
        
    def generate_triangles(self) -> None:
        self.triangles = np.array((
            (0, 4, 5),
            (0, 1, 5),
            (1, 5, 6),
            (1, 1, 6),
            (2, 3, 7),
            (2, 6, 7),
            (0, 3, 7),
            (0, 4, 7),
            (0, 1, 2),
            (0, 2, 3),
            (4, 5, 6),
            (4, 6, 7)
            )
        )
    
    def generate_vortices(self) -> None:
        self.vertices = np.array([(0,4),(0,3),(0,1),(7,4),(7,3),(7,6),(5,4),(5,6),(5,1),(2,3),(2,1),(2,6)])
    
    def get_coordinates(self) -> np.ndarray:
        return self.coordinates
    
    def get_triangles(self) -> np.ndarray:
        return self.triangles
    
    def set_state(self) -> None:
        pass

for i in range(0,2):
    for j in range(0,2):
        for k in range(0,2):
            print([i,j,k])

print(np.array([[i,j,k] for k in range(0,2) for j in range(0,2) for i in range(0,2)]))