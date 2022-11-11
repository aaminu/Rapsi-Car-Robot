class Servos:

    def __init__(self, motor_hat: object, output_pin: int, *, min_max_degree: tuple = (0, 180), start_position: int = 90) -> None:
        self._motor_hat = motor_hat
        self.min_angle = min_max_degree[0] if min_max_degree[0] >= 0 else 0
        self.max_angle = min_max_degree[1] if min_max_degree[1] <= 0 else 180
        self.start_position = start_position
        self.initState = False
        self._output_pin = -1
        if (output_pin >= 0) and (output_pin <= 5):
            self._output_pin = output_pin
            self._motor_hat.setOutputConfig(output_pin, 2)
            self.initState = True
        else:
            print("[Error]: Servo intialization failed due to wrong pin selection")

    def set_angle(self, angle: int):
        if self.initState and (self.min_angle <= angle and self.max_angle >= angle):
            self._motor_hat.setOutput(self._output_pin, angle)
        else:
            print("[Error]: Angle outside allowed region")

    def cleanup(self):
        if self.initState and (self.min_angle <= self.start_position and self.max_angle >= self.start_position):
            self._motor_hat.setOutput(self._output_pin, self.start_position)
