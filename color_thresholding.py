#!/usr/bin/env python
import numpy as np
import cv2
# from matplotlib import pyplot as plt

red_color = ([5, 5, 50], [60, 60, 255])
orange_color = ([30, 120, 230], [100, 200, 255])
# 255, 153, 51
# rgb
# bgr -> 51, 153, 255

open_range = ([0, 0, 0], [255, 255, 255])

# boundaries = [
#     ([17, 15, 100], [50, 56, 200]),
#     ([86, 31, 4], [220, 88, 50]),
#     ([25, 146, 190], [62, 174, 250]),
#     ([103, 86, 65], [145, 133, 128])
# ]

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    image = frame

    # thresholded = cv2.inRange()

    # edges = cv2.Canny(gray,100,200)

    # create NumPy arrays from the boundaries
    lower = np.array(orange_color[0], dtype="uint8")
    upper = np.array(orange_color[1], dtype="uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)

    # plt.subplot(121),plt.imshow(gray,cmap = 'gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    # plt.show()

    # Display the resulting frame
    cv2.imshow('frame', output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
