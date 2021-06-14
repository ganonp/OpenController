import utime
from machine import ADC, Timer, Pin, UART
from AnalogSensor import AnalogSensor
import ujson
import sys
import select
import micropython

micropython.alloc_emergency_exception_buf(100)

config = {}

with open("""/config.json""") as data_file:
    config = ujson.load(data_file)

serial_no = config["serial_no"]
num_sensors = config["no_channels"]

analog_sensors = {}

for v in config["channels"].values():
    analog_sensor = AnalogSensor(v)
    analog_sensors[str(analog_sensor.index)] = analog_sensor

led = Pin(25, Pin.OUT)
led.on()

p1 = Pin(5, Pin.IN, pull=Pin.PULL_DOWN)

command = '12345'
channel = '-1'

poll = select.poll()
poll.register(sys.stdin, select.POLLIN)


def interrupt_handler():
    global poll, command, channel
    led.on()
    command = str(poll.poll()[0][0].read(4))
    if command == 'init':
        print(config)
    elif command == 'data':
        channel = str(poll.poll()[0][0].read(1))
        print(analog_sensors[channel].response_dict)


lbo = p1.irq(handler=lambda pin: interrupt_handler(), trigger=Pin.IRQ_RISING)

timer = Timer()


def loop():
    for sensor in analog_sensors.values():
        sensor.add_value()
        sensor.update_response_dict()
    led.toggle()
    utime.sleep(.1)


timer.init(period=500, mode=Timer.PERIODIC, callback=lambda k: loop())
