from robots import Robot
from time import sleep


class ObstacleAvoidance:

    def __init__(self, the_robot: Robot) -> None:
        self.robot = the_robot
        self.speed = 60

    def get_speeds(self, nearest_distance):
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

    def run(self):
        while True:
            # get sensor reading
            left_distance = self.robot.left_distance_sensor.distance
            right_distance = self.robot.right_distance_sensor.distance
            print("Left: {:.2f}, Right{:.2f}".format(
                left_distance, right_distance))

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
    behavior = ObstacleAvoidance(bot)
    behavior.run()
