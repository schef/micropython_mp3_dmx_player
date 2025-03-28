from machine import Pin
from time import ticks_ms, sleep
import asyncio

last_millis = 0
millis_overflow_counter = 0
millis_overflow_value = 2 ** 30 - 1

def get_real_millis():
    return ticks_ms()

def get_millis():
    global last_millis, millis_overflow_counter
    millis = get_real_millis()
    if millis < last_millis:
        millis_overflow_counter += 1
    last_millis = millis
    return (millis_overflow_counter * millis_overflow_value) + millis

def millis_passed(timestamp):
    return get_millis() - timestamp

def get_seconds():
    return int(get_millis() / 1000)

def seconds_passed(timestamp):
    return get_seconds() - timestamp

def dump_func(pexit=False, timing=False, showarg=False):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            enter_string = "%s.%s <enter>" % (f.__globals__['__name__'], f.__name__)
            pexit_local = False
            if showarg:
                enter_string += ", <args[%s%s]>" % (args, kwargs)
            print(enter_string)
            timestamp = get_millis()
            if timing:
                pexit_local = True
            response = f(*args, **kwargs)
            exit_string = "%s <exit>" % (f.__name__)
            if timing:
                exit_string += ", <time[%d]>" % (millis_passed(timestamp))
            if pexit or pexit_local:
                print(exit_string)
            return response
        return wrapped
    return inner_decorator

def print_available_pins():
    print(dir(Pin.board))
    print(dir(Pin.cpu))

def create_output(pin):
    return Pin(pin, Pin.OUT)

def create_input(pin, pullup=None):
    if pullup == None:
        return Pin(pin, Pin.IN, None)
    if pullup:
        return Pin(pin, Pin.IN, Pin.PULL_UP)
    else:
        return Pin(pin, Pin.IN, Pin.PULL_DOWN)

def create_interrupt(pin, cb=None):
    interrupt_pin = create_input(pin)
    interrupt_pin.irq(trigger=Pin.IRQ_FALLING, handler=cb)
    return interrupt_pin

def test_out_pin(pin_name, reversed=False):
    outpin = create_output(pin_name)
    if reversed:
        outpin.on()
    else:
        outpin.off()
    sleep(0.2)
    if reversed:
        outpin.off()
    else:
        outpin.on()
    sleep(2)
    if reversed:
        outpin.on()
    else:
        outpin.off()

def test_in_pin(pin_name, pullup=None):
    inpin = create_input(pin_name, pullup=pullup)
    state = None
    while True:
        new_state = inpin.value()
        if new_state != state:
            state = new_state
            print(state)

async def loop_async(name, action, timeout=3):
    print("[%s]: start loop_async" % (name))
    bigest = 0
    while True:
        timestamp = get_millis()
        action()
        timepassed = millis_passed(timestamp)
        if timepassed >= timeout:
            if timepassed > bigest:
                bigest = timepassed
            print("[%s]: timeout warning %d ms with bigest %d" % (name, timepassed, bigest))
        await asyncio.sleep(0)
