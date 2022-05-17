import numpy as np

import math

class Sphere():

    def __init__(self, x:int = 0, y:int = 0, z:int = 0, radius:int = 10, iteration:int = 10) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.r = radius
        self.iter = iteration
        self.generate_coordinates()
        self.generate_vertices()

    def generate_coordinates(self) -> None:
        self.coordinates = []
        for psi in np.linspace(0,2*math.pi,self.iter):
            for theta in np.linspace(0,math.pi,self.iter):
                self.coordinates.append([
                    self.r*math.cos(psi)*math.sin(theta) + self.x,
                    self.r*math.sin(psi)*math.sin(theta) + self.y,
                    self.r*math.cos(theta) + self.z
                ])
        self.coordinates = np.array(self.coordinates)

    def generate_vertices(self) -> None:
        self.vertices = []
        for i in range(self.iter):
            for j in range(self.iter - 1):
                self.vertices.append((j+(i*self.iter),j+1+(i*self.iter)))
                self.vertices.append((j+(i*self.iter),j+self.iter+(i*self.iter)))
                self.vertices.append((j+(i*self.iter),j+1+self.iter+(i*self.iter)))
        self.vertices = np.array(self.vertices) % self.iter**2 

    def set_state() -> None:
        pass 