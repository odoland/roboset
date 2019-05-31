import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from setcard import SetCard
from vision.carddetect import CardDetector
from typing import List
import cv2
import itertools as it


class Robot:

    def __init__(self, cards_list=None):
        self.cards_list = cards_list or []
    
    def load_robot_brain(self, image_paths: List):
        """Loads a list of image paths into a list of SetCard objects """
        self.cards_list = [self._create_card(image_path) for image_path in image_paths]

    def _create_card(self, image_path):
        """Converts the path to an image (.png file) into a SetCard instance """
        image_dic = CardDetector.detect_card(image_path)

        if any(image_dic[key] >= 3 for key in image_dic):
            print(image_dic, "something wrong", image_path)
        
        return SetCard(**image_dic)

    def find_sets(self):
        set_of_sets = set(set_card.encoding for set_card in self.cards_list)
        
        matches = []
        for card1, card2 in it.combinations(self.cards_list, 2):
            card3 = SetCard.getMatch(card1, card2)
            if card3.encoding in set_of_sets:
                matches.append([card1, card2, card3])
        
        return matches
    
    def find_first_set(self):
        set_of_sets = set(set_card.encoding for set_card in self.cards_list)

        for card1, card2 in it.combinations(self.cards_list, 2):
            card3 = SetCard.getMatch(card1, card2)
            if card3.encoding in set_of_sets:
                return [card1, card2, card3]


if __name__ == "__main__":
    list_images = [f'./driver/{i}.png' for i in range(20)]
    # ['./driver/0.png', './driver/1.png', './driver/2.png', './driver/3.png', './driver/4.png', './driver/5.png', './driver/6.png', './driver/7.png', './driver/8.png', './driver/9.png', './driver/10.png', './driver/11.png', './driver/12.png', './driver/13.png', './driver/14.png', './driver/15.png', './driver/16.png', './driver/17.png', './driver/18.png', './driver/19.png']
    robo = Robot()
    robo.load_robot_brain(list_images)
    matches = robo.find_sets()

    print(matches)


    