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

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))



    root.mainloop()






def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")





# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()