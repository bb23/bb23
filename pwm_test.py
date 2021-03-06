#!/usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

# Right front motor
rf_forward = 18
rf_backward = 16
rf_pwm = 12

# Right Rear Motor
rr_forward = 33
rr_backward = 31
rr_pwm = 29

# Left front motor
lf_forward = 15
lf_backward = 13
lf_pwm = 11

# Left Rear Motor
lr_forward = 36
lr_backward = 37
lr_pwm = 32


HIGH = GPIO.HIGH
LOW = GPIO.LOW
OUT = GPIO.OUT

hertz = 60

class Driver(object):
    def __init__(self):
        # Initialize Right Front Motor
        GPIO.setup(rf_forward, OUT)
        GPIO.setup(rf_backward, OUT)
        GPIO.setup(rf_pwm, OUT)

        # Initialize Left Front Motor
        GPIO.setup(lf_forward, OUT)
        GPIO.setup(lf_backward, OUT)
        GPIO.setup(lf_pwm, OUT)

        # Initialize Right Rear Motor
        GPIO.setup(rr_forward, OUT)
        GPIO.setup(rr_backward, OUT)
        GPIO.setup(rr_pwm, OUT)

        # Initialize Left Rear Motor
        GPIO.setup(lr_forward, OUT)
        GPIO.setup(lr_backward, OUT)
        GPIO.setup(lr_pwm, OUT)

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

    def forward_pwm(self, seconds):
        print "Forward engaged."
        # forward pins to high
        rf = GPIO.PWM(rf_forward, hertz)
        rr = GPIO.PWM(rr_forward, hertz)

        lf = GPIO.PWM(lf_forward, hertz)
        lr = GPIO.PWM(lr_forward, hertz)

        rf.start(50)
        rr.start(50)

        lf.start(50)
        lr.start(50)

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

    def forward_back_pwm(self, seconds):
        print "Forward engaged."
        # forward pins to high
        rf1 = GPIO.PWM(rf_forward, hertz)
        rf2 = GPIO.PWM(rf_backward, hertz)

        rr1 = GPIO.PWM(rr_forward, hertz)
        rr2 = GPIO.PWM(rr_backward, hertz)

        lf1 = GPIO.PWM(lf_forward, hertz)
        lf2 = GPIO.PWM(lf_backward, hertz)

        lr1 = GPIO.PWM(lr_forward, hertz)
        lr2 = GPIO.PWM(lr_backward, hertz)

        rf2.start(0)
        rr2.start(0)
        lf2.start(0)
        lr2.start(0)

        rf1.start(50)
        rr1.start(50)
        lf1.start(50)
        lr1.start(50)

        # Engage pwmm
        GPIO.output(rf_pwm, HIGH)
        GPIO.output(lf_pwm, HIGH)

        GPIO.output(rr_pwm, HIGH)
        GPIO.output(lr_pwm, HIGH)

        sleep(seconds)

        rf2.ChangeDutyCycle(50)
        rr2.ChangeDutyCycle(50)
        lf2.ChangeDutyCycle(50)
        lr2.ChangeDutyCycle(50)

        rf1.ChangeDutyCycle(0)
        rr1.ChangeDutyCycle(0)
        lf1.ChangeDutyCycle(0)
        lr1.ChangeDutyCycle(0)
        sleep(seconds)

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":

    driver = Driver()
    driver.forward_back_pwm(5)

    driver.cleanup()
