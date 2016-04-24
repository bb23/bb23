#import the necessary packages
import numpy as np
import cv2
import glob

file_list = glob.glob("images/*.jpg")
# file_list = glob.glob("images/4_both.jpg")

# define ROI for detecting edges

detect_width = 600
detect_height = 600

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

print file_list

for f_name in file_list:
    print f_name

    image = cv2.imread(f_name)

    height, width, channels = image.shape

    center_x_low = width / 2 - detect_width / 2
    center_x_high = width / 2 + detect_width / 2

    print "Width: %d, Height: %d, Channels: %d" % (height, width, channels)

    x1_e = center_x_low
    x2_e = center_x_high
    y1_e = height - detect_height
    y2_e = height

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)


    edges = auto_canny(blurred, 0.33)

    center_roi = edges[y1_e: y2_e, x1_e:x2_e]

    # find contours in the masked image and keep the largest one
    (_, cnts, _) = cv2.findContours(center_roi.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    print len(cnts)

    if len(cnts) == 0:
        print "No contours found"
        continue

    print "Found countours"

    c = max(cnts, key=cv2.contourArea)

    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.05 * peri, True)

    print approx.shape
    print approx

    # Move the x coords
    approx[:,:,0] += x1_e
    approx[:,:,1] += y1_e

    # draw a green bounding box surrounding the detected object
    cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)

    cv2.line(image,
        (x1_e, y1_e),
        (x1_e, y2_e),
        color=(0,0,255),
        thickness=3)
    cv2.line(image,
        (x2_e, y1_e),
        (x2_e, y2_e),
        color=(0,0,255),
        thickness=3)
    cv2.line(image,
        (x1_e, y1_e),
        (x2_e, y1_e),
        color=(0,0,255),
        thickness=3)
    cv2.line(image,
        (x1_e, y2_e),
        (x2_e, y2_e),
        color=(0,0,255),
        thickness=3)

    # cv2.line(image,
    #     (center_x_high, 0),
    #     (center_x_high, height),
    #     color=(0,0,255),
    #     thickness=3)

    # cv2.imshow("ROI", center_roi)

    cv2.imshow("Image", cv2.resize(image, (0,0), fx=0.5, fy=0.5))
    cv2.imshow("Edges", cv2.resize(edges, (0,0), fx=0.5, fy=0.5))
    # cv2.imshow("Mask", mask)
    cv2.waitKey(0)



    # if len(cnts) == 0:
    #     print "No contours found"
    #     cv2.imshow("Mask", mask)
    #     cv2.waitKey(0)
    #     continue

    # c = max(cnts, key=cv2.contourArea)

    # # approximate the contour
    # peri = cv2.arcLength(c, True)
    # approx = cv2.approxPolyDP(c, 0.05 * peri, True)

    # M = cv2.moments(approx)

    # cx = int(M['m10']/M['m00'])
    # cy = int(M['m01']/M['m00'])

    # print "cx is %.2f, cy is %.2f" % (cx, cy)

    # if cx < center_x_low:
    #     print "Ball on left"
    # elif cx > center_x_high:
    #     print "Ball on right"
    # else:
    #     print "Ball in middle"

    # draw a green bounding box surrounding the orange game
    # cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
    # cv2.line(image,
    #     (center_x_low, 0),
    #     (center_x_low, height),
    #     color=(0,0,255),
    #     thickness=3)
    # cv2.line(image,
    #     (center_x_high, 0),
    #     (center_x_high, height),
    #     color=(0,0,255),
    #     thickness=3)


