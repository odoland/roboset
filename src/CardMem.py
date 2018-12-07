""" Class for the Robot's Memory (CardMem)
author @odoland
"""

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

SLEEP = 0.2


class Roboset:
	""" Robot to play set"""

	def __init__(self, buttons_list):		
		

		self.cards_list = [None]*15
		self.cards_map = {}
		self.buttons = buttons_list
		self.count = 12 # count of the cards


	def find_Sets(self):	

		# Produce a list of cards that are currently clickable for the Robot
		clickable = [card for card in self.cards_list if card is not None]
		length = len(clickable)
		self.count = length

		i = 0
		while i < self.count-1 and self.cards_list[i] is not None:
			j = i + 1
			while j < self.count and self.cards_list[j] is not None:
				
				card1, card2 = self.cards_list[i], self.cards_list[j]
				print(f"check {card1} {card2}")
				
				"""
				# Handle 3-of-a-kind
				if card1 == card2 and len(self.cards_map[card1.hash()]) == 3:
					button_idx= self.cards_map[self.cards_list[i].hash()].pop()
					self.cards_map.pop(self.cards_list[i].hash())
					self.click_Sets(button_idx)
					self.update_card_memory(button_idx)
				"""

				if card1 and card2:  # Handle regular set
					card3 = SetCard.getMatch(card1,card2)
					c1key, c2key, c3key = card1.hash(), card2.hash(), card3.hash()

					if c1key == c2key and len(self.cards_map[c1key]) == 3: # three of a kind
						
						print(f"Yay! I found three of a kind! {c1key} {c2key} {c3key}")
						card1_idx = self.cards_map[c1key].pop()
						card2_idx = self.cards_map[c2key].pop()
						card3_idx = self.cards_map[c3key].pop()

						if len(self.cards_map[c1key]) == 0:
							self.cards_map.pop(c1key)

						self.click_Sets(card1_idx, card2_idx, card3_idx)
						self.update_card_memory(card1_idx,card2_idx,card3_idx)

					elif c3key in self.cards_map and c1key != c2key: # Found a match

						print(f"Yay! I found a set! {c1key}, {c2key}, {c3key}")

						card1_idx = self.cards_map[c1key].pop()
						card2_idx = self.cards_map[c2key].pop()
						card3_idx = self.cards_map[c3key].pop()

						for key in [c1key,c2key,c3key]: # Remove when empty
							if len(self.cards_map[key]) == 0:
								self.cards_map.pop(key)

						self.click_Sets(card1_idx, card2_idx, card3_idx)
						self.update_card_memory(card1_idx,card2_idx,card3_idx)
				j += 1 # increment inner j loop
			i += 1 # increment outer i loop
					
	def update_card_memory(self,*idx_list):
		""" Updates the memory the self.cards_list and the cards_map. Updates only the indexes passed in """

		driver.save_screenshot('allsets.png')
		allsets = cv2.imread('allsets.png')

		if len(idx_list) == 0: # Means we are initializing, so we will update all buttons
			idx_list = range(len(self.buttons))
		
		for idx in idx_list:

			
			# Crop until get a valid picture
			while True:

				button = self.buttons[idx]
				# Crop button image out
				location, size = button.location, button.size
				x, y, h, w = location['x'], location['y'], size['height'], size['width']
				cardimg = allsets[y:y+h, x:x+w]

				img_path = f"button{idx}.png"
				cv2.imwrite(img_path, cardimg)
				imagepair = cardimg, cv2.cvtColor(cardimg, cv2.COLOR_BGR2GRAY) # regular color and also grayscale

				if has_Tint(cardimg,TINTBS, TINTBG):
					print(f"Found a tint in image, waiting a bit")
					time.sleep(0.2)
					driver.save_screenshot('allsets.png')
					allsets = cv2.imread('allsets.png')
				else:
					break

			# Card creation
			try:
				self.cards_list[idx] = create_Card(img_path, KERNEL)
				key = self.cards_list[idx].hash()
				# Update cards_map
				if key not in self.cards_map:
					self.cards_map[key] = [idx]
				else:
					self.cards_map[key].append(idx)

			except (TypeError, ValueError) as e: # Bumped into a blank
				print(f"Bumped into a blank card at index {idx}")
				self.cards_list[idx] = None 
		
	def click_Sets(self,*idx_list):
		""" Clicks the buttons, and sleeps a little bit """
		if len(idx_list) != 3:
			print(idx_list)
		for idx in idx_list:
			self.buttons[idx].click()

		self.count = 12 

		time.sleep(0.1)

	@staticmethod
	def checkPossibleSets(force=False):
		""" 
		Reads for remaining possible sets. Returns max index added
		"""
		remain_sets = int(driver.find_element_by_xpath('//*[@id="setcounter"]').text[-1])
		
		count = 0
		while remain_sets == 0:
			remain_sets = int(driver.find_element_by_xpath('//*[@id="setcounter"]').text[-1])
			driver.find_element_by_xpath('/html/body/button[2]').click()
			time.sleep(1)
			count += 1
		if force:
			driver.find_element_by_xpath('/html/body/button[2]').click()
			count += 1

		return True
		





if __name__ == '__main__':

	import argparse
	
	TINTBS = np.array([200,250,200]),  np.array([235,255,235]) # Green tint boundary is 225,253,225
	TINTBG = np.array([200,200,200]), np.array([225,225,225])
	
	# PATH_TO_CHROME_DRIVER = '/Users/elisaur/Desktop/PythonScripts/autograder/chromedriver'
	PATH_TO_CHROME_DRIVER = '/home/orlando/Projects/Autograder/chromedriver.exe'

	URL = 'https://hills.ccsf.edu/~jfyfe/set.html'

	ap = argparse.ArgumentParser()

	# Full Screen - to take full screenshot
	chrome_options = Options()
	chrome_options.add_argument("--kiosk")

	driver = webdriver.Chrome(executable_path=PATH_TO_CHROME_DRIVER, chrome_options=chrome_options)
	driver.get(URL)

	time.sleep(2)

	buttons_list = driver.find_elements(By.CLASS_NAME,"button") 
	card_memory = Roboset(buttons_list)

	Roboset.checkPossibleSets()
	card_memory.update_card_memory()

	while True:
		card_memory.find_Sets()
		extra_slot = Roboset.checkPossibleSets()
		if extra_slot: 
			card_memory.update_card_memory()

		


