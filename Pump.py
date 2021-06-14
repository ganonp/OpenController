from machine import PWM, Pin
import ujson


class Pump:

    def __init__(self, data):
        self.index = data["index"]
        self.serial_no = data["serial_no"]
        self.en = Pin(data["en"], Pin.OUT)
        self.gpio0 = Pin(data["gpio0"], Pin.OUT)
        self.gpio1 = Pin(data["gpio1"], Pin.OUT)
        self.gpio0.on()
        self.type = data["type"]
        self.pwm = PWM(self.en)
        self.pwm.freq(100)
        self.state = "off"

        self.response_dict = {"serial_no": str(self.serial_no), "index": str(self.index), "type": self.type,
                              "state": "off"}

    def set_state(self, state):
        if state == "on":
            self.turn_on()
        elif state == "off":
            self.turn_off()

        return self.response_dict

    def turn_on(self):
        self.pwm.duty_u16(65025)
        self.state = "on"
        self.update_response_dict("on")

    def turn_off(self):
        self.pwm.duty_u16(0)
        self.state = "off"
        self.update_response_dict("off")

    def update_response_dict(self, state):
        self.response_dict["state"] = state
