from vision.carddetect import CardDetector
from vision.filldetect import FillDetector
from vision.colordetect import ColorDetector
from vision.shapedetect import ShapeDetector

if __name__ == "__main__":
    import argparse
    import cv2

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    ap.add_argument("-a", "--all", help="Run the full detector on an entire directory", action="store_true")
    ap.add_argument("-f", "--fill", help="Run the fill detector", action="store_true")
    ap.add_argument("-c", "--color", help="Run the color detector", action="store_true")
    ap.add_argument("-s", "--shape", help="Run the shape detector", action="store_true")
    args = vars(ap.parse_args())


    if args['fill']:
        image_path = args['image']
        image = cv2.imread(image_path)
        print(FillDetector.find_fill(image, plot=True))
    elif args['color']:
        image_path = args['image']
        image = cv2.imread(image_path)
        print(ColorDetector.find_shape_count(image, debug=True))
    elif args['shape']:
        image_path = args['image']
        image = cv2.imread(image_path)
        print(ShapeDetector.find_shape_count(image, debug=True))
    elif args['all']:
        directory = args['image']
        print("Scanning all files under directory:", directory)
        for i in range(19):
            image_path = f"{directory}/{i}.png"
            print("Checking...", image_path, end="|")
            CardDetector.pretty_print_detect_card(image_path)
    else:
        print("Detecting card:")
        CardDetector.pretty_print_detect_card(image_path)

    
        
    


    