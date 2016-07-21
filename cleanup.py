#!/usr/bin/env python

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

# Right front motor
rf_forward = 18
rf_backward = 16
rf_pwm = 12

#Right Rear Motor
rr_forward = 33
rr_backward = 31
rr_pwm = 29

# Left front motor
lf_forward = 15
lf_backward = 13
lf_pwm = 11

#left Rear Motor
lr_forward = 36
lr_backward = 37
lr_pwm = 32


HIGH = GPIO.HIGH
LOW = GPIO.LOW
OUT = GPIO.OUT

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

GPIO.cleanup()

