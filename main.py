import utime
from machine import ADC, Pin, disable_irq, enable_irq
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

# command = '12345'
# channel = '-1'

poll = select.poll()
poll.register(sys.stdin, select.POLLIN)
interrupt = False


def interrupt_handler():
    global interrupt
    led.on()
    interrupt = True


# lbo = p1.irq(handler=lambda pin: interrupt_handler(), trigger=Pin.IRQ_RISING)


def loop():
    global poll
    try:
        command = str(poll.poll(200)[0][0].read(4))
    except Exception as e:
        command = ''
    finally:
        if command == 'data':
            channel = str(poll.poll()[0][0].read(1))
            print(analog_sensors[channel].response_dict)
        if command == 'init':
            print(config)

    for sensor in analog_sensors.values():
        sensor.add_value()
        sensor.update_response_dict()
    led.toggle()
    # utime.sleep(.3)


while True:
    loop()

# timer.init(period=500, mode=Timer.PERIODIC, callback=lambda k: loop())
