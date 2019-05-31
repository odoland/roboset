"""
Shape Detection and Shape counter Module
author @odoland
"""
from __future__ import absolute_import
import cv2
import numpy as np
import matplotlib
matplotlib.use("TkAgg") # Use TkAgg as backend to plot stuff  

from matplotlib import pyplot as plt
from .attributes import Shapes, Fills, Counts
from .filldetect import FillDetector

class ShapeDetector:

    KERNEL = np.ones((5,5), np.uint8)

    @classmethod
    def process_hollow(cls, image, threshold=200, debug=False):
        """ Processes the image file if it is a hollow image by converting it into a solid.
        @Parameters: image (np.array) 3 dimensions
                    threshold (int) - threshold value for BW - default at 200
                    debug (boolean) - flag to display the images for developing
        @Returns: processed image (np.array)
        """

        # Threshold image to black and white.
        ret, thresh_clean = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)
        im_floodfill = thresh_clean.copy()
        
        # Floodfill the image
        h, w = im_floodfill.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        cv2.floodFill(im_floodfill, mask, (0,0), 255); # Fill from (0,0)
        im_floodfill_inv = cv2.bitwise_not(im_floodfill) # Invert the fill

        if debug: # debug mode to show pictures and print to stdout
            cv2.imshow("threshold clean", thresh_clean)
            cv2.imshow("Floodfilled", im_floodfill)
            cv2.imshow("inv floodfill", im_floodfill_inv)
            cv2.waitKey(0)

        return im_floodfill_inv

    @classmethod
    def process_stripes_full(cls, image, threshold=200, debug=False ):
        """ Processes Stripes and Full image by 1 iteration of blur and erosion.
        
        @Parameters: image (np.array) 
                    kernel (default is  kernel = np.ones((5,5), np.uint8)
                    threshold (int) threshold value for BW - default 200
                    debug (boolean) - flag to display images for developing

        @Returns: processed striped or solid image (np.array)
        """

        erosion = cv2.erode(image, cls.KERNEL, iterations=1)
        dilation = cv2.dilate(erosion, cls.KERNEL, iterations=1)
        _, thresh = cv2.threshold(dilation,200,255,1)


        if debug:
            cv2.imshow("erosion", erosion)
            cv2.imshow("dilation", dilation)
            cv2.imshow("After processing:", thresh)
            cv2.waitKey(0)

        return thresh

    @staticmethod
    def detect_shape_count(processed_img, debug=False):
        """ Input takes in a processed image, either from processHollow() or processStripesFull()
        @Parameters: processed_img (np.array), processed after one of two functions
        @Return: Tuple of the shape, and the count (int, count)
        Shape is a global variable (DIAMOND, OVAL, or SQUIGGLE) which is an int
        """
        _, contours, _ = cv2.findContours(processed_img, 1, 2)

        shape = []
        for cnt in contours:
            perim = cv2.arcLength(cnt, closed=True)  # Squiggles have a longer perimeter
            approx = cv2.approxPolyDP(cnt, epsilon=0.01*perim, closed=True)  # prev 0.01
            
            if len(approx) == 4:
                shape.append(Shapes.DIAMOND)
            elif len(approx) < 11 and perim < 250: # Determined by trial and error
                shape.append(Shapes.OVAL)
            else:
                shape.append(Shapes.SQUIGGLE) # Squiggle range from 13, 14, 15 ... 
        
        mapping = {
            1: Counts.ONE, 
            2: Counts.TWO,
            3: Counts.THREE
        }
        if len(shape) not in mapping:
            if shape[0] == Shapes.SQUIGGLE:
                amount = mapping[len(shape)//2] # probably the 2 green squiggles solid
            else:
                print('Run debugger. Something wrong w/ counts, not a squiggle', shape)
                amount = 2
        else:
            amount = mapping[len(shape)]
        # Amount of shapes detected -> map to an enum
        return shape[0], amount

    @classmethod
    def find_shape_count(cls, image, debug=False):
        
        bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if FillDetector.find_fill(image, plot=0) == Fills.HOLLOW:
            if debug:
                print("Processing it as a hollow")
            processed_img = cls.process_hollow(bw_image, debug=debug)
        else:
            if debug:
                print("Processing as stripes or full")
            processed_img = cls.process_stripes_full(bw_image, debug=debug)

        return cls.detect_shape_count(processed_img, debug) 

if __name__ == "__main__":

    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    ap.add_argument("-f", "--filled", help="fill", action="store_true")
    ap.add_argument("-e", "--empty", help="empty", action="store_true")
    ap.add_argument("-s", "--striped", help="striped", action="store_true")
    args = vars(ap.parse_args())

    image = cv2.imread(args['image'])

    print(ShapeDetector.find_shape_count(image))

