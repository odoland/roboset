"""
Color Detection Module
author @odoland
"""
import cv2
import numpy as np


def is_Blank(image):
	""" Checks to see if an image is the "Blank unclickable Card"
	Blank Cards BGR values are:
	 B: 151, G: 203, R: 237 
	@Parameters: raw image 
	@Returns: Boolean
	"""
	return np.array_equal(image[30,30],np.array([151,204,237]))

def has_Tint(image, tintbs, tintbg):
	""" Checks to see if the image has the Green tint - which means that card was a succesful 
	@Paramters: image (raw image) np.array
	tintbs (tuple of np.array (length 3 of BGR values)) for boundary- success - green)
	tintbf(tuple of np.array (length 3 of BGR values)) for boundary - failure - grey )
	@Returns boolean
	"""
	lower_success, upper_success = tintbs
	lower_fail, upper_fail = tintbg
	img = image[10,10]
	return (all(img > lower_success) and all(img < upper_success))



def find_Color(image, purpb, greenb, redb ):
	""" Finds the Color of an image based on the maximum count amongst the three boundaries.
	@Paramters: image: Pass in an image lower and upper boundaries for each purple, green, red in BGR format
	purpb  (tuple of np.array (length 3 of BGR values)) for boundary - purple)
	greenb (tuple of np.array (length 3 of BGR values)) for boundary - green)
	redb  (tuple of np.array (length 3 of BGR values)) for boundary - red)
	
	@Returns at tuple: t
	t[0] Returns the color in number format (0 for purp, 1 for green, 2 for red)
	t[1] Returns the count
	"""
	
	lower_purp, upper_purp = purpb
	lower_green, upper_green = greenb
	lower_red, upper_red = redb

	# Filter image for whatever passes the boundaries
	purples = cv2.inRange(image, lower_purp, upper_purp)
	greens = cv2.inRange(image, lower_green, upper_green)
	reds = cv2.inRange(image, lower_red, upper_red)

	mp = len(np.flatnonzero(purples))
	mg = len(np.flatnonzero(greens))
	mr = len(np.flatnonzero(reds))

	colors = (mp, mg, mr)

	total_pixels = max(colors)
	
	return colors.index(total_pixels), total_pixels


# DEBUG MODE:
if __name__ == '__main__':
	
	import argparse
	from matplotlib import pyplot as plt
	from SetCard import *

	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="Path to the set card img")
	ap.add_argument("-g", "--debug", action="store_true") 
	args = vars(ap.parse_args())

	image = cv2.imread(args['image'])

	debug = args['debug'] # for graphing
	
	colors = ["purple", "green", "red"]

	purpb = np.array ([80, 0, 80]), np.array([160,60,160])
	greenb = np.array([0,100,0]), np.array([45,180,45])
	redb = np.array([0,0,160]), np.array([30,30,255])

	print("It is Blank:",is_Blank(image))
	print(colors[find_Color(image, purpb, greenb, redb)[0]])
	print(find_Color(image, purpb, greenb, redb)[1])

	if debug:
		calc= cv2.calcHist( [res], [2] , None, [256], [0,256])
		max_channel = max(calc)
		plt.plot(calc)
		plt.show()


	if debug:

		color = ('b','g','r') # OpenCV's format - also for matplotlib
		hist_colors = {}

		cutoff_range = [0,256] # ignore the whites - they are 255
		for channel, col in enumerate(color):

			calc = cv2.calcHist([img], [channel], None, [256], cutoff_range) 
			max_channel = max(calc[0:255]) # no one cares about the other crap
			hist_colors[col] = int(max_channel)
			plt.plot(calc, color = col)
			plt.xlim(cutoff_range)


		plt.title('Histogram for color scale picture')
		plt.xlabel("Pixel intensity"), plt.ylabel("counts")
		plt.show()
		print((hist_colors))