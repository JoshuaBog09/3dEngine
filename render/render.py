import pygame as pg
import numpy as np

import math
import json

from render.camera import Camera 

from settings.colors import Colors as colors
import utility.utils as utils

class Screen():

    def __init__(self) -> None:

        with open('settings/settings.json') as f:
            self.file = json.load(f)
        
        self.WIDTH = self.file["width"]
        self.HEIGHT = self.file["height"]
        self.FPS = self.file["fps"]

        RESOLUTION = (self.WIDTH,self.HEIGHT)
        self.SCREEN = pg.display.set_mode(RESOLUTION)
    
        pg.display.set_caption(self.file["title"])

        self.stack: list = []
    
    def run(self):

        pg.init()
        
        run_state = True
        clock = pg.time.Clock()

        camera = Camera(0,0,0)

        a, b, c = 0, 0, 0
        d, e, f = 0, 0, 0

        while run_state:
            clock.tick(self.FPS)

            # Event handling
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
                camera.moveBackward()
            if keys[pg.K_SPACE]:
                camera.moveUp()
            if keys[pg.K_LSHIFT]:
                camera.moveDown()
            
            # main script

            self.SCREEN.fill(colors.BLACK)

            ## Begin Objects

            a += math.pi / 256
            b += math.pi / 356
            c += math.pi / 156

            d -= math.pi / 256
            e -= math.pi / 356
            f -= math.pi / 156

            # q += 1
            # w += 1
            # e += 1

            for obj in self.stack:
                self.drawobject(obj, camera)
                obj.update(np.array([a, b, c]))

            ## End objects

            pg.display.flip()
            pg.display.update()
        
        pg.quit()


    def drawobject(self, obj: object, camera_obj: object, rotate = np.array([0,0,0])):
        """
        Draw a cube given a set of coordinates
        [x: left/right, y: forward/backword, z: up/down]
        """    

        draw_scale = 1
        draw_depth = 100

        def project(corner_node):
            y = corner_node[1]
            if y > 0:
                x = ((self.WIDTH // draw_scale) * corner_node[0]/corner_node[1]) + self.WIDTH // 2
                z = - ((self.HEIGHT // draw_scale) * corner_node[2]/corner_node[1]) + self.HEIGHT // 2
            else:
                x = np.Infinity
                z = np.Infinity
            return np.array([x,y,z])


        def drawN(corner_node):

            x = corner_node[0]
            y = corner_node[1]
            z = corner_node[2]
            
            if y > 0:
                pg.draw.circle(self.SCREEN, colors.WHITE, (x,z), draw_depth/y)

        
        def drawV(vertice_node):
            x1 = corner_nodes[vertice_node[0],0]
            y1 = corner_nodes[vertice_node[0],1] 
            z1 = corner_nodes[vertice_node[0],2]
            x2 = corner_nodes[vertice_node[1],0]
            y2 = corner_nodes[vertice_node[1],1]
            z2 = corner_nodes[vertice_node[1],2]

            if y1 > 0 and y2 > 0:
                pg.draw.line(self.SCREEN, colors.WHITE, (x1,z1), (x2,z2))

        
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
                pg.draw.polygon(self.SCREEN, colors.WHITE, ((x1,z1), (x2,z2), (x3, z3)), width= 1)

        
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
    
    def add_objects(self, item: object):
        self.stack.extend(item)