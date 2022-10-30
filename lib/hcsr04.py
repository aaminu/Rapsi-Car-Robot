
import RPi.GPIO as GPIO 
import time


class DistanceSensor:
    """ Distance Sensor HC-SR04 object class. This class provides an API for the distance sensor to be used on available GPIO pins."""

    def __init__(self, echo_pin:int, trigger_pin:int) -> None:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.echo = echo_pin
        self.trigger = trigger_pin


    @property #getter property 
    def distance(self) -> float:
        return self._getDistance()


    def cleanup(self) -> None:
        GPIO.cleanup()


    def _getDistance(self) -> float:
        """ 
        UltraSonic Function 
        _getDistance(). Returns the distance in cm to the nearest reflecting object
        """
        GPIO.setup(self.trigger, GPIO.OUT)

        # Send 10us pulse to trigger
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
        start = time.time()
        count=time.time()

        GPIO.setup(self.echo, GPIO.IN)
        while GPIO.input(self.echo)==0 and time.time()-count<0.1:
            start = time.time()
        count=time.time()
        stop=count
        while GPIO.input(self.echo)==1 and time.time()-count<0.1:
            stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34000

        # That was the distance there and back so halve the value
        distance = distance / 2
        return distance


# Testing Distance Sensors Purpose
if __name__ == "__main__":
    try:
        right_sensor = DistanceSensor(echo_pin=13, trigger_pin=15) #GPIO 27=13, 22=15
        left_sensor = DistanceSensor(echo_pin=38, trigger_pin=38) #Uses same pin for trig and echo
        while True:
            print("Left: {}, Right: {}".format(left_sensor.distance, right_sensor.distance))
            time.sleep(1)
    except KeyboardInterrupt:
        print()
    finally:
        right_sensor.cleanup()
        left_sensor.cleanup()