import math
import sys
import numpy as np
import pygame as pg

from render.camera import Camera
from assets.cube import Cube
from assets.sphere import Sphere
from assets.ring import Ring, RingT, RingBevel, RingBevelT

import utility.utils as utils

import settings.colors as colors
import settings.screen as scr

RESOLUTION = (scr.WIDTH,scr.HEIGHT)
SCREEN = pg.display.set_mode(RESOLUTION)

pg.display.set_caption("3D-Engine")

def drawobject(obj: object, camera_obj: object, rotate = np.array([0,0,0])):
    """
    Draw a cube given a set of coordinates
    [x: left/right, y: forward/backword, z: up/down]
    """    

    draw_scale = 1
    draw_depth = 100

    def project(corner_node):
        y = corner_node[1]
        if y > 0:
            x = ((scr.WIDTH // draw_scale) * corner_node[0]/corner_node[1]) + scr.WIDTH // 2
            z = - ((scr.HEIGHT // draw_scale) * corner_node[2]/corner_node[1]) + scr.HEIGHT // 2
        else:
            x = np.Infinity
            z = np.Infinity
        return np.array([x,y,z])


    def drawN(corner_node):

        x = corner_node[0]
        y = corner_node[1]
        z = corner_node[2]
        
        if y > 0:
            pg.draw.circle(SCREEN, colors.WHITE, (x,z), draw_depth/y)

    
    def drawV(vertice_node):
        x1 = corner_nodes[vertice_node[0],0]
        y1 = corner_nodes[vertice_node[0],1] 
        z1 = corner_nodes[vertice_node[0],2]
        x2 = corner_nodes[vertice_node[1],0]
        y2 = corner_nodes[vertice_node[1],1]
        z2 = corner_nodes[vertice_node[1],2]

        if y1 > 0 and y2 > 0:
            pg.draw.line(SCREEN, colors.WHITE, (x1,z1), (x2,z2))

    
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
            pg.draw.polygon(SCREEN, colors.WHITE, ((x1,z1), (x2,z2), (x3, z3)), width= 1)

    
    try:
        vertex = obj.get_coordinates()
        vertex = utils.transform_V1(vertex, rotate)
        corner_nodes = np.apply_along_axis(project, -1, utils.transform_V1((vertex - camera_obj.get_position()), camera_obj.get_orientation()))
        np.apply_along_axis(drawN, -1, corner_nodes)
    except AttributeError:
        raise Exception(f".coordinates in {obj.__class__} is empty")

    
    try:
        triangles = obj.get_triangles()
        np.apply_along_axis(drawT, -1, triangles)
    except AttributeError:
        raise Exception(f".triangles in {obj.__class__} is empty")
    
    # try:
    #     vertices_cube = cube_obj.vertices
    #     np.apply_along_axis(drawV, -1, vertices_cube)
    # except AttributeError:
    #     raise Exception(f".vertices in {cube_obj.__class__} is empty")


def main():
    pg.init()

    run_state = True
    clock = pg.time.Clock()

    a, b, c = 0, 0, 0
    d, e, f = 0, 0, 0
    # q, w, e = 0, 0, 0

    camera = Camera(0,0,0)
    

    render_list = []
    render_list.append(Ring(0,0,0,0,0,0, radius=10))
    render_list[-1].initialize(False)

    while run_state:
        clock.tick(scr.FPS)

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

        SCREEN.fill(colors.BLACK)
        
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
            drawobject(obj, camera)
            obj.update(np.array([a, b, c]))


        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
    sys.exit()