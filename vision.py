import cv2
import pyautogui
import numpy as np

import matplotlib.pyplot as plt

class Vision:
    def __init__(self, window_width=1302, window_height=776, window_location=[0, 0], match_threshold=0.9):
        self.window_width = window_width
        self.window_height = window_height
        self.window_location = window_location
        self.match_threshold = match_threshold

    # helper methods
    def get_screenshot(self):
        # take screenshot
        image = pyautogui.screenshot()

        # convert the image to a bgr cv2 image
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # crop to window width and height
        # image is in rows then columns, so it is y then x
        image = image[self.window_location[1]:self.window_location[1] + self.window_height, self.window_location[0]:self.window_location[0] + self.window_width]

        return image

    # image detection
    # returns a tuple: boolean: found image, top left corner of the match
    def image_detection(self, image, target_path):
        target = cv2.imread(target_path, cv2.IMREAD_UNCHANGED)

        # remove the transparency channel
        target = cv2.cvtColor(target, cv2.COLOR_BGRA2BGR)

        # find the location of a match
        # matchTemplate finds the best match
        # we don't care about the worst match, only the max val + loc
        # max val will be between -1 and 1
        result = cv2.matchTemplate(image, target, cv2.TM_CCORR_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        print(max_val)
        
        # check whether the best match is good enough
        if max_val >= self.match_threshold:
            # return true and location of the match
            return True, max_loc
        else:
            return False, None