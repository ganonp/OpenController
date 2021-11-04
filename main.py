from machine import ADC, Pin
from AnalogSensor import AnalogSensor
from ACAnalogSensor import ACAnalogSensor
from Pump import Pump
import ujson
import sys
import select
import micropython

from Relay import Relay

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
            elif v['type'] == 'acsensor':
                analog_sensor = ACAnalogSensor(v)
                io_components[str(analog_sensor.index)] = analog_sensor
            elif v['type'] == 'pump':
                pump = Pump(v)
                io_components[str(pump.index)] = pump
            elif v['type'] == 'relay':
                relay = Relay(v)
                io_components[str(relay.index)] = relay
    except Exception as e:
        print(e)
        config = {}

    return io_components


def loop():
    global poll, io_components, led, serial_no
    command = ''
    try:
        command = (str(poll.poll(200)[0][0].readline())).strip()
        command_json = ujson.loads(command)
    except Exception as e:
        command_json = {}
    finally:
        try:
            if 'command' in command_json.keys():
                command = command_json['command']
                if command == 'data':
                    channel = command_json['channel']
                    print(io_components[str(channel)].response_dict)
                elif command == 'serial':
                    print(serial_no)
                elif command == 'init':
                    new_config = command_json['config']
                    try:
                        with open("""/config.json""", 'w') as data_file:
                            ujson.dump(new_config, data_file)
                    except Exception as e:
                        print(e)
                    io_components = init()
                elif command == 'state':
                    channel = command_json['channel']
                    state = command_json['state']
                    print(str(io_components[channel].set_state(state)))
        except Exception as e:
            print(e)
        finally:
            for sensor in io_components.values():
                if sensor.type == 'sensor' or sensor.type == 'acsensor':
                    sensor.add_value()
                    sensor.update_response_dict()
            led.toggle()


io_components = init()

while True:
    loop()
