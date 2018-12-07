""" Main module for creation of the Card object 
@author odoland
"""

import numpy as np
import cv2


import SetCard
from SetCard import DIAMOND, SQUIGGLE, OVAL
from SetCard import PURPLE, GREEN, RED
from SetCard import HOLLOW, STRIPE, FULL
from SetCard import ONE, TWO, THREE 

from FillDetect import is_Stripe, Hollow_or_Full 
from ShapeDetect import processHollow, processStripesFull, detectShapeCount
from ColorDetect import find_Color, is_Blank, has_Tint


KERNEL = np.ones((5,5), np.uint8) # Kernel for the erosion and dilation (for solid /hollow only)
PURPB = np.array ([80, 0, 80]), np.array([160,60,160])
GREENB = np.array([0,100,0]), np.array([45,180,45])
REDB = np.array([0,0,160]), np.array([30,30,255])


def create_Card(img_path, kernel, debug=False):
	""" Creates a SetCard object from an image.
	@Parameters img (path to the file)
	Pass in the path to the image file and a kernel - will generate the card
	"""
	image = cv2.imread(img_path) # colored 
	image0 = cv2.imread(img_path, 0) # grayscale

	# Color detection
	color, pixel_count = find_Color(image, PURPB, GREENB, REDB)

	# Fill detection
	if is_Stripe(image0,12):
		fill = STRIPE
	else:
		fill = Hollow_or_Full(image0, KERNEL,color,pixel_count)

	if fill == HOLLOW: # The solid green oval shapes may be mistakenly taken as hollow
		processed_img = processHollow(image0)
	else: 
		processed_img = processStripesFull(image0, KERNEL)
 	
 	# Shape & count detection
	shape, count = detectShapeCount(processed_img)
	
	if debug:
		print("creating a card:")
		print(f"shape{shape}")
		print(f"color{color}")
		print(f"fill{fill}")
		print(f"count{count}")

	return SetCard(shape,color,fill,count)

if __name__ == '__main__':
	import argparse

	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="Path to the set card img")
	ap.add_argument("-d", "--debug", action="store_true") # flag for debug
	args = vars(ap.parse_args())

	image = args['image']

	# image = image [ 4 :-4]
	# image0 = image0 [ 4 :-4] (optional cropping)

	debug = args['debug']

	s_card = create_Card(image,KERNEL,debug) # call function in debug mode
	print(f"That is a {s_card}")


