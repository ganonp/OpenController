from machine import Pin
import ujson


class Relay:

    def __init__(self, data):
        self.index = str(data["index"])
        self.serial_no = data["serial_no"]
        self.gpio = Pin(int(data["gpio"]), Pin.OUT)
        self.gpio.off()
        self.type = data["type"]
        self.state = "off"

        self.response_dict = {"serial_no": str(self.serial_no), "index": str(self.index), "type": self.type,
                              "state": "off"}

    def set_state(self, state):
        if self.state != state:
            if state == "on":
                self.turn_on()
            elif state == "off":
                self.turn_off()

        return self.response_dict

    def turn_on(self):
        self.gpio.on()
        self.state = "on"
        self.update_response_dict("on")

    def turn_off(self):
        self.gpio.off()
        self.state = "off"
        self.update_response_dict("off")

    def update_response_dict(self, state):
        self.response_dict["state"] = state
