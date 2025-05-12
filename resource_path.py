import sys
import os

# this file implements a helper function for the path

# the resource path changes when compiled into an executable
def get_resource_path(relative_path):
    # detect whether we are in an executable
    if hasattr(sys, "_MEIPASS"):
        # executable puts everything in a temp folder
        # sys._MEIPASS is a special pyinstaller variable pointing to the temp folder
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # just return '.' + relative path
        return os.path.join(".", relative_path)