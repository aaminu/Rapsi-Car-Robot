from typing import Literal
from lib import piconzero as pz
from lib.hcsr04 import DistanceSensor
from lib.led_strip import Leds
from lib.servos import Servos
from enum import IntEnum
import atexit


class MotorDirection(IntEnum):
    FORWARD = 1
    BACKWARD = 2
    STOP = 3


directionEnum = Literal[MotorDirection.FORWARD,
                        MotorDirection.BACKWARD, MotorDirection.STOP]


class Robot:

    def __init__(self) -> None:

        # objects
        self._mh = pz
        self.mvt = MotorDirection

        # Set motor number
        self.left_motor = 0
        self.right_motor = 1

        # Setup distance sensors
        self.left_distance_sensor = DistanceSensor(echo_pin=38, trigger_pin=38)
        self.right_distance_sensor = DistanceSensor(
            echo_pin=13, trigger_pin=15)

        # ensure clean up stops when code exits
        atexit.register(self.clean_up)

        # initialize hat
        self._mh.init()

        # Place Ledstrip intialitzation after hat intialization to allow proper functionality
        self.leds = Leds(motor_hat=self._mh, output_pin=5, led_count=16)

        # servos
        self._pan = Servos(self._mh, 1, min_max_degree=(
            50, 150), start_position=103)
        self._tilt = Servos(self._mh, 0, min_max_degree=(
            55, 180), start_position=155)

    def convert_speed(self, speed: float) -> tuple[directionEnum, float]:
        """ Converts speeds and check moveement mode """
        # choose running mode
        mode = self.mvt.STOP
        if speed > 0:
            mode = self.mvt.FORWARD
        elif speed < 0:
            mode = self.mvt.BACKWARD

        # Convert speed
        output_speed = (abs(speed) * 127) // 100
        return mode, output_speed

    def run(self, motor: int, mode: directionEnum, speed: int) -> None:
        """ Run function that determines direction """
        if mode == self.mvt.FORWARD:
            self._mh.setMotor(motor, speed)

        elif mode == self.mvt.BACKWARD:
            self._mh.setMotor(motor, -speed)

    def set_left(self, speed: float) -> None:
        """ Left motor control """
        mode, output_speed = self.convert_speed(speed)
        self.run(self.left_motor, mode, output_speed)

    def set_right(self, speed: float) -> None:
        """ Right motor control """
        mode, output_speed = self.convert_speed(speed)
        self.run(self.right_motor, mode, output_speed)

    def set_pan(self, angle) -> None:
        """ Set pan angle for camera """
        self._pan.set_angle(angle)

    def set_tilt(self, angle) -> None:
        """ Set tilt angle for camera """
        self._tilt.set_angle(angle)

    def clean_up(self) -> None:
        """ Stop both motors, distance sensor and cleanup """
        self._mh.stop()
        self.left_distance_sensor.cleanup()
        self.right_distance_sensor.cleanup()
        self.leds.clear()
        self._pan.cleanup()
        self._tilt.cleanup()
        self._mh.cleanup()
