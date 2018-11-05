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
from CardGen import * # the connection from the eyes to the brain
from itertools import combinations # to slow down the code 

import argparse

debug = True
count = 12

# BGR format
TINTBS = np.array([200,250,200]),  np.array([235,255,235]) # Green tint boundary is 225,253,225
TINTBG = np.array([200,200,200]), np.array([225,225,225]) # Grey tint is 217, 217, 217


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

BUTTONS = driver.find_elements(By.CLASS_NAME,"button") 
CARDS_LIST = [None]*15 # List of SetCard objects

def checkPossibleSets(force=False):
	""" 
	Reads for remaining possible sets
	"""
	global count
	remain_sets = int(driver.find_element_by_xpath('//*[@id="setcounter"]').text[-1])
	
	while remain_sets == 0:
		remain_sets = int(driver.find_element_by_xpath('//*[@id="setcounter"]').text[-1])
		driver.find_element_by_xpath('/html/body/button[2]').click()
		count += 1
		time.sleep(1) 
	if force:
		driver.find_element_by_xpath('/html/body/button[2]').click()


def delay(func):
	""" Delaying decorator """
	def wrapper(*args):
		time.sleep(1)
		func(*args)
	return wrapper

@delay
def find_Sets_iter(debug=False):
	
	global count 
	clean = [c for c in CARDS_LIST if c is not None]
	combos = combinations(clean,3)

	if debug:
		debug_display = [(str(card), card.hash()) for card in clean]
		print(f"clean BUTTONS are: {debug_display} ")
	

	for combo in combos:
		
		if SetCard.isSet(*combo):
			
			a, b, c = combo
			if debug:
				print(f"yay i found a set:{a} {b} {c}")
	
			if a != b and a != c and b != c:
				aa = CARDS_LIST.index(a) 
				bb = CARDS_LIST.index(b)
				cc = CARDS_LIST.index(c)
			else: # Handle self duplicates
				aa = CARDS_LIST.index(a)
				bb = CARDS_LIST.index(b, aa+1)
				cc = CARDS_LIST.index(c, bb+1)

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
		
		button = BUTTONS[idx]
		location, size = button.location, button.size
		x, y, h, w = location['x'], location['y'], size['height'], size['width']
		cardimg = allsets[y:y+h, x:x+w]
		
		img_path = f"button{idx}.png" # Path to save the image
		cv2.imwrite(img_path, cardimg) # Debug check
		img = cardimg, cv2.cvtColor(cardimg, cv2.COLOR_BGR2GRAY)

		# If there is a tint, pause, let the page load, and then retake the pic
		if has_Tint(cardimg,TINTBS,TINTBG):
			print(f" Found a tint, gonna wait a bit {idx}")
			time.sleep(1)
			driver.save_screenshot('allsets.png')
			allsets = cv2.imread('allsets.png') 
			idx -= 1 
		else:
			CARDS_LIST[idx] = create_Card(img_path, KERNEL)

def update_Screen(*idx_list):
	""" Updates the screen. Pass in the index for """
	driver.save_screenshot('allsets.png')
	allsets = cv2.imread('allsets.png') 	


@delay
def click_Sets(*idx_list):
	""" Pass in the indices of the three cards for thedriver to click, will also reupdate the CARDS_LIST idx """
	for idx in idx_list:
		BUTTONS[idx].click()
	
	time.sleep(1) # Wait for the screen to complete

	driver.save_screenshot('allsets.png')
	allsets = cv2.imread('allsets.png') 

	for idx in idx_list:
		button = BUTTONS[idx] # Obtain the button element
		# crop out the button image
		location, size = button.location, button.size
		x, y, h, w = location['x'], location['y'], size['height'], size['width']
		cardimg = allsets[y:y+h, x:x+w]
		
		img_path = f"button{idx}.png" # Path to save the image
		cv2.imwrite(img_path, cardimg) # Debug check
		img = cardimg, cv2.cvtColor(cardimg, cv2.COLOR_BGR2GRAY)

		# If there is a tint, pause, let the page load, and then retake the pic
		if has_Tint(cardimg,TINTBS,TINTBG):
			print(f" Found a tint, gonna wait a bit {idx}")
			time.sleep(1)
			driver.save_screenshot('allsets.png')
			allsets = cv2.imread('allsets.png') 
			idx -= 1 
		else:
			CARDS_LIST[idx] = create_Card(img_path, KERNEL)



for i in range(30):
	count = 12

	print(" Next Iteration ")


	# time.sleep(sleep_time)
	
	checkPossibleSets()

	process_Screen_slowly()

	print(CARDS_LIST, "before finding sets")
	find_Sets_iter()
	print(CARDS_LIST, "after")
	
	# checkPossibleSets()

	process_Screen_slowly()
	time.sleep(sleep_time)







		








