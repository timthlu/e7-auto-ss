import cv2
import pyautogui
import numpy as np

import matplotlib.pyplot as plt

class Vision:
    def __init__(self, window_width=1302, window_height=776, window_location=[0, 0], match_threshold=0.8):
        self.match_threshold = match_threshold
        self.window_width = window_width
        self.window_height = window_height
        self.window_location = window_location

    # helper methods
    def get_screenshot(self):
        # take screenshot
        image = pyautogui.screenshot()

        # convert the image to a gray cv2 image
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # crop to window width and height
        # image is in rows then columns, so it is y then x
        image = image[self.window_location[1]:self.window_location[1] + self.window_height, self.window_location[0]:self.window_location[0] + self.window_width]

        return image

    # image detection
    # returns a tuple: boolean: found image, top left corner of the match
    def image_detection(self, image, target_path, bought_target_path):
        target = cv2.imread(target_path, cv2.IMREAD_GRAYSCALE)
        bought_target = cv2.imread(bought_target_path, cv2.IMREAD_GRAYSCALE)

        # find the location of a match
        # matchTemplate finds the best match
        # we don't care about the worst match, only the max val + loc
        # max val will be between -1 and 1
        result = cv2.matchTemplate(image, target, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        bought_result = cv2.matchTemplate(image, bought_target, cv2.TM_CCOEFF_NORMED)
        _, bought_max_val, _, _ = cv2.minMaxLoc(bought_result)
        
        # check whether the best match is good enough AND it does not look like the bought version
        if max_val >= self.match_threshold and max_val > bought_max_val:
            # return true and location of the match
            return True, max_loc
        else:
            return False, None