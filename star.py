from mirrorGui import Gui_Mirror
import os
import sys

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        os.chdir(application_path)
    elif __file__:
        application_path = os.path.dirname(__file__)
        os.chdir(application_path)

    star = Gui_Mirror()
    star.set_init_window()