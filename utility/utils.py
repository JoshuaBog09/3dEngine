import numpy as np
import math 

def transform_V1(coordinates, angles):
        """
        
        """
        transform_x = np.array([[1,0,0],[0,math.cos(angles[0]),math.sin(angles[0])],[0,-math.sin(angles[0]),math.cos(angles[0])]])
        transform_y = np.array([[math.cos(angles[1]),0,-math.sin(angles[1])],[0,1,0],[math.sin(angles[1]),0,math.cos(angles[1])]])
        transform_z = np.array([[math.cos(angles[2]),math.sin(angles[2]),0],[-math.sin(angles[2]),math.cos(angles[2]),0],[0,0,1]])
        transform = transform_x @ transform_y @ transform_z
        
        return np.matmul(coordinates, transform)

def transform_V2(coordinates, angles):
        """
        
        """
        transform_x = np.array([[1,0,0],[0,math.cos(angles[0]),math.sin(angles[0])],[0,-math.sin(angles[0]),math.cos(angles[0])]])
        transform_y = np.array([[math.cos(angles[1]),0,-math.sin(angles[1])],[0,1,0],[math.sin(angles[1]),0,math.cos(angles[1])]])
        transform_z = np.array([[math.cos(angles[2]),math.sin(angles[2]),0],[-math.sin(angles[2]),math.cos(angles[2]),0],[0,0,1]])
        transform = transform_z @ transform_y @ transform_x
        
        return np.matmul(coordinates, transform)