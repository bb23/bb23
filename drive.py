#!usr/bin/env python
import inspect
import io
import datetime
import logging
import random
import time


import cv2
import numpy as np
import picamera
import picamera.array
# from random_walker import RandomWalker

from bbCamera import BbCamera
import driver


TICKLE = 0.2

LOWER = np.array([0, 70, 120])
UPPER = np.array([30, 160, 255])

VERBOTTEN_METHODS = set("cleanup")


def main():
    logging.basicConfig(filename='/home/pi/bb23/example.log', level=logging.DEBUG)
    start_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S.%f")
    image_path = "/home/pi/bb23/images/%s_%s.jpg"
    try:
        cam = BbCamera()
        # cam.start_recording(image_path % (start_timestamp))
        # cam.start_preview()
        time.sleep(2)

        # Initialize drive controller and get methods sans Verbotten
        drive_controller = driver.Driver()
        logging.info("\n\nDriver enabled")

        #methods = set(inspect.getmembers(drive_controller,
        #                                 predicate=inspect.ismethod))
        #methods -= VERBOTTEN_METHODS
        methods = ["forward", "left_motor_high_forward", "right_motor_high_forward"]
        loopery = True
        while loopery:
            # current_time = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S.%f")
            # CAPTURE IMAGE
            with picamera.array.PiRGBArray(cam) as stream:
                cam.capture(stream, 'bgr')
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
                # Jitter'd random walk.
                print "==================================="
                print "     Random walk mode enabled      "
                print "==================================="
                random_method = random.choice(methods)
                getattr(drive_controller, random_method)(TICKLE)
                continue

            c = max(cnts, key=cv2.contourArea)

            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.05 * peri, True)

            M = cv2.moments(approx)
            try:
                c_x = int(M['m10']/M['m00'])
                c_y = int(M['m01']/M['m00'])
            except ZeroDivisionError:
                logging.info("dividing by zero")
                continue
                
            if c_x < center_x_low:
                drive_controller.right_motor_high_forward(TICKLE/2)
            elif c_x > center_x_high:
                drive_controller.left_motor_high_forward(TICKLE/2)
            else:
                drive_controller.forward(TICKLE/2)

    except Exception as e:
        error_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S.%f")
        import traceback
        logging.debug(error_timestamp + ": " + str(e))
        logging.debug(traceback.print_exc(file=open('/home/pi/bb23/traceback.log','a')))

if __name__ == "__main__":
    main()
