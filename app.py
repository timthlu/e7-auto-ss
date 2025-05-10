from looper import Looper
from vision import Vision
from noiser import Noiser
from bezier_mouse import BezierMouse

import pygetwindow as gw
import tkinter as tk
from PIL import Image, ImageTk

# constants
window_width = 1302
window_height = 776
window_location = [0, 0]
bm_image_path = "./images/bm_image_small.png"
mm_image_path = "./images/mm_image_small.png"

# wrapper class
# controls gui and looping
class App:
    def __init__(self):
        self.speed = 1
        self.deviation = 10
        self.max_refreshes = 100

        self.bms_bought = 0
        self.mms_bought = 0
        self.refreshes = 0

    def center_window(self):
        # obtain the application window
        window = gw.getWindowsWithTitle("Epic Seven")[0]

        if window:
            # application window was found

            # prepare window
            window.resizeTo(window_width, window_height) # resize to default resolution
            window.moveTo(window_location[0], window_location[1]) # move to top left corner of screen
            window.activate() # bring window to foreground
            return True
        else:
            print("Could not find an open Epic Seven application window. Ensure that the game is open.")
            return False

    def run_loop(self, speed, deviation, max_refreshes):
        # center window
        window_found = self.center_window()

        # initialize looper
        if window_found:
            self.looper = Looper(Vision(), Noiser(), BezierMouse(deviation, speed), self.increment_bms, self.increment_mms, self.increment_refreshes, self.trigger_stop, max_refreshes)

            # start loop
            self.looper.loop()

    def increment_bms(self):
        # update counts
        self.bms_bought += 1

        # update label
        self.bm_label.config(text=f"{self.bms_bought}")
        self.skystones_bm_label.config(text=f"Skystones / Covenant Summon: {self.refreshes * 3 / self.bms_bought}")

        # force repaint on ui
        self.root.update()
    
    def increment_mms(self):
        # update counts
        self.mms_bought += 1

        # update labels
        self.mm_label.config(text=f"{self.mms_bought}")
        self.skystones_mm_label.config(text=f"Skystones / Mystic Summon: {self.refreshes * 3 / self.mms_bought}")

        # force repaint on ui
        self.root.update()

    def increment_refreshes(self):
        # update counts
        self.refreshes += 1

        # update labels
        self.refreshes_label.config(text=f"# of Refreshes: {self.refreshes}")
        self.skystones_spent_label.config(text=f"Skystones spent: {self.refreshes * 3}")
        
        if self.bms_bought != 0:
            self.skystones_bm_label.config(text=f"Skystones / Covenant Summon: {self.refreshes * 3 / self.bms_bought}")
        
        if self.mms_bought != 0:
            self.skystones_mm_label.config(text=f"Skystones / Mystic Summon: {self.refreshes * 3 / self.mms_bought}")

        # force repaint on ui
        self.root.update()
    
    def trigger_stop(self):
        # update stop label
        self.stop_label.config(text="Stopping...")

        # force repaint on ui
        self.root.update()

    def run(self):
        def on_start_clicked():
            # obtain input values
            speed = int(speed_entry.get())
            deviation = int(deviation_entry.get())
            max_skystones = int(max_skystones_entry.get())
            max_refreshes = max_skystones // 3

            # update gui
            # delete start button widget and ss label
            self.start_button.destroy()
            self.ss_label.destroy()

            # stop label
            self.stop_label = tk.Label(self.root, text="Taking control of your cursor... press \"q\" at any time to stop!\n(may take a couple seconds to do so)")
            self.stop_label.pack(pady=15)

            # force repaint on ui
            self.root.update()

            # trigger actual loop
            self.run_loop(speed, deviation, max_refreshes)

            # destroy stop label
            self.stop_label.destroy()

            # update gui to reconstruct ss label and start button
            self.ss_label = tk.Label(self.root, text="Ensure your secret shop is open before pressing start!")
            self.ss_label.pack(pady=15)

            self.start_button = tk.Button(self.root, text="Start!", command=on_start_clicked)
            self.start_button.pack(pady=20)

        # initialize gui
        self.root = tk.Tk()
        self.root.title("E7 Auto SS")
        self.root.geometry("500x1000")

        # stats label
        stats_label = tk.Label(self.root, text="Statistics", font=("Helvetica", 16, "bold"))
        stats_label.pack(pady=10)

        # create bm and mm images and counters
        bm_image = ImageTk.PhotoImage(Image.open(bm_image_path))
        mm_image = ImageTk.PhotoImage(Image.open(mm_image_path))

        bm_frame = tk.Frame(self.root)
        bm_frame.pack(pady=10)
        mm_frame = tk.Frame(self.root)
        mm_frame.pack(pady=10)

        self.bm_image_label = tk.Label(bm_frame, image=bm_image)
        self.mm_image_label = tk.Label(mm_frame, image=mm_image)

        self.bm_image_label.pack(side="left", padx=10)
        self.mm_image_label.pack(side="left", padx=10)

        self.bm_label = tk.Label(bm_frame, text=f"{self.bms_bought}")
        self.mm_label = tk.Label(mm_frame, text=f"{self.mms_bought}")

        self.bm_label.pack(side="left")
        self.mm_label.pack(side="left")

        # refreshes label
        self.refreshes_label = tk.Label(self.root, text=f"# of Refreshes: {self.refreshes}")
        self.refreshes_label.pack(pady=10)

        # skystones spent label
        self.skystones_spent_label = tk.Label(self.root, text=f"Skystones spent: {self.refreshes * 3}")
        self.skystones_spent_label.pack(pady=10)

        # skystones per cov pull label
        self.skystones_bm_label = tk.Label(self.root, text=f"Skystones / Covenant Summon: N/A")
        self.skystones_bm_label.pack(pady=10)

        # skystones per mystic pull label
        self.skystones_mm_label = tk.Label(self.root, text=f"Skystones / Mystic Summon: N/A")
        self.skystones_mm_label.pack(pady=10)

        # control panel label
        control_panel_label = tk.Label(self.root, text="Control Panel", font=("Helvetica", 16, "bold"))
        control_panel_label.pack(pady=10)

        # speed label
        speed_label = tk.Label(self.root, text="Speed:")
        speed_label.pack(pady=10)

        # speed input
        speed_entry = tk.Entry(self.root, width=30)
        speed_entry.pack(pady=10)
        speed_entry.insert(0, 1)

        # deviation label
        deviation_label = tk.Label(self.root, text="Deviation:")
        deviation_label.pack(pady=10)

        # deviation input
        deviation_entry = tk.Entry(self.root, width=30)
        deviation_entry.pack(pady=10)
        deviation_entry.insert(0, 10)

        # max skystones to spend label
        max_skystones_label = tk.Label(self.root, text="Max # of Skystones to Spend:")
        max_skystones_label.pack(pady=10)

        # max skystones input
        max_skystones_entry = tk.Entry(self.root, width=30)
        max_skystones_entry.pack(pady=10)
        max_skystones_entry.insert(0, 100)

        # ss label
        self.ss_label = tk.Label(self.root, text="Ensure your secret shop is open before pressing start!")
        self.ss_label.pack(pady=10)

        # start button
        self.start_button = tk.Button(self.root, text="Start!", command=on_start_clicked)
        self.start_button.pack(pady=10)

        # start gui
        self.root.mainloop()
