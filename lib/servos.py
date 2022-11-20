class Servos:

    def __init__(self, motor_hat: object, output_pin: int, *, min_max_degree: tuple = (-90, 90), start_position: int = 0) -> None:
        self._motor_hat = motor_hat
        self.min_angle = self._convert_angle(min_max_degree[0]) if self._convert_angle(
            min_max_degree[0]) != None else 0
        self.max_angle = self._convert_angle(min_max_degree[1]) if self._convert_angle(
            min_max_degree[1]) != None else 180
        self.start_position = self._convert_angle(
            start_position) if self._convert_angle(start_position) != None else 90
        self.initState = False
        self._output_pin = -1
        if (output_pin >= 0) and (output_pin <= 5):
            self._output_pin = output_pin
            self._motor_hat.setOutputConfig(output_pin, 2)
            self.initState = True
        else:
            print("[Error]: Servo intialization failed due to wrong pin selection")

        # Start Up
        self.set_angle(start_position)

    def set_angle(self, angle: int):
        position = self._convert_angle(_angle=angle)
        if self.initState and self.verify(position):
            self._motor_hat.setOutput(self._output_pin, position)
        else:
            print("[Error]: Angle outside allowed region")

    def _convert_angle(self, _angle: int):
        if (_angle < -90 or _angle > 90):
            print("Angle out of range expected, please enter -90 to +90")
            return None
        angle = _angle + 90
        return angle

    def cleanup(self):
        if self.initState and self.verify(self.start_position):
            self._motor_hat.setOutput(self._output_pin, self.start_position)

    def verify(self, angle: int):
        if angle is None:
            return False
        if (self.min_angle <= angle and self.max_angle >= angle):
            return True
        return False


# Testing Pan and Tilt Servos
if __name__ == "__main__":
    import time
    import piconzero as pz
    pz.init()

    pan_pin = 1
    pan_swing_angle = (-40, 60)
    pan_start_angle = 10

    tilt_pin = 0
    tilt_swing_angle = (-90, 80)
    tilt_start_angle = 0

    pan = Servos(motor_hat=pz, output_pin=pan_pin,
                 min_max_degree=pan_swing_angle, start_position=pan_start_angle)
    tilt = Servos(motor_hat=pz, output_pin=tilt_pin,
                  min_max_degree=tilt_swing_angle, start_position=tilt_start_angle)

    pan.set_angle(-25)
    tilt.set_angle(60)
    time.sleep(2)
    pan.cleanup()
    tilt.cleanup()
