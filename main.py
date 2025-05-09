from looper import Looper
from vision import Vision
from noiser import Noiser
from bezier_mouse import BezierMouse

import pygetwindow as gw
import sys

# constants
window_width = 1302
window_height = 776
window_location = [0, 0]
speed = 1
deviation = 10

# obtain the application window
window = gw.getWindowsWithTitle("Epic Seven")[0]

if window:
    # application window was found

    # prepare window
    window.resizeTo(window_width, window_height) # resize to default resolution
    window.moveTo(window_location[0], window_location[1]) # move to top left corner of screen
    window.activate() # bring window to foreground
else:
    print("Could not find an open Epic Seven application window. Ensure that the game is open.")
    sys.exit()

# initialize all objects
looper = Looper(Vision(), Noiser(), BezierMouse(deviation, speed))

# start loop
looper.loop()