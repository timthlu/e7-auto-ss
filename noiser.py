import random
import pyautogui
import time

buy_width = 150
buy_height = 20
refresh_width = 250
refresh_height = 40
middle_width = 400
middle_height = 400
buy_confirm_width = 200
buy_confirm_height = 30
refresh_confirm_width = 150
refresh_confirm_height = 30

class Noiser:
    def add_mouse_location_noise_buy(self, location):
        location[0] += random.uniform(- buy_width / 2, buy_width / 2)
        location[1] += random.uniform(- buy_height / 2, buy_height / 2)

        return location

    def add_mouse_location_noise_refresh(self, location):
        location[0] += random.uniform(- refresh_width / 2, refresh_width / 2)
        location[1] += random.uniform(- refresh_height / 2, refresh_height / 2)

        return location

    def add_mouse_location_noise_buy_confirm(self, location):
        location[0] += random.uniform(- buy_confirm_width / 2, buy_confirm_width / 2)
        location[1] += random.uniform(- buy_confirm_height / 2, buy_confirm_height / 2)

        return location

    def add_mouse_location_noise_refresh_confirm(self, location):
        location[0] += random.uniform(- refresh_confirm_width / 2, refresh_confirm_width / 2)
        location[1] += random.uniform(- refresh_confirm_height / 2, refresh_confirm_height / 2)

        return location

    def add_mouse_location_noise_middle(self, location):
        location[0] += random.uniform(- middle_width / 2, middle_width / 2)
        location[1] += random.uniform(- middle_height / 2, middle_height / 2)

        return location

    # def move_mouse_with_noise(self, location):
    #     self.wait_random_time()

    #     steps = random.randint(10, 15)

    #     # compute entire path first then use the moveTo
    #     # prevents the mouse from looking like it is starting and stopping all the time

    #     for i in range(steps - 1):
    #         # obtain current mouse position
    #         start_x, start_y = pyautogui.position()

    #         # obtain current target
    #         # add some noise to the target
    #         target_x = start_x + (location[0] - start_x) / (steps - i) + random.uniform(-10, 10)
    #         target_y = start_y + (location[1] - start_y) / (steps - i) + random.uniform(-10, 10)

    #         # move to this location
    #         pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.1, 0.2))
        
    #     # for the last step, just move directly to the location
    #     pyautogui.moveTo(location[0], location[1], duration=random.uniform(0.5, 0.6))

    def click_with_noise(self):
        self.wait_random_time()
        pyautogui.click()

    def scroll_with_noise(self):
        self.wait_random_time()
        pyautogui.scroll(random.randint(- middle_height * 2, - middle_height))

    def wait_random_time(self):
        # generate a random delay
        time.sleep(random.uniform(0.5, 0.75))
    