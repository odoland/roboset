""" This file is just to draw the contours found """


import cv2
import argparse
from matplotlib import pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", required=True, help="path2imagepls")

args = vars(ap.parse_args())

image = cv2.imread(args['image'],0)

ret, thresh = cv2.threshold(image,127,255,1)
_, contours, _ = cv2.findContours(thresh,1,2)

for cnt in contours:
	approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
	print(len(approx))

backtorgb = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
newimage = cv2.drawContours(backtorgb, contours, -1, (0,255,0), 3)

cv2.imshow("old", image)
cv2.imshow("cv2 reading", newimage)
cv2.waitKey(0)
cv2.destroyAllWindows()