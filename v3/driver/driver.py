
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import numpy as np
import cv2
import time
import base64

# TODO: screenshot alignments not working 
if __name__ == "__main__":

    PATH_TO_CHROME_DRIVER = '/Users/orlando/Projects/roboset/chromedriver'

    # URL = 'https://hills.ccsf.edu/~jfyfe/set.html'
    URL = 'localhost:3000'

    chrome_options = Options()

    driver = webdriver.Chrome(executable_path=PATH_TO_CHROME_DRIVER, options=chrome_options)
    driver.get(URL)

    time.sleep(2)

    # Grab a screenshot, load it into array
    driver.save_screenshot('temp.png')
    screenshot = cv2.imread('temp.png')

    print(screenshot.shape) # 1712 x 2880
    win_size = driver.get_window_size() # 1440 x 900
    aw, ah = win_size['width'], win_size['height']


    # Grab location of all canvas elements:
    canvas_list = driver.find_elements(By.CLASS_NAME,"Card-Canvas")

    # Crop an image for each button
    for i, canvas in enumerate(canvas_list):
        # get the canvas as a PNG base64 string
        canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
        
         # decode
        canvas_png = base64.b64decode(canvas_base64)
            # https://stackoverflow.com/questions/38316402/how-to-save-a-canvas-as-png-in-selenium
        # save to a file
        with open(f"{i}.png", 'wb') as f:
            f.write(canvas_png)
        
        img = cv2.imread(f"{i}.png")

        # TODO: Mask where all 3 channels are 0 --> into 255
        img[np.where((img==[0,0,0]).all(axis=2))] = [255, 255, 255]
        cv2.imwrite(f"{i}.png", img)



