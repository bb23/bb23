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

    def high(self, duty_cycle):
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
        self.rf_wheel = Wheel(rf_forward, rf_backward, rf_enabler)

        # Initialize Right Rear Wheel
        self.rr_wheel = Wheel(rr_forward, rr_backward, rr_enabler)

        # Initialize Left Front Wheel
        self.lf_wheel = Wheel(lf_forward, lf_backward, lf_enabler)

        # Initialize Left Rear Wheel
        self.lr_wheel = Wheel(lr_forward, lr_backward, lr_enabler)

        print "Initialized Driver Object."

    def right_turn(self, speed=25):
        self.lf_wheel.forward(speed)
        self.lr_wheel.forward(speed)

        self.rr_wheel.backward(speed)
        self.rf_wheel.backward(speed)

    def left_turn(self, speed=25):
        self.lf_wheel.backward(speed)
        self.lr_wheel.backward(speed)

        self.rr_wheel.forward(speed)
        self.rf_wheel.forward(speed)

    def backward(self, speed=50):
        self.lf_wheel.backward(speed)
        self.lr_wheel.backward(speed)

        self.rr_wheel.backward(speed)
        self.rf_wheel.backward(speed)

    def forward(self, speed=50):
        self.lf_wheel.forward(speed)
        self.lr_wheel.forward(speed)

        self.rr_wheel.forward(speed)
        self.rf_wheel.forward(speed)

    def cleanup(self):
        GPIO.cleanup()
