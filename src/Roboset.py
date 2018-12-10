""" Class for the Robot's Memory (CardMem)
author @odoland
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import numpy as np
import cv2
import time

from SetCard import *  # The Brain
from ColorDetect import *  # The eyes
from FillDetect import *  # more of the eyes
from CardGen import *  # the connection from the eyes to the brain

SLEEP = 0.2


class PageLoadedIncorrectly(Exception):
	pass


class Roboset:
	""" Robot to play set"""

	def __init__(self, driver):
		""" Constructor for Roboset. Takes in the selenium webdriver """

		# Selenium counterpart
		self.driver = driver
		self.buttons = self._makeButtonList()  # List of Selenium button objects. (clickable)
		self.window_size = driver.get_window_size()  # Dictionary of width and height
		self.win_ratio = self._getWindowRatio()  # Gets ratio of device's screen and screenshot

		# Roboset's Memory
		self.cards_list = [None] * 15  # List of SetCard objects
		self.cards_map = {}  # Mapping of SetCards. Key: SetCard Hash value, Value: List of indexed positions of the card

		# Keep track of how many additional cards were added onto the field
		self.additional = 0

	def _makeButtonList(self):
		""" Uses the selenium driver to obtain all the buttons by HTML scraping """
		return self.driver.find_elements(By.CLASS_NAME, "button")

	def _getWindowRatio(self):
		""" Creates the window ratio for those incompatible screen devices like
		on a Windows
		"""
		# Get window size of the device
		win_height, win_width = self.window_size['height'], self.window_size['width']

		# Get size of the screenshot
		driver.save_screenshot('views/allsets.png')
		allsets = cv2.imread('views/allsets.png')
		pic_height, pic_width = allsets.shape[:2]

		width_ratio, height_ratio = win_width / pic_width, win_height / pic_height

		return width_ratio, height_ratio

	def find_Sets(self):
		""" Function finds sets out of the clickable buttons.
		1) Filters self.buttons_list for only clickable buttons
		2) Out of those clickable buttons, find the sets

		"""

		# Produce a list of cards that are currently clickable for the Robot
		# clickable = [card for card in self.cards_list if card is not None]

		i = 0
		while i < self.count - 1 and self.cards_list[i] is not None:
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
					card3 = SetCard.getMatch(card1, card2)
					c1key, c2key, c3key = card1.hash(), card2.hash(), card3.hash()

					if c1key == c2key and len(self.cards_map[c1key]) == 3:  # three of a kind

						print(f"Yay! I found three of a kind! {c1key} {c2key} {c3key}")
						card1_idx = self.cards_map[c1key].pop()
						card2_idx = self.cards_map[c2key].pop()
						card3_idx = self.cards_map[c3key].pop()

						if len(self.cards_map[c1key]) == 0:
							self.cards_map.pop(c1key)

						self.click_Sets(card1_idx, card2_idx, card3_idx)
						self.update_card_memory(card1_idx, card2_idx, card3_idx)

					elif c3key in self.cards_map and c1key != c2key:  # Found a match

						print(f"Yay! I found a set! {c1key}, {c2key}, {c3key}")

						card1_idx = self.cards_map[c1key].pop()
						card2_idx = self.cards_map[c2key].pop()
						card3_idx = self.cards_map[c3key].pop()

						for key in [c1key, c2key, c3key]:  # Remove when empty
							if len(self.cards_map[key]) == 0:
								self.cards_map.pop(key)

						self.click_Sets(card1_idx, card2_idx, card3_idx)
						self.update_card_memory(card1_idx, card2_idx, card3_idx)
				j += 1  # increment inner j loop
			i += 1  # increment outer i loop

	def update_card_memory(self, *idx_list):
		""" Updates the memory the self.cards_list and the cards_map. Updates only the indexes passed in """

		driver.save_screenshot('views/allsets.png')

		# win_width, win_height = self.window_size['width'], self.window_size['height']

		print("Window size: ", driver.get_window_size())
		allsets = cv2.imread('views/allsets.png')
		print("Image size:", allsets.shape[:2])

		if len(idx_list) == 0:  # Means we are initializing, so we will update all buttons
			idx_list = range(len(self.buttons))

		for i, button in enumerate(self.buttons):
			location, size = button.location, button.size
			x, y, h, w = location['x'], location['y'], size['height'], size['width']
			assert h == 136 and w == 210
			x + y

		# for idx in idx_list:
		# 	while True:

		# 		button = self.buttons[idx]
		# 		# Crop button image out
		# 		location, size = button.location, button.size
		# 		x, y, h, w = location['x'], location['y'], size['height'], size['width']
		# 		cardimg = allsets[y:y+h, x:x+w]

		# 		img_path = f"views/button{idx}.png"
		# 		cv2.imwrite(img_path, cardimg)
		# 		imagepair = cardimg, cv2.cvtColor(cardimg, cv2.COLOR_BGR2GRAY) # regular color and also grayscale

		# 		if has_Tint(cardimg,TINTBS, TINTBG):
		# 			print(f"Found a tint in image, waiting a bit")
		# 			time.sleep(0.2)
		# 			driver.save_screenshot('views/allsets.png')
		# 			allsets = cv2.imread('views/allsets.png')
		# 		else:
		# 			break

		# 	# Card creation
		# 	count_blank_cards = 0
		# 	try:
		# 		self.cards_list[idx] = create_Card(img_path, KERNEL)
		# 		key = self.cards_list[idx].hash()
		# 		# Update cards_map
		# 		if key not in self.cards_map:
		# 			self.cards_map[key] = [idx]
		# 		else:
		# 			self.cards_map[key].append(idx)

		# 	except (TypeError, ValueError) as e: # Bumped into a blank
		# 		print(f"Bumped into a blank card at index {idx}")
		# 		self.cards_list[idx] = None
		# 		count_blank_cards += 1
		# 		if count_blank_cards > 12:
		# 			raise PageLoadedIncorrectly

	def click_Sets(self, *idx_list):
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

	TINTBS = np.array([200, 250, 200]), np.array([235, 255, 235])  # Green tint boundary is 225,253,225
	TINTBG = np.array([200, 200, 200]), np.array([225, 225, 225])

	# PATH_TO_CHROME_DRIVER = '/Users/elisaur/Desktop/PythonScripts/autograder/chromedriver'
	PATH_TO_CHROME_DRIVER = '/home/orlando/Projects/Autograder/chromedriver.exe'

	URL = 'https://hills.ccsf.edu/~jfyfe/set.html'

	ap = argparse.ArgumentParser()

	# Full Screen - to take full screenshot
	chrome_options = Options()
	chrome_options.add_argument("--kiosk")

	driver = webdriver.Chrome(executable_path=PATH_TO_CHROME_DRIVER)  # options=chrome_options)
	driver.get(URL)

	time.sleep(2)

	robot = Roboset(driver)

	print(len(robot.buttons))
	try:
		robot.update_card_memory()
	except PageLoadedIncorrectly:
		print("Page not loaded correctly")
		robot.driver.navigate().refresh()
		robot.update_card_memory()
