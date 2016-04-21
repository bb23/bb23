#!/usr/bin/env python

import drive
import picamera
import time

def main():

    d = drive.Driver()
    cam = picamera.PiCamera()
    time.sleep(0.5)
    cam.vflip=True
    cam.hflip=True
    for i in range(20):
        cam.capture("%s.jpg" % i)
        d.forward(0.5)
        d.right_motor_high_forward(0.05*i)
    d.cleanup()

if __name__=='__main__':
    main()

