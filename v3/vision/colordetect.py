"""
Color Detection Module
author @odoland
"""
import cv2
import numpy as np
from attributes import Colors


class ColorDetector:

    # BGR format
    GREEN_RANGE = np.array([0, 100, 0]), np.array([45, 180, 45])
    RED_RANGE = np.array([0, 0, 160]), np.array([30, 30, 255])
    PURPLE_RANGE = np.array([80, 0, 80]), np.array([160, 60, 160])

    @classmethod
    def find_color(cls, image):
        """ Finds the color of an image based on maximum count for the three colors.

        @Returns at tuple: t
        t[0] Returns the color in number format (0 for purp, 1 for green, 2 for red)
        t[1] Returns the count
        """

        # Filter image for whatever passes the boundaries
        greens = cv2.inRange(image, *cls.GREEN_RANGE)
        reds = cv2.inRange(image, *cls.RED_RANGE)
        purples = cv2.inRange(image, *cls.PURPLE_RANGE)

        mg = len(np.flatnonzero(greens))
        mr = len(np.flatnonzero(reds))
        mp = len(np.flatnonzero(purples))

        colors = (mg, mr, mp)

        total_pixels = max(colors)
        
        enum_colors = [Colors.GREEN, Colors.RED, Colors.PURPLE]
        color_idx = int(np.argmax(colors))

        return enum_colors[color_idx], total_pixels


if __name__ == '__main__':

    import argparse
    from matplotlib import pyplot as plt

    # Arguments 
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="Path to the set card img")
    ap.add_argument("-g", "--debug", action="store_true")
    args = vars(ap.parse_args())


    # Grab options
    image = cv2.imread(args['image'])

    debug = args['debug']  # for graphing

    colors = ["green", "red", "purple"]

    # Create the Color
    index_of_color, total_pixels = ColorDetector.find_color(image) 

    print("The color is:", colors[index_of_color])

    if debug:
        calc = cv2.calcHist([res], [2], None, [256], [0, 256])
        max_channel = max(calc)
        plt.plot(calc)
        plt.show()

    if debug:

        color = ('b', 'g', 'r')  # OpenCV's format - also for matplotlib
        hist_colors = {}

        cutoff_range = [0, 256]  # ignore the whites - they are 255
        for channel, col in enumerate(color):

            calc = cv2.calcHist([img], [channel], None, [256], cutoff_range)
            max_channel = max(calc[0:255])  # no one cares about the other crap
            hist_colors[col] = int(max_channel)
            plt.plot(calc, color=col)
            plt.xlim(cutoff_range)

        plt.title('Histogram for color scale picture')
        plt.xlabel("Pixel intensity"), plt.ylabel("counts")
        plt.show()
        print(hist_colors)
