import math
import sys
import numpy as np
import pygame as pg

from render.camera import Camera
from render.render import Screen
from assets.cube import Cube
from assets.sphere import Sphere
from assets.ring import Ring, RingT, RingBevel, RingBevelT

import utility.utils as utils

def main():

    scr = Screen()

    render_list = []
    render_list.append(Sphere())
    render_list.append(Ring(0,0,0,0,0,0, radius=11))
    for i in render_list:
        i.initialize(False)

    scr.add_objects(render_list)

    scr.run()    


if __name__ == "__main__":
    main()
    sys.exit()