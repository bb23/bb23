#!/usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)


# Right front motor
rf_forward = 18
rf_backward = 16
rf_enabler = 12

#Right Rear Motor
rr_forward = 33
rr_backward = 31
rr_enabler = 29

# Left front motor
lf_forward = 15
lf_backward = 13
lf_enabler = 11

#left Rear Motor
lr_forward = 36
lr_backward = 37
lr_enabler = 32


HIGH = GPIO.HIGH
LOW = GPIO.LOW
OUT = GPIO.OUT

class Pin(object):
    # freq = hertz (cycles/second)
    def __init__(self, pin_number, freq=60):

        GPIO.setup(pin_number, OUT)
        self.p = GPIO.pwm(pin_number, freq)

    def high(self, duty_cycle=50):
        self.p.ChangeDutyCycle(duty_cycle)

    def low(self):
        self.p.ChangeDutyCycle(0)

    def cleanup():
        self.p.stop()


class EnablerPin(object):
    def __init__(self, pin_number):
        GPIO.setup(pin_number, OUT)
        self.pin_number = pin_number

    def high(self):
        GPIO.output(self.pin_number, HIGH)

    def low(self):
        GPIO.output(self.pin_number, LOW)

    def cleanup():
        GPIO.output(self.pin_number, LOW)

class Wheel(object):
    def __init__(self, pin1, pin2, enabler):

        self.pin1 = Pin(pin1)
        self.pin2 = Pin(pin2)
        self.enabler = EnablerPin(enabler)


    # go forward at speed (0-100)
    def forward(self, speed):
        self.pin1.high(speed)
        self.pin2.low()

    def backward(self, speed):
        self.pin1.low()
        self.pin2.high(speed)

    def stop(self):
        self.pin1.low()
        self.pin2.low()

    def cleanup(self):
        self.pin1.cleanup()
        self.pin2.cleanup()


class Driver(object):
    # Create and assign all the pins
    def __init__(self):
        # Initialize Right Front Wheel
        rf_wheel = Wheel(rf_forward, rf_backward, rf_enabler)

        # Initialize Right Rear Wheel
        rr_wheel = Wheel(rr_forward, rr_backward, rr_enabler)

        # Initialize Left Front Wheel
        lf_wheel = Wheel(lf_forward, lf_backward, lf_enabler)

        # Initialize Left Rear Wheel
        lr_wheel = Wheel(lr_forward, lr_backward, lr_enabler)

        print "Initialized Driver Object."

    def right_motor_high_forward(self, seconds):
        print "Right motor engaged."
        GPIO.output(rf_forward, HIGH)
        GPIO.output(rf_backward, LOW)
        GPIO.output(rr_forward, HIGH)
        GPIO.output(rr_backward, LOW)

        GPIO.output(rr_pwm, HIGH)
        GPIO.output(rf_pwm, HIGH)

        sleep(seconds)

        GPIO.output(rf_pwm, LOW)
        GPIO.output(rr_pwm, LOW)

        print "Ran for %s seconds. " % seconds
        print "Right motor disengaged."

    def left_motor_high_forward(self, seconds):
        print "Left motor engaged."
        GPIO.output(lf_forward, HIGH)
        GPIO.output(lf_backward, LOW)
        GPIO.output(lr_forward, HIGH)
        GPIO.output(lr_backward, LOW)

        GPIO.output(lr_pwm, HIGH)
        GPIO.output(lf_pwm, HIGH)

        sleep(seconds)

        GPIO.output(lf_pwm, LOW)
        GPIO.output(lr_pwm, LOW)

        print "Ran for %s seconds. " % seconds
        print "Left motor disengaged."

    def forward(self, seconds):
        print "Forward engaged."
        # forward pins to high
        GPIO.output(rf_forward, HIGH)
        GPIO.output(rr_forward, HIGH)

        GPIO.output(lf_forward, HIGH)
        GPIO.output(lr_forward, HIGH)

        # back pins to low
        GPIO.output(rf_backward, LOW)
        GPIO.output(rr_backward, LOW)

        GPIO.output(lf_backward, LOW)
        GPIO.output(lr_backward, LOW)

        # engage pwmm
        GPIO.output(rf_pwm, HIGH)
        GPIO.output(lf_pwm, HIGH)

        GPIO.output(rr_pwm, HIGH)
        GPIO.output(lr_pwm, HIGH)

        sleep(seconds)

        print "Ran for %s seconds" % seconds
        GPIO.output(rf_pwm, LOW)
        GPIO.output(lf_pwm, LOW)

        GPIO.output(rr_pwm, LOW)
        GPIO.output(lr_pwm, LOW)

        print "Forward disengaged."

    def cleanup(self):
        GPIO.cleanup()
