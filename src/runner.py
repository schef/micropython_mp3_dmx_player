import asyncio
import common
import buttons
import leds
import music
import lights
import oled_display

async def process_time_measure(timeout=20):
    print("[RUNNER]: start process_time_measure")
    timestamp = common.get_millis()
    bigest = 0
    while True:
        await asyncio.sleep(0)
        timepassed = common.millis_passed(timestamp)
        if timepassed >= timeout:
            if timepassed > bigest:
                bigest = timepassed
            print("[RUNNER]: timeout warning %d ms with bigest %d" % (timepassed, bigest))
        timestamp = common.get_millis()

def init():
    print("[RUNNER]: init")

    buttons.init()
    buttons.action()
    leds.init()
    music.init()
    lights.init()
    oled_display.init()

async def main():
    init()
    tasks = []
    tasks.append(asyncio.create_task(common.loop_async("BUTTONS", buttons.action)))
    tasks.append(asyncio.create_task(common.loop_async("LEDS", leds.action)))
    tasks.append(asyncio.create_task(lights.action()))
    tasks.append(asyncio.create_task(process_time_measure()))
    for task in tasks:
        await task
    print("[RUNNER]: Error: loop task finished!")

def run():
    asyncio.run(main())
