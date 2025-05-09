from vision import Vision
from noiser import Noiser
from bezier_mouse import BezierMouse

import time
import pyautogui

# constants
bm_image_path = "./images/bm_image_small.png"
bm_bought_image_path = "./images/bm_bought_image_small.png"
mm_image_path = "./images/mm_image_small.png"
mm_bought_image_path = "./images/mm_bought_image_small.png"

# for 4k monitor
# buy_delta_x = 1125
# buy_delta_y = 128
# refresh_x = 500
# refresh_y = 1260
# middle_x = 1700
# middle_y = 700
# buy_confirm_x = 1500
# buy_confirm_y = 1000
# refresh_confirm_x = 1480
# refresh_confirm_y = 900

# for resolution: 1302 x 776
# currently assumes that the application window is located on the top left
# add an offset width/height if located elsewhere on the page
buy_x = 1155
buy_delta_y = 60
refresh_x = 210
refresh_y = 705
middle_x = 850
middle_y = 400
middle_width = 400
middle_height = 400
buy_confirm_x = 750
buy_confirm_y = 550
refresh_confirm_x = 740
refresh_confirm_y = 500

class Looper:
    def __init__(self, vision : Vision, noiser : Noiser, mouse : BezierMouse):
        self.vision = vision
        self.noiser = noiser
        self.mouse = mouse

        self.bms_bought = 0
        self.mms_bought = 0
        self.refreshes = 0

    # click refresh button
    def refresh(self):
        # get refresh location
        refresh_location = [refresh_x, refresh_y]
        refresh_location = self.noiser.add_mouse_location_noise_refresh(refresh_location)

        # get refresh confirm location
        refresh_confirm_location = [refresh_confirm_x, refresh_confirm_y]
        refresh_confirm_location = self.noiser.add_mouse_location_noise_refresh_confirm(refresh_confirm_location)

        # move mouse
        self.mouse.move_mouse([refresh_location, refresh_confirm_location])

        self.refreshes += 1

        print(f"refreshes: {self.refreshes}")

    # click buy on bm
    def buy_bm(self, location):
        # get buy location
        # obtain location of buy button relative to top left location of bm
        # x coordinate is always the same
        buy_location = [buy_x, location[1] + buy_delta_y]
        buy_location = self.noiser.add_mouse_location_noise_buy(buy_location)

        # get buy confirm location
        buy_confirm_location = [buy_confirm_x, buy_confirm_y]
        buy_confirm_location = self.noiser.add_mouse_location_noise_buy_confirm(buy_confirm_location)

        # move mouse
        self.mouse.move_mouse([buy_location, buy_confirm_location])

        # wait a bit of time for the notification that pops up to disappear
        time.sleep(2)

    # check for bookmarks
    def check_buy_bms(self):
        # check for both bm and mm

        # get screenshot and detect target image
        image = self.vision.get_screenshot()
        bm_found, bm_location = self.vision.image_detection(image, bm_image_path, bm_bought_image_path)

        if bm_found:
            print("bm found")
            self.buy_bm(bm_location)
            
            self.bms_bought += 1
            print(f"bms bought: {self.bms_bought}")
        
        # do the same for mm
        mm_found, mm_location = self.vision.image_detection(image, mm_image_path, mm_bought_image_path)

        if mm_found:
            print("mm found")
            self.buy_bm(mm_location)
            
            self.mms_bought += 1
            print(f"mms bought: {self.mms_bought}")

    def scroll_down(self):
        # get the location of the middle of the screen
        middle_location = [middle_x, middle_y]

        location = pyautogui.position()

        # move mouse to middle of right screen
        # do this only if it is not there already
        if abs(location[0] -  middle_location[0]) > middle_width / 2 or abs(location[1] -  middle_location[1]) > middle_width / 2:
            middle_location = self.noiser.add_mouse_location_noise_middle(middle_location)

            # move mouse to middle of screen
            self.mouse.move_mouse([middle_location])

        # scroll down
        # move mouse to middle of the right screen
        self.noiser.scroll_with_noise()

    # refresh loop
    def loop(self):
        while True:
            # check and buy bms
            self.check_buy_bms()

            # scroll down
            self.scroll_down()

            # check and buy bms again
            self.check_buy_bms()

            # refresh shop
            self.refresh()

            # wait a bit before continuing loop for screen to load in
            time.sleep(2)