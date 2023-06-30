import numpy as np
import matplotlib.pyplot as plt

import math

import assets.baseshape as baseshape

class Ring(baseshape.BaseShape):

    def __init__(self, x: int = 0, y: int = 0, z: int = 0,
                  theta_x: float = 0, theta_y: float = 0, theta_z: float = 0,
                  radius: float = 10, tickness: float = 10, iteration: int = 10) -> None:
        super().__init__(x, y, z, theta_x, theta_y, theta_z)
        
        self.radius = radius
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

        for phi in np.linspace(0,2*math.pi,self.iter):
            self.unit.append([
                    self.radius*math.cos(phi),
                    self.radius*math.sin(phi),
                    + self.tickness // 2
                ])
            self.unit.append([
                    self.radius*math.cos(phi),
                    self.radius*math.sin(phi),
                    - self.tickness // 2
                ])
        self.unit = np.array(self.unit)
    
    def generate_triangles(self):
        self.triangles = []
        for i in range(self.iter - 1):
            self.triangles.append(((i*2) + 0, (i*2) + 1, (i*2) + 2))
            self.triangles.append(((i*2) + 1, (i*2) + 2, (i*2) + 3))
        self.triangles = np.array(self.triangles, dtype=np.uint16) % (self.iter*2)


class RingT(baseshape.BaseShape):

    def __init__(self, x: int = 0, y: int = 0, z: int = 0,
                  theta_x: float = 0, theta_y: float = 0, theta_z: float = 0,
                  radius_inner: float = 10, radius_outer: float = 20, tickness: float = 10,
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

        for phi in np.linspace(0,2*math.pi,self.iter):
            self.unit.append([
                    self.inner*math.cos(phi),
                    self.inner*math.sin(phi),
                    + self.tickness // 2
                ])
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
            self.unit.append([
                    self.inner*math.cos(phi),
                    self.inner*math.sin(phi),
                    - self.tickness // 2
                ])
        self.unit = np.array(self.unit)
    
    def generate_triangles(self):
        self.triangles = []
        for i in range(self.iter - 1):
            for j in range(4):
                self.triangles.append(((i*4) + (0 + j)%3, (i*4) + 1 + j%3 + 2 * (j//3), (i*4) + 4 + j))
                self.triangles.append(((i*4) + 1 + j, (i*4) + 4 + j, (i*4) + (5 + j)%8))
        self.triangles = np.array(self.triangles, dtype=np.uint16) % (self.iter*4)


class RingBevel(baseshape.BaseShape):

    def __init__(self, x: int = 0, y: int = 0, z: int = 0,
                  theta_x: float = 0, theta_y: float = 0, theta_z: float = 0,
                  radius_inner: float = 50, radius_outer: float = 10, tickness: float = 10,
                  iteration: int = 10, bevel_amount: int = 0, bevel_tickness:int = 0) -> None:
        super().__init__(x, y, z, theta_x, theta_y, theta_z)
        
        self.inner = radius_inner
        self.outer = radius_outer
        self.iter = iteration

        self.tickness = tickness
        
        self.bevel_amount = bevel_amount + 2
        self.bevel_tickness = bevel_tickness


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

        bevel_tickness_level = np.sin(np.linspace(0, math.pi, self.bevel_amount, endpoint=True)) * self.bevel_tickness

        for phi in np.linspace(0,2*math.pi,self.iter):
            for idx, t_level in enumerate(np.linspace(- self.tickness // 2, + self.tickness // 2, 
                                                 self.bevel_amount, endpoint=True)):
                self.unit.append([
                        (self.outer + bevel_tickness_level[idx])*math.cos(phi),
                        (self.outer + bevel_tickness_level[idx])*math.sin(phi),
                        t_level
                    ])
        self.unit = np.array(self.unit)
    
    def generate_triangles(self):
        self.triangles = []
        for i in range(self.iter - 1):
            for j in range(self.bevel_amount - 1):
                self.triangles.append((
                    (i*self.bevel_amount) + 0 + j,
                    (i*self.bevel_amount) + 1 + j,
                    (i*self.bevel_amount) + (0 + self.bevel_amount + j)))
                self.triangles.append((
                    (i*self.bevel_amount) + 1 + j,
                    (i*self.bevel_amount) + (0 + self.bevel_amount + j),
                    (i*self.bevel_amount) + (1 + self.bevel_amount + j))) 
        self.triangles = np.array(self.triangles, dtype=np.uint16) % (self.iter*self.bevel_amount)


class RingBevelT(baseshape.BaseShape):

    def __init__(self, x: int = 0, y: int = 0, z: int = 0,
                  theta_x: float = 0, theta_y: float = 0, theta_z: float = 0,
                  radius_inner: float = 50, radius_outer: float = 10, tickness: float = 10,
                  iteration: int = 10, bevel_amount: int = 0, bevel_tickness:int = 0) -> None:
        super().__init__(x, y, z, theta_x, theta_y, theta_z)
        
        self.inner = radius_inner
        self.outer = radius_outer
        self.iter = iteration

        self.tickness = tickness
        
        self.bevel_amount = bevel_amount + 2
        self.bevel_tickness = bevel_tickness


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

        bevel_tickness_level = np.sin(np.linspace(0, math.pi, self.bevel_amount, endpoint=True)) * self.bevel_tickness

        for phi in np.linspace(0,2*math.pi,self.iter):
            self.unit.append([
                    self.inner*math.cos(phi),
                    self.inner*math.sin(phi),
                    - self.tickness // 2
                ])
            for idx, t_level in enumerate(np.linspace(- self.tickness // 2, + self.tickness // 2, 
                                                 self.bevel_amount, endpoint=True)):
                self.unit.append([
                        (self.outer + bevel_tickness_level[idx])*math.cos(phi),
                        (self.outer + bevel_tickness_level[idx])*math.sin(phi),
                        t_level
                    ])
            self.unit.append([
                    self.inner*math.cos(phi),
                    self.inner*math.sin(phi),
                    + self.tickness // 2
                ])
        self.unit = np.array(self.unit)
    
    def generate_triangles(self):
        
        self.triangles = []
        
        self.triangles.append((0, 1, 5))
        self.triangles.append((1, 5, 6))

        self.triangles.append((1, 2, 6))
        self.triangles.append((2, 6, 7))

        self.triangles.append((2, 3, 7))
        self.triangles.append((3, 7, 8))

        self.triangles.append((3, 4, 8))
        self.triangles.append((4, 8, 9))

        self.triangles.append((0, 5, 9))
        self.triangles.append((0, 4, 9))

        self.triangles = np.array(self.triangles, dtype=np.uint16) % (self.iter*(self.bevel_amount+2))


if __name__ == "__main__":
    pass