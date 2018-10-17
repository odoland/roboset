# Functions to figure out the fill
import cv2
import numpy as np 
from scipy.signal import find_peaks

from SetCard import HOLLOW, STRIPE, FULL, GREEN, RED, PURPLE
from ColorDetect import find_Color

# Arbitrary peak threshold value (as percentage of the maximum peak length)
PEAK_THRESH = 0.33 # my default is set at approx 1/3rd


def is_Stripe(image, number_peaks=12):
	""" Returns boolean, if striped. Parameters: threshold for the count of peaks to be qualified as a stripe.
	What work well so far as of 10/ """

	# Crop the edges
	image = image [ 4 :-4]

	# Seek crazy changing  rates across the y-axis of the image w/ Sobel algorithm to estimate the first derivative
	fpx = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5) # Take only the across y-axis (vertically)
	vpr= cv2.reduce(fpx, 1, cv2.REDUCE_SUM) # Project it onto a 1D np array
	vpr_p= np.sqrt(vpr**2).flatten() # Flip the signs of negative changes

	# Large spikes on f'(x) indicate change in the rate of change - seek areas where slope of the second derivative is 0
	unfiltered_peaks, _ = find_peaks(vpr_p, height=0) # Finding peaks
	all_peaks = (vpr_p[i] for i in unfiltered_peaks)
	peak_thresh = max(all_peaks) * PEAK_THRESH 
	filtered_peaks = sum(1 for i in unfiltered_peaks if vpr_p[i] >= peak_thresh)
	
	return (filtered_peaks) > number_peaks


def Hollow_or_Full(image, kernel, color, pixel_count):
	""" Pass in an erosion/dilation kernel. Image must be cv2.imread(image,0). Pass in the color and pixel_count reads
	from ColorDetect module.  """

	# Image preprocessing - magnification of the thinly drawn hollow. TODO: solids should be exempt
	erosion = cv2.erode(image,kernel,iterations=1)		
	dilation = cv2.dilate(erosion,kernel,iterations=1)
	_, thresh = cv2.threshold(dilation,200,255,1) # Threshold cut off value at 200 (white)

	# mark the change from white to black
	first_deriv_y = cv2.Sobel(thresh, cv2.CV_64F, 0,1,ksize=5)
	vpr_1y = cv2.reduce(first_deriv_y, 1, cv2.REDUCE_SUM)
	vpr_1y_p = np.sqrt(vpr_1y**2).flatten()

	# Find every peak index, and access the height of the peak
	unfiltered_peaks_y, _ = find_peaks(vpr_1y_p, height=0)
	all_peaks_y = (vpr_1y_p[i] for i in unfiltered_peaks_y)
	
	# I just arbitrarily set the threshold to .32 (noise reduction)
	peak_thresh_y = max(all_peaks_y) * .32 # cuto ff is 1/3rd of the highest peak
	approx_peaks_y= sum(1 for i in unfiltered_peaks_y if vpr_1y_p[i] >= peak_thresh_y)


	# Todo: Be replaced with an actual neural network
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
