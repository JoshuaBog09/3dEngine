import numpy as np
import utility.utils as utils

class Camera():

    def __init__(self, x:float = 0, y:float = 0, z:float = 0,
                 theta_x: float = 0, theta_y: float = 0, theta_z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

        self.theta_x = theta_x
        self.theta_y = theta_y
        self.theta_z = theta_z

    ## Position
    # effected by: Roll and Yaw
    def moveRight(self):
        
        movement = utils.transform_V2(np.array([1, 0 , 0]), -self.get_orientation())
        self.x += movement[0]
        self.y += movement[1]
        self.z += movement[2]
    def moveLeft(self):
        movement = utils.transform_V2(np.array([1, 0 , 0]), -self.get_orientation())
        self.x -= movement[0]
        self.y -= movement[1]
        self.z -= movement[2]
    
    # Effected by: Pitch and Yaw
    def moveForward(self):
        movement = utils.transform_V2(np.array([0, 1 , 0]), -self.get_orientation())
        self.x += movement[0]
        self.y += movement[1]
        self.z += movement[2]
    def moveBackward(self):
        movement = utils.transform_V2(np.array([0, 1 , 0]), -self.get_orientation())
        self.x -= movement[0]
        self.y -= movement[1]
        self.z -= movement[2]
    
    # effected by: Pitch and Roll
    def moveUp(self):
        movement = utils.transform_V2(np.array([0, 0 , 1]), -self.get_orientation())
        self.x += movement[0]
        self.y += movement[1]
        self.z += movement[2]
    def moveDown(self):
        movement = utils.transform_V2(np.array([0, 0 , 1]), -self.get_orientation())
        self.x -= movement[0]
        self.y -= movement[1]
        self.z -= movement[2]
    
    ## Angle changes
    def positivePitch(self):
        self.theta_x -= np.pi / 128
    def negativePitch(self):
        self.theta_x += np.pi / 128
    def positiveRoll(self):
        self.theta_y -= np.pi / 128
    def negativeRoll(self):
        self.theta_y += np.pi / 128
    def positiveYaw(self):
        self.theta_z -= np.pi / 128
    def negativeYaw(self):
        self.theta_z += np.pi / 128


    def get_position(self):
        return np.array([self.x, self.y, self.z])
    
    def get_orientation(self):
        return np.array([self.theta_x, self.theta_y, self.theta_z])

    def __repr__(self) -> str:
        return f"Camera({self.x},{self.y},{self.z})"
    def __str__(self) -> str:
        return f"Camera object -> ability for movement"