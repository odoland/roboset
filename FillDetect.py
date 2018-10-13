# Functions to figure out the fill
import cv2
import numpy as np 

from scipy.signal import argrelextrema
from scipy.signal import find_peaks
import peakutils

from SetCard import HOLLOW, STRIPE, FULL


# First process the stripe:
def is_Stripe(image, number_peaks=12):
	""" Returns boolean, if striped. Parameters: threshold for peaks """

	# First we take the derivative (f'(x)) on the y-axis to see if there are crazy changes
	fpx = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
	vpr= cv2.reduce(fpx, 1, cv2.REDUCE_SUM)
	vpr_p= np.sqrt(vpr**2).flatten()

	# Each change or "stripe" is essentially a peak on the f'(x). 
	unfiltered_peaks, _ = find_peaks(vpr_p, height=0)
	all_peaks = (vpr_p[i] for i in unfiltered_peaks)
	peak_thresh = max(all_peaks) * 0.33 # arbitrary weight 1/3 of the max_peak
	
	filtered_peaks = sum(1 for i in unfiltered_peaks if vpr_p[i] >= peak_thresh)
	
	return (filtered_peaks) > number_peaks

def Hollow_or_Full(image,kernel):
	""" Pass in an erosion/dilation kernel. Image must be cv2.imread(image,0)  """

	# erode/dilate to magnify the thin pixels
	erosion = cv2.erode(image,kernel,iterations=1)		
	dilation = cv2.dilate(erosion,kernel,iterations=1)
	_, thresh = cv2.threshold(dilation,200,255,1)

	# mark the change from white to black
	first_deriv_y = cv2.Sobel(thresh, cv2.CV_64F, 0,1,ksize=5)
	vpr_1 = cv2.reduce(first_deriv_y, 1, cv2.REDUCE_SUM)
	vpr_1_p = np.sqrt(vpr_1**2).flatten()

	# Find every peak index, and access the height of the peak
	unfiltered_peaks, _ = find_peaks(vpr_1_p, height=0)
	all_peaks = (vpr_1_p[i] for i in unfiltered_peaks)
	
	# I just arbitrarily set the threshold to .32 (noise reduction)
	peak_thresh = max(all_peaks) * .32 # cuto ff is 1/3rd of the highest peak


	approx_peaks = sum(1 for i in unfiltered_peaks if vpr_1_p[i] >= peak_thresh)

	if approx_peaks == 6: # is also a diamond
		return HOLLOW 
	elif approx_peaks == 2:
		return FULL
	elif approx_peaks == 4:
		return HOLLOW 



if __name__ == '__main__':
	import argparse
	from matplotlib import pyplot as plt 

	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="path to the input image")
	ap.add_argument("-d", "--debug", action="store_true")
	args = vars(ap.parse_args())

	debug = args['debug']
	image = cv2.imread(args['image'],0) # read image in BW 
	image = image [ 4 :-4] # Numpy slice the last 4 pixels (noise removal)

	kernel = np.ones((5,5), np.uint8) # Kernel for the erosion and dilation

	if is_Stripe(image,12): # using 12 
		print("is a stripe")
	else:
		fill = Hollow_or_Full(image, kernel)
		if fill == FULL:
			print("is full")
		elif fill == HOLLOW:
			print("is a hollow")
