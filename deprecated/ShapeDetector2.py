# This section will handle hollows - using a floodfill
import cv2
import argparse
from matplotlib import pyplot as plt 
import numpy as np 


def processHollow(image,threshold=200,debug=False):
	""" Floods the outside to deal with the hollow shapes for more accurate shape detection """

	# convert to just B/W
	ret, thresh_clean = cv2.threshold(image,threshold,255,1)
	
	im_floodfill = thresh_clean.copy()
	
	# Mark used to flood filling
	h, w = im_floodfill.shape[:2]
	mask = np.zeros( (h+2, w+2), np.uint8)
	cv2.floodFill(im_floodfill, mask, (0,0), 255); # Fill from the corner
	im_floodfill_inv = cv2.bitwise_not(im_floodfill) # Invert the fill

	if debug: # debug mode print to stdout
		cv2.imshow("Thresholded image", thresh)
		cv2.imshow("Floodfilled", im_floodfill)
		cv2.imshow("inv floodfill", im_floodfill_inv)
		cv2.waitKey(0)

	return im_floodfill_inv

def processStripesSolid(image, kernel, threshold=200, debug=False ):
	""" default kernel is just, kernel = np.ones((5,5), np.uint8) """
	image = image [ :-4, :] # Crop out last 4 pixels 
	erosion = cv2.erode(image, kernel, iterations=1)
	dilation = cv2.dilate(erosion, kernel, iterations=1)
	ret, thresh = cv2.threshold(dilation,200,255,1)

	if debug:
		cv2.imshow("erosion", erosion)
		cv2.imshow("dilation", dilation)
		cv2.imshow("processed stripe:", thresh)
		cv2.waitKey(0)

	return thresh


def detectShape(processed_img, debug=False):
	_, contours, _ = cv2.findContours(processed_img,1,2)

	shape = ""
	for cnt in contours:
		perim = cv2.arcLength(cnt, True) # approx perim
		approx = cv2.approxPolyDP(cnt, 0.01*perim,True) # approximate the contours/ vertices 
		print(len(approx), end = " ")
		if len(approx) == 4:
			shape = "diamond"
		elif len(approx) < 12:
			shape = "oval"
		else:
			shape = "squiggle"

	if debug:
		print(shape)

	return shape

# for debugging
if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="path to the input image")
	ap.add_argument("-f", "--fill", help="fill")
	args = vars(ap.parse_args())

	image = cv2.imread(args['image'],0)
	kernel = np.ones((5,5), np.uint8)
	if args['fill'] == 'h':
		x = processHollow(image)
	else:
		x = processStripes(image,kernel,0)

	print(detectShape(x))



