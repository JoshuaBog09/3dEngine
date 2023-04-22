import math
import sys
import numpy as np
import pygame as pg

from camera import Camera
from assets.cube import Cube
from assets.sphere import Sphere

WHITE = (244, 243, 239)
BLACK = (16, 16, 16)

WIDTH = 800
HEIGHT = 800

RESOLUTION = (WIDTH,HEIGHT)
SCREEN = pg.display.set_mode(RESOLUTION)

FPS = 60

pg.display.set_caption("3D-Engine")


def draw_cube(coordinates_cube:list, coordinate_camera = np.array([0,0,0]), orientation_camera = np.array([0,0,0])):
    """
    Draw a cube given a set of coordinates
    """

    x_camera = coordinate_camera[0]   # left/right
    y_camera = coordinate_camera[1]   # forward/backword
    z_camera = coordinate_camera[2]   # up/down    

    theta_x_camera = orientation_camera[0]
    theta_y_camera = orientation_camera[1]
    theta_z_camera = orientation_camera[2]

    draw_scale = 2

    for coordinate in coordinates_cube:
        
        x_cube = coordinate[0]   # left/right
        y_cube = coordinate[1]   # forward/backword
        z_cube = coordinate[2]   # up/down

        delta_cameracube = np.array([x_cube-x_camera,y_cube-y_camera,z_cube-z_camera])

        transform_x = np.array([[1,0,0],[0,math.cos(theta_x_camera),math.sin(theta_x_camera)],[0,-math.sin(theta_x_camera),math.cos(theta_x_camera)]])
        transform_y = np.array([[math.cos(theta_y_camera),0,-math.sin(theta_y_camera)],[0,1,0],[math.sin(theta_y_camera),0,math.cos(theta_y_camera)]])
        transform_z = np.array([[math.cos(theta_z_camera),math.sin(theta_z_camera),0],[-math.sin(theta_z_camera),math.cos(theta_z_camera),0],[0,0,1]])
        transform = transform_x @ transform_y @ transform_z

        corner_nodes = np.matmul(transform, delta_cameracube)

        x = ((WIDTH // draw_scale) * corner_nodes[0]/corner_nodes[1]) + WIDTH // 2
        z = - ((HEIGHT // draw_scale) * corner_nodes[2]/corner_nodes[1]) + HEIGHT // 2
        y = corner_nodes[1]

        # or this (look into this)
        # x = ((WIDTH // 4) * corner_nodes[0]/corner_nodes[2]) + WIDTH // 2
        # y = ((HEIGHT // 4) * corner_nodes[1]/corner_nodes[2]) + HEIGHT // 2
        # z = corner_nodes[2]

        # print(f"{x=}")
        # print(f"{z=}")
        
        pg.draw.circle(SCREEN, WHITE, (x,z) , 100/y)


def drawcube(cube_obj, coordinate_camera = np.array([0,0,0]), orientation_camera = np.array([0,0,0]), rotate = np.array([0,0,0])):
    """
    Draw a cube given a set of coordinates
    [x: left/right, y: forward/backword, z: up/down]
    """    

    draw_scale = 2
    draw_depth = 50


    def transform(coordinates_cube, coordinate_camera, orientation_camera):
        
        delta_cameracube = (coordinates_cube - coordinate_camera)
        
        transform_x = np.array([[1,0,0],[0,math.cos(orientation_camera[0]),math.sin(orientation_camera[0])],[0,-math.sin(orientation_camera[0]),math.cos(orientation_camera[0])]])
        transform_y = np.array([[math.cos(orientation_camera[1]),0,-math.sin(orientation_camera[1])],[0,1,0],[math.sin(orientation_camera[1]),0,math.cos(orientation_camera[1])]])
        transform_z = np.array([[math.cos(orientation_camera[2]),math.sin(orientation_camera[2]),0],[-math.sin(orientation_camera[2]),math.cos(orientation_camera[2]),0],[0,0,1]])
        transform = transform_x @ transform_y @ transform_z
        
        return np.matmul(delta_cameracube, transform)
    
    def transform_rotate(coordinates, rotate):
        
        transform_x = np.array([[1,0,0],[0,math.cos(rotate[0]),math.sin(rotate[0])],[0,-math.sin(rotate[0]),math.cos(rotate[0])]])
        transform_y = np.array([[math.cos(rotate[1]),0,-math.sin(rotate[1])],[0,1,0],[math.sin(rotate[1]),0,math.cos(rotate[1])]])
        transform_z = np.array([[math.cos(rotate[2]),math.sin(rotate[2]),0],[-math.sin(rotate[2]),math.cos(rotate[2]),0],[0,0,1]])
        transform = transform_x @ transform_y @ transform_z
        
        return np.matmul(coordinates, transform)


    def project(corner_node):
        y = corner_node[1]
        if y > 0:
            x = ((WIDTH // draw_scale) * corner_node[0]/corner_node[1]) + WIDTH // 2
            z = - ((HEIGHT // draw_scale) * corner_node[2]/corner_node[1]) + HEIGHT // 2
        else:
            x = np.Infinity
            z = np.Infinity
        return np.array([x,y,z])


    def drawN(corner_node):

        x = corner_node[0]
        y = corner_node[1]
        z = corner_node[2]
        
        if y > 0:
            pg.draw.circle(SCREEN, WHITE, (x,z), draw_depth/y)

    
    def drawV(vertice_node):
        x1 = corner_nodes[vertice_node[0],0]
        y1 = corner_nodes[vertice_node[0],1] 
        z1 = corner_nodes[vertice_node[0],2]
        x2 = corner_nodes[vertice_node[1],0]
        y2 = corner_nodes[vertice_node[1],1]
        z2 = corner_nodes[vertice_node[1],2]

        if y1 > 0 and y2 > 0:
            pg.draw.line(SCREEN, WHITE, (x1,z1), (x2,z2))

    
    def drawT(triangle_node):
        x1 = corner_nodes[triangle_node[0],0]
        y1 = corner_nodes[triangle_node[0],1] 
        z1 = corner_nodes[triangle_node[0],2]
        x2 = corner_nodes[triangle_node[1],0]
        y2 = corner_nodes[triangle_node[1],1]
        z2 = corner_nodes[triangle_node[1],2]
        x3 = corner_nodes[triangle_node[2],0]
        y3 = corner_nodes[triangle_node[2],1]
        z3 = corner_nodes[triangle_node[2],2]

        if y1 >= 0 and y2 >= 0 and y3 >= 0:
            pg.draw.polygon(SCREEN, WHITE, ((x1,z1), (x2,z2), (x3, z3)), width= 1)

    
    try:
        coordinates = cube_obj.get_coordinates()
        coordinates = transform_rotate(coordinates, rotate)
        corner_nodes = np.apply_along_axis(project, -1, transform(coordinates, coordinate_camera, orientation_camera))
        np.apply_along_axis(drawN, -1, corner_nodes)
    except AttributeError:
        raise Exception(f".coordinates in {cube_obj.__class__} is empty")

    
    try:
        triangles_cube = cube_obj.get_triangles()
        np.apply_along_axis(drawT, -1, triangles_cube)
    except AttributeError:
        raise Exception(f".triangles in {cube_obj.__class__} is empty")
    
    # try:
    #     vertices_cube = cube_obj.vertices
    #     np.apply_along_axis(drawV, -1, vertices_cube)
    # except AttributeError:
    #     raise Exception(f".vertices in {cube_obj.__class__} is empty")


    # for corner_node in corner_nodes:

    #     x = corner_node[0]
    #     y = corner_node[1]
    #     z = corner_node[2]

    #     # print(f"{x=}")
    #     # print(f"{y=}")
    #     # print(f"{z=}")

    #     pg.draw.circle(SCREEN, WHITE, (x,z) , 100/y)
    
    # for vertice in vertices_cube:
    #     if corner_nodes[vertice[0],1] > 0 and corner_nodes[vertice[1],1] > 0:
    #         pg.draw.line(SCREEN, WHITE, (corner_nodes[vertice[0],0],corner_nodes[vertice[0],2]) , (corner_nodes[vertice[1],0],corner_nodes[vertice[1],2]))


def main():
    pg.init()

    run_state = True
    clock = pg.time.Clock()

    a, b, c = 0, 0, 0
    # q, w, e = 0, 0, 0

    camera = Camera(0,0,0)
    
    # cuboids = []
    # for i in range(5):
    #     for j in range(i):
    #         for k in range(i):
    #             cuboids.append(Cube(i*10, j*10, k*10, 10))
    #             cuboids[-1].initialize()
    # print(sys.getsizeof(cuboids))
    
    cuboid1 = Cube(0, 0, 0, 10)
    cuboid2 = Cube(20, 0, 0, 10)
    cuboid3 = Cube(-20, 0, 0, 10)
    cuboid4 = Cube(0, 0, 20, 10)
    cuboid5 = Cube(0, 0, -20, 10)
    element = Sphere(0,0,0,radius=5,iteration=10)
    element.initialize()
    cuboid1.initialize()
    cuboid2.initialize()
    cuboid3.initialize()
    cuboid4.initialize()
    cuboid5.initialize()

    while run_state:
        clock.tick(FPS)

        # Event handeling
        pg.event.pump()     # Flush event que
        
        # Mouse events
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                run_state = False
        # Key events
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            run_state = False
        if keys[pg.K_RIGHT]:
            camera.moveRight()
        if keys[pg.K_LEFT]:
            camera.moveLeft()
        if keys[pg.K_UP]:
            camera.moveForward()
        if keys[pg.K_DOWN]:
            camera.moveBackword()
        if keys[pg.K_SPACE]:
            camera.moveUp()
        if keys[pg.K_LSHIFT]:
            camera.moveDown()
        
        # main script

        SCREEN.fill(BLACK)
        
        a += math.pi / 256
        b += math.pi / 356
        c += math.pi / 156

        # q += 1
        # w += 1
        # e += 1

        #draw_cube(cube(100, 50, 100, 10), np.array([q,w,e]), np.array([a,b,c]))
        #draw_cube(cube(10, 10, 100, 10), np.array([q,w,e]), np.array([a,b,c]))
        # for cuboid in cuboids:
        #     drawcube(cuboid, np.array([camera.x, camera.y , camera.z]), np.array([0,0,0]) , np.array([a,b,c]))
        drawcube(element, np.array([camera.x, camera.y , camera.z]), np.array([0,0,0]), np.array([a,b,c]))
        drawcube(cuboid1, np.array([camera.x, camera.y , camera.z]), np.array([0,0,0]), np.array([a,b,c]))
        cuboid1.update(np.array([a,b,c]))
        drawcube(cuboid2, np.array([camera.x, camera.y , camera.z]), np.array([0,0,0]), np.array([a,b,c]))
        cuboid2.update(np.array([a, b, c]))
        drawcube(cuboid3, np.array([camera.x, camera.y , camera.z]), np.array([0,0,0]), np.array([a,b,c]))
        cuboid3.update(np.array([a, b, c]))
        drawcube(cuboid4, np.array([camera.x, camera.y , camera.z]), np.array([0,0,0]), np.array([a,b,c]))
        cuboid4.update(np.array([a, b, c]))
        drawcube(cuboid5, np.array([camera.x, camera.y , camera.z]), np.array([0,0,0]), np.array([a,b,c]))
        cuboid5.update(np.array([a, b, c]))

        # for i in range(15):
        #     for j in range(15):
        #         draw_cube(np.array(cube(10*i, 50, 10*j, 10)), np.array([camera.x, camera.y , camera.z]), np.array([a,b,c]))

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()