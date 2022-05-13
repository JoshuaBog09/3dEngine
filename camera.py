class Camera():

    def __init__(self, x:float = 0, y:float = 0, z:float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

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

    def __repr__(self) -> str:
        return f"Camera({self.x},{self.y},{self.z})"
    def __str__(self) -> str:
        return f"Camera object -> ability for movement"