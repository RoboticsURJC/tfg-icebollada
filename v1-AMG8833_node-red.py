# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example is for Raspberry Pi (Linux) only!
   It will not work on microcontrollers running CircuitPython!"""

import os
import math
import time
#import pygame

import numpy as np
import busio
import board

from scipy.interpolate import griddata

from colour import Color

import adafruit_amg88xx

i2c_bus = busio.I2C(board.SCL, board.SDA)

# low range of the sensor (this will be blue on the screen)
MINTEMP = 26.0

# high range of the sensor (this will be red on the screen)
MAXTEMP = 32.0

# how many color values we can have
COLORDEPTH = 1024

os.putenv("SDL_FBDEV", "/dev/fb1")
#pygame.init()
# initialize the sensor
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

# pylint: disable=invalid-slice-index
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]
# pylint: enable=invalid-slice-index

# sensor is an 8x8 grid so lets do a square
height = 240
width = 240

# the list of colors we can choose from
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))
# 
# a=[]
# for i in colors:
#     a.append(str(i))
#     
# print(a)

# create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

displayPixelWidth = width / 30
displayPixelHeight = height / 30

#lcd = pygame.display.set_mode((width, height))

#lcd.fill((255, 0, 0))

#pygame.display.update()
#pygame.mouse.set_visible(False)

#lcd.fill((0, 0, 0))
#pygame.display.update()
# some utility functions
def constrain(val, min_val, max_val):
    print(min(max_val, max(min_val, val)))
    return min(max_val, max(min_val, val))


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# let the sensor initialize
time.sleep(0.1)

# msg = ""
# c = 0
# for row in sensor.pixels:
#     c+=1
#     i = 0
#     # print(["{0:.1f}".format(temp) for temp in row])
#     for index in row:
#         i +=1
#         msg += "{0:.1f}".format(index)
#         if(c != 8 or i != 8):
#             msg += ","
# print(msg)     
    # read the pixels
pixels = []
for row in sensor.pixels:
    pixels = pixels + row

pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]

    # perform interpolation
bicubic = griddata(points, pixels, (grid_x, grid_y), method="cubic")
print(len(bicubic[0]))

m=""
c = 0
for row in bicubic:
    c+=1
    i=0
    for pixel in row:
        i+=1
        m += "{0:.1f}".format(pixel)
        if(c != 32 or i != 32):
            m += ","
#print(m)
# for ix, row in enumerate(bicubic):
#     for jx, pixel in enumerate(row):
#         print(pixel)
#         pygame.draw.rect(
#             lcd,
#             colors[constrain(int(pixel), 0, COLORDEPTH - 1)],
#             (
#                 displayPixelHeight * ix,
#                 displayPixelWidth * jx,
#                 displayPixelHeight,
#                 displayPixelWidth,
#             ),
#         )

# pygame.display.update()
