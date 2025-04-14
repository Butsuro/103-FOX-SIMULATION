import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for development and for PyInstaller """
    if hasattr(sys, 'frozen'):
        # If the application is run as a bundle, the PyInstaller bootloader
        # sets the sys._MEIPASS attribute.
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
