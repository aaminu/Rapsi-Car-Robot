from typing import Union
import colorsys


class Leds:

    def __init__(self, motor_hat: object, output_pin: int, led_count: int) -> None:
        self._motor_hat = motor_hat
        self.count = led_count
        if (output_pin >= 0) and (output_pin <= 5):
            self._output_pin = output_pin
            self._motor_hat.setOutputConfig(output_pin, 3)
            self.initState = True
        else:
            self._output_pin = -1
            self.initState = False
            print("[Error]: Ledstrip intialization failed due to wrong pin selection")

    def is_valid(self, led_number: int) -> bool:
        return (led_number >= 0) and (led_number <= self.count)

    def set_one(self, led_number: int, color: tuple) -> None:
        if self.is_valid(led_number):
            self._motor_hat.setPixel(led_number, *color, Update=False)

    def set_range(self, range: Union[list, range], color: tuple) -> None:
        for led in range:
            self.set_one(led, color)

    def set_all(self, color: tuple) -> None:
        self._motor_hat.setAllPixels(*color, Update=False)

    def clear(self) -> None:
        # clears all without the need of calling show() method
        self._motor_hat.setAllPixels(0, 0, 0)

    def show(self) -> None:
        self._motor_hat.updatePixels()

    def show_rainbow(self, led_range: range):
        try:
            led_range = list(led_range)
            hue_step = 1.0/len(led_range)
            for index, led in enumerate(led_range):
                hue = hue_step * index
                rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.6)
                rgb = [int(c*255) for c in rgb]
                self.set_one(led, rgb)
        except:
            pass


# Testing Ledstrip:
if __name__ == "__main__":
    import time
    import piconzero as pz
    pz.init()
    output_pin = 5  # pin on the available picon zero output pin
    number_of_leds = 16  # chained two led strip together

    # Instantiate the led class
    leds = Leds(motor_hat=pz, output_pin=output_pin, led_count=number_of_leds)
    leds.show_rainbow(range(number_of_leds))
    leds.show()
    time.sleep(0.5)
    leds.clear()
    time.sleep(0.5)
    leds.show_rainbow(range(number_of_leds))
    leds.show()
    time.sleep(0.5)
    leds.clear()
