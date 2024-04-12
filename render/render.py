import pygame as pg

import settings.screen as scr

class Screen():

    def __init__(self) -> None:
        self.WIDTH = scr.WIDTH
        self.HEIGHT = scr.HEIGHT

        RESOLUTION = (scr.WIDTH,scr.HEIGHT)
        self.SCREEN = pg.display.set_mode(RESOLUTION)
    
        pg.display.set_caption("3D-Engine")
    
    def eventloop():
        pass