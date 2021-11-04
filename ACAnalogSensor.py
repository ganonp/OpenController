from machine import ADC
import ujson
import utime


class ACAnalogSensor:

    def __init__(self, data):
        self.index = str(data["index"])
        self.serial_no = data["serial_no"]
        self.gpio = int(data["gpio"])
        self.type = data["type"]
        self.window = 10
        self.current_size = 0.0
        self.values = []
        self.adc = ADC(self.gpio)
        self.response_dict = {"serial_no": str(self.serial_no), "index": str(self.index), "type": self.type}
        bin = ujson.dumps(self.response_dict) + "\n"
        self.response_dict_binary = bytes(bin.encode('ascii'))

    def add_value(self):

        if self.current_size >= self.window:
            self.values.pop(0)

        x = 0
        for i in range(2000):
            temp = self.adc.read_u16()
            if temp > x:
                x = temp
            utime.sleep_us(10)

        self.values.append(x)

        if self.current_size < self.window:
            self.current_size = self.current_size + 1.0

    def get_average_value(self):
        x = 0.0
        for element in self.values:
            x = x + element
        return x / self.current_size

    def update_response_dict(self):
        self.response_dict["values"] = str(self.values)
        self.response_dict["averaged"] = str(self.get_average_value())
        bin = ujson.dumps(self.response_dict) + "\n"
        self.response_dict_binary = bytes(bin.encode('ascii'))
        return self.response_dict
