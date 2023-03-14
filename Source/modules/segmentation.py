# ASSIGNMENT DETAILS

# Use the attached "pears.png" image.

# Your task is to write a function in python that will do the following:

# 1) Find the center locations of visible pears. Only consider the ones which are fully visible in the image.
# 2) Determine the relative sizes of each pear in terms of total number of pixels. (that is the number of pixels belonging to each pear)

# Use the segmentation methods and morphological operations to segment out the pears to find their locations and their sizes.

# Write a function that will take the input "img" and return ''pear_x, pear_y, pear_size"

# function (img):
#          ........
#         return ( pear_x, pear_y, pear_size )

# img: input image (could be color image)
# pear_x: a column vector keeping the x coordinates of the center of each pears
# pear_y: a column vector keeping the y coordinates of the center of each pears
# pear_size: a column vector keeping the size of the pears in terms of total number of pixels

# COMMENTS
# Still has an issue with one of the pears. Further tinkering with the gamma and watershed values could fix it.
# I wasn't able to implement pyramid mean shift filtering which could have possibly fixed the issue.
# But I'd rather just turn it in at this point than get a 0.

# SOURCES
# https://pyimagesearch.com/2015/11/02/watershed-opencv/
# https://www.mathworks.com/help/images/marker-controlled-watershed-segmentation.html
# https://machinelearningknowledge.ai/image-segmentation-in-python-opencv/
# https://medium.com/analytics-vidhya/images-processing-segmentation-and-objects-counting-in-an-image-with-python-and-opencv-216cd38aca8e
# https://moodle.selu.edu/moodle/pluginfile.php/4546063/mod_resource/content/1/Segmentation.py
# And finally the slides


import imutils
import matplotlib.pyplot as plt
import numpy as np
from skimage.feature import peak_local_max
import cv2
from skimage.segmentation import watershed
import numpy as np
from scipy import ndimage


class Segmentation():
    img = cv2.imread("D:\Documents\College\CMPS473\pears.png")

    def main():

        grayScaleImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grayScaleImg = cv2.medianBlur(grayScaleImg, 7)
        equalizedImg = cv2.equalizeHist(grayScaleImg)
        contrastAdjImg = np.array(
            255 * (equalizedImg / 255) ** 1.6, dtype='uint8')

        cv2.imshow("equalized", equalizedImg)
        cv2.imshow("gammacorrection", contrastAdjImg)

        img_reshaped = contrastAdjImg.reshape((-1, 3))
        img_reshaped = np.float32(img_reshaped)
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 2
        attempts = 20
        ret, label, center = cv2.kmeans(
            img_reshaped, K, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        result_image = res.reshape((486, 732))

        plt.figure(1)
        plt.title('K-Means')
        plt.imshow(result_image, cmap="gray", vmin=0, vmax=255)
        plt.axis('off')

        watershedImage = contrastAdjImg
        # apply Otsu's thresholding
        thresh = cv2.threshold(watershedImage, 0, 255,
                               cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # compute the exact Euclidean distance from every binary pixel to the nearest zero pixel, then find peaks in this distance map
        D = ndimage.distance_transform_edt(thresh)
        localMax = peak_local_max(
            D, indices=False, min_distance=50, labels=thresh)
        # perform a connected component analysis on the local peaks, using 8-connectivity, then apply the Watershed algorithm
        markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
        labels = watershed(-D, markers, mask=thresh)
        print("[INFO] {} unique segments found".format(
            len(np.unique(labels)) - 1))
        pearSizeList = []
        xList = []
        yList = []
        for label in np.unique(labels):
            # if the label is zero, we are examining the 'background' so simply ignore it
            # so simply ignore it
            if label == 0:
                continue
            # otherwise, allocate memory for the label region and draw it on the mask
            mask = np.zeros(watershedImage.shape, dtype="uint8")
            mask[labels == label] = 255
            # detect contours in the mask and grab the largest one
            contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            c = max(contours, key=cv2.contourArea)
            # draw a circle enclosing the object
            ((x, y), r) = cv2.minEnclosingCircle(c)
            xList.append(x)
            yList.append(y)
            pearSizeList.append(int(r*2*np.pi))
            cv2.circle(watershedImage, (int(x), int(y)),
                       int(r), (0, 255, 0), 2)
            cv2.putText(watershedImage, "#{}".format(label), (int(x) - 10, int(y)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # show the output image
        cv2.imshow("Output", watershedImage)

        # adaptiveThresholding with 20 as block size seems best
        thresh3 = cv2.adaptiveThreshold(
            contrastAdjImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 20)
        plt.figure(4)
        plt.title('Local Adaptive Thresholding HIST20')
        plt.imshow(thresh3, cmap="gray", vmin=0, vmax=255)

        # Dilatation et erosion
        kernel = np.ones((5, 5), np.uint8)
        img_erode = cv2.erode(thresh3, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erode, kernel, iterations=1)
        # clean all noise after dilatation and erosion

        final = cv2.medianBlur(img_dilation, 7)
        plt.figure(5)
        plt.title('Dilatation + erosion')
        plt.imshow(final, cmap="gray", vmin=0, vmax=255)
        plt.axis('off')

        plt.show()
        return xList, yList, pearSizeList
