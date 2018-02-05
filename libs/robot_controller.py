"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time

class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    # TODO: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.MAX_SPEED = 900


    def drive_inches(self, distance, speed):
        print("--------------------------------------------")
        print("  Move")
        print("--------------------------------------------")
        ev3.Sound.speak("Drive using encoders").wait()

        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert left_motor.connected
        assert right_motor.connected

        position = distance * 90

        left_motor.run_to_rel_pos(position_sp=position, speed_sp=speed,
                                      stop_action='brake')
        right_motor.run_to_rel_pos(position_sp=position, speed_sp=speed,
                                       stop_action='brake')
        ev3.Sound.beep().wait()
        ev3.Sound.beep().wait()
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()



    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        print("--------------------------------------------")
        print("  Turn_Degrees")
        print("--------------------------------------------")
        ev3.Sound.speak("drive").wait()

        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        assert left_motor.connected
        assert right_motor.connected

        left_motor.run_to_rel_pos(position_sp=degrees_to_turn*410/90,
                                              speed_sp=turn_speed_sp,
                                              stop_action='brake')
        right_motor.run_to_rel_pos(position_sp=-degrees_to_turn*410/90,
                                               speed_sp=turn_speed_sp,
                                               stop_action='brake')

        ev3.Sound.beep().wait()
        ev3.Sound.beep().wait()
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def arm_calibration(self):
        assert self.arm_motor
        assert self.touch_sensor
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")

        ev3.Sound.beep().wait()
        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range * 360, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)

        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):
        assert self.arm_motor
        assert self.touch_sensor
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

    def arm_down(self):
        assert self.arm_motor
        self.arm_motor.run_to_abs_pos(
            position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

    def shutdown(self):
        ev3.Sound.speak("Goodbye").wait()


