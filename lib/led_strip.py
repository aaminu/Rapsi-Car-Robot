from typing import Union
import colorsys


class Leds:
    
    def __init__(self, motor_hat: object,  led_count: int, output_pin: int = 5, output_mode: int=3,) -> None:
        """Initialization Class for WS2812B Leds

        Args:
            motor_hat (object): Motor
            led_count (int): Number of leds on the strip connected to the Pin (WS2812B)
            output_pin (int): Assigned Output pin on the hat
            output_mode (int): Assigned Output Mode on the Hat

        Notes: motor_hat should have the following methods available
            - setOutputConfig (output, value)
            - setPixel (Pixel, Red, Green, Blue, Update=True/False)
            - setAllPixels(Red, Green, Blue, Update=True/False)
            - updatePixels()
                
        """
        self._motor_hat = motor_hat
        self.count = led_count
        self._motor_hat.setOutputConfig(output_pin, output_mode)

        
    def _is_valid(self, led_number: int) -> bool:
        return (led_number >= 0) and (led_number <= self.count)

    def set_one(self, led_number: int, color: tuple) -> None:
        """ Set a single Led on the strip

        Args:
            led_number (int): _description_
            color (tuple): (Red, Green, Blue)
        
        Notes:
            - Call .show() on the led object for changes to reflect
        """
        if self._is_valid(led_number):
            self._motor_hat.setPixel(led_number, *color, Update=False)

    def set_range(self, range: Union[list, range], color: tuple) -> None:
        """Set a list of Led on the strip

        Args:
            range (Union[list, range]): List or range of Led to set on the strip
            color (tuple): (Red, Green, Blue)
        """
        for led in range:
            self.set_one(led, color)

    def set_all(self, color: tuple) -> None:
        """Set all the Leds on the strip

        Args:
            color (tuple): (Red, Green, Blue)
        """
        self._motor_hat.setAllPixels(*color, Update=False)

    def clear(self) -> None:
        """
        Clear all the set led. This turns off all the led on the strip
        """
        # clears all without the need of calling show() method
        self._motor_hat.setAllPixels(0, 0, 0)

    def show(self) -> None:
        """
        Update the status of the led after calling one of the set_*(..) methods
        """
        self._motor_hat.updatePixels()

    def show_rainbow(self, led_range: range):
        """Show a Rainbow on a number of led in the strip

        Args:
            led_range (range): Range of led to display the rainbow. The longer the range, the more colors shown
        """
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
