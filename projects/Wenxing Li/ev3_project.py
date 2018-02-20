"""
This project is a delivery robot that can follow a line and identify the
color in front of it. If the color is correct, it'll drop the object.
Otherwise it'll send back a message to the tkinter window, and the operator
can choose whether to stay and wait, or to go back to the original position.
"""


import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

print("-----------")
print("start")
print("-----------")


class MyDelegate(object):

    def __init__(self):
        self.robot = robo.Snatch3r()
        self.mqtt_client = None
        self.robot.pixy.mode = "SIG1"

    def go_back_to_origin(self):
        self.robot.turn_degrees(160,100)
        self.robot.drive_inches(2,100)
        self.robot.follow_the_reversed_line()

    def shut_down(self):
        ev3.Sound.speak('end task')
        self.robot.shutdown()

    def start(self):
        self.robot.seek_beacon()
        self.robot.arm_up()
        num = 0
        while True:
            self.robot.follow_the_line()
            if self.robot.pixy.value(3)>10:
                ev3.Sound.speak("found customer")
                self.robot.arm_down()
                self.robot.drive_inches(-4,100)
                break
            elif num<8:
                ev3.Sound.speak("no customer found")
                time.sleep(0.1)
                num += 1
                print(num)
            elif num == 8:
                print(num)
                break

        self.go_back_to_origin()
        self.robot.arm_down()
        ev3.Sound.speak('end task')


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    my_delegate.robot.loop_forever()

main()
