
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import numpy as np
import cv2
import time
import base64

from roboset import Robot
from random import choice

PATH_TO_CHROME_DRIVER = '/Users/orlando/Projects/roboset/chromedriver'
URL = 'localhost:3000'
SLEEP_BETWEEN_CLICKS = 0.15

class RobotDriver:
    """Robot Driver that links Robot instance with selenium web driver """
    def __init__(self, path=PATH_TO_CHROME_DRIVER, url=URL, delay=SLEEP_BETWEEN_CLICKS):
        self.driver = webdriver.Chrome(executable_path=path)
        self.delay = delay

        self.canvas_list = None # will be populated after call to .start()
        self.robot = Robot() # Robot instance for finding the sets
        self.start(url)

    def start(self, url):
        self.driver.get(url)
        time.sleep(0.5)
        self.canvas_list = self.driver.find_elements(By.CLASS_NAME,"Card-Canvas")

    def scan_card_images(self, directory='./images'):
        
        self.canvas_list = self.driver.find_elements(By.CLASS_NAME,"Card-Canvas")

        image_paths = [] # List of paths for each file ['1.png', '2.png' .. etc]

        # Crop an image for each button
        for i, canvas in enumerate(self.canvas_list):
            # get the canvas as a PNG base64 string
            canvas_base64 = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
            
            # decode
            canvas_png = base64.b64decode(canvas_base64)
                # https://stackoverflow.com/questions/38316402/how-to-save-a-canvas-as-png-in-selenium
            
            img_path = f"{directory}/{i}.png"
            # save to a file
            with open(img_path, 'wb') as f:
                f.write(canvas_png)
            
            img = cv2.imread(img_path)

            # Inverts black to white backgrounds, and resaves file
            img[np.where((img==[0,0,0]).all(axis=2))] = [255, 255, 255]
            cv2.imwrite(img_path, img)
            
            image_paths.append(img_path)
        
        # Load the image files into images
        self.robot.load_robot_brain(image_paths=image_paths)


    def find_sets_and_click(self):
        match = choice(self.robot.find_sets())
        
        for i, canvas_element in enumerate(self.canvas_list):
            if self.robot.cards_list[i] in match:
                canvas_element.click()
                time.sleep(self.delay)

    def unclick_all(self):
        self.driver.execute_script("document.getElementById('reset-clicked').click()")

