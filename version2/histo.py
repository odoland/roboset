
from SetCard import DIAMOND, SQUIGGLE, OVAL
from SetCard import PURPLE, GREEN, RED
from SetCard import HOLLOW, STRIPE, FULL
from SetCard import ONE, TWO, THREE

from sklearn import svm
import numpy as np 
import cv2

from sklearn.externals import joblib
import matplotlib.pyplot as plt

import re
import argparse


def preprocess(path):
	""" processes images first 
	"""
	
	_, thresh = cv2.theshold(image, 127, 255, cv2.THRESH_BINARY_INV)



	_, contours, _ = cv2.findContours(thresh,1,2)

	for cnt in contours:
		approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
		print(len(approx))

	backtorgb = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
	newimage = cv2.drawContours(backtorgb, contours, -1, (0,255,0), 3)
	

def color_feature(path, mkplot=False):
	""" Creates a BGR 'vector' feature from the image by obtaining the maximum

	Args:
		path (str) : path to the image file (.jpg or .png OK)
		mkplot (boolean) : whether or not to make  histogram plot (for debugging or visual purposes)

	Returns:
		BGR (list <int>) : # of counts in BGR (percentage) 
	"""

	img = cv2.imread(path)
	colors = ('b', 'g', 'r')

	cutoff_range = [30, 255] # Because the low pixel values are really faint and unneeded
	BGR = []

	for channel, color in enumerate(colors):

		histo = cv2.calcHist( [img], [channel], None, [255], cutoff_range)
		BGR.append(np.amax(histo)) # Save the pixel intensity of the highest peak
		
		plt.plot(histo, color = color)
		plt.xlim(cutoff_range)
		#plt.ylim([])

	total = np.sum(BGR)
	BGR = [channel/total for channel in BGR]

	if mkplot:
		print(BGR)
		plt.title('Histogram for color scale')
		plt.xlabel('Pixel intensity for each channel'), plt.ylabel("Counts")
		plt.show()


	
	
	return BGR

if __name__ == '__main__':

	
	ap = argparse.ArgumentParser()
	ap.add_argument('-i', '--image', required=True, help='Path to image')
	ap.add_argument('-t', '--train', help='Do you want to train')

	args = vars(ap.parse_args())
	image = args['image']
	train = args['train']
	color_feature(image ,True)
	



	if train:

	
		features = []
		labels = []

		pattern = re.compile(r"(red|green|purple)")

		with open('images.txt', "r" ) as inp:

			for line in inp:
				
				img_name = line.strip()

				color = re.findall(pattern, img_name)[0]

				features.append(color_feature(img_name))
				labels.append(color)

		assert len(features) == len(labels)

		with open('feature_data.txt',"w") as out:
			for f , l in zip(features,labels):
				print(f, l, file=out)

		clf = svm.SVC(kernel='linear')
		clf.fit(features,labels)
		# joblib.dump(clf, 'colordetect.joblib') # later to be loaded as clf = joblib.load('filename.joblib')
		
		predictions = []
		with open('predict.txt', 'r') as pinp:

			for line in pinp:

				predictions.append(color_feature(line.strip()))

		pred = clf.predict(predictions)

	

	

