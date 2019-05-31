from vision.carddetect import CardDetector
from vision.filldetect import FillDetector

if __name__ == "__main__":
    import argparse
    import cv2

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    ap.add_argument("-f", "--filled", help="fill", action="store_true")
    ap.add_argument("-e", "--empty", help="empty", action="store_true")
    ap.add_argument("-s", "--striped", help="striped", action="store_true")
    args = vars(ap.parse_args())

    image_path = args['image']
    # CardDetector.pretty_print_detect_card(image_path)
    
    image = cv2.imread(image_path)
    print(FillDetector.find_fill(image, False))

    # for i in range(0,19):
    #     image_path = f"{args['image']}/{i}.png"
    #     print("Checking...", image_path, end="|")
    #     CardDetector.pretty_print_detect_card(image_path)