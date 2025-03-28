import asyncio
import time
from common_pins import DMX_UART
from dmx import DMXController

dmx = None

class Color:
    def __init__(self, r, g, b, dim=10):
        self.r = r
        self.g = g
        self.b = b
        self.dim = dim

    def as_tuple(self):
        return (self.r, self.g, self.b, self.dim)

COLORS = {
    "red": Color(255, 0, 0),
    "green": Color(0, 255, 0),
    "blue": Color(0, 0, 255),
    "white": Color(255, 255, 255),
    "yellow": Color(255, 255, 0),
    "cyan": Color(0, 255, 255),
    "magenta": Color(255, 0, 255),
    "orange": Color(255, 165, 0),
    "purple": Color(128, 0, 128),
    "pink": Color(255, 105, 180),
    "lime": Color(191, 255, 0),
    "teal": Color(0, 128, 128),
    "violet": Color(238, 130, 238),
    "indigo": Color(75, 0, 130),
    "brown": Color(139, 69, 19),
    "gray": Color(128, 128, 128),
}

SCENES = {
    1: [COLORS["red"], COLORS["red"], COLORS["red"], COLORS["red"]],
    2: [COLORS["green"], COLORS["green"], COLORS["green"], COLORS["green"]],
    3: [COLORS["blue"], COLORS["blue"], COLORS["blue"], COLORS["blue"]],
    4: [COLORS["brown"], COLORS["brown"], COLORS["brown"], COLORS["brown"]],
    5: [COLORS["indigo"], COLORS["indigo"], COLORS["indigo"], COLORS["indigo"]],
}

def init():
    global dmx
    dmx = DMXController(uart_id=DMX_UART, tx_pin=4, rx_pin=5, direction_pin=13, num_channels=512)

def set_scene(num):
    scene = SCENES[num]
    light_1 = scene[0]
    light_2 = scene[1]
    light_3 = scene[2]
    light_4 = scene[3]
    dmx.update_light(1, light_1.r, light_1.g, light_1.b, light_1.dim)
    dmx.update_light(2, light_2.r, light_2.g, light_2.b, light_2.dim)
    dmx.update_light(3, light_3.r, light_3.g, light_3.b, light_3.dim)
    dmx.update_light(4, light_4.r, light_4.g, light_4.b, light_4.dim)

def test_scene(light_1, light_2, light_3, light_4):
    dmx.update_light(1, light_1.r, light_1.g, light_1.b, light_1.dim)
    dmx.update_light(2, light_2.r, light_2.g, light_2.b, light_2.dim)
    dmx.update_light(3, light_3.r, light_3.g, light_3.b, light_3.dim)
    dmx.update_light(4, light_4.r, light_4.g, light_4.b, light_4.dim)
    while True:
        dmx.send()
        time.sleep(0.1)

def test_light(num, color):
    dmx.update_light(num, color.r, color.g, color.b, color.dim)
    while True:
        dmx.send()
        time.sleep(0.1)

async def action():
    while True:
        await dmx.send()
        await asyncio.sleep(0.1)
