"""
This project is a delivery robot that can follow a line and identify the
color in front of it. If the color is correct, it'll drop the object.
Otherwise it'll send back a message to the tkinter window, and the operator
can choose whether to stay and wait, or to go back to the original position.
"""


import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3

robot = robo.Snatch3r()
mqtt_client = com.MqttClient(robot)
mqtt_client.connect_to_pc()


def start():
    robot.seek_beacon()
    robot.arm_up()
    while True:
        robot.follow_the_line()
        if robot.color_sensor.color == ev3.ColorSensor.COLOR_WHITE:
            break
        elif robot.pixy.value(3)>10:
            break
    robot.stop()
    while True:
        if robot.pixy.value(3)>10:
            robot.arm_down()
            mqtt_client.send_message('mission_complete')
            break
        elif robot.come_back == True:
            break
        mqtt_client.send_message('no_customer_found')

    robot.turn_degrees(90,400)
    robot.drive_inches(2,300)
    while True:
        robot.follow_the_line()
        if robot.color_sensor == ev3.ColorSensor.COLOR_WHITE:
            ev3.Sound.speak('mission complete')
            robot.stop()
            break
        elif robot.pixy.value(3)>10:
            robot.stop()
            break

def go_back_to_ori_location():
    robot.go_back()

def shut_down():
    ev3.Sound.speak('end project')
    robot.shutdown()