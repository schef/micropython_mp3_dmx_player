import asyncio
import time
from common_pins import DMX_UART
from dmx import DMXController

dmx = None

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class ColorPar:
    def __init__(self, dim, color, strobe = 0):
        self.dim = dim
        self.color = color
        self.strobe = strobe

class Light:
    def __init__(self, w, c):
        self.w = w
        self.c = c

COLORS = {
    "red": Color(255, 0, 0),
    "green": Color(0, 255, 0),
    "blue": Color(0, 0, 255),
    "white": Color(255, 255, 255),
    "yellow": Color(255, 255, 0),
    "cyan": Color(0, 255, 255),
    "magenta": Color(255, 0, 255),
    "orange": Color(255, 128, 0),
    "purple": Color(128, 0, 128),
    "pink": Color(255, 0, 180),
    "lime": Color(191, 255, 0),
    "teal": Color(0, 128, 128),
    "violet": Color(238, 130, 238),
    "indigo": Color(75, 0, 130),
    "brown": Color(139, 69, 19),
    "gray": Color(128, 128, 128),
}

SCENES = {
    1: [Light(0, 0), Light(0, 0), ColorPar(0, COLORS["red"]), ColorPar(0, COLORS["red"])],
    2: [Light(128, 128), Light(128, 128), ColorPar(0, COLORS["red"]), ColorPar(0, COLORS["red"])],
    3: [Light(128, 64), Light(128, 64), ColorPar(255, COLORS["brown"]), ColorPar(255, COLORS["brown"])],
    4: [Light(128, 64), Light(128, 64), ColorPar(128, COLORS["blue"]), ColorPar(128, COLORS["blue"])],
    5: [Light(64, 32), Light(64, 32), ColorPar(255, COLORS["orange"]), ColorPar(255, COLORS["orange"])],
    6: [Light(64, 32), Light(64, 32), ColorPar(255, COLORS["red"], 6), ColorPar(255, COLORS["blue"], 8)], # disco
    7: [Light(64, 32), Light(64, 32), ColorPar(255, COLORS["orange"]), ColorPar(255, COLORS["orange"])],
    8: [Light(64, 32), Light(64, 32), ColorPar(255, COLORS["red"], 6), ColorPar(255, COLORS["blue"], 8)], # disco
    9: [Light(64, 32), Light(64, 32), ColorPar(255, COLORS["orange"]), ColorPar(255, COLORS["orange"])],
    10: [Light(128, 0), Light(128, 0), ColorPar(255, COLORS["pink"]), ColorPar(255, COLORS["yellow"])],
    11: [Light(128, 0), Light(128, 0), ColorPar(255, COLORS["brown"]), ColorPar(255, COLORS["brown"])],
    12: [Light(0, 0), Light(0, 0), ColorPar(0, COLORS["red"]), ColorPar(0, COLORS["red"])],
    13: [Light(64, 0), Light(64, 0), ColorPar(64, COLORS["brown"]), ColorPar(64, COLORS["brown"])],
    14: [Light(64, 32), Light(64, 32), ColorPar(255, COLORS["orange"]), ColorPar(255, COLORS["orange"])],
    15: [Light(0, 64), Light(0, 64), ColorPar(128, COLORS["green"]), ColorPar(128, COLORS["green"])],
    16: [Light(64, 0), Light(64, 0), ColorPar(255, COLORS["brown"]), ColorPar(255, COLORS["brown"])],
    17: [Light(0, 0), Light(0, 0), ColorPar(0, COLORS["red"]), ColorPar(0, COLORS["red"])],
    18: [Light(128, 128), Light(128, 128), ColorPar(0, COLORS["red"]), ColorPar(0, COLORS["red"])],
}

def init():
    global dmx
    dmx = DMXController(uart_id=DMX_UART, tx_pin=4, rx_pin=5, direction_pin=13, num_channels=512)

def set_scene(num):
    scene = SCENES[num]
    light_1 = scene[0]
    light_2 = scene[1]
    color_1 = scene[2]
    color_2 = scene[3]
    dmx.set_channel(1, light_1.w)
    dmx.set_channel(2, light_1.c)
    dmx.set_channel(3, light_2.w)
    dmx.set_channel(4, light_2.c)
    dmx.set_channel(5, color_1.dim)
    dmx.set_channel(6, color_1.strobe)
    dmx.set_channel(7, color_1.color.r)
    dmx.set_channel(8, color_1.color.g)
    dmx.set_channel(9, color_1.color.b)
    dmx.set_channel(13, color_1.dim)
    dmx.set_channel(14, color_1.strobe)
    dmx.set_channel(15, color_2.color.r)
    dmx.set_channel(16, color_2.color.g)
    dmx.set_channel(17, color_2.color.b)

def test_scene(light_1, light_2, color_1, color_2):
    dmx.set_channel(1, light_1.w)
    dmx.set_channel(2, light_1.c)
    dmx.set_channel(3, light_2.w)
    dmx.set_channel(4, light_2.c)
    dmx.set_channel(5, color_1.dim)
    dmx.set_channel(7, color_1.color.r)
    dmx.set_channel(8, color_1.color.g)
    dmx.set_channel(9, color_1.color.b)
    dmx.set_channel(13, color_1.dim)
    dmx.set_channel(15, color_2.color.r)
    dmx.set_channel(16, color_2.color.g)
    dmx.set_channel(17, color_2.color.b)
    while True:
        dmx.send()
        time.sleep(0.1)

async def action():
    while True:
        await dmx.send()
        await asyncio.sleep(0.1)
