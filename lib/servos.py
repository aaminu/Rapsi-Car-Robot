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

        # Start Up
        self.set_angle(self.start_position)

    def set_angle(self, angle: int):
        if self.initState and self.verify(angle):
            self._motor_hat.setOutput(self._output_pin, angle)
        else:
            print("[Error]: Angle outside allowed region")

    def cleanup(self):
        if self.initState and self.verify(self.start_position):
            self._motor_hat.setOutput(self._output_pin, self.start_position)

    def verify(self, angle: int):
        if (self.min_angle <= angle and self.max_angle >= angle):
            return True
        return False


# Testing Pan and Tilt Servos
if __name__ == "__main__":
    import time
    import piconzero as pz
    pz.init()

    pan_pin = 1
    pan_swing_angle = (50, 150)
    pan_start_angle = 103

    tilt_pin = 0
    tilt_swing_angle = (55, 180)
    tilt_start_angle = 155

    pan = Servos(motor_hat=pz, output_pin=pan_pin,
                 min_max_degree=pan_swing_angle, start_position=pan_start_angle)
    tilt = Servos(motor_hat=pz, output_pin=tilt_pin,
                  min_max_degree=tilt_swing_angle, start_position=tilt_start_angle)

    pan.set_angle(65)
    tilt.set_angle(170)
    time.sleep(2)
    pan.cleanup()
    tilt.cleanup()
