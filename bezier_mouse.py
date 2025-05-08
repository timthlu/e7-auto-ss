import pyautogui
from mouse_movement.mouse import mouse_bez, move, connected_bez

class BezierMouse:
    def __init__(self, deviation=10, speed=1):
        self.deviation = deviation
        self.speed = speed
    
    def move_mouse(self, locations):
        start_x, start_y = pyautogui.position()

        # generate bezier points from a start and end position
        mouse_points = connected_bez([[start_x, start_y]] + locations, self.deviation, self.speed)

        # move mouse
        move(mouse_points, draw=False, rand_err=False)
