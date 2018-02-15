import tkinter
from tkinter import ttk
import robot_controller as robo
import mqtt_remote_method_calls as com
def main():
    mqtt_client = com.MqttClient(robo.Snatch3r())
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    go_back_button = ttk.Button(main_frame, text="go back")
    go_back_button.grid(row=1, column=0)
    go_back_button['command'] = lambda: go_back(mqtt_client)

    root.mainloop()


def go_back(mqtt_client):
    mqtt_client.send_message("go_back_to_ori_location")





# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()