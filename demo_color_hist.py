import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt
from SetCard import *



debug = True

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args['image'])

img = image[4:-4] # crop the edge pixels

colors = (PURPLE, GREEN, RED)


# When we sucessfully find a set, the whole card is highighted with this green tint.
# We want to raise an exception when this is found
lower_success = np.array([200,250,200])  # Green tint is 225,253,225
upper_success = np.array([235,255,235])
lower_fail = np.array([200,200,200]) # Grey titn is 217, 217, 217
upper_fail = np.array([225,225,225])

green_tint = (all(img[10,10] > lower_success) and all(img[10,10] < upper_success))
grey_tint = (all(img[10,10]> lower_fail) and all(img[10,10] < upper_fail ))

if green_tint:
	print("Dude, this card is already used, or wrong answer!")
if grey_tint:
	print("Dude, unclick this button!")


# lower and upper range of "purple"
lower_purp = np.array ([80, 0, 80])
upper_purp = np.array([160,60,160])
purples = cv2.inRange(img,lower_purp,upper_purp)

# lower and upper range of "green"
lower_green = np.array([0,100,0])
upper_green = np.array([45,180,45])
greens = cv2.inRange(img, lower_green, upper_green)

# lower and upper range of "red"
lower_red = np.array([0,0,160])
upper_red = np.array([30,30,255])
reds = cv2.inRange(img, lower_red, upper_red)

# Mask the crazy stuff
mg = len(np.flatnonzero(greens))  # Faster than: sum(1 for i in mask_green.ravel() if i > 0) 
mr = len(np.flatnonzero(reds))
mp = len(np.flatnonzero(purples))

col = [mp, mg, mr]
print ( colors[col.index(max(col))] )



if debug:
	print("green,red,purp")
	print(mg,mr,mp)

print()





# cv2.imshow('orig', image)
# cv2.imshow('mask', mask_green)
# cv2.imshow('result', res)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# calc hist
# channel 0 = blue,
# channel 1 = green
# channel 2 = red 


		
