import utime
from machine import Timer, Pin, lightsleep
import ujson
import sys
import select
from Pump import Pump
import micropython

micropython.alloc_emergency_exception_buf(100)


with open("""/config.json""") as data_file:
    config = ujson.load(data_file)

serial_no = config["serial_no"]
num_pumps = config["no_channels"]

pumps = {}

for v in config["channels"].values():
    pump = Pump(v)
    pumps[str(pump.index)] = pump

led = Pin(25, Pin.OUT)
led.on()

p1 = Pin(5, Pin.IN, pull=Pin.PULL_DOWN)

poll = select.poll()
poll.register(sys.stdin, select.POLLIN)


def update_led():
    led.on()
    if list(pumps.values())[0].state == "on" or list(pumps.values())[1].state == "on":
        led.on()
    else:
        utime.sleep_ms(300)
        led.off()


command = '12345'
state = "off"
channel = '-1'


def interrupt_handler():
    global command, poll, channel, config, state, pumps
    led.on()

    command = str(poll.poll()[0][0].read(4))
    if command == 'init':
        print(str(config))
        
    elif command == 'stat':
        channel = str(poll.poll()[0][0].read(1))
        state = (str(poll.poll()[0][0].readline())).strip()
        print(str(pumps[channel].set_state(state)))
    # print("interrupt")
    # print(str(poll.poll()[0][0].read(1)))
    # print(str(poll.poll()[0][0].read(3)))
    # print(pumps[(str(poll.poll()[0][0].read(1)).strip())].set_state((str(poll.poll()[0][0].readline())).strip()))
    update_led()


lbo = p1.irq(handler=lambda pin: interrupt_handler(), trigger=Pin.IRQ_RISING)

timer = Timer()

timer.init(period=2000, mode=Timer.PERIODIC, callback=lambda k: update_led())

lightsleep()
