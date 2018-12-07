"""
Fill Detection Module
author @odoland
"""

import cv2
import numpy as np 
from scipy.signal import find_peaks

from SetCard import HOLLOW, STRIPE, FULL, GREEN, RED, PURPLE
from ColorDetect import find_Color

# Threshold for the peaks
PEAK_THRESH = 0.33 


def is_Stripe(image, number_peaks=12): # -> Boolean
	""" Checks if the image is striped.
	@Parameters: image matrix (binary form - black and white)
				number_peaks (int) Number of peaks to be considered 'striped'

	@Returns Boolean, if striped.
	"""

	# Crop the edges
	image = image [ 4 :-4]

	# Use the Sobel operator across the Y to obtain the Gradient
	fpx = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5) # vertical
	
	# Project it onto single dimension (1D) - by summing them
	vpr= cv2.reduce(fpx, 1, cv2.REDUCE_SUM)

	# Squaring and square rooting removes the negative sign, and flatten
	vpr_p= np.sqrt(vpr**2).flatten() 
	# Large spikes on f'(x) indicate change in the rate of change - seek areas where slope of the second derivative is 0
	unfiltered_peaks, _ = find_peaks(vpr_p, height=0) # Finding peaks
	
	# Filter the peaks for noise which will be defined as any peak with an absolute height of less than PEAK_THRESH * maximum peak length
	all_peaks = (vpr_p[i] for i in unfiltered_peaks)
	peak_thresh = max(all_peaks) * PEAK_THRESH 
	filtered_peaks = sum(1 for i in unfiltered_peaks if vpr_p[i] >= peak_thresh)
	
	return (filtered_peaks) > number_peaks


def Hollow_or_Full(image, kernel, color, pixel_count): # -> Returns either SetCard.HOLLOW or SetCard.FULL
	""" Checks if the image is Hollow or Full
	@Parameters: image matrix (binary form - black and white)
				kernel (5x5) kernel. Default: kernel = np.ones((5,5), np.uint8) (for erosion/ dilation)
				color (int - Global Variable: SetCard.GREEN, SetCard.PURPLE, SetCard.RED)
				pixel_count (count of the pixels)
	@Returns A shape (integer), which is a SetCard.HOLLOW or SetCard.FULL  """

	# Image preprocessing - magnification of the thinly drawn hollow images
	erosion = cv2.erode(image,kernel,iterations=1)		
	dilation = cv2.dilate(erosion,kernel,iterations=1)
	_, thresh = cv2.threshold(dilation,200,255, cv2.THRESH_BINARY_INV) # Threshold cut off value at 200 (white)

	# Use the Sobel operator across the Y to obtain the Gradient, projecting & removing negative signs
	first_deriv_y = cv2.Sobel(thresh, cv2.CV_64F, 0,1,ksize=5)
	vpr_1y = cv2.reduce(first_deriv_y, 1, cv2.REDUCE_SUM)
	vpr_1y_p = np.sqrt(vpr_1y**2).flatten()

	# Find every peak index, and access the height of the peak
	unfiltered_peaks_y, _ = find_peaks(vpr_1y_p, height=0)
	all_peaks_y = (vpr_1y_p[i] for i in unfiltered_peaks_y)
	
	peak_thresh_y = max(all_peaks_y) * (PEAK_THRESH-0.01) 
	approx_peaks_y= sum(1 for i in unfiltered_peaks_y if vpr_1y_p[i] >= peak_thresh_y)


	# 
	if approx_peaks_y == 6: # Is also a diamond # To do, add extra weight to that
		return HOLLOW 
	elif approx_peaks_y == 2:
		return FULL
	elif approx_peaks_y == 4: # Unique case . can be either hollow or a solid oval
		if color == GREEN and pixel_count > 3500: # Density of green cards approx, >3500 - PARAMETER
			return FULL
		else:
			return HOLLOW 
	else:
		raise TypeError("Cannot find fill type. Possibly invalid picture. ")



if __name__ == '__main__':
	import argparse
	from matplotlib import pyplot as plt 

	print("You've entered debugger mode :)")

	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="path to the input image")
	ap.add_argument("-d", "--debug", action="store_true")
	ap.add_argument("-g", "--green_oval", action="store_true", help="is a solid green oval")
	
	args = vars(ap.parse_args())

	debug = args['debug']

	PURPB = np.array ([80, 0, 80]), np.array([160,60,160])
	GREENB = np.array([0,100,0]), np.array([45,180,45])
	REDB = np.array([0,0,160]), np.array([30,30,255])

	color_image = cv2.imread(args['image'])
	image = cv2.imread(args['image'],0) # read image in BW 
	image = image [ 4 :-4] # Numpy slice the last 4 pixels (noise removal)
	# cv2.imshow("sliced", image)
	# cv2.waitKey(0)

	kernel = np.ones((5,5), np.uint8) # Kernel for the erosion and dilation

	color, pixel_count = find_Color(color_image,PURPB,GREENB,REDB)
	
	if is_Stripe(image,12): # using 12 
		print("is a stripe")
	else:
		fill = Hollow_or_Full(image, kernel,color, pixel_count)
		if fill == FULL:
			print("is full")
		elif fill == HOLLOW:
			print("is a hollow")
