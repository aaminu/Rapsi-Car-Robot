from typing import Tuple, Union
from robots import Robot
from time import sleep

intFloat = Union[int, float]


class ObstacleAvoidanceBehaviourWithLeds:

    def __init__(self, the_robot: Robot) -> None:
        self.robot = the_robot
        self.speed = 50
        self.led_half = int(self.robot.leds.count/2)
        self.sense_color = (255, 50, 100)

        # Startup
        self.robot.leds.show_rainbow(range(self.robot.leds.count))
        self.robot.leds.show()
        sleep(0.5)
        self.robot.leds.clear()
        sleep(0.5)
        self.robot.leds.show_rainbow(range(self.robot.leds.count))
        self.robot.leds.show()
        sleep(0.5)
        self.robot.leds.clear()

    def get_speeds(self, nearest_distance: float) -> Tuple[intFloat, intFloat, int]:
        """Choose Speed based on Distance from a sensor"""
        if nearest_distance >= 100:
            nearest_speed = self.speed
            furthest_speed = self.speed
            delay = 100
        elif nearest_distance > 50:
            nearest_speed = self.speed
            furthest_speed = self.speed * 0.8
            delay = 100
        elif nearest_distance > 20:
            nearest_speed = self.speed
            furthest_speed = self.speed * 0.6
            delay = 100
        elif nearest_distance > 10:
            nearest_speed = -self.speed * 0.4
            furthest_speed = -self.speed
            delay = 100
        else:
            nearest_speed = -self.speed
            furthest_speed = -self.speed
            delay = 250

        return nearest_speed, furthest_speed, delay

    def distance_to_led_bar(self, distance: intFloat) -> int:
        """Convert distance to number of leds on the ledstrip"""
        inverted = max(0, 1.0 - distance /
                       100)  # invert distance monitoring and limit to 1m
        led_bar = int(round(inverted * self.led_half))
        return led_bar

    def display_state(self, left_distance: intFloat, right_distance: intFloat) -> None:
        # Clear first
        self.robot.leds.clear()
        # Left side
        led_bar = self.distance_to_led_bar(left_distance)
        self.robot.leds.show_rainbow(range(led_bar))
        # right
        led_bar = self.distance_to_led_bar(right_distance)
        start = self.robot.leds.count - led_bar
        self.robot.leds.show_rainbow(range(start, self.robot.leds.count))

        # show
        self.robot.leds.show()

    def run(self):
        while True:
            # get sensor reading
            left_distance = self.robot.left_distance_sensor.distance
            right_distance = self.robot.right_distance_sensor.distance
            print("Left: {:.2f}, Right{:.2f}".format(
                left_distance, right_distance))
            # Display this
            self.display_state(left_distance, right_distance)

            # get speed and set it
            nearest_speed, furthest_speed, delay = self.get_speeds(
                min(left_distance, right_distance))

            if left_distance < right_distance:
                self.robot.set_left(nearest_speed)
                self.robot.set_right(furthest_speed)
            else:
                self.robot.set_right(nearest_speed)
                self.robot.set_left(furthest_speed)

            # wait
            sleep(delay * 0.001)


if __name__ == "__main__":
    bot = Robot()
    behavior = ObstacleAvoidanceBehaviourWithLeds(bot)
    behavior.run()
