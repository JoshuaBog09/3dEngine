import numpy as np

import math

import assets.baseshape as baseshape

class Ring(baseshape.BaseShape):

    def __init__(self, x: int = 0, y: int = 0, z: int = 0,
                  theta_x: float = 0, theta_y: float = 0, theta_z: float = 0,
                  radius_inner: float = 50, radius_outer: float = 10, tickness: float = 10,
                  iteration: int = 10) -> None:
        super().__init__(x, y, z, theta_x, theta_y, theta_z)
        
        self.inner = radius_inner
        self.outer = radius_outer
        self.iter = iteration

        self.tickness = tickness

    def initialize(self, orientation=True):
        self.generate_triangles()
        self.generate_unit()
        self.transform(self.get_orientation())
        self.translate()

    def update(self, rotate):
        self.transform(rotate)
        self.translate()

    def generate_unit(self):
        self.unit = []
        # for t_level in np.linspace(- self.tickness // 2, + self.tickness // 2, )
        for phi in np.linspace(0,2*math.pi,self.iter):
            self.unit.append([
                    self.outer*math.cos(phi),
                    self.outer*math.sin(phi),
                    + self.tickness // 2
                ])
            self.unit.append([
                    self.outer*math.cos(phi),
                    self.outer*math.sin(phi),
                    - self.tickness // 2
                ])
        self.unit = np.array(self.unit)
    
    def generate_triangles(self):
        self.triangles = []
        for i in range(self.iter - 1):
            self.triangles.append(((i*2) + 0, (i*2) + 1, (i*2) + 2))
            self.triangles.append(((i*2) + 1, (i*2) + 2, (i*2) + 3))
        self.triangles = np.array(self.triangles, dtype=np.uint16) % (self.iter*2)
        
class RingBevel(baseshape.BaseShape):

    def __init__(self, x: int = 0, y: int = 0, z: int = 0,
                  theta_x: float = 0, theta_y: float = 0, theta_z: float = 0,
                  radius_inner: float = 50, radius_outer: float = 10, tickness: float = 10,
                  iteration: int = 10) -> None:
        super().__init__(x, y, z, theta_x, theta_y, theta_z)
        
        self.inner = radius_inner
        self.outer = radius_outer
        self.iter = iteration

        self.tickness = tickness
        self.bevel = 1

    def initialize(self, orientation=True):
        self.generate_triangles()
        self.generate_unit()
        self.transform(self.get_orientation())
        self.translate()

    def update(self, rotate):
        self.transform(rotate)
        self.translate()

    def generate_unit(self):
        self.unit = []
        # for t_level in np.linspace(- self.tickness // 2, + self.tickness // 2, )
        for phi in np.linspace(0,2*math.pi,self.iter):
            self.unit.append([
                    self.outer*math.cos(phi),
                    self.outer*math.sin(phi),
                    + self.tickness // 2
                ])
            self.unit.append([
                    (self.outer + self.bevel)*math.cos(phi),
                    (self.outer + self.bevel)*math.sin(phi),
                    0
                ])
            self.unit.append([
                    self.outer*math.cos(phi),
                    self.outer*math.sin(phi),
                    - self.tickness // 2
                ])
        self.unit = np.array(self.unit)
    
    def generate_triangles(self):
        self.triangles = []
        for i in range(self.iter - 1):
            self.triangles.append(((i*3) + 0, (i*3) + 1, (i*3) + 3))
            self.triangles.append(((i*3) + 1, (i*3) + 3, (i*3) + 4))
            self.triangles.append(((i*3) + 1, (i*3) + 2, (i*3) + 4))
            self.triangles.append(((i*3) + 2, (i*3) + 4, (i*3) + 5))
        self.triangles = np.array(self.triangles, dtype=np.uint16) % (self.iter*3)