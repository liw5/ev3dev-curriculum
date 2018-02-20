
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3

class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True

def main():
    robot = robo.Snatch3r()
    robot.arm_up()
    robot.turn_degrees(180, 900)
    print("--------------------------------------------")
    print(" Drive to the color")
    robot.stop_at_color(3)

    robot.turn_degrees(90, 900)
    robot.drive_inches(5, 900)
    robot.arm_down()
    robot.drive_inches(-5, 900)
    robot.turn_degrees(90, 900)
    robot.stop_at_color(6)


main()