#!usr/bin/env python
import logging
import RPi.GPIO as GPIO
from time import sleep
import datetime
from bbCamera import bbCamera
GPIO.setmode(GPIO.BOARD)

forward1 = 18
backward1 = 16
pwm1 = 12


forward2 = 15
backward2 = 13
pwm2 = 11

HIGH = GPIO.HIGH
LOW = GPIO.LOW
OUT = GPIO.OUT


class Driver(object):
    def __init__(self):
        # Initialize motor1
        GPIO.setup(forward1, OUT)
        GPIO.setup(backward1, OUT)
        GPIO.setup(pwm1, OUT)

        # Initialize motor2

        GPIO.setup(forward2, OUT)
        GPIO.setup(backward2, OUT)
        GPIO.setup(pwm2, OUT)
        print "Initialized Driver Object."

    def right_motor_high_forward(self, seconds):
        print "Right motor engaged."
        GPIO.output(forward1, HIGH)
        GPIO.output(backward1, LOW)
        GPIO.output(pwm1, HIGH)

        sleep(seconds)
        GPIO.output(pwm1, LOW)
        print "Ran for %s seconds. " % seconds
        print "Right motor disengaged."

    def left_motor_high_forward(self, seconds):
        print "Left motor engaged."
        GPIO.output(forward2, HIGH)
        GPIO.output(backward2, LOW)
        GPIO.output(pwm2, HIGH)

        sleep(seconds)
        GPIO.output(pwm2, LOW)
        print "Ran for %s seconds. " % seconds
        print "Left motor disengaged."

    def forward(self, seconds):
        print "Forward engaged."
        GPIO.output(forward1, HIGH)
        GPIO.output(forward2, HIGH)

        GPIO.output(backward1, LOW)
        GPIO.output(backward2, LOW)

        GPIO.output(pwm1, HIGH)
        GPIO.output(pwm2, HIGH)

        sleep(seconds)
        print "Ran for %s seconds" % seconds
        GPIO.output(pwm1, LOW)
        GPIO.output(pwm2, LOW)
        print "Forward disengaged."

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
    d = Driver()
    cam = bbCamera()
    sleep(1)
    try:
        for i in range(20):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S.%f")
            cam.capture("/home/pi/bb23/images/%s_%s.jpg" % (timestamp, i))
            d.forward(0.5)
            sleep(0.2)
            d.right_motor_high_forward(0.1)
            sleep(0.5)
        d.cleanup()
    except Exception as e:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S.%f")
        logging.debug(timestamp + ": " + str(e))
    finally:
        d.cleanup()
