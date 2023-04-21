import numpy as np

import math

class Sphere():

    def __init__(self, x:int = 0, y:int = 0, z:int = 0, radius:int = 10, iteration:int = 10) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.r = radius
        self.iter = iteration
        self.state = False
        # self.coordinates = None
        # self.vertices = None
        # self.triangles = None

    def initialize(self):
        self.generate_coordinates()
        self.generate_triangles()

    def generate_coordinates(self):
        self.coordinates = []
        for psi in np.linspace(0,2*math.pi,self.iter):
            for theta in np.linspace(0,math.pi,self.iter):
                self.coordinates.append([
                    self.r*math.cos(psi)*math.sin(theta) + self.x,
                    self.r*math.sin(psi)*math.sin(theta) + self.y,
                    self.r*math.cos(theta) + self.z
                ])
        self.coordinates = np.array(self.coordinates)


    def generate_vertices(self) -> np.ndarray:
        self.vertices = []
        for i in range(self.iter):
            for j in range(self.iter - 1):
                self.vertices.append((j+(i*self.iter),j+1+(i*self.iter)))
                self.vertices.append((j+(i*self.iter),j+self.iter+(i*self.iter)))
                self.vertices.append((j+(i*self.iter),j+1+self.iter+(i*self.iter)))
        return np.array(self.vertices) % self.iter**2 

    def generate_triangles(self):
        self.triangles = []
        for i in range(self.iter):
            for j in range(self.iter - 1):
                self.triangles.append((j+(i*self.iter),j+self.iter+(i*self.iter),j+1+self.iter+(i*self.iter)))
                self.triangles.append((j+(i*self.iter),j+1+(i*self.iter),j+1+self.iter+(i*self.iter)))
        self.triangles = np.array(self.triangles, dtype=np.uint16) % self.iter**2  

    def get_coordinates(self) -> np.ndarray:
        return self.coordinates
    
    def get_triangles(self) -> np.ndarray:
        return self.triangles
    
    def set_state(self, arg:bool) -> None:
        self.state = not arg

    def get_state(self) -> bool:
        return self.state