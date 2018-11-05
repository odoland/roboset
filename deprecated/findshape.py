import cv2
import argparse
from matplotlib import pyplot as plt
import numpy as np 

# @DEBUG
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())
image = cv2.imread(args['image'], 0)

# IMAGE PROCESS: mostly just to erode the stupid stripes that cause shape recognition failures
kernel = np.ones((5,5), np.uint8) # Kernel for the erosion and dilation
image = image[ :-4 , :] # crop out the last 4 pixels
erosion = cv2.erode(image,kernel,iterations=1)		
dilation = cv2.dilate(erosion,kernel,iterations=1)


# PLOT: EROSION
"""
plt.subplot(121), plt.imshow(erosion), plt.title("erosion")
plt.xticks([]),plt.yticks([])
plt.show()
cv2.imwrite('houghlines.png',edges)
"""


# Sobel derivatives - for determining - stripes  
# slopes in y direction (top down) (first derivative)
gradient_y = cv2.Sobel(image, cv2.CV_64F,0,1,ksize=5) # Previously: Kernel 5x5, but swapped to 3x3 because it's an (almost) noiseless image
second_deriv_y = cv2.Sobel(gradient_y, cv2.CV_64F, 0, 1, ksize=5)
vpr = cv2.reduce(gradient_y, 1, cv2.REDUCE_SUM) # reduce to be projected onto the y-axis -> into 1D array of all the points
vpr2 = cv2.reduce(second_deriv_y,1, cv2.REDUCE_SUM)

# vertical projection - for black pixels 
# https://stackoverflow.com/questions/13320262/calculating-the-area-under-a-curve-given-a-set-of-coordinates-without-knowing-t
img = 255-image
vertical_project = np.sum(img,axis=1).tolist() # sums the y-axis (row by row)
plt.plot(vertical_project)
plt.show()

# TODO: possibly we can use numpy column stack https://stackoverflow.com/questions/27947487/is-zip-the-most-efficient-way-to-combine-arrays-with-respect-to-memory-in-nump
def slopechange(pair,thresh):
	""" Returns true when a negative slope changes to positive slope or vice versa """
	a,b = pair
	difference = abs(a[0] - b[0]) # extract the float values of each 
	# sign_change = (a < 0 and b > 0 ) or (a > 0 and b < 0)
	# print(difference, "difference", difference > thresh, thresh, "sign change?", sign_change)
	return difference > thresh

vpr_max_peak = max(vpr)
print(vpr_max_peak)
spike_thresh = vpr_max_peak * 0.6

changes = sum(1 for pair in zip(vpr, vpr[1:]) if slopechange(pair,spike_thresh)) # count how many times the slope changes in the y-direction from the Sobel
print(f"Number of changes detected passing threshold of {spike_thresh} is: {changes}")

vpr2_max_peak = max(vpr2)
print(vpr2_max_peak)
vpr2_spike_thresh = vpr2_max_peak * 0.6

slope_changes = sum(1 for pair in zip(vpr2, vpr2[1:]) if slopechange(pair,vpr2_spike_thresh)) # count how many times the slope changes in the y-direction from the Sobel
print(f"Number of changes for 2nd deriv detected passing threshold of {vpr2_spike_thresh} is: {slope_changes}")


# track the slope changes for the line/curve matches 
# diamond shape would have 4
# squiggle will have multiple (most)
# oval would have some 
# we can also get count

# color 

ret, thresh = cv2.threshold(dilation,200,255,1) # Set thresh at 200 - essentially removes the stripes
# cv2.imwrite("bw.png",dilation)
 


# PLOT: SHOW THE SOBEL DERIVATIVES
# print(vpr)
plt.subplot(121), plt.plot(vpr), plt.title('vertical projections')
plt.subplot(122),plt.plot(vpr2),plt.title("second derivative, projection vertical")
plt.show()


################
# PLOT: SHOW THE EFFECT AFTER DILATION
plt.subplot(121), plt.imshow(dilation), plt.title("thresh")
plt.xticks([]),plt.yticks([])
plt.show()




cv2.destroyAllWindows()
