import numpy as np

import math

class BaseShape():

    def __init__(self, x:int = 0, y:int = 0, z:int = 0, 
                 theta_x: float = 0, theta_y: float = 0, theta_z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

        self.theta_x = theta_x
        self.theta_y = theta_y
        self.theat_z = theta_z

        self.unit = None
        
        self.coordinates = None
        self.vertices = None
        self.triangles = None

        self.state: bool = None


    def transform(self, rotate=np.array([0,0,0])) -> None:
        
        transform_x = np.array([[1,0,0],[0,math.cos(rotate[0]),math.sin(rotate[0])],[0,-math.sin(rotate[0]),math.cos(rotate[0])]])
        transform_y = np.array([[math.cos(rotate[1]),0,-math.sin(rotate[1])],[0,1,0],[math.sin(rotate[1]),0,math.cos(rotate[1])]])
        transform_z = np.array([[math.cos(rotate[2]),math.sin(rotate[2]),0],[-math.sin(rotate[2]),math.cos(rotate[2]),0],[0,0,1]])
        transform = transform_x @ transform_y @ transform_z
        
        self.coordinates = np.matmul(self.unit, transform)

    def translate(self) -> None:
        self.coordinates += np.array([self.x, self.y, self.z])

    def get_coordinates(self) -> np.ndarray:
        return self.coordinates
    
    def get_triangles(self) -> np.ndarray:
        return self.triangles
    
    def get_vertices(self) -> np.ndarray:
        return self.vertices
    
    def get_state(self) -> None:
        pass

    def set_state(self) -> None:
        pass

    def get_position(self):
        return np.array([self.x, self.y, self.z])
    
    def get_orientation(self):
        return np.array([self.theta_x, self.theta_y, self.theat_z])