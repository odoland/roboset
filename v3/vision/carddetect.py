"""Detects the card """

from colordetect import ColorDetector
from filldetect import FillDetector
from shapedetect import ShapeDetector

class CardDetector:

    @staticmethod
    def detect_card(image):
        color = ColorDetector.find_color(image)
        fill = FillDetector.find_fill(image)
        shape, count = ShapeDetector.find_shape_count(image)

        return {
            'color': color,
            'fill': fill,
            'shape': shape,
            'count': count
        }

    @classmethod
    def pretty_print_detect_card(cls, image):
        card_attributes = cls.detect_card(image)
        colors = ["PURPLE", "GREEN", "RED"]
        color_idx, pixel_count = card_attributes['color']

        color = colors[color_idx]
        count = card_attributes['count']
        shape = card_attributes['shape']
        fill = card_attributes['fill']
        print(count, color, fill, shape)

if __name__ == "__main__":
    import argparse
    import cv2

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    ap.add_argument("-f", "--filled", help="fill", action="store_true")
    ap.add_argument("-e", "--empty", help="empty", action="store_true")
    ap.add_argument("-s", "--striped", help="striped", action="store_true")
    args = vars(ap.parse_args())

    # image = cv2.imread(args['image'])
    # CardDetector.pretty_print_detect_card(image)
    for i in range(19):
        image = cv2.imread(f"{args['image']}/{i}.png")
        CardDetector.pretty_print_detect_card(image)
