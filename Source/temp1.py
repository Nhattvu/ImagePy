import numpy as np
import cv2
from numpy import array
from PIL import Image

image = Image.open('equalizedImage.png')
original_numpy_array = array(image)

# img.shape provides you the shape of img in all directions.
# ie number of rows, number of columns for a 2D array (grayscale image). 
# For 3D array, it gives you number of channels also.
# So if len(img.shape) gives you two, it has a single channel.
# If len(img.shape) gives you three, third element gives you number of channels.

if len(original_numpy_array.shape) == 2:
    print("gray") # Image is grayscale
else:
    channelNum = original_numpy_array.shape[2]
    print(channelNum)
#length(cv2.split(original_numpy_array)))