from looper import Looper
from vision import Vision
from noiser import Noiser
from bezier_mouse import BezierMouse

# NOTE: anaconda prompt must be run as administrator in order for this to work

# initialize
looper = Looper(Vision(), Noiser(), BezierMouse())

# # start loop
looper.loop()

# for debugging
# import matplotlib.pyplot as plt
# import cv2

# image = cv2.imread("./images/test_image_3_small.png", cv2.IMREAD_GRAYSCALE)
# plt.imshow(image)
# plt.show()

