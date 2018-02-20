import time
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3


class MyDelegate(object):
    def __init__(self):
        self.robot = robo.Snatch3r()
        self.mqtt_client = None

    def go_in1(self):

        if self.robot.spot1 == True:
            self.robot.go_in(4)
            self.robot.spot1 = False
            print(self.robot.spot1, 1, 'in')

        elif self.robot.spot1 == False:
            ev3.Sound.beep()

    def go_in2(self):
        if self.robot.spot2 == True:
            self.robot.go_in(1)
            self.robot.spot2 = False


        elif self.robot.spot2 == False:
            ev3.Sound.beep()

    def go_in3(self):
        if self.robot.spot3 == True:
            self.robot.go_in(3)
            self.robot.spot3 = False

        elif self.robot.spot3 == False:
            ev3.Sound.beep()

    def go_in4(self):
        if self.robot.spot4 == True:
            self.robot.go_in(2)
            self.robot.spot4 = False


        elif self.robot.spot4 == False:
            ev3.Sound.beep()

    def go_out1(self):
        print(self.robot.spot1, 1, 'out')
        if self.robot.spot1 == False:
            self.robot.go_out(4)
            self.robot.spot1 = True

        elif self.robot.spot1 == True:
            ev3.Sound.beep()

    def go_out2(self):
        if self.robot.spot2 == False:
            self.robot.go_out(1)
            self.robot.spot2 = True

        elif self.robot.spot2 == True:
            ev3.Sound.beep()

    def go_out3(self):
        if self.robot.spot3 == False:
            self.robot.go_out(3)
            self.robot.spot3 = True

        elif self.robot.spot3 == True:
            ev3.Sound.beep()

    def go_out4(self):
        if self.robot.spot4 == False:
            self.robot.go_out(2)
            self.robot.spot4 = True

        elif self.robot.spot4 == True:
            ev3.Sound.beep()

    def shut_down(self):
        ev3.Sound.speak('end task')
        self.robot.shutdown()


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    my_delegate.robot.loop_forever()


main()
