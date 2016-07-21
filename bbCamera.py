#!/usr/bin/env python
import time
import datetime
import logging
from time import sleep

import cv2
import numpy as np
import picamera
import picamera.array
from picamera import PiCamera

# from random_walker import RandomWalker

TICKLE = 0.2

LOWER = np.array([0, 70, 120])
UPPER = np.array([30, 160, 255])

VERBOTTEN_METHODS = set("cleanup")


class BbCamera(PiCamera):

    def __init__(self):
        PiCamera.__init__(self)
        self.hflip = self.vflip = True
        time.sleep(2)


class Gaffer():

    def __init__(self):
        self.cam = BbCamera()

        logging.info("\n\nCamera enabled")

        self.loopery = True

    def write_status(self, status):
        with open("file_status.txt") as f:
            f.write(status)

    def run(self):

        while self.loopery:
            # CAPTURE IMAGE
            with picamera.array.PiRGBArray(self.cam) as stream:
                self.cam.capture(stream, 'bgr')
                image = stream.array

            # GRAB IMAGE ATTRIBUTES
            height, width, channels = image.shape

            # assign left right center region
            center_x_low = width / 2 - 100
            center_x_high = width / 2 + 100

            # BUILD COLOR MASK WITH CONSTANTS SET FOR ~ORANGE
            color_mask = cv2.inRange(image, LOWER, UPPER)

            # find contours in the masked image and keep the largest one
            (_, cnts, _) = cv2.findContours(color_mask.copy(),
                                            cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
            if len(cnts) == 0:
                continue

            c = max(cnts, key=cv2.contourArea)

            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.05 * peri, True)

            M = cv2.moments(approx)
            try:
                c_x = int(M['m10']/M['m00'])
            except ZeroDivisionError:
                logging.info("dividing by zero")
                continue

            logging.info(c_x)
            sleep(TICKLE)

            if c_x < center_x_low:
                self.write_status("turn_left")

            elif c_x > center_x_high:
                self.write_status("turn_right")
            else:
                self.write_status("forward")


def main():

    logging.basicConfig(filename='/home/pi/bb23/camera.log', level=logging.DEBUG)
    try:

        gaffer = Gaffer()

        gaffer.run()

    except Exception as e:
        error_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S.%f")
        import traceback
        logging.debug(error_timestamp + ": " + str(e))
        logging.debug(traceback.print_exc(file=open('/home/pi/bb23/camera_traceback.log','a')))

if __name__ == "__main__":
    main()
