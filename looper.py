from vision import Vision
from noiser import Noiser
from bezier_mouse import BezierMouse

import time
import pyautogui
import keyboard
import threading

# constants
bm_image_path = "./images/bm_image_small.png"
bm_bought_image_path = "./images/bm_bought_image_small.png"
mm_image_path = "./images/mm_image_small.png"
mm_bought_image_path = "./images/mm_bought_image_small.png"
ss_image_path = "./images/ss_image_small.png"

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
daily_confirm_x = 1025
daily_confirm_y = 700
ss_x = 60
ss_y = 310
buffs_x = 650
buffs_y = 720

class Looper:
    def __init__(self, vision : Vision, noiser : Noiser, mouse : BezierMouse, increment_bms, increment_mms, increment_refreshes, trigger_stop, max_refreshes=3000):
        self.vision = vision
        self.noiser = noiser
        self.mouse = mouse

        # for current refresh
        self.bm_bought = False
        self.mm_bought = False

        # gui methods
        self.increment_bms = increment_bms
        self.increment_mms = increment_mms
        self.increment_refreshes = increment_refreshes
        self.trigger_stop = trigger_stop

        self.refreshes = 0 # for stopping condition
        self.max_refreshes = max_refreshes

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

        # update gui for number of refreshes
        self.increment_refreshes()
        self.refreshes += 1

        # reset bm and mm bought flags for next refresh
        self.bm_bought = False
        self.mm_bought = False

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
        if self.bm_bought and self.mm_bought:
            # no need to check anymore as cannot be another bm or mm
            return

        # get screenshot and detect target image
        image = self.vision.get_screenshot()

        # if bm has already been bought, can skip bm detection step
        if not self.bm_bought:
            bm_found, bm_location = self.vision.image_detection(image, bm_image_path)

            if bm_found:
                print("bm found")
                
                self.buy_bm(bm_location)
                
                # increment number of bms
                self.increment_bms()

                self.bm_bought = True
        
        # do the same for mm
        if not self.mm_bought:
            mm_found, mm_location = self.vision.image_detection(image, mm_image_path)

            if mm_found:
                print("mm found")
                
                self.buy_bm(mm_location)
                
                # increment number of mms
                self.increment_mms()

                self.mm_bought = True

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

    def daily_confirm(self):
        daily_confirm_location = [daily_confirm_x, daily_confirm_y]
        daily_confirm_location = self.noiser.add_mouse_location_noise_daily_confirm(daily_confirm_location)

        # move mouse
        self.mouse.move_mouse([daily_confirm_location])

        # wait a bit of time for the daily login to disappear
        time.sleep(2)

    def close_buffs(self):
        buffs_location = [buffs_x, buffs_y]
        buffs_location = self.noiser.add_mouse_location_noise_buffs(buffs_location)

        # move mouse
        self.mouse.move_mouse([buffs_location])

        # wait a bit of time for buffs to disappear
        time.sleep(2)

    def open_ss(self):
        ss_location = [ss_x, ss_y]
        ss_location = self.noiser.add_mouse_location_noise_ss(ss_location)

        # move mouse
        self.mouse.move_mouse([ss_location])

        # wait a bit of time for the secret shop to appear
        time.sleep(2)

    def check_handle_reset(self):
        # check whether we are still in the secret shop
        image = self.vision.get_screenshot()
        ss_found, _ = self.vision.image_detection(image, ss_image_path)

        while not ss_found:
            # we are not in the secret shop
            # press confirm for daily login and secret shop button repeatedly until we are in the secret shop
            self.daily_confirm()

            self.close_buffs()

            self.open_ss()

            # check whether we are in the secret shop again
            image = self.vision.get_screenshot()
            ss_found, _ = self.vision.image_detection(image, ss_image_path)

    # refresh loop
    def loop(self):
        # initialize stopping mechanism
        # stopping mechanism
        stop = threading.Event() # use a thread safe variable

        def stop_callback(_):
            print("Stopping...")

            # update gui
            # self.trigger_stop()

            # set thread safe flag
            stop.set()

        # callback is invoked on another thread
        keyboard.on_press_key("q", stop_callback)

        while self.refreshes < self.max_refreshes:
            # check and handle reset
            self.check_handle_reset()

            # check and buy bms
            self.check_buy_bms()

            if stop.is_set():
                break

            # scroll down
            self.scroll_down()

            if stop.is_set():
                break

            # check and buy bms again
            self.check_buy_bms()

            if stop.is_set():
                break

            # refresh shop
            self.refresh()

            if stop.is_set():
                break

            # wait a bit before continuing loop for screen to load in
            time.sleep(2)

            if stop.is_set():
                break
        
        # check shop again after last refresh
        # do this only if natural stop (not user stop)
        if not stop.is_set():
            self.bm_bought = False
            self.mm_bought = False

            # check and buy bms
            self.check_buy_bms()

            # scroll down
            self.scroll_down()

            # check and buy bms again
            self.check_buy_bms()

        print("Stopped")