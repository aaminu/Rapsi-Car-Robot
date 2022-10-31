from typing import Literal
from lib import piconzero as pz
from lib.hcsr04 import DistanceSensor
from enum import IntEnum
import atexit


class MotorDirection(IntEnum):
    FORWARD = 1
    BACKWARD = 2
    STOP = 3


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

    def convert_speed(self, speed: float) -> tuple[Literal[MotorDirection.FORWARD, MotorDirection.BACKWARD, MotorDirection.STOP], float]:
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

    def run(self, motor, mode, speed) -> None:
        """ Run function that determines direction """
        if mode == self.mvt.FORWARD:
            self._mh.setMotor(motor, speed)

        elif mode == self.mvt.BACKWARD:
            self._mh.setMotor(motor, -speed)

    def set_left(self, speed) -> None:
        """ Left motor control """
        mode, output_speed = self.convert_speed(speed)
        self.run(self.left_motor, mode, output_speed)

    def set_right(self, speed) -> None:
        """ Right motor control """
        mode, output_speed = self.convert_speed(speed)
        self.run(self.right_motor, mode, output_speed)

    def clean_up(self) -> None:
        """ Stop both motors, distance sensor and cleanup """
        self._mh.stop()
        self.left_distance_sensor.cleanup()
        self.right_distance_sensor.cleanup()
        self._mh.cleanup()
