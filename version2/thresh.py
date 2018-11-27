import cv2

from sklearn.externals import joblib
import matplotlib.pyplot as plt

import re
import argparse
import numpy as np
from math import exp

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image', required=True, help='path to image')
args = vars(ap.parse_args())
path = args['image']



# Reading the image
image = cv2.imread(path,0)

# Series: Thresholding -> Canny Edge -> dilate -> 
_, thresh = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
edge = cv2.Canny(thresh,100,200)
kernel = np.ones((5,5), np.uint8)
dilation = cv2.dilate(edge, kernel, iterations=3)
blur = cv2.blur(dilation, (5,5))


dilation = thresh

### Haar Cascades ###
# https://docs.opencv.org/3.4.3/d7/d8b/tutorial_py_face_detection.html  

_, contours, _ = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# Draw contour against a black background
size = image.shape
blank = np.zeros((*size,3))
newimage = cv2.drawContours(blank, contours, -1, (0,200,205), 10) 


plt.subplots_adjust(hspace=0.7)
plt.subplot(3,3,1), plt.title('Original'), plt.imshow(image, cmap='gray')
plt.subplot(3,3,2,), plt.title('Threshold'), plt.imshow(edge, cmap='gray')
plt.subplot(3,3,3), plt.title('Dilation'), plt.imshow(dilation, cmap='gray')
plt.subplot(3,3,4), plt.title('blur'), plt.imshow(blur, cmap='gray')
plt.subplot(3,3,5), plt.title('contours'), plt.imshow(newimage)

# plt.subplot(2,2,3), plt.title('dilation'), plt.imshow(dilation)
plt.show()





