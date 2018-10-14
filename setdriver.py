from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


import numpy as np
import cv2
import time

from SetCard import * # The Brain
from ColorDetect import * # The eyes
from FillDetect import * # more of the eyes
from cardgenerator import * # the connection from the eyes to the brain
from itertools import combinations # to slow down the code 

import argparse

debug = True
count = 12
TINTBS = np.array([200,250,200]),  np.array([235,255,235]) # Green tint boundary is 225,253,225
TINTBG = np.array([200,200,200]), np.array([225,225,225]) # Grey titn is 217, 217, 217


PATH_TO_CHROME_DRIVER = '/Users/elisaur/Desktop/PythonScripts/autograder/chromedriver'
URL = 'https://hills.ccsf.edu/~jfyfe/set.html'

ap = argparse.ArgumentParser()
ap.add_argument("-s","--sleep", required=True, help="Put in the sleep time (multiplied by 5) ")

args = vars(ap.parse_args())
sleep_time = int(args['sleep'])

# Full Screen - to take full screenshot
chrome_options = Options()
chrome_options.add_argument("--kiosk")

driver = webdriver.Chrome(executable_path=PATH_TO_CHROME_DRIVER, chrome_options=chrome_options)
driver.get(URL)


# has on sleep
def checkPossibleSets(force=False):
	""" 
	Scrape possible sets from the HTML.
	Returns the count of cards displayed
	Also updates the blankbuttons
	"""
	remain_sets = int(driver.find_element_by_xpath('//*[@id="setcounter"]').text[-1])
	global count
	 # the website starts with 12 cards 0 .. 11
	while remain_sets == 0:
		remain_sets = int(driver.find_element_by_xpath('//*[@id="setcounter"]').text[-1])
		driver.find_element_by_xpath('/html/body/button[2]').click()
		count += 1
		time.sleep(1) ## SLEEP
	if force:
		driver.find_element_by_xpath('/html/body/button[2]').click()

buttons = driver.find_elements(By.CLASS_NAME,"button") # type: list
# amt_buttons = len(buttons)

cards_list = [None]*15 # List of SetCard objects

cards_map = {}
# blank_button_idx = 15

cards = 12 # initially

def delay(func):
	""" decorator to delay"""
	def wrapper(*args):
		time.sleep(1)
		func(*args)
	return wrapper

# n**3 complexity
@delay
def find_Sets_iter():
	clean = [c for c in cards_list if c is not None]
	debug_display = [(str(card), card.hash()) for card in clean]
	print(f"clean buttons are: {debug_display} ")
	combos = combinations(clean,3)

	global count 
	for combo in combos:
		if SetCard.isSet(*combo):
			print("yay i found a set:")
			a, b, c = combo
			print(a,b,c)
			if a != b and a != c and b != c:
				aa = cards_list.index(a) 
				bb = cards_list.index(b)
				cc = cards_list.index(c)
			else:
				aa = cards_list.index(a)
				bb = cards_list.index(b, aa+1)
				cc = cards_list.index(c, bb+1)

			click_Sets(aa,bb,cc)
			count = 12 # reset value of count, cannot go below 12
			# break

	# else:
		# checkPossibleSets(force=True)

			

def process_Screen_slowly():
	driver.save_screenshot('allsets.png')
	
	allsets = cv2.imread('allsets.png')

	global count
	global sleeptime

	for idx in range(count):
		
		button = buttons[idx]
		location, size = button.location, button.size
		x, y, h, w = location['x'], location['y'], size['height'], size['width']
		cardimg = allsets[y:y+h, x:x+w]
		
		img_path = f"button{idx}.png" # Path to save the image
		cv2.imwrite(img_path, cardimg) # Debug check
		img = cardimg, cv2.cvtColor(cardimg, cv2.COLOR_BGR2GRAY)

		# If there is a tint, pause, let the page load, and then retake the pic
		if has_Tint(cardimg,TINTBS,TINTBG):
			print("Found a tint, gonna wait a bit")
			time.sleep(1) ### SLEEP
			idx -= 1 
		else:
			cards_list[idx] = create_Card(img_path, KERNEL)
			
		





@delay
def click_Sets(*idx_list):
	""" Pass in the indices of the three cards for thedriver to click """
	for idx in idx_list:
		time.sleep(0.1)
		buttons[idx].click()


for i in range(30):
	count = 12

	print(" Next Iteration ")

	# time.sleep(sleep_time)
	
	checkPossibleSets()

	process_Screen_slowly()

	find_Sets_iter()
	
	# checkPossibleSets()

	process_Screen_slowly()
	time.sleep(sleep_time)







		








