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

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.MAX_SPEED = 900
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor
        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor
        self.beacon_seeker = ev3.BeaconSeeker(channel=1)
        assert self.beacon_seeker
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy
        self.come_back = False
        self.spot1 = True
        self.spot2 = True
        self.spot3 = True
        self.spot4 = True

    def drive_inches(self, distance, speed):

        assert self.left_motor.connected
        assert self.right_motor.connected

        position = distance * 90

        self.left_motor.run_to_rel_pos(position_sp=position, speed_sp=speed,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=position, speed_sp=speed,
                                        stop_action='brake')
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):

        assert self.left_motor.connected
        assert self.right_motor.connected

        self.left_motor.run_to_rel_pos(position_sp=degrees_to_turn * 470 / 90,
                                       speed_sp=turn_speed_sp,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(
            position_sp=-degrees_to_turn * 470 / 90,
            speed_sp=turn_speed_sp,
            stop_action='brake')

        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

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
            position_sp=-arm_revolutions_for_full_range * 360,
            speed_sp=self.MAX_SPEED)
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

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

    def shutdown(self):
        self.running = False
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Sound.speak("Goodbye").wait()

    def drive_forward(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def turn_left(self, left_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=left_speed)

    def turn_right(self, right_speed):
        self.left_motor.run_forever(speed_sp=right_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def stop(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def drive_backward(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def seek_beacon(self):

        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading
            current_distance = self.beacon_seeker.distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                    if current_distance == 0:
                        self.stop()
                        return True

                    elif current_distance > 0:
                        self.drive_forward(forward_speed, forward_speed)

                elif math.fabs(current_heading) < 10:
                    print("Adjusting heading: ", current_heading)
                    if current_heading < 0:
                        self.turn_left(turn_speed)

                    elif current_heading > 0:
                        self.turn_right(turn_speed)

                elif math.fabs(current_heading) > 10:
                    print("Heading is too far off to fix: ", current_heading)

            time.sleep(0.2)

        # The touch_sensor was pressed to abort the attempt if this code runs.

        self.stop()
        return False

    def follow_the_line(self):
        while True:
            print('follow line')
            if self.color_sensor.reflected_light_intensity >= 90:
                self.turn_right(100)

            elif self.color_sensor.reflected_light_intensity <= 10:
                self.drive_forward(300, 300)

            elif self.color_sensor.color == ev3.ColorSensor.COLOR_RED:
                self.stop()
                break

            time.sleep(0.01)

    def go_back(self):
        self.come_back = True

    def stop_at_color(self, color_to_seek):
        while True:
            self.drive_forward(900, 900)
            if self.color_sensor.color == color_to_seek:
                self.stop()
                break
            time.sleep(0.1)

    def go_in(self, color):
        self.arm_up()
        self.turn_degrees(180, 300)
        self.stop_at_color(color)
        self.turn_degrees(90, 300)
        self.drive_inches(5, 300)
        print(233)
        self.arm_down()
        self.drive_inches(-5, 300)
        self.turn_degrees(90, 300)
        self.turn_toward_beacon()
        self.stop_at_color(5)

    def go_out(self, color):
        self.turn_degrees(180, 300)
        self.stop_at_color(color)
        self.turn_degrees(90, 300)
        self.drive_inches(5, 300)
        print(233)
        self.arm_up()
        print(666)
        self.drive_inches(-5, 300)
        self.turn_degrees(90, 300)
        self.turn_toward_beacon()
        self.stop_at_color(5)
        self.arm_down()

    def turn_toward_beacon(self):

        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading
            current_distance = self.beacon_seeker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ",
                          current_distance)


                elif math.fabs(current_heading) >= 2:
                    print("Adjusting heading: ", current_heading)
                    if current_heading < 0:
                        self.turn_left(turn_speed)

                    elif current_heading > 0:
                        self.turn_right(turn_speed)

            time.sleep(0.2)

            # The touch_sensor was pressed to abort the attempt if this code runs.

            self.stop()
            return False
