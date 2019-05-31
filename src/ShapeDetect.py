"""
Shape Detection and Shape counter Module
author @odoland
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

import SetCard
from SetCard import *


def processHollow(image, threshold=200, debug=False):
	""" Processes the image file if it is a hollow image by converting it into a solid.
	@Parameters: image (np.array) 3 dimensions
				threshold (int) - threshold value for BW - default at 200
				debug (boolean) - flag to display the images for developing
	@Returns: processed image (np.array)
	"""

	# Threshold image to black and white.
	ret, thresh_clean = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)
	im_floodfill = thresh_clean.copy()
	
	# Floodfill the image
	h, w = im_floodfill.shape[:2]
	mask = np.zeros( (h+2, w+2), np.uint8)
	cv2.floodFill(im_floodfill, mask, (0,0), 255); # Fill from (0,0)
	im_floodfill_inv = cv2.bitwise_not(im_floodfill) # Invert the fill

	if debug: # debug mode to show pictures and print to stdout
		cv2.imshow("Thresholded image", thresh)
		cv2.imshow("Floodfilled", im_floodfill)
		cv2.imshow("inv floodfill", im_floodfill_inv)
		cv2.waitKey(0)

	return im_floodfill_inv

def processStripesFull(image, kernel=None, threshold=200, debug=False ):
	""" Processes Stripes and Full image by 1 iteration of blur and erosion.
	
	@Parameters: image (np.array) 
				kernel (default is  kernel = np.ones((5,5), np.uint8)
				threshold (int) threshold value for BW - default 200
				debug (boolean) - flag to display images for developing

	@Returns: processed striped or solid image (np.array)
	"""

	if kernel is None:
		kernel = np.ones((5,5), np.uint8)

	image = image [ :-4, :] # Crop out last 4 pixels 
	erosion = cv2.erode(image, kernel, iterations=1)
	dilation = cv2.dilate(erosion, kernel, iterations=1)
	_, thresh = cv2.threshold(dilation,200,255,1)


	if debug:
		cv2.imshow("erosion", erosion)
		cv2.imshow("dilation", dilation)
		cv2.imshow("After processing:", thresh)
		cv2.waitKey(0)

	return thresh


def detectShapeCount(processed_img, debug=False):
	""" Input takes in a processed image, either from processHollow() or processStripesFull()
	@Parameters: processed_img (np.array), processed after one of two functions
	@Return: Tuple of the shape, and the count (int, count)
	Shape is a global variable (DIAMOND, OVAL, or SQUIGGLE) which is an int
	"""
	_, contours, _ = cv2.findContours(processed_img, 1, 2)

	shape = []
	for cnt in contours:
		perim = cv2.arcLength(cnt, True) 
		approx = cv2.approxPolyDP(cnt, 0.01*perim, True) 
		
		if len(approx) == 4:
			shape.append(DIAMOND)
		elif len(approx) < 12: # Determined by trial and error
			shape.append(OVAL)
		else:
			shape.append(SQUIGGLE) # Squiggle range from 13, 14, 15 ... 
	
	# print(contours,shape)

	return shape[0], len(shape) - 1 



if __name__ == "__main__":

	import argparse

	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="path to the input image")
	ap.add_argument("-f", "--filled", help="fill", action="store_true")
	ap.add_argument("-e", "--empty", help="empty", action="store_true")
	ap.add_argument("-s", "--striped", help="striped", action="store_true")
	args = vars(ap.parse_args())

	image = cv2.imread(args['image'],0)
	kernel = np.ones((5,5), np.uint8)

	if args['empty']:
		x = processHollow(image)
	else:
		x = processStripesFull(image, kernel, 0, True)

	print(detectShapeCount(x))
	cv2.imshow("the image is" ,image)
	cv2.waitKey(0)

