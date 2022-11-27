from time import sleep
from robots import Robot
import math


class CirclePanTiltBehavior:
    def __init__(self, robot: Robot, radius: int = 30) -> None:
        self.robot = robot
        self.current_time = 0
        self.frames_per_circle = 50
        # divide circle into radians
        self.radians_per_frame = (2 * math.pi)/self.frames_per_circle
        self.radius = radius

    def run(self):
        while True:
            frame_number = self.current_time % self.frames_per_circle
            frame_in_radian = frame_number * self.radians_per_frame

            # Draw Cirlce
            self.robot.set_pan(self.radius * math.cos(frame_in_radian))
            self.robot.set_tilt(self.radius * math.sin(frame_in_radian))

            sleep(0.05)
            self.current_time += 1


if __name__ == "__main__":
    bot = Robot()
    behavior = CirclePanTiltBehavior(bot)
    behavior.run()
