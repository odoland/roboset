"""
Fill Detection Module
author @odoland
"""

import cv2
import numpy as np
from scipy.signal import find_peaks

import matplotlib
matplotlib.use("TkAgg") # Use TkAgg as backend to plot stuff  
import matplotlib.pyplot as plt
from colordetect import ColorDetector

import itertools as it


class FillDetector:

    # Threshold for the peaks
    PEAK_THRESH = 0.33
    KERNEL = np.ones((5,5), np.uint8) # For erosion and dilation

    @classmethod
    def is_stripe(cls, image, number_peaks=12, plot=False):  # -> Boolean
        """ Checks if the image is striped.
        @Parameters: image matrix (binary form - black and white)
                    number_peaks (int) Number of peaks to be considered 'striped'

        @Returns Boolean, if striped.
        """
        
        _, w , _ = image.shape
        
        # Spot to go down the Y axis
        spot = np.floor(w * 0.45).astype(int)
    
        # Use the Sobel operator across the Y to obtain the Gradient
        sobel_gradient = cv2.Sobel(image[:, spot], cv2.CV_64F, 0, 1, ksize=5)  # vertical

        # Project it onto single dimension (1D) - by summing them
        projected_sum = cv2.reduce(sobel_gradient, 1, cv2.REDUCE_SUM)

        # Squaring and square rooting removes the negative sign, and flatten
        proj_pos_sums = np.sqrt(projected_sum**2).flatten()
        
        # Large spikes on f'(x) indicate change in the rate of change - seek areas where slope of the second derivative is 0
        unfiltered_peaks, _ = find_peaks(proj_pos_sums, height=0)  # Finding peaks

        # Filter the peaks for noise which will be defined as any peak with an absolute height of less than PEAK_THRESH * maximum peak length
        all_peaks = [proj_pos_sums[i] for i in unfiltered_peaks]

        peak_thresh = max(all_peaks) * cls.PEAK_THRESH

        seen = set()
        filtered_peaks = ([
            i for i in unfiltered_peaks 
            if proj_pos_sums[i] >= peak_thresh 
            # and not (proj_pos_sums[i] in seen or seen.add(proj_pos_sums[i]))
            ])

        if plot:
            plt.plot(proj_pos_sums), plt.title("f'(x) of the image")
            plt.plot(filtered_peaks, proj_pos_sums[filtered_peaks], "x")
            plt.show()
            print("Calling is_stripe:", len(filtered_peaks), "peaks found")
        return len(filtered_peaks) > number_peaks

    @classmethod
    def check_hollow_or_full(cls, image, color, pixel_count, plot=False):  # -> Returns either SetCard.HOLLOW or SetCard.FULL
        """ Checks if the image is Hollow or Full
        @Parameters: image matrix (binary form - black and white)
                    color (int - Global Variable: SetCard.GREEN, SetCard.PURPLE, SetCard.RED)
                    pixel_count (count of the pixels)
        @Returns A shape (integer), which is a SetCard.HOLLOW or SetCard.FULL  """

        # Image preprocessing - magnification of the thinly drawn hollow images to help with detecting peaks
        erosion = cv2.erode(image, cls.KERNEL, iterations=1)
        dilation = cv2.dilate(erosion, cls.KERNEL, iterations=1)
        _, thresh = cv2.threshold(dilation, 200, 255, cv2.THRESH_BINARY_INV)  # Threshold cut off value at 200 (white)

        _, w = image.shape
        spot = np.floor(w * 0.45).astype(int)

        # Use the Sobel operator across the Y to obtain the Gradient, projecting & removing negative signs
        first_deriv_y = cv2.Sobel(thresh[:, spot], cv2.CV_64F, 0, 1, ksize=5)
        vpr_1y = cv2.reduce(first_deriv_y, 1, cv2.REDUCE_SUM)
        
        # Group by will remove constant values of increase, such as the increasing slope from the diamond shapes
        vpr_1y = np.array([k for (k,), v in it.groupby(list(vpr_1y))])
        vertical_projection = np.sqrt(vpr_1y**2).flatten()

        # Find every peak index, and access the height of the peak
        unfiltered_peaks_indices, _ = find_peaks(vertical_projection, height=0)
        all_peak_heights = (vertical_projection[i] for i in unfiltered_peaks_indices) # Grab the peak heights

        peak_thresh_y = max(all_peak_heights) * (cls.PEAK_THRESH)
        filtered_peaks = [i for i in unfiltered_peaks_indices if vertical_projection[i] >= peak_thresh_y] 


        approx_peaks_y = len(filtered_peaks)
        print("Peaks found:", approx_peaks_y)
        if plot:
            plt.plot(vertical_projection), plt.title("f'(x) of the image")
            plt.plot(filtered_peaks, vertical_projection[filtered_peaks], "x")
            plt.show()
            print("Calling check_hollow_or_full:", len(filtered_peaks), "peaks found")

        if approx_peaks_y == 2:
            return "FULL"
        elif approx_peaks_y == 4:
            return "HOLLOW"
        else:
            print("there are some weird peak counts", approx_peaks_y)
            return "HOLLOW"

    @classmethod
    def find_fill(cls, image, plot=False):
        if cls.is_stripe(image, plot=plot):
            return "STRIPE"
        else:
            color, pixel_count = ColorDetector.find_color(image)
            bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return cls.check_hollow_or_full(bw_image, color, pixel_count, plot=plot)

if __name__ == '__main__':
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    ap.add_argument("-d", "--debug", action="store_true")
    ap.add_argument("-g", "--green_oval", action="store_true", help="is a solid green oval")

    args = vars(ap.parse_args())

    debug = args['debug']

    color_image = cv2.imread(args['image'])

    print(FillDetector.find_fill(color_image, True))
