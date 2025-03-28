import asyncio
import time
import common
import common_pins

leds = []

led_pins = [
    common_pins.ONBOARD_LED,
]

class Led:
    def __init__(self, id, name, active_high=False):
        self.output = common.create_output(id)
        self.active_high = active_high
        self.state = None
        self.set_state(0)
        self.name = name

    def set_state(self, state):
        if self.active_high:
            if state:
                self.output.off()
            else:
                self.output.on()
        else:
            if state:
                self.output.on()
            else:
                self.output.off()
        self.state = state

    def get_state(self):
        return self.state

def set_state_by_name(name, state):
    print("[LEDS]: set_state_by_name(%s, %s)" % (name, state))
    for led in leds:
        if led.name == name:
            led.set_state(state)

def get_state_by_name(name):
    for led in leds:
        if led.name == name:
            return led.state
    return None

def get_led_by_name(name):
    for led in leds:
        if led.name == name:
            return led
    return None

def test_leds():
    global leds
    leds = []
    init_leds()
    for led in leds:
        print("[LEDS]: testing %s" % (led.name))
        led.set_state(1)
        time.sleep_ms(1000)
        led.set_state(0)
        time.sleep_ms(1000)

def init_leds():
    for pin in led_pins:
        leds.append(Led(pin.id, pin.name))

def init():
    print("[LEDS]: init")
    init_leds()
    action()

def action():
    pass

def test():
    print("[LEDS]: test")
    init()
    while True:
        action()

def test_async():
    print("[LEDS]: test_async")
    init()
    asyncio.run(common.loop_async("LEDS", action))
