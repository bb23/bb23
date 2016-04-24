#!/usr/bin/env python
# import the necessary packages

import numpy as np
import cv2
import glob

# load the ball image
# image = cv2.imread("images/1_close.jpg")

# find the orange color ball in the image
lower = np.array([0, 70, 120])
upper = np.array([30, 160, 255])
# lower = np.array([0, 95, 190])
# upper = np.array([30, 160, 255])

# file_list = glob.glob("images/8_uber_far.jpg")

file_list = glob.glob("images/*.jpg")
print file_list

for f_name in file_list:
    print f_name

    image = cv2.imread(f_name)

    height, width, channels = image.shape

    center_x_low = width / 2 - 100
    center_x_high = width / 2 + 100

    print "Width: %d, Height: %d, Channels: %d" % (height, width, channels)

    mask = cv2.inRange(image, lower, upper)

    # find contours in the masked image and keep the largest one
    (_, cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    print len(cnts)

    if len(cnts) == 0:
        print "No contours found"
        cv2.imshow("Mask", mask)
        cv2.waitKey(0)
        continue

    c = max(cnts, key=cv2.contourArea)

    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * peri, True)

    M = cv2.moments(approx)

    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    print "cx is %.2f, cy is %.2f" % (cx, cy)

    if cx < center_x_low:
        print "Ball on left"
    elif cx > center_x_high:
        print "Ball on right"
    else:
        print "Ball in middle"

    # draw a green bounding box surrounding the orange game
    cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
    cv2.line(image,
        (center_x_low, 0),
        (center_x_low, height),
        color=(0,0,255),
        thickness=3)
    cv2.line(image,
        (center_x_high, 0),
        (center_x_high, height),
        color=(0,0,255),
        thickness=3)
    cv2.imshow("Image", image)
    # cv2.imshow("Mask", mask)
    cv2.waitKey(0)

