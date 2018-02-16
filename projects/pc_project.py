import tkinter
from tkinter import ttk
import robot_controller as robo
import mqtt_remote_method_calls as com

class MyDelegate(object):

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def mission_complete(self):
        message_to_display = "Mission Complete"
        self.display_label.configure(text=message_to_display)

    def no_customer_found(self):
        message_to_display = "No Customer Found"
        self.display_label.configure(text=message_to_display)


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    start_button = ttk.Button(main_frame, text="start")
    start_button.grid(row=1, column=0)
    start_button['command'] = lambda: start(mqtt_client)


    go_back_button = ttk.Button(main_frame, text="go back")
    go_back_button.grid(row=2, column=0)
    go_back_button['command'] = lambda: go_back(mqtt_client)

    quit_button = ttk.Button(main_frame, text="quit")
    quit_button.grid(row=3, column=0)
    quit_button['command'] = lambda : shut_down(mqtt_client)

    root.mainloop()


def go_back(mqtt_client):
    mqtt_client.send_message("go_back_to_ori_location")

def start(mqtt_client):
    mqtt_client.send_message("start")

def shut_down(mqtt_client):
    mqtt_client.send_message("shut_down")






# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()