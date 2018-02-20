import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

def main():

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Parking")

    main_frame = ttk.Frame(root, padding=50, relief='raised')
    main_frame.grid()

    in1_button = ttk.Button(main_frame, text="in1")
    in1_button.grid(row=1, column=0)
    in1_button['command'] = lambda: go_in1(mqtt_client)

    out1_button = ttk.Button(main_frame, text="out1")
    out1_button.grid(row=2, column=0)
    out1_button['command'] = lambda: go_out1(mqtt_client)

    in2_button = ttk.Button(main_frame, text="in2")
    in2_button.grid(row=1, column=1)
    in2_button['command'] = lambda: go_in2(mqtt_client)

    out2_button = ttk.Button(main_frame, text="out2")
    out2_button.grid(row=2, column=1)
    out2_button['command'] = lambda: go_out2(mqtt_client)

    in3_button = ttk.Button(main_frame, text="in3")
    in3_button.grid(row=1, column=2)
    in3_button['command'] = lambda: go_in3(mqtt_client)

    out3_button = ttk.Button(main_frame, text="out3")
    out3_button.grid(row=2, column=2)
    out3_button['command'] = lambda: go_out3(mqtt_client)

    in4_button = ttk.Button(main_frame, text="in4")
    in4_button.grid(row=1, column=3)
    in4_button['command'] = lambda: go_in4(mqtt_client)

    out4_button = ttk.Button(main_frame, text="out4")
    out4_button.grid(row=2, column=3)
    out4_button['command'] = lambda: go_out4(mqtt_client)

    quit_button = ttk.Button(main_frame, text="quit")
    quit_button.grid(row=3, column=0)
    quit_button['command'] = lambda : shut_down(mqtt_client)

    root.mainloop()

def go_in1(mqtt_client):
    mqtt_client.send_message("go_in1")

def go_in2(mqtt_client):
    mqtt_client.send_message("go_in2")

def go_in3(mqtt_client):
    mqtt_client.send_message("go_in3")

def go_in4(mqtt_client):
    mqtt_client.send_message("go_in4")

def go_out1(mqtt_client):
    mqtt_client.send_message("go_out1")

def go_out2(mqtt_client):
    mqtt_client.send_message("go_out2")

def go_out3(mqtt_client):
    mqtt_client.send_message("go_out3")

def go_out4(mqtt_client):
    mqtt_client.send_message("go_out4")


def shut_down(mqtt_client):
    mqtt_client.send_message("shut_down")
    mqtt_client.close()
    exit()


main()
