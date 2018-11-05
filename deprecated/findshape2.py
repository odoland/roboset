import cv2
import argparse
from matplotlib import pyplot as plt 
import numpy as np 

#@Debug
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args['image'],0) # read image in BW 

kernel = np.ones((5,5), np.uint8) # 5x5 Kernel of ones for erosion / dilation
image = image [ :-4, :] # Crop out last 4 pixels 
erosion = cv2.erode(image, kernel, iterations=1)
dilation = cv2.dilate(erosion, kernel, iterations=1)


# f(x) is pixel intensity (y-axis) vs. y coordinate (vertical)
# Plots the y-axis projection of f(x)
img = 255 - image
vertical_project = np.sum(img, axis=1).tolist()

# Plot f(x)
plt.plot(vertical_project), plt.title('f(x)')
plt.show()

# Plots y axis projection of f'(x) and f''(x)
first_deriv_y = cv2.Sobel(image, cv2.CV_64F, 0,1,ksize=5)
second_deriv_y = cv2.Sobel(first_deriv_y, cv2.CV_64F, 0,1, ksize=5)
vpr_1 = cv2.reduce(first_deriv_y, 1, cv2.REDUCE_SUM)
vpr_2 = cv2.reduce(second_deriv_y, 1, cv2.REDUCE_SUM)

# Plot f'(x), f''(x)
plt.subplot(121), plt.plot(vpr_1), plt.title("f'(x)")
plt.subplot(122),plt.plot(vpr_2),plt.title("f''(x)")
plt.show()

# Plot dilation image
plt.subplot(121), plt.imshow(dilation), plt.title("After dilation")
plt.xticks([]), plt.yticks([])
plt.show()


def slopechange(pair, slope_thresh):
	 # https://stackoverflow.com/questions/27947487/is-zip-the-most-efficient-way-to-combine-arrays-with-respect-to-memory-in-nump
	 a,b = pair
	 difference = abs(a[0] - b[0])
	 return difference > slope_thresh

# Track changes in each derivative
vpr_max_peak = max(vpr_1)
spike_thresh = vpr_max_peak * 0.6

changes = sum(1 for pair in zip(vpr_1, vpr_1[1:]) if slopechange(pair,spike_thresh)) # count how many times the slope changes in the y-direction from the Sobel
print(f"Number of changes detected passing threshold of {spike_thresh} is: {changes}")

vpr2_max_peak = max(vpr_2)
print(vpr2_max_peak)
vpr2_spike_thresh = vpr2_max_peak * 0.6

slope_changes = sum(1 for pair in zip(vpr_2, vpr_2[1:]) if slopechange(pair,vpr2_spike_thresh)) # count how many times the slope changes in the y-direction from the Sobel
print(f"Number of changes for 2nd deriv detected passing threshold of {vpr2_spike_thresh} is: {slope_changes}")






cv2.destroyAllWindows()