import numpy as np
import cv2



def produce_feature_vector(image, debug=False):
	
	image = cv2.imread(image)
	# Convert to HSV for second mask
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	purp_hsv = np.array([140, 30, 30]) , np.array ([160, 255, 255])
	red_hsv = np.array([0, 30, 30]), np.array([10, 255, 255])
	green_hsv = np.array([50, 30, 30]), np.array( [70, 255, 255])

	purple_mask = cv2.inRange(hsv, *purp_hsv)
	red_mask = cv2.inRange(hsv, *red_hsv)
	green_mask = cv2.inRange(hsv, *green_hsv)

	purp = cv2.bitwise_and(image, image, mask=purple_mask)
	red = cv2.bitwise_and(image, image, mask=red_mask)
	green = cv2.bitwise_and(image, image, mask=green_mask)

	features = []
	for color in [purp, red, green]:
		gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
		_, thresh = cv2.threshold(color, 150, 255, cv2.THRESH_BINARY_INV)
		final_result = cv2.bitwise_and(color, color, mask=thresh[...,0])
		features.append(final_result)

	ftr = np.array( [len(np.flatnonzero(ft)) for ft in features])

	vector = ftr / np.sum(ftr)


	if debug:
		cv2.imshow('Original', image)
		cv2.imshow('Purple Mask', red)
		cv2.imshow('purple only', features[1] )
		# cv2.imshow('thresh', thresh)
		# cv2.imshow('final', final_result)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	return vector

if __name__ == '__main__':

	"""
	import argparse

	# Parse Arguments
	ap = argparse.ArgumentParser()
	ap.add_argument('-i','--image', required=True, help="Path 2 image")
	args = vars(ap.parse_args())
	image = cv2.imread(args['image'])

	# Resize Image
	height, width, channel = image.shape
	if height > 300 or width > 300:
		image = cv2.resize(image, (width//10, width//10))
	"""

	# Produce training set
	features_train = []
	labels_train = []

	import re
	pat = r'red|green|purple'

	print('Opening image file for read...')
	with open("images.txt") as inpfile:
		for line in inpfile:
			label = re.findall(pat,line)[0]
			feat = produce_feature_vector('img/' + line.strip())

			features_train.append(feat)
			labels_train.append(label)


	print('Performing fit...')
	from sklearn.naive_bayes import GaussianNB

	clf = GaussianNB()
	clf.fit(features_train, labels_train)

	features_test = []
	with open('predict.txt') as predfile:
		for line in predfile:
		 	feat = produce_feature_vector('img/' + line.strip())
		 	features_test.append(feat)
	
	print('Predictions: ', clf.predict(features_test))
	





# Mask 2: W
# lower_white = np.array([0, 0, 0])
# upper_white = np.array([180, 215, 215])

# mask = cv2.inRange(hsv, lower_white, upper_white)
# result = cv2.bitwise_and(result_1, result_1, mask=mask)

