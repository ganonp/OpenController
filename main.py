import utime
from machine import ADC, Pin, disable_irq, enable_irq
from AnalogSensor import AnalogSensor
from Pump import Pump
import ujson
import sys
import select
import micropython

micropython.alloc_emergency_exception_buf(100)

led = Pin(25, Pin.OUT)
led.on()

with open("""/serial_no.json""") as serial_json_file:
    serial_json = ujson.load(serial_json_file)

serial_no = serial_json["serial_no"]

poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

config = {}


def init():
    global config, io_components
    io_components = {}

    try:

        with open("""/config.json""") as data_file:
            config = ujson.load(data_file)

        for v in config["channels"]:
            if v['type'] == 'sensor':
                analog_sensor = AnalogSensor(v)
                io_components[str(analog_sensor.index)] = analog_sensor
            elif v['type'] == 'pump':
                pump = Pump(v)
                io_components[str(pump.index)] = pump
    except Exception as e:
        print(e)
        config = {}

    return io_components


def loop():
    global poll, io_components, led, serial_no
    command = ''
    try:
        command = str(poll.poll(200)[0][0].read(4))
    except Exception as e:
        command = ''
    finally:
        if command == 'data':
            channel = str(poll.poll()[0][0].read(1))
            print(io_components[str(channel)].response_dict)
        elif command == 'init':
            print(serial_no)
            new_config = (str(poll.poll()[0][0].readline())).strip()
            try:
                with open("""/config.json""", 'w') as data_file:
                    ujson.dump(ujson.loads(new_config), data_file)
            except Exception as e:
                print(e)
            io_components = init()
        elif command == 'stat':
            channel = str(poll.poll()[0][0].read(1))
            state = (str(poll.poll()[0][0].readline())).strip()
            print(str(io_components[channel].set_state(state)))

        for sensor in io_components.values():
            if sensor.type == 'sensor':
                sensor.add_value()
                sensor.update_response_dict()
        led.toggle()


io_components = init()

while True:
    loop()
