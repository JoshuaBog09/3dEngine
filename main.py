import math
import sys
import numpy as np
import pygame as pg

from camera import Camera
from assets.cube import Cube
from assets.sphere import Sphere
from assets.ring import Ring, RingT, RingBevel, RingBevelT

import utility.utils as utils

WHITE = (244, 243, 239)
BLACK = (16, 16, 16)

WIDTH = 800
HEIGHT = 800

RESOLUTION = (WIDTH,HEIGHT)
SCREEN = pg.display.set_mode(RESOLUTION)

FPS = 60

pg.display.set_caption("3D-Engine")

def drawcube(cube_obj: object, camera_obj: object, rotate = np.array([0,0,0])):
    """
    Draw a cube given a set of coordinates
    [x: left/right, y: forward/backword, z: up/down]
    """    

    draw_scale = 1
    draw_depth = 100

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
        coordinates = utils.transform_V1(coordinates, rotate)
        corner_nodes = np.apply_along_axis(project, -1, utils.transform_V1((coordinates - camera_obj.get_position()), camera_obj.get_orientation()))
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
    d, e, f = 0, 0, 0
    # q, w, e = 0, 0, 0

    camera = Camera(0,0,0)
    

    render_list = []

    for i in range(1):
        for j in range(1):
            for k in range(1):
                # render_list.append(RingBevel(i*10,j*10,k*10,0,0,0, bevel_amount=10,bevel_tickness=1))
                # render_list.append(Ring(i*10,j*10,k*10,0,0,0, radius=10))
                # render_list.append(RingT())
                render_list.append(RingBevelT(i*10,j*10,k*10,0,0,0, bevel_amount=1, bevel_tickness=1, radius_inner=5, radius_outer=7))
                render_list[-1].initialize(False)


    # cuboid1 = Cube(0, 0, 0, math.pi/4, math.pi/4, math.pi/4, size=10)
    
    # cuboid1.initialize()

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

        d -= math.pi / 256
        e -= math.pi / 356
        f -= math.pi / 156

        # q += 1
        # w += 1
        # e += 1

        for obj in render_list:
            drawcube(obj, camera)
            obj.update(np.array([a, b, c]))


        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()