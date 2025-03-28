class Pin:
    def __init__(self, id, name):
        self.id = id
        self.name = name

OLED_SPI_MOSI = Pin(11, "OLED_SPI_MOSI")
OLED_SPI_SCK = Pin(10, "OLED_SPI_SCK")
OLED_RST = Pin(12, "OLED_RST")
OLED_SPI_DC = Pin(8, "OLED_SPI_DC")
OLED_SPI_CS = Pin(9, "OLED_SPI_CS")
ONBOARD_LED = Pin("LED", "ONBOARD_LED")

BUTTON_DMX_UP = Pin(26, "BUTTON_DMX_UP")
BUTTON_DMX_DOWN = Pin(27, "BUTTON_DMX_DOWN")
BUTTON_SOUND_UP = Pin(21, "BUTTON_SOUND_UP")
BUTTON_SOUND_DOWN = Pin(20, "BUTTON_SOUND_DOWN")
BUTTON_SOUND_PLAY = Pin(3, "BUTTON_SOUND_PLAY")
BUTTON_SOUND_STOP = Pin(2, "BUTTON_SOUND_STOP")

AUDIO_UART = 0
DMX_UART = 1
