from dataclasses import dataclass
import pygame as pg

@dataclass
class Colors:
    """ Datacontainer to keep track of various avalable colors """
    WHITE = (244, 243, 239)
    BLACK = (16, 16, 16)
    # sky = pg.Color('cornflowerblue')