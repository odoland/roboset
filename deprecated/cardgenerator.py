# Test if this produces the correct card ID

import numpy as np
import cv2
import argparse



from SetCard import *
from ColorDetect import *
from FillDetect import *
from ShapeDetect import *


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the set card img")
ap.add_argument("-d", "--debug", action="store_true") # flag for debug
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
image0 = cv2.imread(args['image'],0)
# image = image [ 4 :-4]
# image0 = image0 [ 4 :-4] (optional cropping)

debug = args['debug']

kernel = np.ones((5,5), np.uint8) # Kernel for the erosion and dilation (for solid /hollow only)
purpb = np.array ([80, 0, 80]), np.array([160,60,160])
greenb = np.array([0,100,0]), np.array([45,180,45])
redb = np.array([0,0,160]), np.array([30,30,255])



if is_Stripe(image0,12):
	fill = STRIPE
else:
	fill = Hollow_or_Full(image0, kernel)

color = find_Color(image, purpb, greenb, redb)

if fill == HOLLOW:
	processed_img = processHollow(image0)
else:
	processed_img = processStripesFull(image0, kernel)

shape, count = detectShapeCount(processed_img)

card = SetCard(shape,color,fill,count)

print(card)