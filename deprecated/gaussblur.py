import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('button3.png')
gauss_blur = cv2.GaussianBlur(image, (5,5), 0)

print(image, gauss_blur)

plt.subplot(121), plt.imshow(image), plt.title('BEFORE_BLUR:')
plt.subplot(122), plt.imshow(gauss_blur), plt.title('AFTER_BLUR:')


plt.show()