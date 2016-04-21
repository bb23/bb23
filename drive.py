#!usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep
import picamera
import time
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
        print "initialized"

        
    def right_motor_high_forward(self, seconds):
        
        GPIO.output(forward1, HIGH)
        GPIO.output(backward1, LOW)
        GPIO.output(pwm1, HIGH)
        
        sleep(seconds)
        GPIO.output(pwm1, LOW)


    def left_motor_high_forward(self, seconds):
    
        GPIO.output(forward2, HIGH)
        GPIO.output(backward2, LOW)
        GPIO.output(pwm2, HIGH)
        
        sleep(seconds)
        GPIO.output(pwm2, LOW)


    def forward(self, seconds):
        GPIO.output(forward1, HIGH)
        GPIO.output(forward2, HIGH)

        GPIO.output(backward1, LOW)
        GPIO.output(backward2, LOW)

        GPIO.output(pwm1, HIGH)
        GPIO.output(pwm2, HIGH)

        sleep(seconds)
        
        GPIO.output(pwm1, LOW)
        GPIO.output(pwm2, LOW)
   
    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    d = Driver()
    cam = picamera.PiCamera()
    sleep(0.5)
    cam.vflip=True
    cam.hflip=True
    for i in range(25):
        cam.capture("/home/pi/bb23/images/%s_%s.jpg" % (time.time(), i))
        d.forward(0.5)
        d.right_motor_high_forward(0.05*i)
    d.cleanup()

