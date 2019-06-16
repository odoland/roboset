
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

import time
from driver.robotdriver import RobotDriver
 
if __name__ == "__main__":
    SLEEP_BETWEEN_SCANNING = 0
    SLEEP_BETWEEN_CLICKING = 0.11

    PATH_TO_CHROME_DRIVER = '/Users/orlando/Projects/roboset/chromedriver'
    URL = 'localhost:3000'

    # Initialize robot
    roboset = RobotDriver(path=PATH_TO_CHROME_DRIVER, url=URL, delay=SLEEP_BETWEEN_CLICKING)
    
    # Do initial scan
    roboset.scan_card_images(directory="./driver/images")
    roboset.find_sets_and_click()

    while True:
        roboset.unclick_all()
        time.sleep(SLEEP_BETWEEN_SCANNING)
        roboset.scan_card_images(directory="./driver/images")
        try:
            roboset.find_sets_and_click()
        except StaleElementReferenceException: # Clicking too fasts
            print("Clicked too fast, unclicking all")
            roboset.unclick_all()
            time.sleep(SLEEP_BETWEEN_SCANNING)
            continue







