# Test if this produces the correct card ID

import numpy as np
import cv2




from SetCard import *
from ColorDetect import *
from FillDetect import *
from ShapeDetect import *

KERNEL = np.ones((5,5), np.uint8) # Kernel for the erosion and dilation (for solid /hollow only)
PURPB = np.array ([80, 0, 80]), np.array([160,60,160])
GREENB = np.array([0,100,0]), np.array([45,180,45])
REDB = np.array([0,0,160]), np.array([30,30,255])



def create_Card(img, kernel):
	""" 
	Pass in the path to the image file
	"""


	image = cv2.imread(img)
	image0 = cv2.imread(img,0) # BW


	color, pixel_count = find_Color(image, PURPB, GREENB, REDB)

	if is_Stripe(image0,12):
		fill = STRIPE
	else:
		fill = Hollow_or_Full(image0, KERNEL,color,pixel_count)

	

	if fill == HOLLOW: # The solid green oval shapes may be mistakenly taken as hollow
		processed_img = processHollow(image0)
	else: 
		processed_img = processStripesFull(image0, KERNEL)
 
	shape, count = detectShapeCount(processed_img)
	

	debug = False
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

	s_card = create_Card(image,KERNEL) # call function in debug mode
	print(s_card)

