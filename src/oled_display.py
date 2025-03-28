from machine import Pin, reset, SPI
import common_pins
from pico_oled_1_3_spi import OLED_1inch3
from writer import Writer
import font32

import buttons
import music
import lights

oled = None
spi_oled = None
wri = None

music_index = 1
light_index = 1

def init():
    global oled, spi_oled, wri
    print("[OLED]: init")
    spi_oled = SPI(1, 20_000_000, polarity = 0, phase = 0, sck = Pin(common_pins.OLED_SPI_SCK.id), mosi = Pin(common_pins.OLED_SPI_MOSI.id), miso = None)
    oled = OLED_1inch3(spi = spi_oled, dc = Pin(common_pins.OLED_SPI_DC.id, Pin.OUT), cs = Pin(common_pins.OLED_SPI_CS.id, Pin.OUT), rst = Pin(common_pins.OLED_RST.id, Pin.OUT))
    wri = Writer(oled, font32)
    buttons.register_on_state_change_callback(on_button_state_change_cb)
    handle_display()

def set_music_index(index):
    global music_index
    music_index = index
    if music_index > len(music.SONGS):
        music_index = len(music.SONGS)
    elif music_index < 1:
        music_index = 1

def set_light_index(index):
    global light_index
    light_index = index
    if light_index > len(lights.SCENES):
        light_index = len(lights.SCENES)
    elif light_index < 1:
        light_index = 1

def handle_display():
    oled.fill(0x0000)
    oled.text("MUSIC", 4, 10, 0xFFFF)
    oled.text("LIGHT", 85, 10, 0xFFFF)
    wri.set_textpos(oled, 30, 4)
    show_music_index = sorted(list(music.SONGS.keys()))[music_index - 1]
    wri.printstring(f"{show_music_index:02}")
    wri.set_textpos(oled, 30, 85)
    wri.printstring(f"{light_index:02}")
    oled.show()

def on_button_state_change_cb(name, state):
    if state:
        if name == common_pins.BUTTON_DMX_UP.name:
            set_light_index(light_index + 1)
            handle_display()
            lights.set_scene(light_index)
        elif name == common_pins.BUTTON_DMX_DOWN.name:
            set_light_index(light_index - 1)
            handle_display()
            lights.set_scene(light_index)
        elif name == common_pins.BUTTON_SOUND_UP.name:
            set_music_index(music_index + 1)
            handle_display()
        elif name == common_pins.BUTTON_SOUND_DOWN.name:
            set_music_index(music_index - 1)
            handle_display()
        elif name == common_pins.BUTTON_SOUND_PLAY.name:
            music.play_by_index(music_index)
        elif name == common_pins.BUTTON_SOUND_STOP.name:
            music.stop()

