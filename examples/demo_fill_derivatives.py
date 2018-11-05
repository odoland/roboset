import cv2
import numpy as np
from scipy.signal import argrelextrema
from scipy.signal import find_peaks
import peakutils
import argparse

from matplotlib import pyplot as plt 
from ColorDetect import find_Color
from SetCard import PURPLE, GREEN, RED



ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("-d", "--debug", action="store_true")
args = vars(ap.parse_args())

debug = args['debug']

color_image = cv2.imread(args['image'])
image = cv2.imread(args['image'],0) # read image in BW 
image = image [ 4 :-4, :] # Numpy slice the last 4 pixels (noise removal)

kernel = np.ones((5,5), np.uint8) # Kernel for the erosion and dilation

def is_stripe(image, number_peaks,debug=False):
	""" Returns boolean, if striped. Parameters: threshold for peaks """

	# First we take the derivative (f'(x)) on the y-axis to see if there are crazy changes
	

	fpx = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
	vpr= cv2.reduce(fpx, 1, cv2.REDUCE_SUM)
	
	vpr_p= np.sqrt(vpr**2).flatten()

	# Each change or "stripe" is essentially a peak on the f'(x). 
	unfiltered_peaks, _ = find_peaks(vpr_p, height=0)
	all_peaks = (vpr_p[i] for i in unfiltered_peaks)
	peak_thresh = max(all_peaks) * 0.33 # arbitrary weight 1/3 of the max_peak
	filtered_peaks = [i for i in unfiltered_peaks if vpr_p[i] >= peak_thresh] 

	if debug:
		plt.plot(vpr_p), plt.title(f"f'(x) of the striped image!")
		plt.plot(filtered_peaks, vpr_p[filtered_peaks], "x")
		plt.show()


	return len(filtered_peaks) > number_peaks

stripe = False
if is_stripe(image,12,debug):
	print("striped")
	stripe=True

else:

	erosion = cv2.erode(image,kernel,iterations=1)		
	dilation = cv2.dilate(erosion,kernel,iterations=1)
	_, thresh = cv2.threshold(dilation,200,255,1)


	first_deriv_y = cv2.Sobel(thresh, cv2.CV_64F, 0,1,ksize=5)
	vpr_1y = cv2.reduce(first_deriv_y, 1, cv2.REDUCE_SUM)
	
	# for the y ######## y
	vpr_1y_p = np.sqrt(vpr_1y**2).flatten()

	# Find every peak index, and access the height of the peak
	unfiltered_peaks_y, _ = find_peaks(vpr_1y_p, height=0)
	all_peaks_y = (vpr_1y_p[i] for i in unfiltered_peaks_y)
	
	# I just arbitrarily set the threshold to .32 (noise reduction)
	peak_thresh_y = max(all_peaks_y) * .32 # cuto ff is 1/3rd of the highest peak

	approx_peaks_y= sum(1 for i in unfiltered_peaks_y if vpr_1y_p[i] >= peak_thresh_y)

	filtered_peaks_y = [i for i in unfiltered_peaks_y if vpr_1y_p[i] >= peak_thresh_y]
	approx_peaks_y = len(filtered_peaks_y)


	print(approx_peaks_y, "approx peaks found")
	PURPB = np.array ([80, 0, 80]), np.array([160,60,160])
	GREENB = np.array([0,100,0]), np.array([45,180,45])
	REDB = np.array([0,0,160]), np.array([30,30,255])
	
	color, pixel_count = find_Color(color_image, PURPB, GREENB, REDB)

	if approx_peaks_y == 6:
		print("diamond, hollow")
	elif approx_peaks_y == 2:
		print("solid")
	elif approx_peaks_y == 4:
		 # unique case . can be either hollow or a solid oval
		if color == GREEN and pixel_count > 3500:
			print("solid green oval")
		else:
			print("hollow")


if debug and not stripe:
	print("debugger mode plotting stuff now:")
	# f(x) 
	img = 255 - image
	vertical_project = np.sum(img, axis=1).tolist()

	# Plot f(x)
	plt.plot(vertical_project), plt.title('y direction f(x)')
	plt.show()

	# Plot f'(x), f''(x)
	plt.plot(vpr_1y_p), plt.title("y direction f'(x)")
	plt.plot(filtered_peaks_y, vpr_1y_p[filtered_peaks_y], "x") # plot the peaks too
	plt.show()

	

	# f pp x (f "" x )
	# fppx = cv2.Sobel(fpx, cv2.CV_64F, 0, 1, ksize=5)
	# vpr_2= cv2.reduce(fppx, 1, cv2.REDUCE_SUM)
	# plt.subplot(121),plt.plot(vpr_2),plt.title("f''(x)")
	# plt.show()


	plt.imshow(erosion), plt.title("eroded")
	plt.show()
	plt.imshow(dilation), plt.title("dilated")
	plt.show()
