"""
This project is a delivery robot that can follow a line and identify the
color in front of it. If the color is correct, it'll drop the object.
Otherwise it'll send back a message to the tkinter window, and the operator
can choose whether to stay and wait, or to go back to the original position.
"""


import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3

print("-----------")
print("start")
print("-----------")


class MyDelegate(object):

    def __init__(self):
        self.robot = robo.Snatch3r()
        self.mqtt_client = None
        self.robot.pixy.mode = "SIG1"

    def go_back_to_origin(self):
        self.robot.turn_degrees(180,100)
        self.robot.drive_inches(2,100)
        self.robot.follow_the_line()

    def shut_down(self):
        ev3.Sound.speak('end project')
        self.robot.shutdown()

    def start(self):
        self.robot.seek_beacon()
        self.robot.arm_up()
        while True:
            self.robot.follow_the_line()
            if self.robot.pixy.value(3)>10:
                print("found color")
                ev3.Sound.speak("found color")
                self.robot.arm_down()
                self.mqtt_client.send_message('mission_complete')
                break
            else:
                self.mqtt_client.send_message('no_customer_found')
        self.go_back_to_origin()
def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    my_delegate.robot.loop_forever()

main()
