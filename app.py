from looper import Looper
from vision import Vision
from noiser import Noiser
from bezier_mouse import BezierMouse

import pygetwindow as gw
import tkinter as tk
from PIL import Image, ImageTk
import time
import threading

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
        self.time_elapsed = 0
        self.timer_id = None

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

    def run_loop(self, speed, deviation, max_refreshes, on_start, on_stop):
        # center window
        window_found = self.center_window()

        # call on start since we can actually start
        on_start()

        # initialize looper
        if window_found:
            self.looper = Looper(Vision(), Noiser(), BezierMouse(deviation, speed), self.increment_bms, self.increment_mms, self.increment_refreshes, self.trigger_stop, max_refreshes)

            # start loop
            self.looper.loop()
        
        # call on stop when stopped
        on_stop()

    def run_timer(self):
        # obtain start time
        start_time = time.time()
        cur_time_elapsed = 0

        while not self.stop_timer.is_set():
            # poll frequently so time is accurate
            time.sleep(0.2)

            # update time_elapsed from current run
            cur_time_elapsed = int(time.time() - start_time)

            # update time elapsed label
            self.time_elapsed_label.config(text=f"Time Elapsed (hh:mm:ss): {time.strftime('%H:%M:%S', time.gmtime(self.time_elapsed + cur_time_elapsed))}")

            # force repaint on ui
            self.root.update()
        
        # update time elapsed for next loop
        self.time_elapsed += cur_time_elapsed

    # callbacks for the looper
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
    
    # gui button methods
    def on_start_clicked(self):
        # obtain input values
        speed = int(self.speed_entry.get())
        deviation = int(self.deviation_entry.get())
        max_skystones = int(self.max_skystones_entry.get())
        max_refreshes = max_skystones // 3

        # trigger actual loop
        # use a separate thread to avoid blocking main thread
        threading.Thread(target=self.run_loop, args=(speed, deviation, max_refreshes, self.on_start, self.on_stop), daemon=True).start()
    
    def on_reset_stats_clicked(self):
        # reset all stats
        self.bms_bought = 0
        self.mms_bought = 0
        self.refreshes = 0
        self.time_elapsed = 0

        # reset stat label text
        self.bm_label.config(text=f"{self.bms_bought}")
        self.mm_label.config(text=f"{self.mms_bought}")
        self.refreshes_label.config(text=f"# of Refreshes: {self.refreshes}")
        self.skystones_spent_label.config(text=f"Skystones spent: {self.refreshes * 3}")
        self.skystones_bm_label.config(text=f"Skystones / Covenant Summon: N/A")
        self.skystones_mm_label.config(text=f"Skystones / Mystic Summon: N/A")
        self.time_elapsed_label.config(text=f"Time Elapsed (hh:mm:ss): {time.strftime('%H:%M:%S', time.gmtime(self.time_elapsed))}")

        self.root.update()

    # callbacks for the run_loop function to update the ui
    # this is since run_loop is run on a different thread and we want to free the main thread
    def on_start(self):
        # update gui
        # delete start button widget and ss label
        self.start_button.destroy()
        self.ss_label.destroy()

        # stop label
        self.stop_label = tk.Label(self.root, text="Taking control of your cursor... press \"q\" at any time to stop!\n(may take a couple seconds to do so)")
        self.stop_label.pack(pady=15)

        # force repaint on ui
        self.root.update()

        # initialize a separate thread to run the timer, so that we don't interrupt the looper
        # trigger timer updates
        # use a separate thread
        self.stop_timer = threading.Event()
        threading.Thread(target=self.run_timer, daemon=True).start()

    def on_stop(self):
        # stop timer
        self.stop_timer.set()

        # destroy stop label
        self.stop_label.destroy()

        # update gui to reconstruct ss label and start button
        self.ss_label = tk.Label(self.root, text="Ensure your secret shop is open before pressing start!")
        self.ss_label.pack(pady=15)

        self.start_button = tk.Button(self.root, text="Start!", command=self.on_start_clicked)
        self.start_button.pack(pady=20)

    def run(self):
        # initialize gui
        self.root = tk.Tk()
        self.root.title("E7 Auto SS")
        self.root.geometry("500x1200")

        # stats label
        self.stats_label = tk.Label(self.root, text="Statistics", font=("Helvetica", 16, "bold"))
        self.stats_label.pack(pady=10)

        # create bm and mm images and counters
        bm_image = ImageTk.PhotoImage(Image.open(bm_image_path))
        mm_image = ImageTk.PhotoImage(Image.open(mm_image_path))

        self.bm_frame = tk.Frame(self.root)
        self.bm_frame.pack(pady=10)
        self.mm_frame = tk.Frame(self.root)
        self.mm_frame.pack(pady=10)

        self.bm_image_label = tk.Label(self.bm_frame, image=bm_image)
        self.mm_image_label = tk.Label(self.mm_frame, image=mm_image)

        self.bm_image_label.pack(side="left", padx=10)
        self.mm_image_label.pack(side="left", padx=10)

        self.bm_label = tk.Label(self.bm_frame, text=f"{self.bms_bought}")
        self.mm_label = tk.Label(self.mm_frame, text=f"{self.mms_bought}")

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

        # time elapsed label
        self.time_elapsed_label = tk.Label(self.root, text=f"Time Elapsed (hh:mm:ss): {time.strftime('%H:%M:%S', time.gmtime(self.time_elapsed))}")
        self.time_elapsed_label.pack(pady=10)

        # reset stats button
        self.reset_stats_button = tk.Button(self.root, text="Reset Stats", command=self.on_reset_stats_clicked)
        self.reset_stats_button.pack(pady=10)

        # control panel label
        self.control_panel_label = tk.Label(self.root, text="Control Panel", font=("Helvetica", 16, "bold"))
        self.control_panel_label.pack(pady=10)

        # speed label
        self.speed_label = tk.Label(self.root, text="Speed:")
        self.speed_label.pack(pady=10)

        # speed input
        self.speed_entry = tk.Entry(self.root, width=30)
        self.speed_entry.pack(pady=10)
        self.speed_entry.insert(0, 1)

        # deviation label
        self.deviation_label = tk.Label(self.root, text="Deviation:")
        self.deviation_label.pack(pady=10)

        # deviation input
        self.deviation_entry = tk.Entry(self.root, width=30)
        self.deviation_entry.pack(pady=10)
        self.deviation_entry.insert(0, 10)

        # max skystones to spend label
        self.max_skystones_label = tk.Label(self.root, text="Max # of Skystones to Spend:")
        self.max_skystones_label.pack(pady=10)

        # max skystones input
        self.max_skystones_entry = tk.Entry(self.root, width=30)
        self.max_skystones_entry.pack(pady=10)
        self.max_skystones_entry.insert(0, 100)

        # ss label
        self.ss_label = tk.Label(self.root, text="Ensure your secret shop is open before pressing start!")
        self.ss_label.pack(pady=10)

        # start button
        self.start_button = tk.Button(self.root, text="Start!", command=self.on_start_clicked)
        self.start_button.pack(pady=10)

        # start gui
        self.root.mainloop()
