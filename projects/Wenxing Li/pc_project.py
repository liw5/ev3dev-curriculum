import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

def main():

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Delivery Robot")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    start_button = ttk.Button(main_frame, text="start")
    start_button.grid(row=1, column=0)
    start_button['command'] = lambda: start(mqtt_client)

    quit_button = ttk.Button(main_frame, text="quit")
    quit_button.grid(row=3, column=0)
    quit_button['command'] = lambda : shut_down(mqtt_client)

    root.mainloop()

def start(mqtt_client):
    mqtt_client.send_message("start")

def shut_down(mqtt_client):
    mqtt_client.send_message("shut_down")
    mqtt_client.close()
    exit()






# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()