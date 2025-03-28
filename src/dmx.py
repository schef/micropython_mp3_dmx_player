import asyncio
from machine import UART, Pin
import utime

class DMXController:
    def __init__(self, uart_id=0, tx_pin=0, rx_pin=1, direction_pin=2, num_channels=512):
        self.uart_id = uart_id
        self.tx_pin_num = tx_pin
        self.direction = Pin(direction_pin, Pin.OUT)
        self.num_channels = num_channels
        self.dmx_data = bytearray(num_channels + 1)
        self.dmx_data[0] = 0
        self.uart = UART(uart_id, baudrate=250000, bits=8, parity=None, stop=2, tx=Pin(tx_pin), rx=Pin(rx_pin))

    def set_channel(self, channel, value):
        if 1 <= channel <= self.num_channels:
            self.dmx_data[channel] = value

    async def send(self):
        self.direction.value(1)

        self.uart.deinit()
        tx_pin = Pin(self.tx_pin_num, Pin.OUT)
        tx_pin.value(0)
        #utime.sleep_us(100)
        await asyncio.sleep_ms(200)
        tx_pin.value(1)
        #utime.sleep_us(12)
        await asyncio.sleep_ms(20)

        self.uart.init(baudrate=250000, bits=8, parity=None, stop=2, tx=Pin(self.tx_pin_num))
        self.uart.write(self.dmx_data)

        self.direction.value(0)

    def update_light(self, light_number, r, g, b, dimmer=255):
        base_channel = 1 + (light_number - 1) * 4
        self.set_channel(base_channel, dimmer)
        self.set_channel(base_channel + 1, r)
        self.set_channel(base_channel + 2, g)
        self.set_channel(base_channel + 3, b)

