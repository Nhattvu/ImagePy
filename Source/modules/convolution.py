# source: https://medium.com/analytics-vidhya/2d-convolution-using-python-numpy-43442ff5f381

# please give the file selector enough time to run, it's a bit slow

# 2-dimensional Convolution Function

import time
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image
from numpy import asarray
from skimage import filters
from scipy.ndimage.filters import convolve
from skimage import data


class Convolution():

    avg_kernel = np.array([[1/9, 1/9, 1/9],
                           [1/9, 1/9, 1/9],
                           [1/9, 1/9, 1/9]])

    gaussian_kernel = np.array([[0.0146375,	0.0212974,	0.0241331,	0.0212974,	0.0146375],
                                [0.0212974,	0.0309875,	0.0351134,
                                    0.0309875,	0.0212974],
                                [0.0241331,	0.0351134,	0.0397887,
                                    0.0351134,	0.0241331],
                                [0.0212974,	0.0309875,	0.0351134,
                                    0.0309875,	0.0212974],
                                [0.0146375,	0.0212974,	0.0241331,	0.0212974,	0.0146375]])

    padding = 1

    def customConvolve(image, kernel, padding):

        # Cross Correlation
        kernel = np.flipud(np.fliplr(kernel))

        # Gather Shapes of Kernel and Image
        xKernelPixels = kernel.shape[0]
        yKernelPixels = kernel.shape[1]
        xImgPixels = image.shape[0]
        yImgPixels = image.shape[1]

        # Pixels of Output Convolution
        paddingBothSides = 2 * padding
        xOutput = int((xImgPixels - xKernelPixels + paddingBothSides) + 1)
        yOutput = int((yImgPixels - yKernelPixels + paddingBothSides) + 1)
        output = np.zeros((xOutput, yOutput))

        # Apply Equal Padding to All Sides
        if padding != 0:
            imagePadded = np.zeros(
                (xImgPixels + paddingBothSides, yImgPixels + paddingBothSides))
            # Slices the padded zeros and inserts the image in the "frame"
            imagePadded[int(padding):int(-1 * padding),
                        int(padding):int(-1 * padding)] = image
            print("Padded Image Size: " + str(imagePadded))
        else:
            imagePadded = image

        xImgPixels = imagePadded.shape[0]
        yImgPixels = imagePadded.shape[1]

        # Iterate through image
        for y in range(yImgPixels):
            # Exit Convolution
            if y > yImgPixels - yKernelPixels:
                break
            for x in range(xImgPixels):
                # Go to next row once kernel is out of bounds
                if x > xImgPixels - xKernelPixels:
                    break
                try:
                    output[x, y] = (
                        kernel * imagePadded[x: x + xKernelPixels, y: y + yKernelPixels]).sum()
                except:
                    break

        return output

    def select_file():

        filename = fd.askopenfilename(
            title='Open an Image', initialdir='/', filetypes=[('image files', ('.png', '.jpg'))])
        return(filename)

    def main(self):
        # create the root window
        root = tk.Tk()
        time.sleep(1)
        root.title('Tkinter Open Image Dialog')
        filename = select_file()
        time.sleep(1)

        root.update()
        image = Image.open(filename)
        #image = data.astronaut()
        # summarize some details about the image
        print(image.format + " " + str(image.size) + " " + image.mode)

        numpydata = asarray(image)

        # plt.imshow(numpydata)

        img_gray = rgb2gray(numpydata)

        plt.figure(1)
        plt.imshow(img_gray, cmap='gray')
        plt.title('Input Image')

        img_avg_filtered = self.customConvolve(
            img_gray, self.avg_kernel, self.padding)
        #img_avg_filtered = convolve(img_gray, avg_kernel)

        plt.figure(2)
        plt.imshow(img_avg_filtered, cmap='gray')
        plt.title('Input Image filtered by Averaging Filter')

        img_gaussian_filtered = self.customConvolve(
            img_gray, self.gaussian_kernel, self.padding)
        #img_gaussian_filtered = convolve(img_gray, gaussian_kernel)

        plt.figure(3)
        plt.imshow(img_gaussian_filtered, cmap='gray')
        plt.title('Input Image filtered by Gaussian Filter')

        plt.show()
