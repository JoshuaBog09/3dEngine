import numpy as np

class Camera():

    def __init__(self, x:float = 0, y:float = 0, z:float = 0,
                 theta_x: float = 0, theta_y: float = 0, theta_z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

        self.theta_x = theta_x
        self.theta_y = theta_y
        self.theat_z = theta_z

    def moveRight(self):
        self.x += 1
    def moveLeft(self):
        self.x -= 1
    def moveForward(self):
        self.y += 1
    def moveBackword(self):
        self.y -= 1
    def moveUp(self):
        self.z += 1
    def moveDown(self):
        self.z -= 1

    def get_position(self):
        return np.array([self.x, self.y, self.z])
    
    def get_orientation(self):
        return np.array([self.theta_x, self.theta_y, self.theat_z])

    def __repr__(self) -> str:
        return f"Camera({self.x},{self.y},{self.z})"
    def __str__(self) -> str:
        return f"Camera object -> ability for movement"