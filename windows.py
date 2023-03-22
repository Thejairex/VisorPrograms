import cv2 as cv
import numpy as np
import os
from time import time
from windowsCapture import WindowCapture

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
print(WindowCapture('Símbolo del sistema - python  main.py').list_window_names()) 