from matplotlib.pyplot import new_figure_manager
import numpy as np
import cv2
from numpy import array
from PIL import Image

# Adaptive Thresholding
# https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html

def adaptive_Thresholding(inputPath, outputPath, algorithm):
        #NEED TO CREATE OUTPUT FILE
        img = cv2.imread(inputPath,0)
        img = cv2.medianBlur(img,5)
        if algorithm == "Gaussian":
            th = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,2)
        elif algorithm == "Mean":
            th = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
        
        newImage = Image.fromarray(th)
        newImage.save(outputPath)
        return newImage