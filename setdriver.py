from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


import numpy as np
import cv2
import time

from SetCard import *
from ColorDetect import *
from FillDetect import *



PATH_TO_CHROME_DRIVER = '/Users/elisaur/Desktop/PythonScripts/autograder/chromedriver'
URL = 'https://hills.ccsf.edu/~jfyfe/set.html'

# Full Screen - to take full screenshot
chrome_options = Options()
chrome_options.add_argument("--kiosk")

driver = webdriver.Chrome(executable_path=PATH_TO_CHROME_DRIVER, chrome_options=chrome_options)
driver.get(URL)



def checkPossibleSets():
	""" Scrape possible sets from the HTML """
	remain_sets = int(driver.find_element_by_xpath('//*[@id="setcounter"]').text[-1])
	while remain_sets == 0:
		remain_sets = int(driver.find_element_by_xpath('//*[@id="setcounter"]').text[-1])
		driver.find_element_by_xpath('/html/body/button[2]').click()


def processImage(img):
	""" Returns a named tuple """ 
	# Open CV reads in BGR
	# Top corner Coordinates - gets color and count  (x,y) (   ,   )      (103, 20)   ( ) 
	return sum(numeric(shape=shape, color=color, fill=fill, count=count))


cards_list = [None]*16 # Stores numerical value (namedtuple) - (shape,color,fill, number)
buttons = driver.find_elements(By.CLASS_NAME,"button") # type: list

checkPossibleSets()
time.sleep(1)


driver.save_screenshot('allsets.png')
setss = cv2.imread('allsets.png')

## Get initial pic of all the cards
for idx, button in enumerate(buttons):
	if cards_list[idx] is None:
		# Crop the image
		location, size = button.location, button.size
		x, y, h, w = location['x'], location['y'], size['height'], size['width']
		cardimg = allsets[y:y+h, x:x+w]
		cv2.imwrite(f"button{idx}.png", cardimg) # Debug check
		







