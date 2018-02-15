"""
This project is a delivery robot that can follow a line and identify the
color in front of it. If the color is correct, it'll drop the object.
Otherwise it'll send back a message to the tkinter window, and the operator
can choose whether to stay and wait, or to go back to the original position.
"""

import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()


main()